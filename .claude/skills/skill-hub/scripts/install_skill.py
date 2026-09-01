#!/usr/bin/env python3
"""
Install a Skill directly from GitHub URL or local path.

Usage:
    python install_skill.py <url_or_path> [--skill-name <name>]

Examples:
    python install_skill.py https://github.com/user/repo/skill-name
    python install_skill.py https://github.com/anthropics/skills/tree/main/skills/xlsx --skill-name xlsx
    python install_skill.py /path/to/local/skill

This script:
1. Fetches/copies the Skill content
2. Installs it to ~/.claude/skills/
3. Verifies SKILL.md exists and is valid
4. Reports installation status
"""

import sys
import json
import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from urllib.parse import urlparse

def get_skills_directory():
    """Get the Claude skills directory path."""
    home = Path.home()
    skills_dir = home / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    return skills_dir

def extract_skill_name_from_url(url):
    """Extract skill name from GitHub URL."""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')

    # https://github.com/user/repo/tree/branch/skills/skill-name
    if 'skills' in path_parts:
        idx = path_parts.index('skills')
        if idx + 1 < len(path_parts):
            return path_parts[idx + 1]

    # https://github.com/user/repo (use repo name)
    if len(path_parts) >= 2:
        return path_parts[1]

    return None

def is_github_url(path):
    """Check if path is a GitHub URL."""
    return path.startswith('http') and 'github.com' in path

def clone_from_github(url, target_dir):
    """Clone skill from GitHub repository."""
    # Convert tree URL to clone URL if needed
    # https://github.com/user/repo/tree/main/skills/skill-name
    # -> https://github.com/user/repo.git

    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')

    if len(path_parts) >= 2:
        user = path_parts[0]
        repo = path_parts[1]
        clone_url = f"https://github.com/{user}/{repo}.git"

        # Determine subdirectory if it's a deep link
        subdirectory = None
        if 'tree' in path_parts and len(path_parts) > 4:
            # Extract path after branch name
            tree_idx = path_parts.index('tree')
            if tree_idx + 2 < len(path_parts):
                subdirectory = '/'.join(path_parts[tree_idx + 2:])

        # Clone to temp directory
        temp_dir = tempfile.mkdtemp()
        try:
            # Clone repository
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', clone_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                return False, f"Git clone failed: {result.stderr}"

            # Copy the right subdirectory
            if subdirectory:
                source_dir = Path(temp_dir) / subdirectory
            else:
                source_dir = Path(temp_dir)

            if not source_dir.exists():
                return False, f"Subdirectory {subdirectory} not found in repository"

            # Copy to target
            if source_dir.is_dir():
                shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
            else:
                return False, f"{source_dir} is not a directory"

            return True, "Cloned successfully"

        except subprocess.TimeoutExpired:
            return False, "Git clone timed out (>60s)"
        except Exception as e:
            return False, f"Error during clone: {str(e)}"
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    return False, "Invalid GitHub URL format"

def copy_from_local(source_path, target_dir):
    """Copy skill from local path."""
    source = Path(source_path).resolve()

    if not source.exists():
        return False, f"Source path does not exist: {source}"

    if not source.is_dir():
        return False, f"Source path is not a directory: {source}"

    try:
        shutil.copytree(source, target_dir, dirs_exist_ok=True)
        return True, "Copied successfully"
    except Exception as e:
        return False, f"Error during copy: {str(e)}"

def verify_skill(skill_dir):
    """Verify that the installed Skill is valid."""
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Check SKILL.md has YAML frontmatter
    try:
        content = skill_md.read_text()
        if not content.startswith('---'):
            return False, "SKILL.md missing YAML frontmatter"

        # Basic check for name and description
        if 'name:' not in content or 'description:' not in content:
            return False, "SKILL.md missing required fields (name, description)"

        return True, "Skill is valid"
    except Exception as e:
        return False, f"Error reading SKILL.md: {str(e)}"

def install_skill(url_or_path, skill_name=None):
    """Install a Skill from URL or local path."""
    result = {
        "success": False,
        "skill_name": None,
        "install_path": None,
        "message": None,
        "error": None
    }

    # Determine skill name
    if not skill_name:
        if is_github_url(url_or_path):
            skill_name = extract_skill_name_from_url(url_or_path)
        else:
            skill_name = Path(url_or_path).name

    if not skill_name:
        result["error"] = "Could not determine skill name. Please provide --skill-name"
        return result

    result["skill_name"] = skill_name

    # Prepare target directory
    skills_dir = get_skills_directory()
    target_dir = skills_dir / skill_name

    # Check if already exists
    if target_dir.exists():
        result["error"] = f"Skill '{skill_name}' already exists at {target_dir}. Remove it first or use a different name."
        return result

    result["install_path"] = str(target_dir)

    # Install from GitHub or local
    if is_github_url(url_or_path):
        success, message = clone_from_github(url_or_path, target_dir)
    else:
        success, message = copy_from_local(url_or_path, target_dir)

    if not success:
        result["error"] = message
        # Clean up partial installation
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        return result

    # Verify installation
    valid, verify_message = verify_skill(target_dir)
    if not valid:
        result["error"] = f"Installation completed but verification failed: {verify_message}"
        # Clean up invalid installation
        shutil.rmtree(target_dir, ignore_errors=True)
        return result

    # Success!
    result["success"] = True
    result["message"] = f"✅ Skill '{skill_name}' installed successfully to {target_dir}"

    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python install_skill.py <url_or_path> [--skill-name <name>]"
        }))
        sys.exit(1)

    url_or_path = sys.argv[1]
    skill_name = None

    # Parse optional --skill-name argument
    if len(sys.argv) >= 4 and sys.argv[2] == '--skill-name':
        skill_name = sys.argv[3]

    result = install_skill(url_or_path, skill_name)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result["success"]:
        print("\n🎉 Installation complete! Restart Claude Code to use the new skill.", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"\n❌ Installation failed: {result['error']}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
