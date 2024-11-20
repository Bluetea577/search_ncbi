# search_ncbi

提供了一种简单高效的方法，使用NCBI（国家生物技术信息中心）的Entrez编程实用工具（E-utilities）来搜索其各种生物医学数据库。


## 注意

本模块仍处于开发阶段。如果您遇到任何问题或有任何建议，请：

1. 在我们的 GitHub 仓库中开启一个 issue 进行讨论
2. 提交一个包含您建议修改的 pull request
3. 直接联系项目维护者：limingyang577@163.com

我们欢迎各种形式的贡献和反馈，以帮助改进这个项目。

---

**注意：** 作为一个开源项目，请确保您的所有交流和贡献都遵守我们的行为准则和贡献指南。


## 功能特性

- 搜索 NCBI 数据库（如 PubMed、核苷酸、蛋白质等）
- 检索和处理搜索结果
- 分析和可视化 NCBI 数据
- 命令行界面，方便快速搜索
- Python API，可集成到您自己的脚本和工作流程中


## 安装

您可以使用以下方法之一进行安装：

### 方法一：conda安装（推荐）

您可以从bioconda进行安装：

```bash
conda create -n search_ncbi -c bioconda search_ncbi
```

### 方法二：从源代码安装

要从源代码安装 search ncbi，请按照以下步骤操作：

1. 克隆仓库：
   ```bash
   git clone https://github.com/Bluetea577/search_ncbi.git
   ```

2. 进入项目目录：
   ```bash
   cd search_ncbi
   ```

3. 安装包：
   ```bash
   pip install .
   ```

### 依赖项

search ncbi 需要 Python 3.6 或更高版本。使用上述安装方法时，其他依赖项将自动安装。

## 支持的ncbi库

支持的ncbi库如下:

- protein
- nuccore
- nucleotide
- assembly
- blastdbinfo
- books
- cdd
- clinvar
- gap
- gene
- geoprofiles
- medgen
- omim
- orgtrack
- popset
- pcassay
- protfam
- pccompound
- pcsubstance
- seqannot
- biocollections
- taxonomy
- bioproject
- biosample
- sra




## search_ncbi 命令行界面使用说明

安装完成后，您可以使用 `searchncbi` 命令与 NCBI 数据库进行交互。

### 基本用法

```
searchncbi --email <您的邮箱> --api-key <您的API密钥> -d <数据库> -t <搜索词> [选项]
```

### 必需参数

- `--email`: 您的邮箱地址，用于 NCBI 查询（必需）
- `-d, --db`: 要搜索的 NCBI 数据库（必需）
- `-t, --term`: 搜索词（必需）

### 可选参数

- `--api-key`: 您的 NCBI API 密钥（可选，但建议使用以获得更高的请求限制）
- `-m, --max-results`: 返回结果的最大数量（默认：所有可用结果）
- `-b, --batch-size`: 每批处理的结果数量（默认：500）
- `-o, --output`: 输出文件名（默认："output.csv"）
- `-a, --action`: 要执行的操作（默认："metadata"）

### 操作类型

1. `metadata`: 处理并保存所有元数据（默认）
2. `custom`: 处理并保存自定义过滤的元数据
3. `raw`: 检索并保存原始数据
4. `count`: 获取搜索结果的总数
5. `id_list`: 检索并保存 ID 列表

### 自定义过滤选项（用于 `custom` 操作）

- `--include`: 要包含的列名列表
- `--exclude`: 要排除的列名列表
- `--contains`: 列名应包含的字符串列表
- `--regex`: 用于过滤列名的正则表达式

### 示例

1. 搜索 BioProject 并保存所有元数据：
   ```
   searchncbi --email user@example.com --api-key ABCDEF123456 -d bioproject -t "cancer" -o bioproject_results.csv
   ```

2. 使用自定义过滤搜索核苷酸数据库：
   ```
   searchncbi --email user@example.com -d nucleotide -t "BRCA1" -a custom --include "GBSeq_locus" "GBSeq_length" -o brca1_custom.csv
   ```

3. 从蛋白质数据库获取原始数据：
   ```
   searchncbi --email user@example.com -d protein -t "insulin" -a raw -m 100 -o insulin_raw.csv
   ```

4. 获取基因搜索结果的总数：
   ```
   searchncbi --email user@example.com -d gene -t "human[organism] AND cancer" -a count
   ```

5. 获取 SRA 数据库的 ID 列表：
   ```
   searchncbi --email user@example.com -d sra -t "RNA-Seq" -a id_list -m 1000 -o sra_ids.txt
   ```





## Python 模块

### 导入

首先，确保已安装 `search_ncbi` 包。然后，在您的 Python 脚本中导入 `NCBITools` 类：

```python
from search_ncbi import NCBITools
```

### 初始化

创建 `NCBITools` 实例，提供您的电子邮件地址和可选的 API 密钥：

```python
searcher = NCBITools("your_email@example.com", api_key="your_api_key")
```

注意：API 密钥是可选的，但建议使用以获得更高的请求限制。

### 主要方法

#### 1. 搜索并处理数据

```python
results = searcher.search_and_process(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=10,
    batch_size=500,
    process_method='all'
)
```

参数说明：
- `db`: NCBI 数据库名称（字符串）
- `term`: 搜索词（字符串）
- `max_results`: 最大结果数（整数，可选）
- `batch_size`: 批处理大小（整数，默认 500）
- `process_method`: 处理方法，'all' 或 'custom'（字符串，默认 'all'）

对于 'custom' 处理方法，可以使用额外的过滤参数：`include`, `exclude`, `contains`, `regex`。

#### 2. 获取原始数据

```python
raw_data = searcher.get_raw_data(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=10,
    batch_size=500
)
```

#### 3. 获取搜索结果数量

```python
count = searcher.search_count(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]"
)
```

#### 4. 获取 ID 列表

```python
id_list = searcher.get_id_list(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=100,
    batch_size=500
)
```

#### 5. 搜索并保存元数据

```python
searcher.search_and_save_metadata(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    output_file="metadata.csv",
    max_results=100,
    batch_size=500
)
```

#### 6. 过滤元数据

```python
filtered_data = searcher.filter_metadata(
    input_file="metadata.csv",
    output_file="filtered_metadata.csv",
    filter_term="specific_term"
)
```

#### 7. 搜索、保存和过滤元数据（完整工作流）

```python
filtered_data = searcher.search_and_filter_metadata(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    filter_term="specific_term",
    metadata_file="metadata.csv",
    filter_file="filtered_metadata.csv",
    max_results=100,
    batch_size=500
)
```

注意：所有方法都返回 pandas DataFrame 或适当的数据结构，除非另有说明。确保正确处理返回的数据。

## 贡献

我们欢迎对 NCBI 工具包的贡献！请参阅我们的[贡献指南](CONTRIBUTING.md)以获取更多信息。

## 许可证

本项目采用 MIT 许可证 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如果您有任何问题或反馈，请在我们的 [GitHub 仓库](https://github.com/Bluetea577/search_ncbi)上开一个 issue。
