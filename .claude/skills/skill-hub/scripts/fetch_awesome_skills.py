#!/usr/bin/env python3
"""
Fetch all Skills from ComposioHQ/awesome-claude-skills repository.

This script parses the README and extracts all Skill names, URLs, and descriptions.
"""

import json
import urllib.request
import urllib.error
import re
from typing import List, Dict, Any

def fetch_awesome_skills_readme() -> str:
    """Fetch the README from awesome-claude-skills repository."""
    url = "https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/README.md"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching README: {e}")
        return ""

def parse_skills_from_readme(readme: str) -> List[Dict[str, Any]]:
    """Parse Skills from the README markdown."""
    skills = []

    # Pattern to match skill entries like:
    # - [Name](url) - Description
    pattern = r'-\s+\[([^\]]+)\]\(([^\)]+)\)\s+-\s+([^\n]+)'

    matches = re.findall(pattern, readme)

    current_category = "General"
    category_pattern = r'###\s+([^\n]+)'
    categories = re.findall(category_pattern, readme)

    # Parse with category context
    lines = readme.split('\n')
    current_category = "General"

    for line in lines:
        # Update category
        category_match = re.match(r'###\s+([^\n]+)', line)
        if category_match:
            current_category = category_match.group(1).strip()
            continue

        # Parse skill entry
        skill_match = re.match(r'-\s+\[([^\]]+)\]\(([^\)]+)\)\s+-\s+(.+)', line)
        if skill_match:
            name = skill_match.group(1).strip()
            url = skill_match.group(2).strip()
            description = skill_match.group(3).strip()

            # Remove author attributions
            description = re.sub(r'\*By\s+\[@[^\]]+\]\([^\)]+\)\*', '', description).strip()

            # Determine source
            if 'anthropics/skills' in url or 'github.com/anthropics' in url:
                source = "anthropic-official"
                category_type = "official"
            elif url.startswith('./') or url.startswith('../'):
                # Local Skills in awesome-claude-skills repo
                full_url = f"https://github.com/ComposioHQ/awesome-claude-skills/tree/master/{url.lstrip('./')}"
                url = full_url
                source = "ComposioHQ/awesome-claude-skills"
                category_type = "community-verified"
            else:
                source = url.split('github.com/')[-1].split('/tree/')[0].split('/blob/')[0] if 'github.com' in url else "unknown"
                category_type = "community"

            skills.append({
                "name": name,
                "url": url,
                "description": description,
                "source": source,
                "category": category_type,
                "domain": current_category
            })

    return skills

def main():
    print("Fetching Skills from ComposioHQ/awesome-claude-skills...")

    readme = fetch_awesome_skills_readme()
    if not readme:
        print("Failed to fetch README")
        return

    skills = parse_skills_from_readme(readme)

    # Output results
    result = {
        "total_found": len(skills),
        "skills": skills,
        "categories": list(set(s['domain'] for s in skills)),
        "sources": {
            "official": len([s for s in skills if s['category'] == 'official']),
            "community-verified": len([s for s in skills if s['category'] == 'community-verified']),
            "community": len([s for s in skills if s['category'] == 'community'])
        }
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
