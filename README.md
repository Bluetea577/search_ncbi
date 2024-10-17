# search_ncbi
This tool provides a simple and efficient way to search NCBI databases using the Entrez Programming Utilities (E-utilities)


## Notice

This module is still in the development stage. If you encounter any issues or have suggestions, please:

1. Open an issue in our GitHub repository for discussion
2. Submit a pull request with your proposed changes
3. Contact the maintainer directly at limingyang577@163.com

We welcome all forms of contribution and feedback to improve this project.

---

**Note:** As this is an open-source project, please ensure that any communication or contribution adheres to our code of conduct and contribution guidelines.


## Features

- Search NCBI databases (e.g., PubMed, Nucleotide, Protein)
- Retrieve and process search results
- Analyze and visualize NCBI data
- Command-line interface for quick searches
- Python API for integration into your own scripts and workflows

## Installation

Currently, search ncbi is not available on PyPI. You can install it using one of the following methods:

### Option 1: Install directly from GitHub

You can install the latest version directly from the GitHub repository using pip:

```bash
pip install git+https://github.com/Bluetea577/search_ncbi.git
```

### Option 2: Install from source

To install search ncbi from source, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Bluetea577/search_ncbi.git
   ```

2. Navigate to the project directory:
   ```bash
   cd search_ncbi
   ```

3. Install the package:
   ```bash
   pip install .
   ```

   If you want to install in editable mode for development:
   ```bash
   pip install -e .
   ```

### Dependencies

search ncbi requires Python 3.6 or later. Other dependencies will be automatically installed when you install the package using one of the methods above.

### Verifying the Installation

After installation, you can verify that search ncbi is installed correctly by running:

```bash
python -c "import search_ncbi; print(search_ncbi.__version__)"
```

This should print the version number of search ncbi.

Note: Once search ncbi is available on PyPI, you will be able to install it using `pip install search-ncbi`.

## Usage

### Command Line Interface

After installation, you can use the `ncbisearch` command to perform searches from the command line:

```bash
searchncbi --email youremail@example.com --db bioproject --term "metagenome" --max-results 10
```

This will search Bioproject for projects related to metagenome and return up to 10 results.

### Python Module

You can also use NCBI Tools as a Python module in your own scripts:

```python
from search_ncbi import NCBITools

# Initialize the searcher
searcher = NCBITools("youremail@example.com")

# Perform a search
results = searcher.search_and_process(db="nucleotide", term="BRCA1", max_results=5)
```

## Examples

### Example 1: Searching PubMed

```python
from search_ncbi import NCBITools

searcher = NCBITools("youremail@example.com")
results = searcher.search_and_process(db="pubmed", term="CRISPR", max_results=3)
```

### Example 2: Retrieving Protein Sequences

```python
from search_ncbi import NCBITools

searcher = NCBITools("youremail@example.com")
results = searcher.search_and_process(db="protein", term="insulin homo sapiens", max_results=1)
```

## Contributing

Contributions to NCBI Tools are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue on our [GitHub repository](https://github.com/Bluetea577/search_ncbi).
