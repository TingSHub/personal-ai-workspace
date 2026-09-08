import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_content_collaboration.py"


BASE = """---
topic_id: \"TOPIC-1\"
review_mode: \"manual\"
discussion_status: \"{discussion_status}\"
assistant_ready: {assistant_ready}
user_ready: {user_ready}
mother_review: \"{mother_review}\"
spoken_review: \"{spoken_review}\"
---

# Content Collaboration: TOPIC-1

## Topic Research Discussion
### Round 1
用户观点：待核验

## Current Synthesis
当前判断：待收敛

## Mother Draft
母稿：待审核

## Mother Draft Review
状态：{mother_review}

## Spoken Draft And Review
口播：待审核

## Handoff
执行允许：待定
"""


def run_check(text: str, phase: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "content-collaboration.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            ["python3", str(SCRIPT), "--collaboration", str(path), "--phase", phase],
            text=True,
            capture_output=True,
            check=False,
        )


class ContentCollaborationCheckTest(unittest.TestCase):
    def test_research_can_remain_active(self):
        result = run_check(BASE.format(discussion_status="active", assistant_ready="false", user_ready="false", mother_review="pending", spoken_review="pending"), "research")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_mother_requires_both_ready_flags(self):
        result = run_check(BASE.format(discussion_status="closed", assistant_ready="true", user_ready="false", mother_review="pending", spoken_review="pending"), "mother")
        self.assertEqual(result.returncode, 1)
        self.assertIn("discussion_status=closed", result.stdout)

    def test_spoken_requires_mother_and_spoken_approval(self):
        result = run_check(BASE.format(discussion_status="closed", assistant_ready="true", user_ready="true", mother_review="approved", spoken_review="approved"), "spoken")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_spoken_blocks_until_mother_is_approved(self):
        result = run_check(BASE.format(discussion_status="closed", assistant_ready="true", user_ready="true", mother_review="revise", spoken_review="approved"), "spoken")
        self.assertEqual(result.returncode, 1)
        self.assertIn("mother_review", result.stdout)


if __name__ == "__main__":
    unittest.main()
