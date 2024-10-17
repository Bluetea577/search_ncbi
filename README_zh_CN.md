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

目前，search ncbi 尚未在 PyPI 上发布。您可以使用以下方法之一进行安装：

### 方法一：直接从 GitHub 安装

您可以使用 pip 直接从 GitHub 仓库安装最新版本：

```bash
pip install git+https://github.com/Bluetea577/search_ncbi.git
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

   如果您想以可编辑模式安装以进行开发，请使用：
   ```bash
   pip install -e .
   ```

### 依赖项

search ncbi 需要 Python 3.6 或更高版本。使用上述安装方法时，其他依赖项将自动安装。

### 验证安装

安装完成后，您可以通过运行以下命令来验证 search ncbi 是否正确安装：

```bash
python -c "import search_ncbi; print(search_ncbi.__version__)"
```

这应该会打印出 search ncbi 的版本号。

注意：一旦 search ncbi 在 PyPI 上可用，您就可以使用 `pip install search-ncbi` 来安装它。


## 使用方法

### 命令行界面

安装后，您可以使用 `ncbisearch` 命令从命令行执行搜索：

```bash
searchncbi --email youremail@example.com --db bioproject --term "metagenome" --max-results 10
```

这将在 bioproject 中搜索与宏基因组相关的研究，并返回最多 10 个结果。

### Python 模块

您也可以在自己的 Python 脚本中使用 NCBI 工具包：

```python
from search_ncbi import NCBITools

# 初始化搜索器
searcher = NCBITools("youremail@example.com")

# 执行搜索
results = searcher.search_and_process(db="nucleotide", term="BRCA1", max_results=5)
```

## 示例

### 示例 1：搜索 PubMed

```python
from search_ncbi import NCBITools

searcher = NCBITools("youremail@example.com")
results = searcher.search_and_process(db="pubmed", term="CRISPR", max_results=3)
```

### 示例 2：检索蛋白质序列

```python
from search_ncbi import NCBITools

searcher = NCBITools("youremail@example.com")
results = searcher.search_and_proces(db="protein", term="insulin homo sapiens", max_results=1)
```

## 贡献

我们欢迎对 NCBI 工具包的贡献！请参阅我们的[贡献指南](CONTRIBUTING.md)以获取更多信息。

## 许可证

本项目采用 MIT 许可证 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如果您有任何问题或反馈，请在我们的 [GitHub 仓库](https://github.com/Bluetea577/search_ncbi)上开一个 issue。
