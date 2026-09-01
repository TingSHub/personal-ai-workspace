#!/usr/bin/env python3
"""
Analyze a Skill to extract construction patterns and best practices.

Usage:
    python analyze_skill_patterns.py <github_url_or_local_path>

This script analyzes an existing Skill and provides:
1. Architecture patterns (how it's structured)
2. Key implementation techniques
3. Reusable components
4. Construction guidance for building similar Skills

Returns JSON with construction guidance.
"""

import sys
import json
import re
from pathlib import Path
import subprocess

def analyze_skill_structure(skill_md_content):
    """Analyze SKILL.md structure and extract patterns."""
    patterns = {
        "frontmatter": {},
        "has_workflows": False,
        "has_progressive_disclosure": False,
        "trigger_patterns": [],
        "tool_usage": [],
        "reference_files": [],
        "script_files": [],
        "asset_files": []
    }

    # Extract YAML frontmatter
    if skill_md_content.startswith('---'):
        parts = skill_md_content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    patterns["frontmatter"][key.strip()] = value.strip()

    # Check for workflow patterns
    if 'workflow' in skill_md_content.lower() or '## step' in skill_md_content.lower():
        patterns["has_workflows"] = True

    # Check for progressive disclosure (references to other files)
    ref_pattern = r'\[([^\]]+)\]\(([^\)]+\.md)\)'
    refs = re.findall(ref_pattern, skill_md_content)
    patterns["reference_files"] = [ref[1] for ref in refs]
    if refs:
        patterns["has_progressive_disclosure"] = True

    # Extract trigger patterns from description
    desc = patterns["frontmatter"].get("description", "")
    if "trigger" in desc.lower() or "use when" in desc.lower():
        # Extract quoted phrases as trigger examples
        trigger_matches = re.findall(r'"([^"]+)"', desc)
        patterns["trigger_patterns"] = trigger_matches

    # Extract tool usage mentions
    tool_keywords = ['bash', 'read', 'write', 'edit', 'glob', 'grep', 'webfetch']
    content_lower = skill_md_content.lower()
    for tool in tool_keywords:
        if tool in content_lower:
            patterns["tool_usage"].append(tool)

    # Extract script references
    script_pattern = r'scripts/([a-zA-Z0-9_\-\.]+)'
    scripts = re.findall(script_pattern, skill_md_content)
    patterns["script_files"] = list(set(scripts))

    # Extract asset references
    asset_pattern = r'assets/([a-zA-Z0-9_\-\.\/]+)'
    assets = re.findall(asset_pattern, skill_md_content)
    patterns["asset_files"] = list(set(assets))

    return patterns

def analyze_scripts(scripts_content):
    """Analyze scripts to extract implementation patterns."""
    script_patterns = {
        "languages": set(),
        "external_dependencies": [],
        "api_usage": [],
        "file_operations": [],
        "complexity_level": "simple"
    }

    for filename, content in scripts_content.items():
        # Detect language
        if filename.endswith('.py'):
            script_patterns["languages"].add("Python")
            # Extract Python imports
            imports = re.findall(r'^import\s+(\S+)', content, re.MULTILINE)
            imports += re.findall(r'^from\s+(\S+)', content, re.MULTILINE)
            script_patterns["external_dependencies"].extend(imports)

        elif filename.endswith('.sh') or filename.endswith('.bash'):
            script_patterns["languages"].add("Bash")

        elif filename.endswith('.js') or filename.endswith('.ts'):
            script_patterns["languages"].add("JavaScript/TypeScript")
            # Extract npm requires
            requires = re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', content)
            script_patterns["external_dependencies"].extend(requires)

        # Detect API usage
        if 'urllib.request' in content or 'requests.' in content:
            script_patterns["api_usage"].append("HTTP requests")
        if 'json.' in content:
            script_patterns["api_usage"].append("JSON processing")

        # Detect file operations
        if 'open(' in content or 'Path(' in content:
            script_patterns["file_operations"].append("File I/O")

        # Estimate complexity
        lines = len(content.split('\n'))
        if lines > 200:
            script_patterns["complexity_level"] = "complex"
        elif lines > 100:
            script_patterns["complexity_level"] = "moderate"

    script_patterns["languages"] = list(script_patterns["languages"])
    script_patterns["external_dependencies"] = list(set(script_patterns["external_dependencies"]))
    script_patterns["api_usage"] = list(set(script_patterns["api_usage"]))
    script_patterns["file_operations"] = list(set(script_patterns["file_operations"]))

    return script_patterns

