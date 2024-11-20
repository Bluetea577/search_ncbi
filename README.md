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

You can install it using one of the following methods:

### Option 1: Install from Conda (Recommended)

You can install it from bioconda:

```bash
conda create -n search_ncbi -c bioconda search_ncbi
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

### Dependencies

search ncbi requires Python 3.6 or later. Other dependencies will be automatically installed when you install the package using one of the methods above.

## Supported NCBI Libraries

This project supports the following NCBI libraries:

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

## search_ncbi Command Line Interface Usage

After installation, you can use the `searchncbi` command to interact with NCBI databases.


### Basic Usage

```
searchncbi --email <your_email> --api-key <your_api_key> -d <database> -t <search_term> [options]
```

### Required Arguments

- `--email`: Your email address for NCBI queries (required)
- `-d, --db`: NCBI database to search (required)
- `-t, --term`: Search term (required)

### Optional Arguments

- `--api-key`: Your NCBI API key (optional, but recommended for higher request limits)
- `-m, --max-results`: Maximum number of results to return (default: all available results)
- `-b, --batch-size`: Number of results to process in each batch (default: 500)
- `-o, --output`: Output file name (default: "output.csv")
- `-a, --action`: Action to perform (default: "metadata")

### Actions

1. `metadata`: Process and save all metadata (default)
2. `custom`: Process and save custom filtered metadata
3. `raw`: Retrieve and save raw data
4. `count`: Get the total count of search results
5. `id_list`: Retrieve and save a list of IDs

### Custom Filtering Options (for `custom` action)

- `--include`: List of column names to include
- `--exclude`: List of column names to exclude
- `--contains`: List of strings that column names should contain
- `--regex`: Regular expression for filtering column names

### Examples

1. Search BioProject and save all metadata:
   ```
   searchncbi --email user@example.com --api-key ABCDEF123456 -d bioproject -t "cancer" -o bioproject_results.csv
   ```

2. Search Nucleotide database with custom filtering:
   ```
   searchncbi --email user@example.com -d nucleotide -t "BRCA1" -a custom --include "GBSeq_locus" "GBSeq_length" -o brca1_custom.csv
   ```

3. Get raw data from Protein database:
   ```
   searchncbi --email user@example.com -d protein -t "insulin" -a raw -m 100 -o insulin_raw.csv
   ```

4. Get total count of results for a Gene search:
   ```
   searchncbi --email user@example.com -d gene -t "human[organism] AND cancer" -a count
   ```

5. Get ID list for SRA database:
   ```
   searchncbi --email user@example.com -d sra -t "RNA-Seq" -a id_list -m 1000 -o sra_ids.txt
   ```



## Python Module

### Import

First, ensure that the `search_ncbi` package is installed. Then, import the `NCBITools` class in your Python script:

```python
from search_ncbi import NCBITools
```

### Initialization

Create an instance of `NCBITools` by providing your email address and an optional API key:

```python
searcher = NCBITools("your_email@example.com", api_key="your_api_key")
```

Note: The API key is optional but recommended for higher request limits.

### Main Methods

#### 1. Search and Process Data

```python
results = searcher.search_and_process(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=10,
    batch_size=500,
    process_method='all'
)
```

Parameters:
- `db`: NCBI database name (string)
- `term`: Search term (string)
- `max_results`: Maximum number of results (integer, optional)
- `batch_size`: Batch size for processing (integer, default 500)
- `process_method`: Processing method, 'all' or 'custom' (string, default 'all')

For 'custom' processing method, additional filtering parameters can be used: `include`, `exclude`, `contains`, `regex`.

#### 2. Get Raw Data

```python
raw_data = searcher.get_raw_data(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=10,
    batch_size=500
)
```

#### 3. Get Search Result Count

```python
count = searcher.search_count(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]"
)
```

#### 4. Get ID List

```python
id_list = searcher.get_id_list(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    max_results=100,
    batch_size=500
)
```

#### 5. Search and Save Metadata

```python
searcher.search_and_save_metadata(
    db="nucleotide",
    term="SARS-CoV-2[Organism] AND complete genome[Title]",
    output_file="metadata.csv",
    max_results=100,
    batch_size=500
)
```

#### 6. Filter Metadata

```python
filtered_data = searcher.filter_metadata(
    input_file="metadata.csv",
    output_file="filtered_metadata.csv",
    filter_term="specific_term"
)
```

#### 7. Search, Save, and Filter Metadata (Complete Workflow)

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

Note: All methods return pandas DataFrames or appropriate data structures unless otherwise specified. Ensure proper handling of the returned data.

## Contributing

Contributions to NCBI Tools are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue on our [GitHub repository](https://github.com/Bluetea577/search_ncbi).
