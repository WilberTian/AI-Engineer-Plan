"""判分器体检：往 cite.py 里塞已知错。

    python3 labs/p2-9/tools/self_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
sys.path.insert(0, str(LAB.parent / "_shared"))
from refkit import self_test  # noqa: E402

from verify_reference import build  # noqa: E402

MUTATIONS = [
    (
        "编号从 0 开始",
        '    return "\\n\\n".join(f"[{i}] ({src}) {text}" for i, (src, text) in enumerate(chunks, 1))',
        '    return "\\n\\n".join(f"[{i}] ({src}) {text}" for i, (src, text) in enumerate(chunks))',
        "编号从 1 开始",
    ),
    (
        "上下文不带来源路径",
        'f"[{i}] ({src}) {text}"',
        'f"[{i}] {text}"',
        "每块带来源路径",
    ),
    (
        "块之间不隔开",
        '    return "\\n\\n".join(',
        '    return "\\n".join(',
        "块之间有空行分隔",
    ),
    (
        "不判超范围编号",
        "    invalid = [c for c in cited if c < 1 or c > n_chunks]",
        "    invalid = []",
        "超范围编号判非法",
    ),
    (
        "不去重",
        "    cited = sorted({int(m) for m in CITE.findall(answer)})",
        "    cited = sorted([int(m) for m in CITE.findall(answer)])",
        "重复引用去重",
    ),
    (
        "拒答句式不在豁免名单里",
        'REFUSAL = ("资料中没有", "无法回答", "没有相关信息")',
        "REFUSAL = ()",
        "拒答句豁免",
    ),
    (
        "加回 15 字长度过滤（短句被跳过）",
        "    sentences = [s for s in sentences if len(CITE.sub(\"\", s).strip()) >= 2]",
        "    sentences = [s for s in sentences if len(s) > 15]",
        "短句也检查",
    ),
    (
        "只按中文句号切（英文整段算一句）",
        'SENT_SPLIT = re.compile(r"[。！？；\\n]|(?<=[.!?])\\s+")',
        'SENT_SPLIT = re.compile(r"[。\\n]")',
        "英文句子也被切分",
    ),
    (
        "ok 永远为真",
        "        return not self.invalid and len(self.uncited_sentences) <= 1",
        "        return True",
        "ok 判据一致",
    ),
]


def main() -> int:
    return self_test(
        page="stage-p2.html", card="p2-9", lab=LAB, build=build, combine=[1, 0],
        mutations=MUTATIONS,
    )


if __name__ == "__main__":
    sys.exit(main())
