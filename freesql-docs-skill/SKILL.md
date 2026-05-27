---
name: freesql-docs-skill
description: Fetch the latest official FreeSql guide page as clean Markdown when the user needs current FreeSql usage docs, category lookup, or structured reference output from https://freesql.net/guide/.
---

# FreeSql Docs Skill

## Overview

Use this skill when the user needs the latest official FreeSql usage documentation from `https://freesql.net/guide/`, especially for CRUD, query patterns, Repository, drivers, CodeFirst, or advanced features.

This skill keeps the official `/guide/` category index in-context and delegates page fetching, HTML cleaning, and HTML-to-Markdown conversion to `scripts/freesql_docs.py`. The output should be clean Markdown only.

## Use It When

- The user asks for the latest FreeSql documentation for a known guide category such as `插入`, `多表查询 ✨`, `Repository`, `CodeFirst`, or `AOP✨`.
- The user wants a specific official guide page converted from live HTML into agent-readable Markdown.
- The user asks for the current FreeSql `/guide/` category structure and corresponding URLs.

## Workflow

1. Match the request to one guide slug or one official guide URL from the category index below.
2. Run `python3 scripts/freesql_docs.py fetch --slug <slug>` or `python3 scripts/freesql_docs.py fetch --url <official-guide-url>`.
3. Return the Markdown produced by the script. Do not re-wrap it in extra explanation unless the user explicitly asks.

If the user asks for the available guide categories first, run:

```bash
python3 scripts/freesql_docs.py list
```

## Commands

Fetch by slug:

```bash
python3 scripts/freesql_docs.py fetch --slug insert
python3 scripts/freesql_docs.py fetch --slug select-multi-table
```

Fetch by official URL:

```bash
python3 scripts/freesql_docs.py fetch --url https://freesql.net/guide/insert.html
```

Write the converted Markdown to a file:

```bash
python3 scripts/freesql_docs.py fetch --slug insert --output /tmp/freesql-insert.md
```

Trim output for quick validation:

```bash
python3 scripts/freesql_docs.py fetch --slug select-multi-table --max-lines 120
```

## Output Contract

- Source of truth: live official HTML under `https://freesql.net/guide/`
- Cleaning: strip nav, sidebar, footer, ads, line-number chrome, and unrelated UI fragments
- Conversion: preserve headings, paragraphs, lists, blockquotes, code blocks, tables, inline code, and links
- Result: clean Markdown with source URL and last-updated metadata at the top

## Official Guide Categories

The index below mirrors the official `/guide/` sidebar order. The `其他作品` section is intentionally excluded.

### 基础文档

- 入门: `https://freesql.net/guide/`
- 插入: `https://freesql.net/guide/insert.html`
- 删除: `https://freesql.net/guide/delete.html`
- 修改: `https://freesql.net/guide/update.html`
- 插入或更新: `https://freesql.net/guide/insert-or-update.html`
- 实体特性✨: `https://freesql.net/guide/entity-attribute.html`
- 导航属性: `https://freesql.net/guide/navigate-attribute.html`
- 类型映射: `https://freesql.net/guide/type-mapping.html`

### 查询 ✨

- 查询: `https://freesql.net/guide/select.html`
- 分页查询: `https://freesql.net/guide/paging.html`
- 单表查询: `https://freesql.net/guide/select-single-table.html`
- 多表查询 ✨: `https://freesql.net/guide/select-multi-table.html`
- 嵌套查询 ✨: `https://freesql.net/guide/withtempquery.html`
- 联合查询: `https://freesql.net/guide/unionall.html`
- 分组聚合: `https://freesql.net/guide/select-group-by.html`
- 返回数据 ✨: `https://freesql.net/guide/select-return-data.html`
- 延时加载: `https://freesql.net/guide/select-lazy-loading.html`
- 贪婪加载 ✨: `https://freesql.net/guide/select-include.html`
- 树型查询 ✨: `https://freesql.net/guide/select-as-tree.html`
- LinqToSql: `https://freesql.net/guide/linq-to-sql.html`

### Repository ✨

- 仓储: `https://freesql.net/guide/repository.html`
- UnitOfWork: `https://freesql.net/guide/unit-of-work.html`
- 级联保存: `https://freesql.net/guide/cascade-saving.html`
- 级联删除: `https://freesql.net/guide/cascade-delete.html`
- UowManager 事务 ✨: `https://freesql.net/guide/unitofwork-manager.html`
- 聚合根（实验室）: `https://freesql.net/guide/aggregateroot.html`

### 数据库驱动

- 国产数据库: `https://freesql.net/guide/freesql-provider-custom.html`
- MySql 系列数据库: `https://freesql.net/guide/freesql-provider-mysqlconnector.html`
- PostgreSQL: `https://freesql.net/guide/freesql-provider-postgresql.html`
- Sqlite: `https://freesql.net/guide/freesql-provider-sqlitecore.html`
- Oracle: `https://freesql.net/guide/freesql-provider-oracle.html`
- SqlServer: `https://freesql.net/guide/freesql-provider-sqlserver.html`
- ODBC: `https://freesql.net/guide/freesql-provider-odbc.html`
- ClickHouse: `https://freesql.net/guide/freesql-provider-clickhouse.html`
- QuestDB: `https://freesql.net/guide/freesql-provider-questdb.html`
- Firebird（嵌入式）: `https://freesql.net/guide/freesql-provider-firebird.html`
- DuckDB（嵌入式 OLAP）: `https://freesql.net/guide/freesql-provider-duckdb.html`
- TDengine: `https://freesql.net/guide/freesql-provider-tdengine.html`

### 独立页面

- 表达式函数: `https://freesql.net/guide/expression-function.html`
- 事务Transaction: `https://freesql.net/guide/transaction.html`
- 过滤器: `https://freesql.net/guide/filters.html`
- ADO: `https://freesql.net/guide/ado.html`
- AOP✨: `https://freesql.net/guide/aop.html`

### CodeFirst

- CodeFirst: `https://freesql.net/guide/code-first.html`
- Fluent API: `https://freesql.net/guide/fluent-api.html`

### 独立页面补充

- DbFirst: `https://freesql.net/guide/db-first.html`
- 你不知道的功能 ✨: `https://freesql.net/guide/more.html`

### 高级功能

- 读写分离: `https://freesql.net/guide/read-write-splitting.html`
- 分表分库: `https://freesql.net/guide/sharding.html`
- 多租户: `https://freesql.net/guide/multi-tenancy.html`
- 性能: `https://freesql.net/guide/performance.html`
- 动态操作: `https://freesql.net/guide/dynamic.html`
- 低代码: `https://freesql.net/guide/lowcode.html`
