from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "freesql_docs.py"
SPEC = importlib.util.spec_from_file_location("freesql_docs", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


SAMPLE_HTML = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta property="article:modified_time" content="2025-01-16T10:00:00.000Z" />
    <title>示例页面 | FreeSql</title>
  </head>
  <body>
    <main id="main-content" class="vp-page">
      <div class="vp-page-title">
        <h1><!---->示例页面<!----></h1>
        <div class="page-info"><span>ignore me</span></div>
      </div>
      <p>正文 <code>IFreeSql</code> 和 <a class="route-link" href="/guide/select-include.html">IncludeMany</a>。</p>
      <blockquote><p>注意：这里只是测试。</p></blockquote>
      <ul>
        <li>第一项</li>
        <li><code>Set</code> 第二项</li>
      </ul>
      <div class="language-csharp line-numbers-mode" data-ext="csharp">
        <pre class="shiki">
          <code class="language-csharp">
            <span class="line">var id = 1;</span>
            <span class="line">Console.WriteLine(id);</span>
          </code>
        </pre>
        <div class="line-numbers" aria-hidden="true">
          <div class="line-number">1</div>
          <div class="line-number">2</div>
        </div>
      </div>
      <table>
        <thead>
          <tr><th>方法</th><th>说明</th></tr>
        </thead>
        <tbody>
          <tr><td>Insert</td><td>插入数据</td></tr>
        </tbody>
      </table>
      <footer class="vp-page-meta">skip footer</footer>
    </main>
  </body>
</html>
"""

SUMMARY_HTML = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>多表查询 ✨ | FreeSql</title>
  </head>
  <body>
    <main id="main-content" class="vp-page">
      <div class="vp-page-title">
        <h1>多表查询 ✨</h1>
      </div>
      <p>说明 FreeSql 多表查询的核心写法与适用场景。</p>
      <h2>1、多表 Join</h2>
      <p>演示 LeftJoin、From 和结果投影。</p>
      <h2>2、导航属性 Join</h2>
      <h2>3、WithoutJoin</h2>
      <h2>4、子表Exists</h2>
      <h2>5、子表In</h2>
      <h2>6、子表List导航属性</h2>
      <h2>7、子表string.Join</h2>
    </main>
  </body>
</html>
"""


class FreeSqlDocsTests(unittest.TestCase):
    def test_root_aliases_resolve_to_guide_index(self) -> None:
        self.assertEqual(MODULE.resolve_guide_url(slug="guide"), MODULE.GUIDE_ROOT)
        self.assertEqual(MODULE.resolve_guide_url(slug="root"), MODULE.GUIDE_ROOT)

    def test_markdown_render_keeps_key_blocks(self) -> None:
        markdown = MODULE.render_markdown_from_html(SAMPLE_HTML, "https://freesql.net/guide/sample.html")
        self.assertIn("# 示例页面", markdown)
        self.assertIn("> Source: https://freesql.net/guide/sample.html", markdown)
        self.assertIn("> Last Updated: 2025-01-16T10:00:00.000Z", markdown)
        self.assertIn("正文 `IFreeSql` 和 [IncludeMany](https://freesql.net/guide/select-include.html)。", markdown)
        self.assertIn("> 注意：这里只是测试。", markdown)
        self.assertIn("- 第一项", markdown)
        self.assertIn("- `Set` 第二项", markdown)
        self.assertIn("```csharp\nvar id = 1;\nConsole.WriteLine(id);\n```", markdown)
        self.assertIn("| 方法 | 说明 |", markdown)
        self.assertIn("| Insert | 插入数据 |", markdown)
        self.assertNotIn("skip footer", markdown)
        self.assertNotIn("ignore me", markdown)

    def test_nav_listing_includes_insert_and_multi_table(self) -> None:
        listing = MODULE.print_nav()
        self.assertIn("`insert` 插入 - https://freesql.net/guide/insert.html", listing)
        self.assertIn(
            "`select-multi-table` 多表查询 ✨ - https://freesql.net/guide/select-multi-table.html",
            listing,
        )
        self.assertNotIn("其他作品", listing)

    def test_page_summary_uses_live_page_headings(self) -> None:
        summary = MODULE.build_page_summary_from_html(
            SUMMARY_HTML,
            "https://freesql.net/guide/select-multi-table.html",
            max_chars=300,
        )
        self.assertIn("说明 FreeSql 多表查询的核心写法与适用场景。", summary)
        self.assertIn("涵盖多表 Join、导航属性 Join、WithoutJoin、子表Exists", summary)
        self.assertLessEqual(len(summary), 300)

    def test_render_skill_guide_index_adds_summary_text(self) -> None:
        block = MODULE.render_skill_guide_index(
            {"insert": "涵盖单条插入、返回自增、批量插入与 BulkCopy。"},
            summary_max_chars=300,
        )
        self.assertIn(MODULE.GUIDE_INDEX_START, block)
        self.assertIn(
            "- 插入: `https://freesql.net/guide/insert.html`  子功能：涵盖单条插入、返回自增、批量插入与 BulkCopy。",
            block,
        )

    def test_replace_skill_guide_index_swaps_marked_block(self) -> None:
        original = """---\nname: freesql-docs-skill\n---\n\n## Official Guide Categories\n\n<!-- GUIDE_INDEX_START -->\nold\n<!-- GUIDE_INDEX_END -->\n"""
        updated = MODULE.replace_skill_guide_index(
            original,
            "## Official Guide Categories\n\n<!-- GUIDE_INDEX_START -->\nnew\n<!-- GUIDE_INDEX_END -->\n",
        )
        self.assertIn("new", updated)
        self.assertNotIn("\nold\n", updated)


if __name__ == "__main__":
    unittest.main()
