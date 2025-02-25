"""search ncbi datasets"""
from Bio import Entrez
from .config import EMAIL, API_KEY, MAX_RESULTS
from typing import List, Dict, Any, Optional
import time
from tqdm import tqdm
import xml.etree.ElementTree as ET
import xmltodict
import requests

class NCBISearcher:
    # 设置email和api-key
    def __init__(self, email: Optional[str] = EMAIL, api_key: Optional[str] = API_KEY):
        if email:
            Entrez.email = email
        elif not Entrez.email:
            raise ValueError("Email must be provided or set globally")
        if api_key:
            Entrez.api_key = api_key

        self.last_search_db: Optional[str] = None
        self.last_search_term: Optional[str] = None
        self.search_results: List[str] = []
        self.detailed_results: List[Dict[str, Any]] = []
        self.search_count: int = 0

    def search(self, db: str, term: str, retstart: int = 0, retmax: int = MAX_RESULTS, fetch_details: bool = False):
        """
        Perform a search and optionally fetch details.

        db: The NCBI database to search
        term: The search term
        retmax: Maximum number of results to return
        fetch_details: Whether to automatically fetch details

        return: List of IDs from the search
        """
        try:
            handle = Entrez.esearch(db=db, term=term, retstart = retstart, retmax=retmax)
            record = Entrez.read(handle)
            self.search_count = int(record['Count'])
            self.search_results = record["IdList"]
            self.last_search_db = db
            self.last_search_term = term

            if fetch_details:
                self.fetch_details()

            return self.search_results
        except Exception as e:
            print(f"Error occurred during search: {e}")
            return []

    def _search_generator(self, db: str, term: str, batch_size : int = 500, max_results: int = None, fetch_details: bool = False):
        """
        Perform a search with count and optionally fetch details, handling large result sets.

        db: The NCBI database to search
        term: The search term
        batch_size:
        fetch_details: Whether to fetch detailed information for each ID

        return: List of IDs from the search
        """
        if self.search_count == 0:
            self.search(db, term, retmax=1)

        all_ids = []
        all_details = []

        total_count = self.search_count

        if max_results is not None:
            total_count = min(max_results, total_count)

        for batch in tqdm(range(0, total_count, batch_size), desc = "Looking for IDs"):
            current_batch_size = min(batch_size, total_count)
            batch_ids = self.search(db, term, retstart=batch, retmax=current_batch_size)
            all_ids.extend(batch_ids)

            if fetch_details:
                batch_details = self.fetch_details(db, batch_ids)
                all_details.extend(batch_details)

            time.sleep(2)

        self.search_results = all_ids
        if fetch_details:
            self.detailed_results = all_details

        return self.search_results, self.detailed_results

    def fetch_details(self, db: Optional[str] = None, id_list: Optional[List[str]] = None):
        """
        Fetch details for given IDs or for the last search results.

        db: The NCBI database to fetch from (uses last search db if not provided)
        id_list: List of IDs to fetch details for (uses last search results if not provided)

        return: List of detailed results
        """
        if not db:
            if not self.last_search_db:
                raise ValueError("No database specified and no previous search performed.")
            db = self.last_search_db

        if not id_list:
            if not self.search_results:
                raise ValueError("No ID list provided and no previous search results available.")
            id_list = self.search_results

        try:
            ids = ",".join(id_list)
            
            esummary_dbs = {
                "assembly", "blastdbinfo", "books", "cdd", "clinvar", "gap",
                "geoprofiles", "medgen", "omim", "orgtrack", "pcassay",
                "protfam", "pccompound", "pcsubstance", "seqannot",
                "biocollections", "annotinfo"
            }
            
            xml_dbs = {"bioproject", "biosample", "sra"}
            
            if db in esummary_dbs:
                handle = Entrez.esummary(db=db, id=ids, report="full")
                records = Entrez.read(handle, validate=False)
                self.detailed_results = records['DocumentSummarySet']['DocumentSummary']
            elif db == "pubmed":
                handle = Entrez.efetch(db=db, id=ids, retmode="xml")
                records = Entrez.read(handle)
                self.detailed_results = records['PubmedArticle']
            elif db in xml_dbs:
                handle = Entrez.efetch(db=db, id=ids, retmode="xml")
                records = xmltodict.parse(handle.read())
                if db == "bioproject":
                    self.detailed_results = records['RecordSet']['DocumentSummary']
                elif db == "biosample":
                    self.detailed_results = records['BioSampleSet']['BioSample']
                else:
                    self.detailed_results = records['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']
            else:
                handle = Entrez.efetch(db=db, id=ids, retmode="xml")
                self.detailed_results = Entrez.read(handle)
            return self.detailed_results
        except Exception as e:
            print(f"Error occurred during fetching details: {e}")
            return []

    def get_search_results(self):
        """Get the IDs from the last search."""
        return self.search_results

    def get_detailed_results(self):
        """Get the detailed results from the last fetch operation."""
        return self.detailed_results

# 使用示例
if __name__ == "__main__":
    searcher = NCBISearcher('your_email@example.com')  # 请替换为你的邮箱

    # 基本搜索
    print("1. Basic search:")
    ids = searcher.search("nucleotide", "Cypripedium[Organism]", retmax=5)
    print(f"Found {len(ids)} results. First few IDs: {ids[:3]}")
    print()

    # 搜索并获取详细信息
    print("2. Search and fetch details:")
    searcher.search("nucleotide", "Cypripedium[Organism]", retmax=5, fetch_details=True)
    detailed_results = searcher.get_detailed_results()
    print(f"Fetched details for {len(detailed_results)} records.")
    searcher.print_summary(detailed=True)
    print()

    # 使用 _search_generator 进行大规模搜索
    print("3. Large-scale search using _search_generator:")
    all_ids, all_details = searcher._search_generator("nucleotide", "Orchidaceae[Organism]", batch_size=100, max_results = 10)
    print(f"Total IDs found: {len(all_ids)}")
    print(f"First few IDs: {all_ids[:5]}")
    print()

    # 为特定ID获取详细信息
    print("4. Fetching details for specific IDs:")
    specific_ids = all_ids[:3]  # 使用前面搜索到的ID
    emp = searcher.fetch_details(db="nucleotide", id_list=specific_ids)
    searcher.print_summary(detailed=True)
    print()

    # 错误处理演示
    print("5. Error handling demonstration:")
    try:
        searcher.search("invalid_db", "test")
    except Exception as e:
        print(f"Expected error occurred: {e}")
    print()

    # 使用不同的数据库
    print("6. Using a different database:")
    protein_ids = searcher.search("protein", "insulin[Protein Name] AND human[Organism]", retmax=5)
    print(f"Found {len(protein_ids)} protein results. First few IDs: {protein_ids[:3]}")
