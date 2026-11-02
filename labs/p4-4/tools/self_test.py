"""判分器体检：往 safety.py 里塞已知漏洞，看判分能不能抓住。

    python3 labs/p4-4/tools/self_test.py

这里 5 个 mutation 全是**真实存在的绕过手法**，不是随手改坏。
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
        "路径比较退回 startswith（前缀绕过）",
        "    if not any(p.is_relative_to(root) for root in ALLOWED_ROOTS):",
        '    if not any(str(p).startswith(str(root)) for root in ALLOWED_ROOTS):',
        "前缀绕过 ../data-evil 被拦",
    ),
    (
        "白名单少写一个根目录",
        'ALLOWED_ROOTS = [Path("data").resolve(), Path("notes").resolve()]',
        'ALLOWED_ROOTS = [Path("notes").resolve()]',
        "正常相对路径放行",
    ),
    (
        "只允许 http 的检查被删",
        '    if u.scheme not in {"http", "https"}:',
        "    if False:",
        "file:// 被拦且理由提协议",
    ),
    (
        "内网 IP 却报「域名不在白名单」（理由被吞的等价效果）",
        '            raise ValueError(f"不允许访问内网地址：{host}")',
        '            raise ValueError(f"域名不在白名单：{host}")',
        "内网地址的拒绝理由点明「内网」",
    ),
    (
        "内容不做转义",
        '    body = escape(text, quote=False)',
        "    body = text",
        "内容里的闭合标签被转义",
    ),
    (
        "只转义一对精确字符串（旧写法）",
        '    body = escape(text, quote=False)',
        '    body = text.replace("&lt;untrusted&gt;", "xxxx").replace("&lt;/untrusted&gt;", "yyyy").replace("<untrusted>", "&lt;untrusted&gt;").replace("</untrusted>", "&lt;/untrusted&gt;")',
        "内容里的开标签被转义",
    ),
    (
        "source 不转义",
        "    src = escape(source, quote=True)",
        "    src = source",
        "source 属性不可注入",
    ),
]


def main() -> int:
    return self_test(
        page="stage-p4.html", card="p4-4", lab=LAB, build=build,
        combine=[1, 0], mutations=MUTATIONS,
    )


if __name__ == "__main__":
    sys.exit(main())
