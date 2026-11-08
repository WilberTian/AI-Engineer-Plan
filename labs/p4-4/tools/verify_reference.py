"""证明「参考实现能过判分」。两个代码块合并成一个 safety.py（手册里分两段讲）。

    python3 labs/p4-4/tools/verify_reference.py

15 条全绿。这 5 类写法（前缀绕过、内网理由、开标签、大小写变体、source 注入）
最容易被顺手「简化」掉，退回任何一条都会立刻变红，逐条修法见 NOTES §2。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
sys.path.insert(0, str(LAB.parent / "_shared"))
from refkit import verify_reference  # noqa: E402

KNOWN_RED: list[str] = []   # 5 条已全部修掉（2026-11-02），别再把条目加回来当挡箭牌


def build(tmp: Path, code: str) -> None:
    pkg = tmp / "agentlab"
    (pkg / "resilience").mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "resilience" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "resilience" / "safety.py").write_text(code, encoding="utf-8")


def main() -> int:
    return verify_reference(
        page="stage-p4.html", card="p4-4", lab=LAB, build=build,
        combine=[1, 0],              # 先 safe_path/safe_url（要 import），再 SYSTEM/wrap
        expect_red=KNOWN_RED,
    )


if __name__ == "__main__":
    sys.exit(main())
