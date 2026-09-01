#!/usr/bin/env python3
"""
Search for Claude Skills based on user requirements.

Usage:
    python search_skills.py "<user requirement>"

Example:
    python search_skills.py "数据分析和可视化"
    python search_skills.py "project management and task tracking"

Returns JSON with:
    {
        "query": "original query",
        "results": [
            {
                "name": "skill-name",
                "url": "github-url",
                "description": "description",
                "relevance_score": 0.85,
                "category": "category-name"
            }
        ]
    }
"""

import sys
import json
import urllib.request
import urllib.error
import re
from typing import List, Dict, Any

# Known high-quality Skill sources
SKILL_SOURCES = [
    {
        "type": "github_api",
        "repo": "anthropics/skills",
        "base_url": "https://api.github.com/repos/anthropics/skills/contents/skills",
        "category": "official"
    },
    {
        "type": "github_search",
        "query": "claude skill SKILL.md",
        "category": "community"
    }
]

# Keyword mapping for common requirements (bilingual)
KEYWORD_MAPPINGS = {
    # Data & Analytics
    "数据分析": ["data analysis", "analytics", "csv", "excel", "pandas", "visualization"],
    "数据可视化": ["visualization", "chart", "plot", "graph", "matplotlib"],
    "表格处理": ["spreadsheet", "excel", "csv", "xlsx", "table"],

    # Project Management
    "项目管理": ["project management", "task", "issue", "kanban", "linear", "jira"],
    "任务追踪": ["task tracking", "todo", "issue", "ticket", "project"],

    # Development
    "代码审查": ["code review", "review", "pull request", "pr"],
    "测试": ["test", "testing", "tdd", "unit test", "playwright"],
    "调试": ["debug", "debugging", "troubleshoot"],
    "前端开发": ["frontend", "react", "vue", "web", "ui"],
    "后端开发": ["backend", "api", "server", "database"],

    # Documentation
    "文档": ["documentation", "doc", "docx", "pdf", "markdown"],
    "演示文稿": ["presentation", "slides", "pptx", "powerpoint"],
    "写作": ["writing", "content", "article", "blog"],

    # Security
    "安全": ["security", "vulnerability", "audit", "penetration"],
    "加密": ["encryption", "crypto", "blockchain", "bitcoin"],

    # Research
    "研究": ["research", "analysis", "investigation", "study"],
    "学术": ["academic", "paper", "citation", "reference"],

    # Design
    "设计": ["design", "ui", "ux", "canvas", "figma"],
    "艺术": ["art", "creative", "generative", "algorithmic"],

    # Automation
    "自动化": ["automation", "workflow", "integration", "api"],
    "集成": ["integration", "connect", "sync", "api"]
}

def expand_keywords(query: str) -> List[str]:
    """Expand user query with related keywords."""
    keywords = [query.lower()]

    # Add exact matches from mapping
    for chinese, english_list in KEYWORD_MAPPINGS.items():
        if chinese in query:
            keywords.extend(english_list)

    # Extract English words and add variations
    words = re.findall(r'[a-zA-Z]+', query.lower())
    keywords.extend(words)

    return list(set(keywords))

