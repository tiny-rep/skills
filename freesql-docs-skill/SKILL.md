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

If you need to refresh the guide index in this skill with live, per-page child-feature summaries, run:

```bash
python3 scripts/freesql_docs.py update-skill-md
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

Generate one live child-feature summary:

```bash
python3 scripts/freesql_docs.py summarize --slug repository
```

Render the full guide index block with live child-feature summaries:

```bash
python3 scripts/freesql_docs.py summarize
```

## Output Contract

- Source of truth: live official HTML under `https://freesql.net/guide/`
- Cleaning: strip nav, sidebar, footer, ads, line-number chrome, and unrelated UI fragments
- Conversion: preserve headings, paragraphs, lists, blockquotes, code blocks, tables, inline code, and links
- Result: clean Markdown with source URL and last-updated metadata at the top

## Official Guide Categories

<!-- GUIDE_INDEX_START -->
### 基础文档

- 入门: `https://freesql.net/guide/`  子功能：FreeSql 是一款功能强大的对象关系映射（O/RM）组件，支持 .NET Core 2.1+、.NET Framework 4.0+。 涵盖安装包、创建实体、如何接入、FreeSqlBuilder、ConnectionStrings。
- 插入: `https://freesql.net/guide/insert.html`  子功能：涵盖单条插入、返回自增、批量插入、高性能 BulkCopy、动态表名、插入指定列、忽略列、字典插入、导入表、MySql `Insert Ignore Into`、MySql `On Duplicate Key Update`、PostgreSQL `On Conflict Do Update`、API。
- 删除: `https://freesql.net/guide/delete.html`  子功能：删除是一个非常危险的操作，FreeSql 默认仅支持单表、且有条件的删除方法。 涵盖动态条件、动态表名、删除条件、字典删除、ISelect.ToDelete 高级删除、IBaseRepository 级联删除、API。
- 修改: `https://freesql.net/guide/update.html`  子功能：`FreeSql` 提供丰富的数据库更新功能，支持单条或批量更新，在特定的数据库执行还可以返回更新后的记录。 涵盖动态条件、动态表名、更新条件、更新指定列 Set、更新实体 SetSource、更新 SetDto、Set/SetSource/SetDto 区别、字典更新、乐观锁、悲观锁、ISelect.ToUpdate 高级更新、联表更新 UpdateJoin、高性能 BulkCopy。
- 插入或更新: `https://freesql.net/guide/insert-or-update.html`  子功能：涵盖IFreeSql.InsertOrUpdate、字典插入或更新、高性能 BulkCopy、表格编辑 BeginEdit、MySql `On Duplicate Key Update`、PostgreSQL `On Conflict Do Update`。
- 实体特性✨: `https://freesql.net/guide/entity-attribute.html`  子功能：v1.4.0+ 已自动识别 EF 特性 Key/Required/NotMapped/MaxLength/StringLength/DatabaseGenerated/Table/Column。 涵盖表名、主键(Primary Key)、自增(Identity)、唯一键(Unique Key)、索引（Index）、数据库类型(DbType)、decimal 精度、string 长度、Nullable 可空、服务器时间(ServerTime)、忽略(Ignore)、乐观锁(RowVersion)、自定义类型映射(MapType)、字段位置(Position)。
- 导航属性: `https://freesql.net/guide/navigate-attribute.html`  子功能：FreeSql 提供 OneToMany, ManyToOne, ManyToMany, OneToOne, Parent, [PgArrayToMany](https://www.cnblogs.…。 涵盖自定义配置、与非主键关联、检测导航属性、OneToOne、PgArrayToMany、约定命名（无须指明 Navigate）。
- 类型映射: `https://freesql.net/guide/type-mapping.html`  子功能：涵盖类型映射（默认）、MapType、Json、DateOnly/TimeOnly、TypeHandlers（自定义）、类型映射（特别）、重写、重读。

### 查询 ✨

- 查询: `https://freesql.net/guide/select.html`  子功能：FreeSql 在查询数据下足了功夫，链式风格、多表查询、表达式函数、导航属性支持得非常到位。 涵盖表达式函数、SqlServer WithLock/WithIndex、动态过滤 WhereDynamicFilter、克隆查询 ISelect、API。
- 分页查询: `https://freesql.net/guide/paging.html`  子功能：涵盖每页 20 条数据，查询第 1 页、优化、API。
- 单表查询: `https://freesql.net/guide/select-single-table.html`  子功能：涵盖单表、WithSql。
- 多表查询 ✨: `https://freesql.net/guide/select-multi-table.html`  子功能：涵盖多表 Join、导航属性 Join、WithoutJoin、子表Exists、子表In、子表List导航属性、子表string.Join、子表First/Count/Sum/Max/Min/Avg、子表ToList、WhereCascade。
- 嵌套查询 ✨: `https://freesql.net/guide/withtempquery.html`  子功能：涵盖WithTempQuery、场景1：查询分组第一条记录、场景2：嵌套查询 + Join、场景3：分组查询嵌套、场景4：内存数据嵌套、场景5：自动分表后分页 分组聚合、场景6：FromQuery 多个查询，最后映射查询、场景7：报表（每日）、WithParameters 参数化共享、子表Exists、子表In、子表Join、子表First/Count/Sum/Max/Min/Avg、子表ToList、ToSql + WithSql。
- 联合查询: `https://freesql.net/guide/unionall.html`  子功能：在之前都是推荐使用 ToSql + WithSql 完成联合查询操作，v3.2.666 新增功能直接使用 UnionAll 方法。 涵盖单表 UNION ALL、多表 UNION ALL、WithParameters 参数化共享。
- 分组聚合: `https://freesql.net/guide/select-group-by.html`  子功能：涵盖单表分组、多表分组、分组第一条记录、Aggregate、Distinct、SqlExt.DistinctCount、ToAggregate + SqlExt.DistinctCount、导航属性分组、动态分组、API。
- 返回数据 ✨: `https://freesql.net/guide/select-return-data.html`  子功能：FreeSql 使用 ExpressionTree 读取数据记录，.NET 技术下除了原生代码，最快的方案是 Emit 和 ExpressionTree。 涵盖返回单条记录、返回 List、返回 TreeList、返回 List + 导航属性的数据、指定返回、忽略字段返回、Dto 映射返回、ToChunk 分段返回、ToSql、执行 SQL、API。
- 延时加载: `https://freesql.net/guide/select-lazy-loading.html`  子功能：FreeSql 支持延时加载，当需要用到的时候才加载（读数据库），支持 1对1、多对 1、1对多、多对多导航属性。 涵盖多对多延时加载、总结。
- 贪婪加载 ✨: `https://freesql.net/guide/select-include.html`  子功能：涵盖子表ToList、导航属性 ManyToOne/OneToOne、集合属性 OneToMany/ManyToMany/PgArrayToMany、IncludeMany 增强、IncludeMany 扩展方法、IncludeMany 两种方式对比。
- 树型查询 ✨: `https://freesql.net/guide/select-as-tree.html`  子功能：无限级分类（父子）是一种比较常用的表设计，每种设计方式突出优势的同时也带来缺陷，如：。 涵盖父子导航属性、ToTreeList、AsTreeCte 递归删除、AsTreeCte 递归查询。
- LinqToSql: `https://freesql.net/guide/linq-to-sql.html`  子功能：linq to sql 写法过于生硬不灵活，left join 写法非常不好，建议慢慢放充转向 Labmda 链式风格，早日走向康庄大道。 涵盖特别说明、IQueryable、Where、Select(指定字段)、CaseWhen、Join、LeftJoin、From(多表查询)、GroupBy(分组)。

### Repository ✨

- 仓储: `https://freesql.net/guide/repository.html`  子功能：`FreeSql.DbContext` 参考 abp vnext 接口规范，实现了通用的仓储层功能（CURD），理解成传统增强版（DAL）。 涵盖临时用法、泛型仓储（依赖注入）、继承仓储（依赖注入）、对比更新、登陆信息（依赖注入）、兼容问题、联级保存、API。
- UnitOfWork: `https://freesql.net/guide/unit-of-work.html`  子功能：UnitOfWork 是对 DbTransaction 事务对象的封装，方便夹带私有数据。 涵盖如何使用、外部事务、接口定义、实体变化事件。
- 级联保存: `https://freesql.net/guide/cascade-saving.html`  子功能：接下来的内容，严重依赖[【导航属性】](https://freesql.net/guide/navigate-attribute.html)的正确配置，请先学会再继续向下！ 涵盖开启功能、机制规则、示例。
- 级联删除: `https://freesql.net/guide/cascade-delete.html`  子功能：接下来的内容，严重依赖[【导航属性】](https://freesql.net/guide/navigate-attribute.html)的正确配置，请先学会再继续向下！ 涵盖基于【对象】级联删除、基于【数据库】级联删除。
- UowManager 事务 ✨: `https://freesql.net/guide/unitofwork-manager.html`  子功能：本篇文章内容引导，如何在 asp.net core 项目中使用特性(注解) 的方式管理事务。 涵盖第一步：依赖注入、中间件、第二步：引入动态代理库、扩展：重写仓储、扩展：多库场景。
- 聚合根（实验室）: `https://freesql.net/guide/aggregateroot.html`  子功能：FreeSql.DbContext 定义了 IBaseRepository<T> 仓储接口，（虽然）支持了级联保存、级联删除功能，（但是）使用时需要人工自己判断何时开启、何时使用。 涵盖设定边界、插入数据、查询数据、删除数据、更新数据、插入或更新数据、扩展边界、总结。

### 数据库驱动

- 国产数据库: `https://freesql.net/guide/freesql-provider-custom.html`  子功能：由于太多，在此不一一列举，它们大多数语法兼容 MySql、Oracle、SqlServer、PostgreSQL 四种常用数据库之一。
- MySql 系列数据库: `https://freesql.net/guide/freesql-provider-mysqlconnector.html`  子功能：`FreeSql.Provider.MySqlConnector`是`FreeSql`基于社区提供的最新的[`MySqlConnector`](https://github.com/mysql-ne…。 涵盖MySql Enum 映射、增删改 BulkCopy。
- PostgreSQL: `https://freesql.net/guide/freesql-provider-postgresql.html`  子功能：nuget 安装：FreeSql.Provider.PostgreSQL。 涵盖数组、字典、JSONB、空间地理类型、时序数据库、增删改 PgCopy。
- Sqlite: `https://freesql.net/guide/freesql-provider-sqlitecore.html`  子功能：FreeSql.Provider.SqliteCore是`FreeSql`基于微软提供的最新的[`Microsoft.Data.Sqlite.Core`](https://docs.microsof…。 涵盖支持的版本、只有 **SQLitePCLRaw.bundle_e_sqlcipher** 才支持加密、验证是否登录是否加密？、|DataDirectory| 默认不支持、数学函数、TimeSpanTest、完整代码、iOS、NET Framework 支持、复制.NET Core中的dll、转换项目 **（建议）**。
- Oracle: `https://freesql.net/guide/freesql-provider-oracle.html`  子功能：FreeSql 对 Oracle 支持非常友好，是 c#.net ORM 不二之选，提供了 Ado.net/Odbc/Oledb 三种实现包，他们都支持 .NETCore2.1+、.NET4.0+…。 涵盖主键名长度大于30、增删改 BulkCopy。
- SqlServer: `https://freesql.net/guide/freesql-provider-sqlserver.html`  子功能：FreeSql 最多支持 SqlServer2000，根据不同的需求选择驱动包，微软提供了两个 SqlClient 访问包，因此我们也发布了两个，分别是：。 涵盖WithLock/WithIndex、增删改 SqlBulkCopy、访问 SqlServer2000。
- ODBC: `https://freesql.net/guide/freesql-provider-odbc.html`  子功能：FreeSql.Provider.Odbc 实现 ODBC 访问数据库，ODBC 属于比较原始的技术，更新慢，各大数据库厂支持得标准不一，不到万不得已最好别用 odbc，坑比较多。
- ClickHouse: `https://freesql.net/guide/freesql-provider-clickhouse.html`  子功能：`ClickHouse` 是一个高性能的开源列式数据库，专为实时大数据分析设计。它以列存储数据，支持快速查询和聚合操作，适合处理大规模数据集。`ClickHouse` 具备分布式架构、数据压缩和高可…。 涵盖介绍、安装包、声明。
- QuestDB: `https://freesql.net/guide/freesql-provider-questdb.html`  子功能：`QuestDB`是一款针对时序数据实时处理优化的关系型列存数据库， 支持 Rest API 方式访问，同时兼容 PostgreSQL 访问协议，以及 InfluxDB 写入的访问协议。自带 Web…。 涵盖介绍、安装包、声明、特有功能、QuestFunc、Sample By、GroupBy、Latest On、BulkCopy、自动分表、索引、常见问题、table busy、RestAPI设置账号密码、QuestDb不支持删除？、在线测试。
- Firebird（嵌入式）: `https://freesql.net/guide/freesql-provider-firebird.html`  子功能：`Firebird` 是一个开源的关系型数据库管理系统，它支持嵌入式部署。`Firebird` 嵌入式数据库适用于需要在本地应用程序中直接集成数据库的场景，无需单独的数据库服务器。它提供了强大的事务…。 涵盖介绍、安装包、声明、嵌入式例子。
- DuckDB（嵌入式 OLAP）: `https://freesql.net/guide/freesql-provider-duckdb.html`  子功能：DuckDB 是一款进程内分析数据库，它可以在无需维护分布式多服务器系统的情况下处理出人意料的大型数据集。 涵盖介绍、安装包、声明、类型映射。
- TDengine: `https://freesql.net/guide/freesql-provider-tdengine.html`  子功能：TDengine 是一款开源、高性能、云原生的时序数据库, 它专为物联网、车联网、工业互联网、金融、IT 运维等场景优化设计。 涵盖介绍、安装包、安装客户端驱动、声明、特有功能、超级表、子表、例子。

### 表达式函数

- 表达式函数: `https://freesql.net/guide/expression-function.html`  子功能：这是 `FreeSql` 非常特色的功能之一，请别错过文档的细节，可映射的类型基本都可以使用对应的表达式函数，例如 日期、字符串、`IN` 查询、数组（PostgreSQL 数组）、字典（Postg…。 涵盖Lambda接拼、In查询、In多列查询、In子表、Exists子表、查找今天创建的数据、日期格式化、开窗函数、子表Join、子表First/Count/Sum/Max/Min/Avg、子表ToList、自定义解析、参数化、表达式函数全览、数组、字典 Dictionary<string, string>、JSON JToken/JObject/JArray、字符串、日期、数学函数。

### 事务Transaction

- 事务Transaction: `https://freesql.net/guide/transaction.html`  子功能：涵盖常规事务、仓储事务（依赖注入）、同线程事务、悲观锁、外部事务。

### 过滤器

- 过滤器: `https://freesql.net/guide/filters.html`  子功能：IFreeSql 基础层实现了 Select/Update/Delete 可设置的全局过滤器功能，这些设置将追加到执行的 SQL WHERE 语句中。 涵盖如何禁用？、租户字段（动态值）。

### ADO

- ADO: `https://freesql.net/guide/ado.html`  子功能：Ado 是 IFreeSql 下重要的对象之一，它包括所有对 SQL 操作的封装，提供 ExecuteReader、ExecuteDataSet、ExecuteDataTable、ExecuteNo…。 涵盖查询 SQL 返回实体、参数化、参数前缀、检测连接、CommandFluent、Ado.net 扩展方法。

### AOP✨

- AOP✨: `https://freesql.net/guide/aop.html`  子功能：FreeSql AOP 已有的功能介绍，未来为会根据用户需求不断增强。 涵盖审计命令(如何监视 SQL？)、审计属性值、审计迁移脚本、ConfigEntity、统一设置架构名、MySql Enum 映射、修改 decimal 默认特性、字典表应用、自定义实体特性、Ado .net 读取拦截、表达式拦截、自定义全局类型转换。

### CodeFirst

- CodeFirst: `https://freesql.net/guide/code-first.html`  子功能：`FreeSql` 支持 `CodeFirst` 迁移结构至数据库，这应该是(`O/RM`)必须标配的一个功能。 涵盖迁移结构、FreeSql 提供两种 CodeFirst 移迁方法，自动和手动、自动同步实体结构【开发环境必备】、禁用迁移、备注、手工同步实体结构、批量生成表结构、实体特性。
- Fluent API: `https://freesql.net/guide/fluent-api.html`  子功能：FreeSql 提供了 Fluent Api 的方式,使用链式调用，可在外部配置实体的数据库特性。`Fluent Api` 的方法命名与特性名保持一致，共三种使用方法，选择**一种即可**：。 涵盖支持 Fluent API、ConfigEntity、Entity、IEntityTypeConfiguration、实体配置类、二种使用方式、优先级。

### DbFirst

- DbFirst: `https://freesql.net/guide/db-first.html`  子功能：涵盖获取所有数据库、获取指定数据库的表信息、NET Core CLI(推荐使用)、常用选项、DB 参数、示例、安装 Winform 生成器（已停止更新）。

### 你不知道的功能 ✨

- 你不知道的功能 ✨: `https://freesql.net/guide/more.html`  子功能：涵盖备注 -> 迁移到数据库、NoneParameter、添加或修改、弱类型 CURD、WithSql、你不知道的，指定字段返回、Dto 映射查询、父子关系表、级联加载、WhereCascade、WhereDynamicFilter、ISelect.ToDelete、ISelect.ToUpdate、自定义表达式函数、自定义实体特性、与其他 ORM 共用特性、审计 CURD、审计属性值、Ado .Net 扩展方法。

### 高级功能

- 读写分离: `https://freesql.net/guide/read-write-splitting.html`  子功能：FreeSql 支持数据库读写分离，本功能是客户端的读写分离行为，数据库服务器该怎么配置仍然那样配置，不受本功能影响，为了方便描述后面讲到的【读写分离】都是指客户端的功能支持。 涵盖使用 FreeSqlCloud 另一种读写分离。
- 分表分库: `https://freesql.net/guide/sharding.html`  子功能：涵盖理论知识、手工分表 AsTable、自动分表 AsTable (beta)、【分库】常规技巧、【分库】使用 FreeSql.Cloud。
- 多租户: `https://freesql.net/guide/multi-tenancy.html`  子功能：涵盖什么是多租户、方案一：按租户字段区分、WhereCascade、方案二：按租户分表、方案三：按租户分库。
- 性能: `https://freesql.net/guide/performance.html`  子功能：FreeSql 实现了强大功能的同时，性能没有受到影响，项目中使用反射或耗时的操作都经过了缓存处理。读取数据部分采用了 ExpressionTree，使得 FreeSql 解析实体数据的速度与 Da…。 涵盖测试结果(52 个字段)、测试结果(10 个字段)、测试结果、执行 SQL 返回实体列表 Dapper.Query<Class> VS FreeSql.Query<Class>、执行 SQL 返回元组列表 Dapper.Query<Tuple> VS FreeSql.Query<Tuple>。
- 动态操作: `https://freesql.net/guide/dynamic.html`  子功能：涵盖弱类型 CRUD、字典 CUD、无类型 CRUD（更高级）、动态表名、动态条件、动态排序、动态贪婪加载、动态返回数据、动态片段。
- 低代码: `https://freesql.net/guide/lowcode.html`  子功能：本篇是继[《动态操作》](https://freesql.net/guide/dynamic.html)文档之后的大功能，专门为低代码设计。 涵盖字典 CUD（单表）、无类型 CRUD（更高级）、级联机制。
<!-- GUIDE_INDEX_END -->
