#!/usr/bin/env python3
"""
Fetch Skill content from GitHub URL or local path.

Usage:
    python fetch_skill.py <url_or_path>

Returns JSON with:
    {
        "skill_md": "content of SKILL.md",
        "scripts": {"filename": "content", ...},
        "error": "error message if any"
    }
"""

import sys
import json
import os
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import urllib.error


def convert_github_url_to_raw(url):
    """Convert GitHub URL to raw content URL."""
    parsed = urlparse(url)

    # Handle github.com URLs
    if 'github.com' in parsed.netloc:
        path_parts = parsed.path.strip('/').split('/')

        # Case 1: Direct file URL with blob
        # https://github.com/user/repo/blob/main/path/to/SKILL.md
        if len(path_parts) >= 4 and path_parts[2] == 'blob':
            user = path_parts[0]
            repo = path_parts[1]
            branch = path_parts[3]
            file_path = '/'.join(path_parts[4:])
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"

        # Case 2: Directory URL with tree
        # https://github.com/user/repo/tree/main/path/to/skill
        if len(path_parts) >= 4 and path_parts[2] == 'tree':
            user = path_parts[0]
            repo = path_parts[1]
            branch = path_parts[3]
            file_path = '/'.join(path_parts[4:]) if len(path_parts) > 4 else ''
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"

        # Case 3: Repository root URL - try main branch by default
        # https://github.com/user/repo
        if len(path_parts) >= 2:
            user = path_parts[0]
            repo = path_parts[1]
            return f"https://raw.githubusercontent.com/{user}/{repo}/main/SKILL.md"

    # Already raw.githubusercontent.com
    if 'raw.githubusercontent.com' in parsed.netloc:
        return url

    return None


def fetch_url_content(url):
    """Fetch content from URL."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        return None
    except Exception as e:
        return None


def fetch_from_github(url):
    """Fetch Skill content from GitHub URL."""
    result = {
        "skill_md": None,
        "scripts": {},
        "error": None
    }

    # Convert to raw URL if needed
    if '/SKILL.md' not in url:
        # Assume user provided repo root, append /SKILL.md
        base_url = url.rstrip('/')
        skill_url = f"{base_url}/SKILL.md"
    else:
        skill_url = url

    raw_url = convert_github_url_to_raw(skill_url)
    if not raw_url:
        result["error"] = "无法解析 GitHub URL，请提供正确的 GitHub 文件链接"
        return result

    # Fetch SKILL.md
    skill_content = fetch_url_content(raw_url)
    if not skill_content:
        result["error"] = f"无法访问 {skill_url}，请确认 URL 是否正确或仓库是否公开"
        return result

    result["skill_md"] = skill_content

    # Try to fetch scripts directory
    # Calculate scripts directory URL
    base_raw_url = raw_url.rsplit('/SKILL.md', 1)[0]
    scripts_base = f"{base_raw_url}/scripts"

    # Try common script filenames
    common_scripts = [
        'example.py', 'main.py', 'script.py', 'run.py',
        'example.sh', 'main.sh', 'script.sh', 'run.sh'
    ]

    for script_name in common_scripts:
        script_url = f"{scripts_base}/{script_name}"
        script_content = fetch_url_content(script_url)
        if script_content:
            result["scripts"][script_name] = script_content

    return result


def fetch_from_local(path):
    """Fetch Skill content from local path."""
    result = {
        "skill_md": None,
        "scripts": {},
        "error": None
    }

    path_obj = Path(path).expanduser().resolve()

    # If path is a file, assume it's SKILL.md
    if path_obj.is_file():
        try:
            result["skill_md"] = path_obj.read_text(encoding='utf-8')
        except Exception as e:
            result["error"] = f"无法读取文件：{e}"
            return result

        # Look for scripts in same directory
        scripts_dir = path_obj.parent / 'scripts'
    else:
        # Path is a directory
        skill_file = path_obj / 'SKILL.md'
        if not skill_file.exists():
            result["error"] = f"未找到 SKILL.md 文件：{skill_file}"
            return result

        try:
            result["skill_md"] = skill_file.read_text(encoding='utf-8')
        except Exception as e:
            result["error"] = f"无法读取文件：{e}"
            return result

        scripts_dir = path_obj / 'scripts'

    # Read scripts if directory exists
    if scripts_dir.exists() and scripts_dir.is_dir():
        for script_file in scripts_dir.iterdir():
            if script_file.is_file() and script_file.suffix in ['.py', '.sh', '.js']:
                try:
                    result["scripts"][script_file.name] = script_file.read_text(encoding='utf-8')
                except Exception:
                    pass  # Skip unreadable files

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "skill_md": None,
            "scripts": {},
            "error": "用法：python fetch_skill.py <url_or_path>"
        }))
        sys.exit(1)

    input_path = sys.argv[1]

    # Determine if input is URL or local path
    if input_path.startswith('http://') or input_path.startswith('https://'):
        result = fetch_from_github(input_path)
    else:
        result = fetch_from_local(input_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
