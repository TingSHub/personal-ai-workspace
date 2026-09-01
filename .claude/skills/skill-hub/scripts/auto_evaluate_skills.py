#!/usr/bin/env python3
"""
Auto-evaluate Skills based on metadata without fetching full content.

Uses simplified scoring based on:
1. Source credibility (official > community-verified > community)
2. Description quality (length, specificity)
3. Domain relevance
"""

import json
import sys
from typing import Dict, Any

def quick_evaluate_skill(skill: Dict[str, Any]) -> Dict[str, Any]:
    """Quick evaluation without fetching full SKILL.md."""

    # 1. 来源可信度 (25分)
    source_score = 0
    if skill['category'] == 'official':
        source_score = 25
    elif skill['category'] == 'community-verified':
        source_score = 20  # awesome-claude-skills验证过
    elif 'github.com' in skill['url']:
        # 社区Skills基础分
        source_score = 12
    else:
        source_score = 5

    # 2. 社区热度 (20分) - 基于来源推测
    activity_score = 0
    if skill['category'] == 'official':
        activity_score = 20
    elif skill['category'] == 'community-verified':
        activity_score = 18  # awesome-claude-skills收录说明有热度
    else:
        activity_score = 10

    # 3. 任务明确性 (20分) - 基于描述质量
    clarity_score = 0
    desc = skill.get('description', '')
    if len(desc) > 80:
        clarity_score = 18
    elif len(desc) > 50:
        clarity_score = 15
    elif len(desc) > 20:
        clarity_score = 10
    else:
        clarity_score = 5

    # 描述中包含关键词加分
    keywords = ['automate', 'create', 'analyze', 'manage', 'integrate', 'generate']
    if any(kw in desc.lower() for kw in keywords):
        clarity_score = min(clarity_score + 2, 20)

    # 4. 可复用性 (15分) - 默认推测
    reusability_score = 12  # 假设大部分Skills可复用

    # 5. 安全性 (10分) - 保守估计
    security_score = 8  # 假设基本安全

    # 6. 跨平台兼容 (10分)
    compatibility_score = 9  # 假设大部分跨平台

    total_score = (source_score + activity_score + clarity_score +
                   reusability_score + security_score + compatibility_score)

    return {
        **skill,
        'scores': {
            'source': source_score,
            'activity': activity_score,
            'clarity': clarity_score,
            'reusability': reusability_score,
            'security': security_score,
            'compatibility': compatibility_score,
            'total': total_score
        },
        'recommendation': get_recommendation(total_score)
    }

def get_recommendation(score: int) -> str:
    """Get recommendation level based on score."""
    if score >= 90:
        return "强烈推荐"
    elif score >= 80:
        return "推荐"
    elif score >= 70:
        return "建议"
    elif score >= 60:
        return "谨慎"
    else:
        return "不推荐"

def main():
    if len(sys.argv) < 2:
        print("用法: python auto_evaluate_skills.py <skills_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        data = json.load(f)

    skills = data.get('skills', [])

    print(f"正在评估 {len(skills)} 个Skills...")

    evaluated_skills = []
    for skill in skills:
        evaluated = quick_evaluate_skill(skill)
        evaluated_skills.append(evaluated)

    # 按总分排序
    evaluated_skills.sort(key=lambda x: x['scores']['total'], reverse=True)

    # 统计
    recommendations = {}
    for skill in evaluated_skills:
        rec = skill['recommendation']
        recommendations[rec] = recommendations.get(rec, 0) + 1

    result = {
        'total_evaluated': len(evaluated_skills),
        'recommendations': recommendations,
        'skills': evaluated_skills
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