def search_github_api(repo: str, base_url: str) -> List[Dict[str, Any]]:
    """Search Skills using GitHub API."""
    skills = []

    try:
        req = urllib.request.Request(
            base_url,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if isinstance(data, list):
                for item in data:
                    if item['type'] == 'dir':
                        skill_name = item['name']
                        skill_url = f"https://github.com/{repo}/tree/main/skills/{skill_name}"

                        # Try to fetch SKILL.md for description
                        skill_md_url = f"https://raw.githubusercontent.com/{repo}/main/skills/{skill_name}/SKILL.md"
                        description = fetch_skill_description(skill_md_url)

                        skills.append({
                            "name": skill_name,
                            "url": skill_url,
                            "description": description,
                            "source": "anthropic-official",
                            "category": "official"
                        })
    except Exception as e:
        pass  # Silently fail and continue with other sources

    return skills

def fetch_skill_description(url: str) -> str:
    """Fetch description from SKILL.md file."""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')

            # Extract description from YAML frontmatter
            match = re.search(r'description:\s*["\']?([^"\n]+)["\']?', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

            # Fallback: get first paragraph after # heading
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('# ') and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('#'):
                        return next_line[:200]
    except Exception:
        pass

    return "No description available"

def search_github_code_search(query: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """Search GitHub code for SKILL.md files with pagination."""
    skills = []

    # Try multiple search strategies
    search_strategies = [
        f'filename:SKILL.md {query}',
        f'filename:SKILL.md path:.claude/skills {query}',
        f'filename:SKILL.md "claude skill" {query}',
        f'SKILL.md in:file {query}'
    ]

    for search_strategy in search_strategies:
        try:
            # GitHub API allows up to 100 per_page, max 1000 results total (10 pages)
            per_page = 100
            max_pages = min(10, (max_results + per_page - 1) // per_page)

            for page in range(1, max_pages + 1):
                search_query = urllib.parse.quote(search_strategy)
                url = f"https://api.github.com/search/code?q={search_query}&per_page={per_page}&page={page}"

                req = urllib.request.Request(
                    url,
                    headers={'Accept': 'application/vnd.github.v3+json'}
                )

                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode('utf-8'))

                    if 'items' in data and len(data['items']) > 0:
                        for item in data['items']:
                            repo_url = item['repository']['html_url']
                            file_path = item['path']

                            # Extract skill name from path
                            path_parts = file_path.split('/')
                            if 'SKILL.md' in path_parts:
                                idx = path_parts.index('SKILL.md')
                                skill_name = path_parts[idx - 1] if idx > 0 else 'unknown'
                            else:
                                skill_name = path_parts[-2] if len(path_parts) > 1 else 'unknown'

                            # Build skill directory URL
                            skill_dir = '/'.join(file_path.split('/')[:-1])
                            skill_url = f"{repo_url}/tree/{item['repository']['default_branch']}/{skill_dir}"

                            # Fetch description
                            raw_url = item['html_url'].replace('/blob/', '/raw/')
                            description = fetch_skill_description(raw_url)

                            skills.append({
                                "name": skill_name,
                                "url": skill_url,
                                "description": description,
                                "source": item['repository']['full_name'],
                                "category": "community",
                                "stars": item['repository'].get('stargazers_count', 0)
                            })
                    else:
                        # No more results for this strategy
                        break

                # Rate limiting: GitHub allows 10 requests per minute for unauthenticated
                import time
                time.sleep(0.5)

        except urllib.error.HTTPError as e:
            if e.code == 403:  # Rate limit exceeded
                break
            pass  # Continue with next strategy
        except Exception as e:
            pass  # Continue with next strategy

    return skills

def calculate_relevance(skill: Dict[str, Any], keywords: List[str]) -> float:
    """Calculate relevance score based on keyword matching."""
    text = f"{skill['name']} {skill['description']}".lower()

    matches = 0
    total = len(keywords)

    for keyword in keywords:
        if keyword.lower() in text:
            matches += 1

    # Bonus for official Anthropic Skills
    bonus = 0.2 if skill.get('category') == 'official' else 0

    return min((matches / max(total, 1)) + bonus, 1.0)

def deduplicate_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate Skills by name."""
    seen = set()
    unique_skills = []

    for skill in skills:
        if skill['name'] not in seen:
            seen.add(skill['name'])
            unique_skills.append(skill)

    return unique_skills

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "query": None,
            "results": [],
            "error": "用法：python search_skills.py \"<需求描述>\""
        }))
        sys.exit(1)

    user_query = sys.argv[1]

    # Expand keywords
    keywords = expand_keywords(user_query)

    # Search from multiple sources
    all_skills = []

    # 1. Search Anthropic official Skills
    anthropic_skills = search_github_api(
        "anthropics/skills",
        "https://api.github.com/repos/anthropics/skills/contents/skills"
    )
    all_skills.extend(anthropic_skills)

    # 2. Search ComposioHQ/awesome-claude-skills (Priority: 160+ curated Skills)
    awesome_skills = search_github_api(
        "ComposioHQ/awesome-claude-skills",
        "https://api.github.com/repos/ComposioHQ/awesome-claude-skills/contents"
    )
    all_skills.extend(awesome_skills)

    # 3. Search GitHub code (community Skills) - now with pagination
    community_skills = search_github_code_search(user_query, max_results=200)
    all_skills.extend(community_skills)

    # Deduplicate
    all_skills = deduplicate_skills(all_skills)

    # Calculate relevance scores
    for skill in all_skills:
        skill['relevance_score'] = calculate_relevance(skill, keywords)

    # Sort by relevance (descending)
    all_skills.sort(key=lambda x: x['relevance_score'], reverse=True)

    # Filter results with relevance > 0.1
    filtered_skills = [s for s in all_skills if s['relevance_score'] > 0.1]

    # Output results
    result = {
        "query": user_query,
        "keywords": keywords[:5],  # Show top 5 keywords used
        "total_found": len(filtered_skills),
        "results": filtered_skills[:10]  # Top 10 results
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