def generate_construction_guide(patterns, script_patterns):
    """Generate construction guidance based on analyzed patterns."""
    guide = {
        "skill_type": classify_skill_type(patterns, script_patterns),
        "architecture_overview": describe_architecture(patterns, script_patterns),
        "key_components": list_key_components(patterns, script_patterns),
        "implementation_steps": generate_implementation_steps(patterns, script_patterns),
        "reusable_patterns": extract_reusable_patterns(patterns, script_patterns),
        "similar_examples": suggest_similar_examples(patterns, script_patterns),
        "construction_tips": generate_tips(patterns, script_patterns)
    }

    return guide

def classify_skill_type(patterns, script_patterns):
    """Classify the type of Skill."""
    if script_patterns["languages"]:
        if "HTTP requests" in script_patterns["api_usage"]:
            return "API Integration Skill"
        elif script_patterns["file_operations"]:
            return "File Processing Skill"
        else:
            return "Automation Skill"
    elif patterns["has_workflows"]:
        return "Workflow Guidance Skill"
    else:
        return "Knowledge/Domain Skill"

def describe_architecture(patterns, script_patterns):
    """Describe the architectural approach."""
    desc = []

    if patterns["has_workflows"]:
        desc.append("Uses step-by-step workflow structure")

    if patterns["has_progressive_disclosure"]:
        desc.append(f"Employs progressive disclosure with {len(patterns['reference_files'])} reference files")

    if script_patterns["languages"]:
        langs = ", ".join(script_patterns["languages"])
        desc.append(f"Includes executable scripts in: {langs}")

    if not desc:
        desc.append("Simple instructional Skill with minimal structure")

    return " | ".join(desc)

def list_key_components(patterns, script_patterns):
    """List key components of the Skill."""
    components = []

    # SKILL.md components
    if patterns["frontmatter"]:
        components.append({
            "type": "SKILL.md frontmatter",
            "purpose": "Metadata and triggering information",
            "details": f"Contains: {', '.join(patterns['frontmatter'].keys())}"
        })

    if patterns["trigger_patterns"]:
        components.append({
            "type": "Trigger patterns",
            "purpose": "Define when Skill activates",
            "details": f"Examples: {', '.join(patterns['trigger_patterns'][:3])}"
        })

    # Scripts
    if script_patterns["languages"]:
        components.append({
            "type": "Executable scripts",
            "purpose": "Perform deterministic operations",
            "details": f"Languages: {', '.join(script_patterns['languages'])}, Complexity: {script_patterns['complexity_level']}"
        })

    # References
    if patterns["reference_files"]:
        components.append({
            "type": "Reference files",
            "purpose": "Extended documentation for progressive disclosure",
            "details": f"Files: {', '.join(patterns['reference_files'])}"
        })

    # Assets
    if patterns["asset_files"]:
        components.append({
            "type": "Asset files",
            "purpose": "Templates or resources used in output",
            "details": f"Assets: {len(patterns['asset_files'])} files"
        })

    return components

def generate_implementation_steps(patterns, script_patterns):
    """Generate step-by-step implementation guide."""
    steps = []

    steps.append({
        "step": 1,
        "title": "Initialize Skill structure",
        "action": "Use skill-creator's init_skill.py to generate the Skill skeleton",
        "command": "python scripts/init_skill.py <skill-name>"
    })

    steps.append({
        "step": 2,
        "title": "Define SKILL.md frontmatter",
        "action": "Write clear name and comprehensive description with trigger patterns",
        "tips": [
            "Include 'Use when' scenarios in description",
            "Add example trigger phrases in quotes",
            "Be specific about what the Skill does"
        ]
    })

    if script_patterns["languages"]:
        steps.append({
            "step": 3,
            "title": "Implement scripts",
            "action": f"Write executable scripts in {', '.join(script_patterns['languages'])}",
            "tips": [
                "Keep scripts focused on single responsibility",
                "Return JSON for easy parsing",
                "Handle errors gracefully with clear messages",
                f"Install dependencies: {', '.join(script_patterns['external_dependencies'][:5])}"
            ]
        })

    if patterns["has_workflows"]:
        steps.append({
            "step": 4,
            "title": "Document workflows",
            "action": "Write step-by-step workflow instructions in SKILL.md",
            "tips": [
                "Use numbered steps for sequential workflows",
                "Show example commands with expected outputs",
                "Document edge cases and error handling"
            ]
        })

    if patterns["reference_files"]:
        steps.append({
            "step": 5,
            "title": "Create reference files",
            "action": "Move detailed documentation to references/ directory",
            "tips": [
                "Keep SKILL.md under 500 lines",
                "Reference files should be linked from SKILL.md",
                "Include table of contents for long reference files"
            ]
        })

    steps.append({
        "step": len(steps) + 1,
        "title": "Test and validate",
        "action": "Use skill-creator's package_skill.py to validate",
        "command": "python scripts/package_skill.py <path/to/skill>"
    })

    return steps

