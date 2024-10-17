# search_ncbi
This tool provides a simple and efficient way to search NCBI databases using the Entrez Programming Utilities (E-utilities)

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
   cd search-ncbi
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
ncbisearch --database pubmed --term "cancer AND genetics" --max_results 10
```

This will search PubMed for articles related to cancer genetics and return up to 10 results.

### Python Module

You can also use NCBI Tools as a Python module in your own scripts:

```python
from search_ncbi import NCBISearcher

# Initialize the searcher
searcher = NCBISearcher()

# Perform a search
results = searcher.search(database="nucleotide", term="BRCA1", max_results=5)

# Process the results
for result in results:
    print(f"Title: {result.title}")
    print(f"Accession: {result.accession}")
    print(f"Sequence Length: {result.sequence_length}")
    print("---")
```

## Examples

### Example 1: Searching PubMed

```python
from search_ncbi import NCBISearcher

searcher = NCBISearcher()
results = searcher.search(database="pubmed", term="CRISPR", max_results=3)

for result in results:
    print(f"Title: {result.title}")
    print(f"Authors: {', '.join(result.authors)}")
    print(f"Journal: {result.journal}")
    print(f"Publication Date: {result.pub_date}")
    print("---")
```

### Example 2: Retrieving Protein Sequences

```python
from search_ncbi import NCBISearcher

searcher = NCBISearcher()
results = searcher.search(database="protein", term="insulin homo sapiens", max_results=1)

for result in results:
    print(f"Protein Name: {result.title}")
    print(f"Accession: {result.accession}")
    print(f"Sequence:\n{result.sequence[:100]}...")  # Print first 100 characters of the sequence
```

## Contributing

Contributions to NCBI Tools are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue on our [GitHub repository](https://github.com/Bluetea577/search_ncbi).
