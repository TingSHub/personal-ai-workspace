#!/usr/bin/env python3
"""
Generate 100 unique Skills recommendations for 10 professional roles (10 Skills each).
"""

import json
import sys
from typing import List, Dict, Any

# 10大职业角色及其需求关键词
ROLES = {
    "内容创作者/编辑": {
        "keywords": ["doc", "write", "content", "article", "blog", "social", "twitter", "linkedin", "newsletter", "communication"],
        "must_have": ["doc-coauthoring", "docx", "pptx", "canvas-design", "pdf"]
    },
    "产品经理/项目经理": {
        "keywords": ["project", "task", "linear", "jira", "asana", "notion", "trello", "manage", "workflow", "collaboration"],
        "must_have": ["doc-coauthoring", "xlsx", "pptx", "Linear", "Notion Automation"]
    },
    "前端工程师": {
        "keywords": ["frontend", "react", "web", "ui", "design", "test", "playwright", "figma", "component", "artifact"],
        "must_have": ["skill-creator", "frontend-design", "web-artifacts-builder", "webapp-testing", "Figma Automation"]
    },
    "后端工程师/架构师": {
        "keywords": ["backend", "api", "database", "server", "aws", "docker", "ci", "github", "gitlab", "deploy"],
        "must_have": ["skill-creator", "mcp-builder", "GitHub Automation", "aws-skills", "postgres"]
    },
    "数据分析师": {
        "keywords": ["data", "analytics", "spreadsheet", "csv", "chart", "visualization", "python", "sql", "database"],
        "must_have": ["xlsx", "CSV Data Summarizer", "pdf", "postgres", "Google Sheets Automation"]
    },
    "商业运营": {
        "keywords": ["business", "crm", "sales", "marketing", "email", "campaign", "hubspot", "salesforce", "analytics"],
        "must_have": ["xlsx", "pptx", "HubSpot Automation", "Gmail Automation", "Google Analytics Automation"]
    },
    "研究人员/学者": {
        "keywords": ["research", "pdf", "doc", "academic", "paper", "citation", "notebook", "analysis", "deep"],
        "must_have": ["skill-creator", "pdf", "xlsx", "doc-coauthoring", "deep-research"]
    },
    "UI/UX设计师": {
        "keywords": ["design", "ui", "ux", "figma", "canvas", "miro", "webflow", "creative", "brand", "theme"],
        "must_have": ["canvas-design", "frontend-design", "Figma Automation", "brand-guidelines", "theme-factory"]
    },
    "企业管理者/高管": {
        "keywords": ["business", "analytics", "report", "dashboard", "communication", "strategy", "finance", "team"],
        "must_have": ["pptx", "doc-coauthoring", "xlsx", "internal-comms", "Google Analytics Automation"]
    },
    "教师/培训师": {
        "keywords": ["education", "teaching", "training", "course", "presentation", "doc", "youtube", "canvas", "content"],
        "must_have": ["pptx", "doc-coauthoring", "docx", "pdf", "canvas-design"]
    }
}

def calculate_role_relevance(skill: Dict[str, Any], role_keywords: List[str]) -> float:
    """Calculate how relevant a skill is to a role."""
    text = f"{skill['name']} {skill['description']}".lower()

    matches = sum(1 for kw in role_keywords if kw in text)
    return matches / len(role_keywords) if role_keywords else 0

def assign_skills_to_roles(skills: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Assign 10 Skills to each of the 10 roles."""

    role_skills = {}
    used_skills = set()

    for role_name, role_config in ROLES.items():
        role_keywords = role_config['keywords']
        must_have_names = role_config['must_have']

        assigned = []

        # 1. 首先添加必装Skills
        for must_have in must_have_names:
            for skill in skills:
                if (skill['name'] == must_have or must_have.lower() in skill['name'].lower()) and skill['name'] not in used_skills:
                    assigned.append(skill)
                    used_skills.add(skill['name'])
                    break

        # 2. 然后根据相关性添加推荐Skills
        candidates = []
        for skill in skills:
            if skill['name'] not in used_skills:
                relevance = calculate_role_relevance(skill, role_keywords)
                if relevance > 0:
                    candidates.append((skill, relevance))

        # 按相关性排序
        candidates.sort(key=lambda x: (-x[1], -x[0]['scores']['total']))

        # 补充到10个
        for skill, _ in candidates:
            if len(assigned) >= 10:
                break
            if skill['name'] not in used_skills:
                assigned.append(skill)
                used_skills.add(skill['name'])

        # 如果还不够10个，从剩余高分Skills中补充
        if len(assigned) < 10:
            remaining = [s for s in skills if s['name'] not in used_skills]
            remaining.sort(key=lambda x: -x['scores']['total'])
            for skill in remaining:
                if len(assigned) >= 10:
                    break
                assigned.append(skill)
                used_skills.add(skill['name'])

        role_skills[role_name] = assigned[:10]  # 确保最多10个

    return role_skills

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_role_recommendations.py <evaluated_skills.json>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        data = json.load(f)

    # 只选择80分以上的Skills
    high_quality_skills = [s for s in data['skills'] if s['scores']['total'] >= 80]

    print(f"从 {len(high_quality_skills)} 个高质量Skills中分配...")

    role_assignments = assign_skills_to_roles(high_quality_skills)

    # 统计
    total_unique = len(set(s['name'] for skills in role_assignments.values() for s in skills))

    result = {
        'total_roles': len(role_assignments),
        'total_unique_skills': total_unique,
        'roles': role_assignments
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