def extract_reusable_patterns(patterns, script_patterns):
    """Extract reusable patterns from this Skill."""
    reusable = []

    if patterns["trigger_patterns"]:
        reusable.append({
            "pattern": "Trigger pattern definition",
            "description": "Define multiple trigger phrases in description",
            "example": f'description: "... Use when: {patterns["trigger_patterns"][0]}"'
        })

    if patterns["has_progressive_disclosure"]:
        reusable.append({
            "pattern": "Progressive disclosure",
            "description": "Keep SKILL.md concise, move details to reference files",
            "example": "See [REFERENCE.md](references/REFERENCE.md) for details"
        })

    if "JSON processing" in script_patterns["api_usage"]:
        reusable.append({
            "pattern": "JSON output format",
            "description": "Scripts return structured JSON for easy parsing",
            "example": 'print(json.dumps(result, ensure_ascii=False, indent=2))'
        })

    if patterns["has_workflows"]:
        reusable.append({
            "pattern": "Multi-step workflow",
            "description": "Break complex tasks into sequential steps",
            "example": "Step 1: ... Step 2: ... Step 3: ..."
        })

    return reusable

def suggest_similar_examples(patterns, script_patterns):
    """Suggest similar Skills as examples."""
    suggestions = []

    skill_type = classify_skill_type(patterns, script_patterns)

    if skill_type == "API Integration Skill":
        suggestions = [
            "safe-skill-copy (GitHub API integration)",
            "mcp-builder (API server creation)",
            "web-fetch Skills (HTTP requests)"
        ]
    elif skill_type == "File Processing Skill":
        suggestions = [
            "docx (Word document processing)",
            "xlsx (Spreadsheet processing)",
            "pdf (PDF manipulation)",
            "pptx (Presentation processing)"
        ]
    elif skill_type == "Workflow Guidance Skill":
        suggestions = [
            "skill-creator (Skill creation workflow)",
            "doc-coauthoring (Document co-authoring workflow)"
        ]
    else:
        suggestions = [
            "Anthropic official Skills (github.com/anthropics/skills)",
            "awesome-claude-skills community Skills"
        ]

    return suggestions

def generate_tips(patterns, script_patterns):
    """Generate construction tips."""
    tips = [
        "Start with concrete examples of how the Skill will be used",
        "Keep SKILL.md under 500 lines for better context efficiency",
        "Test scripts independently before integrating",
        "Use descriptive names for scripts (fetch_X.py, analyze_Y.py)"
    ]

    if script_patterns["complexity_level"] == "complex":
        tips.append("Consider breaking complex scripts into smaller modules")

    if patterns["has_workflows"]:
        tips.append("Show example outputs after each workflow step")

    if not patterns["trigger_patterns"]:
        tips.append("Add explicit trigger patterns to description for better activation")

    if len(script_patterns["external_dependencies"]) > 5:
        tips.append("Document all dependencies in README or installation guide")

    return tips

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python analyze_skill_patterns.py <github_url_or_local_path>"
        }))
        sys.exit(1)

    url_or_path = sys.argv[1]

    # Fetch Skill content using fetch_skill.py
    fetch_script = Path(__file__).parent / "fetch_skill.py"
    result = subprocess.run(
        ['python3', str(fetch_script), url_or_path],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        print(json.dumps({
            "error": f"Failed to fetch Skill: {result.stderr}"
        }))
        sys.exit(1)

    try:
        skill_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(json.dumps({
            "error": "Failed to parse Skill data"
        }))
        sys.exit(1)

    if skill_data.get("error"):
        print(json.dumps({
            "error": skill_data["error"]
        }))
        sys.exit(1)

    # Analyze patterns
    skill_md = skill_data.get("skill_md", "")
    scripts = skill_data.get("scripts", {})

    patterns = analyze_skill_structure(skill_md)
    script_patterns = analyze_scripts(scripts)
    guide = generate_construction_guide(patterns, script_patterns)

    # Output complete analysis
    output = {
        "patterns": patterns,
        "script_patterns": script_patterns,
        "construction_guide": guide
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
