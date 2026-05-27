#!/usr/bin/env python3
"""Fetch and convert official FreeSql guide pages into clean Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests

SITE_ROOT = "https://freesql.net"
GUIDE_ROOT = f"{SITE_ROOT}/guide/"
USER_AGENT = "freesql-docs-skill/1.0"
ROOT_SLUG_ALIASES = {"", "guide", "index", "readme", "root"}
VOID_TAGS = {"br", "img", "hr", "meta", "link", "input"}
SKIP_TAGS = {"script", "style"}
SKIP_CLASSES = {
    "line-numbers",
    "page-info",
    "vp-breadcrumb",
    "vp-page-meta",
    "vp-page-nav",
}
INLINE_TAGS = {
    "a",
    "b",
    "code",
    "em",
    "i",
    "img",
    "kbd",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
}

GUIDE_NAV = [
    {
        "type": "group",
        "name": "基础文档",
        "items": [
            {"slug": "", "title": "入门", "url": GUIDE_ROOT},
            {"slug": "insert", "title": "插入", "url": f"{GUIDE_ROOT}insert.html"},
            {"slug": "delete", "title": "删除", "url": f"{GUIDE_ROOT}delete.html"},
            {"slug": "update", "title": "修改", "url": f"{GUIDE_ROOT}update.html"},
            {
                "slug": "insert-or-update",
                "title": "插入或更新",
                "url": f"{GUIDE_ROOT}insert-or-update.html",
            },
            {
                "slug": "entity-attribute",
                "title": "实体特性✨",
                "url": f"{GUIDE_ROOT}entity-attribute.html",
            },
            {
                "slug": "navigate-attribute",
                "title": "导航属性",
                "url": f"{GUIDE_ROOT}navigate-attribute.html",
            },
            {
                "slug": "type-mapping",
                "title": "类型映射",
                "url": f"{GUIDE_ROOT}type-mapping.html",
            },
        ],
    },
    {
        "type": "group",
        "name": "查询 ✨",
        "items": [
            {"slug": "select", "title": "查询", "url": f"{GUIDE_ROOT}select.html"},
            {"slug": "paging", "title": "分页查询", "url": f"{GUIDE_ROOT}paging.html"},
            {
                "slug": "select-single-table",
                "title": "单表查询",
                "url": f"{GUIDE_ROOT}select-single-table.html",
            },
            {
                "slug": "select-multi-table",
                "title": "多表查询 ✨",
                "url": f"{GUIDE_ROOT}select-multi-table.html",
            },
            {
                "slug": "withtempquery",
                "title": "嵌套查询 ✨",
                "url": f"{GUIDE_ROOT}withtempquery.html",
            },
            {
                "slug": "unionall",
                "title": "联合查询",
                "url": f"{GUIDE_ROOT}unionall.html",
            },
            {
                "slug": "select-group-by",
                "title": "分组聚合",
                "url": f"{GUIDE_ROOT}select-group-by.html",
            },
            {
                "slug": "select-return-data",
                "title": "返回数据 ✨",
                "url": f"{GUIDE_ROOT}select-return-data.html",
            },
            {
                "slug": "select-lazy-loading",
                "title": "延时加载",
                "url": f"{GUIDE_ROOT}select-lazy-loading.html",
            },
            {
                "slug": "select-include",
                "title": "贪婪加载 ✨",
                "url": f"{GUIDE_ROOT}select-include.html",
            },
            {
                "slug": "select-as-tree",
                "title": "树型查询 ✨",
                "url": f"{GUIDE_ROOT}select-as-tree.html",
            },
            {
                "slug": "linq-to-sql",
                "title": "LinqToSql",
                "url": f"{GUIDE_ROOT}linq-to-sql.html",
            },
        ],
    },
    {
        "type": "group",
        "name": "Repository ✨",
        "items": [
            {
                "slug": "repository",
                "title": "仓储",
                "url": f"{GUIDE_ROOT}repository.html",
            },
            {
                "slug": "unit-of-work",
                "title": "UnitOfWork",
                "url": f"{GUIDE_ROOT}unit-of-work.html",
            },
            {
                "slug": "cascade-saving",
                "title": "级联保存",
                "url": f"{GUIDE_ROOT}cascade-saving.html",
            },
            {
                "slug": "cascade-delete",
                "title": "级联删除",
                "url": f"{GUIDE_ROOT}cascade-delete.html",
            },
            {
                "slug": "unitofwork-manager",
                "title": "UowManager 事务 ✨",
                "url": f"{GUIDE_ROOT}unitofwork-manager.html",
            },
            {
                "slug": "aggregateroot",
                "title": "聚合根（实验室）",
                "url": f"{GUIDE_ROOT}aggregateroot.html",
            },
        ],
    },
    {
        "type": "group",
        "name": "数据库驱动",
        "items": [
            {
                "slug": "freesql-provider-custom",
                "title": "国产数据库",
                "url": f"{GUIDE_ROOT}freesql-provider-custom.html",
            },
            {
                "slug": "freesql-provider-mysqlconnector",
                "title": "MySql 系列数据库",
                "url": f"{GUIDE_ROOT}freesql-provider-mysqlconnector.html",
            },
            {
                "slug": "freesql-provider-postgresql",
                "title": "PostgreSQL",
                "url": f"{GUIDE_ROOT}freesql-provider-postgresql.html",
            },
            {
                "slug": "freesql-provider-sqlitecore",
                "title": "Sqlite",
                "url": f"{GUIDE_ROOT}freesql-provider-sqlitecore.html",
            },
            {
                "slug": "freesql-provider-oracle",
                "title": "Oracle",
                "url": f"{GUIDE_ROOT}freesql-provider-oracle.html",
            },
            {
                "slug": "freesql-provider-sqlserver",
                "title": "SqlServer",
                "url": f"{GUIDE_ROOT}freesql-provider-sqlserver.html",
            },
            {
                "slug": "freesql-provider-odbc",
                "title": "ODBC",
                "url": f"{GUIDE_ROOT}freesql-provider-odbc.html",
            },
            {
                "slug": "freesql-provider-clickhouse",
                "title": "ClickHouse",
                "url": f"{GUIDE_ROOT}freesql-provider-clickhouse.html",
            },
            {
                "slug": "freesql-provider-questdb",
                "title": "QuestDB",
                "url": f"{GUIDE_ROOT}freesql-provider-questdb.html",
            },
            {
                "slug": "freesql-provider-firebird",
                "title": "Firebird（嵌入式）",
                "url": f"{GUIDE_ROOT}freesql-provider-firebird.html",
            },
            {
                "slug": "freesql-provider-duckdb",
                "title": "DuckDB（嵌入式 OLAP）",
                "url": f"{GUIDE_ROOT}freesql-provider-duckdb.html",
            },
            {
                "slug": "freesql-provider-tdengine",
                "title": "TDengine",
                "url": f"{GUIDE_ROOT}freesql-provider-tdengine.html",
            },
        ],
    },
    {
        "type": "page",
        "slug": "expression-function",
        "title": "表达式函数",
        "url": f"{GUIDE_ROOT}expression-function.html",
    },
    {
        "type": "page",
        "slug": "transaction",
        "title": "事务Transaction",
        "url": f"{GUIDE_ROOT}transaction.html",
    },
    {
        "type": "page",
        "slug": "filters",
        "title": "过滤器",
        "url": f"{GUIDE_ROOT}filters.html",
    },
    {"type": "page", "slug": "ado", "title": "ADO", "url": f"{GUIDE_ROOT}ado.html"},
    {"type": "page", "slug": "aop", "title": "AOP✨", "url": f"{GUIDE_ROOT}aop.html"},
    {
        "type": "group",
        "name": "CodeFirst",
        "items": [
            {
                "slug": "code-first",
                "title": "CodeFirst",
                "url": f"{GUIDE_ROOT}code-first.html",
            },
            {
                "slug": "fluent-api",
                "title": "Fluent API",
                "url": f"{GUIDE_ROOT}fluent-api.html",
            },
        ],
    },
    {
        "type": "page",
        "slug": "db-first",
        "title": "DbFirst",
        "url": f"{GUIDE_ROOT}db-first.html",
    },
    {
        "type": "page",
        "slug": "more",
        "title": "你不知道的功能 ✨",
        "url": f"{GUIDE_ROOT}more.html",
    },
    {
        "type": "group",
        "name": "高级功能",
        "items": [
            {
                "slug": "read-write-splitting",
                "title": "读写分离",
                "url": f"{GUIDE_ROOT}read-write-splitting.html",
            },
            {
                "slug": "sharding",
                "title": "分表分库",
                "url": f"{GUIDE_ROOT}sharding.html",
            },
            {
                "slug": "multi-tenancy",
                "title": "多租户",
                "url": f"{GUIDE_ROOT}multi-tenancy.html",
            },
            {
                "slug": "performance",
                "title": "性能",
                "url": f"{GUIDE_ROOT}performance.html",
            },
            {
                "slug": "dynamic",
                "title": "动态操作",
                "url": f"{GUIDE_ROOT}dynamic.html",
            },
            {
                "slug": "lowcode",
                "title": "低代码",
                "url": f"{GUIDE_ROOT}lowcode.html",
            },
        ],
    },
]


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)


class DOMBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack: list[Node] = [self.root]
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        node = Node(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS or self.skip_depth:
            return
        node = Node(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.stack[-1].children.append(data)

    def handle_comment(self, data: str) -> None:  # noqa: ARG002
        return


def iter_nav_items() -> Iterable[dict[str, str]]:
    for entry in GUIDE_NAV:
        if entry["type"] == "group":
            yield from entry["items"]
        else:
            yield entry


GUIDE_INDEX_BY_SLUG = {item["slug"]: item for item in iter_nav_items()}


def class_names(node: Node) -> set[str]:
    return {name for name in node.attrs.get("class", "").split() if name}


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def normalize_slug(slug: str) -> str:
    value = slug.strip().lower()
    if value in ROOT_SLUG_ALIASES:
        return ""
    return value


def resolve_guide_url(*, slug: str | None = None, url: str | None = None) -> str:
    if bool(slug) == bool(url):
        raise ValueError("Provide exactly one of --slug or --url.")
    if url:
        if not url.startswith(GUIDE_ROOT):
            raise ValueError(f"Only official FreeSql guide URLs are supported: {GUIDE_ROOT}")
        return url
    resolved_slug = normalize_slug(slug or "")
    item = GUIDE_INDEX_BY_SLUG.get(resolved_slug)
    if not item:
        supported = ", ".join(sorted(format_slug(value["slug"]) for value in iter_nav_items()))
        raise ValueError(f"Unknown guide slug: {slug}. Supported slugs: {supported}")
    return item["url"]


def format_slug(slug: str) -> str:
    return slug or "guide"


def absolute_url(href: str) -> str:
    if not href:
        return ""
    return urljoin(SITE_ROOT, href)


def fetch_html(url: str, timeout: int = 30) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def extract_title(html: str) -> str:
    match = re.search(r"<title>(.*?)\s*\|\s*FreeSql</title>", html, re.S)
    if match:
        return collapse_ws(match.group(1)).strip()
    match = re.search(r'"headline":"(.*?)"', html)
    if match:
        return match.group(1).strip()
    raise ValueError("Unable to extract page title from HTML.")


def extract_last_updated(html: str) -> str | None:
    for pattern in [
        r'<meta property="article:modified_time" content="([^"]+)"',
        r'<meta property="og:updated_time" content="([^"]+)"',
        r'"dateModified":"([^"]+)"',
    ]:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None


def build_dom(html: str) -> Node:
    parser = DOMBuilder()
    parser.feed(html)
    parser.close()
    return parser.root


def find_first(node: Node, predicate) -> Node | None:
    if predicate(node):
        return node
    for child in node.children:
        if isinstance(child, Node):
            found = find_first(child, predicate)
            if found:
                return found
    return None


def should_skip(node: Node) -> bool:
    classes = class_names(node)
    if classes & SKIP_CLASSES:
        return True
    if node.tag in {"footer", "nav"}:
        return True
    return node.attrs.get("aria-hidden") == "true" and "line-numbers" in classes


def render_markdown_from_html(html: str, page_url: str) -> str:
    dom = build_dom(html)
    main = find_first(
        dom,
        lambda node: node.tag == "main" and node.attrs.get("id") == "main-content",
    )
    if not main:
        raise ValueError("Unable to find the guide main content block.")

    title = extract_title(html)
    updated = extract_last_updated(html)
    blocks = [f"# {title}", f"> Source: {page_url}"]
    if updated:
        blocks[-1] += f"\n> Last Updated: {updated}"

    content_blocks: list[str] = []
    for child in main.children:
        if isinstance(child, Node):
            rendered = render_block(child)
            if rendered:
                content_blocks.extend(rendered)

    while content_blocks and content_blocks[0].strip() == f"# {title}":
        content_blocks.pop(0)

    blocks.extend(content_blocks)

    markdown = "\n\n".join(block for block in blocks if block.strip())
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()
    return f"{markdown}\n"


def render_block(node: Node) -> list[str]:
    if should_skip(node):
        return []

    if node.tag == "div" and "vp-page-title" in class_names(node):
        return []

    if is_code_container(node):
        return [render_pre(node)]

    if node.tag in {"main", "article", "section", "div"}:
        blocks: list[str] = []
        for child in node.children:
            if isinstance(child, Node):
                blocks.extend(render_block(child))
        return blocks

    if node.tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        text = render_inline(node, heading_mode=True).strip()
        if not text:
            return []
        level = int(node.tag[1])
        return [f"{'#' * level} {text}"]

    if node.tag == "p":
        text = render_inline(node).strip()
        return [text] if text else []

    if node.tag == "blockquote":
        lines: list[str] = []
        for child in node.children:
            if isinstance(child, Node):
                for block in render_block(child):
                    for line in block.splitlines():
                        lines.append("> " + line if line else ">")
        if not lines:
            text = render_inline(node).strip()
            lines = ["> " + text] if text else []
        return ["\n".join(lines)] if lines else []

    if node.tag in {"ul", "ol"}:
        text = render_list(node, depth=0)
        return [text] if text else []

    if node.tag == "table":
        table = render_table(node)
        return [table] if table else []

    if node.tag == "pre":
        return [render_pre(node)]

    if node.tag == "hr":
        return ["---"]

    return []


def is_code_container(node: Node) -> bool:
    classes = class_names(node)
    return node.tag == "div" and any(name.startswith("language-") for name in classes)


def detect_language(node: Node | None) -> str:
    if not node:
        return ""
    if node.attrs.get("data-ext"):
        return node.attrs["data-ext"]
    for name in class_names(node):
        if name.startswith("language-"):
            return name.split("language-", 1)[1]
    for child in node.children:
        if isinstance(child, Node):
            found = detect_language(child)
            if found:
                return found
    return ""


def render_pre(node: Node) -> str:
    pre = node if node.tag == "pre" else find_first(node, lambda value: value.tag == "pre")
    if not pre:
        return ""
    language = detect_language(node) or detect_language(pre)
    text = extract_code_text(pre).rstrip("\n")
    fence = "```" if "```" not in text else "````"
    suffix = language if language else ""
    return f"{fence}{suffix}\n{text}\n{fence}"


def extract_code_text(node: Node) -> str:
    line_nodes = list(find_all(node, lambda value: value.tag == "span" and "line" in class_names(value)))
    if line_nodes:
        return "\n".join(raw_text(line) for line in line_nodes)
    return raw_text(node)


def find_all(node: Node, predicate) -> Iterable[Node]:
    if predicate(node):
        yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from find_all(child, predicate)


def raw_text(node: Node | str) -> str:
    if isinstance(node, str):
        return node
    pieces: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            pieces.append(child)
        elif child.tag == "br":
            pieces.append("\n")
        else:
            pieces.append(raw_text(child))
    return "".join(pieces)


def render_list(node: Node, depth: int) -> str:
    ordered = node.tag == "ol"
    lines: list[str] = []
    item_index = 1

    for child in node.children:
        if not isinstance(child, Node) or child.tag != "li":
            continue

        marker = f"{item_index}. " if ordered else "- "
        item_index += 1
        inline_parts: list[str] = []
        nested_blocks: list[str] = []

        for grandchild in child.children:
            if isinstance(grandchild, str):
                inline_parts.append(grandchild)
                continue

            if grandchild.tag in {"ul", "ol"}:
                nested_blocks.append(render_list(grandchild, depth + 1))
                continue

            if grandchild.tag in INLINE_TAGS or grandchild.tag == "br":
                inline_parts.append(render_inline(grandchild))
                continue

            if grandchild.tag == "p" and not nested_blocks:
                inline_parts.append(render_inline(grandchild))
                continue

            nested_blocks.extend(render_block(grandchild))

        head = collapse_ws("".join(inline_parts)).strip()
        lines.append(("  " * depth) + marker + head)

        for block in nested_blocks:
            for line in block.splitlines():
                lines.append(("  " * depth) + "  " + line if line else "")

    return "\n".join(line.rstrip() for line in lines).rstrip()


def render_table(node: Node) -> str:
    rows: list[list[str]] = []
    for row in find_all(node, lambda value: value.tag == "tr"):
        cells = []
        for child in row.children:
            if isinstance(child, Node) and child.tag in {"th", "td"}:
                cell = collapse_ws(render_inline(child)).strip()
                cells.append(cell.replace("|", r"\|"))
        if cells:
            rows.append(cells)

    if not rows:
        return ""

    headers = rows[0]
    body = rows[1:] if len(rows) > 1 else []
    separator = ["---"] * len(headers)
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for row in body:
        padded = row + [""] * (len(headers) - len(row))
        output.append("| " + " | ".join(padded[: len(headers)]) + " |")
    return "\n".join(output)


def render_inline(node: Node | str, *, heading_mode: bool = False) -> str:
    if isinstance(node, str):
        return collapse_ws(node)

    if node.tag == "code":
        code = raw_text(node).strip()
        return f"`{code}`" if code else ""

    if node.tag == "img":
        src = absolute_url(node.attrs.get("src", ""))
        alt = node.attrs.get("alt", "").strip()
        return f"![{alt}]({src})" if src else ""

    if node.tag == "a":
        text = "".join(render_inline(child, heading_mode=heading_mode) for child in node.children).strip()
        href = absolute_url(node.attrs.get("href", ""))
        if "header-anchor" in class_names(node) or heading_mode:
            return text
        if not href:
            return text
        if text == href:
            return f"<{href}>"
        return f"[{text}]({href})"

    pieces: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            pieces.append(collapse_ws(child))
            continue

        if child.tag == "br":
            pieces.append("\n")
            continue

        text = render_inline(child, heading_mode=heading_mode)
        if child.tag in {"strong", "b"} and text.strip():
            pieces.append(f"**{text.strip()}**")
        elif child.tag in {"em", "i"} and text.strip():
            pieces.append(f"*{text.strip()}*")
        else:
            pieces.append(text)

    rendered = "".join(pieces)
    rendered = re.sub(r" *\n *", "\n", rendered)
    return rendered


def print_nav() -> str:
    lines = ["# FreeSql Guide Categories"]
    for entry in GUIDE_NAV:
        if entry["type"] == "group":
            lines.append(f"\n## {entry['name']}")
            for item in entry["items"]:
                lines.append(
                    f"- `{format_slug(item['slug'])}` {item['title']} - {item['url']}"
                )
        else:
            lines.append(
                f"\n- `{format_slug(entry['slug'])}` {entry['title']} - {entry['url']}"
            )
    return "\n".join(lines).strip() + "\n"


def write_output(text: str, output: Path | None) -> None:
    if output:
        output.write_text(text, encoding="utf-8")
        return
    sys.stdout.write(text)


def handle_list(args: argparse.Namespace) -> int:  # noqa: ARG001
    sys.stdout.write(print_nav())
    return 0


def handle_fetch(args: argparse.Namespace) -> int:
    url = resolve_guide_url(slug=args.slug, url=args.url)
    html = fetch_html(url, timeout=args.timeout)
    markdown = render_markdown_from_html(html, url)
    if args.max_lines:
        markdown = "\n".join(markdown.splitlines()[: args.max_lines]).rstrip() + "\n"
    write_output(markdown, args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and convert official FreeSql guide pages to Markdown."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List the supported guide categories and slugs.")
    list_parser.set_defaults(handler=handle_list)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch one guide page and print Markdown.")
    fetch_parser.add_argument("--slug", help="Guide slug, for example: insert or select-multi-table.")
    fetch_parser.add_argument("--url", help="Full official guide URL.")
    fetch_parser.add_argument("--output", type=Path, help="Write Markdown to a file instead of stdout.")
    fetch_parser.add_argument(
        "--max-lines",
        type=int,
        default=0,
        help="Trim output for quick inspection or validation runs.",
    )
    fetch_parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    fetch_parser.set_defaults(handler=handle_fetch)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except Exception as exc:  # noqa: BLE001
        parser.exit(1, f"[ERROR] {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
