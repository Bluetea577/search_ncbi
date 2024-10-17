from typing import Optional, List, Dict, Any, Union
import pandas as pd
from .ncbi_searcher import NCBISearcher
from .ncbi_processor import NCBIMetadataProcessor


class NCBITools:
    def __init__(self, email: str, api_key: Optional[str] = None):
        self.searcher = NCBISearcher(email, api_key)
        self.processor = NCBIMetadataProcessor()

    def search_and_process(self, db: str, term: str, max_results: Optional[int] = None,
                           batch_size: int = 500, process_method: str = 'all',
                           include: Union[List[str], None] = None,
                           exclude: Union[List[str], None] = None,
                           contains: Union[List[str], None] = None,
                           regex: Union[str, None] = None) -> pd.DataFrame:
        """
        Perform a search, fetch details, and process the results.

        Args:
            db (str): The NCBI database to search
            term (str): The search term
            max_results (Optional[int]): Maximum number of results to return (None for no limit)
            batch_size (int): Number of results to process in each batch
            process_method (str): 'all' for all metadata, or 'custom' for custom filtering
            include (List[str], optional): List of column names to include (for custom filtering)
            exclude (List[str], optional): List of column names to exclude (for custom filtering)
            contains (List[str], optional): List of strings that column names should contain (for custom filtering)

        Returns:
            pd.DataFrame: Processed data as a pandas DataFrame
        """
        _, detailed_results = self.searcher._search_generator(db, term, batch_size=batch_size,
                                                              max_results=max_results, fetch_details=True)

        if process_method == 'all':
            return self.processor.extract_all_metadata(detailed_results)
        elif process_method == 'custom':
            all_metadata = self.processor.extract_all_metadata(detailed_results)
            return self.processor.extract_features(all_metadata, include, exclude, contains, regex)
        else:
            raise ValueError("Invalid process_method. Choose 'all', or 'custom'.")

    def get_raw_data(self, db: str, term: str, max_results: Optional[int] = None,
                     batch_size: int = 500) -> List[Dict[str, Any]]:
        """
        Perform a search and return the raw detailed results.

        Args:
            db (str): The NCBI database to search
            term (str): The search term
            max_results (Optional[int]): Maximum number of results to return (None for no limit)
            batch_size (int): Number of results to process in each batch

        Returns:
            List[Dict[str, Any]]: Raw detailed results from NCBI
        """
        _, detailed_results = self.searcher._search_generator(db, term, batch_size=batch_size,
                                                              max_results=max_results, fetch_details=True)
        return detailed_results

    def search_count(self, db: str, term: str) -> int:
        """
        Get the total count of search results without fetching the data.

        Args:
            db (str): The NCBI database to search
            term (str): The search term

        Returns:
            int: Total count of search results
        """
        self.searcher.search(db, term, retmax=1)
        return self.searcher.search_count

    def get_id_list(self, db: str, term: str, max_results: Optional[int] = None,
                    batch_size: int = 500) -> List[str]:
        """
        Perform a search and return only the list of IDs.

        Args:
            db (str): The NCBI database to search
            term (str): The search term
            max_results (Optional[int]): Maximum number of results to return (None for no limit)
            batch_size (int): Number of results to process in each batch

        Returns:
            List[str]: List of IDs from the search results
        """
        id_list, _ = self.searcher._search_generator(db, term, batch_size=batch_size,
                                                     max_results=max_results, fetch_details=False)
        return id_list
    def search_and_save_metadata(self, db: str, term: str, output_file: str,
                                 max_results: Optional[int] = None,
                                 batch_size: int = 500) -> None:
        """
        Perform a search and save the metadata to file.

        Args:
            db (str): The NCBI database to search
            term (str): The search term
            output_file (str): The output file path
            max_results (Optional[int]): Maximum number of results to return (None for no limit)
            batch_size (int): Number of results to process in each batch
        """
        results = self.search_and_process(db, term, max_results, batch_size, process_method='all')
        results.to_csv(output_file, index=False)
        print(f"Metadata saved to {output_file}")
    def filter_metadata(self, input_file: str, output_file: str, filter_term: str) -> pd.DataFrame:
        """
        Filter specific information from saved files

        Args:
        input_file (str): The input file path
        output_file (str): The output file path
        filter_term (str): The filter term

        Returns:
        """
        df = pd.read_csv(input_file)
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(filter_term, case=False).any(), axis=1)]
        filtered_df.to_csv(output_file, index=False)
        print(f"Filtered metadata saved to {output_file}")
        return filtered_df
    def search_and_filter_metadata(self, db: str, term: str, filter_term: str,
                                   metadata_file: str, filter_file: str,
                                   max_results: Optional[int] = None,
                                   batch_size: int = 500) -> pd.DataFrame:
        """
        Perform a complete workflow: searching, saving metadata, filtering data.

        Args:
            db (str): The NCBI database to search
            term (str): The search term
            filter_term (str): The filter term
            metadata_file (str): The metadata file path
            filter_file (str): The filter file path
            max_results (Optional[int]): Maximum number of results to return (None for no limit)
            batch_size (int): Number of results to process in each batch

        Returns:
            pd.DataFrame: Processed data as a pandas DataFrame
        """
        self.search_and_save_metadata(db, term, metadata_file, max_results, batch_size)
        return self.filter_metadata(metadata_file, filter_file, filter_term)


# 使用示例
if __name__ == "__main__":
    ncbi_tools = NCBITools("limingyang577@163.com") #("your_email@example.com", "your_api_key")

    # 获取搜索结果数量
    count = ncbi_tools.search_count("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]")
    print(f"Total results: {count}")

    # # 获取ID列表
    # id_list = ncbi_tools.get_id_list("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]", max_results=100)
    # print(f"Number of IDs retrieved: {len(id_list)}")
    # print("First few IDs:", id_list[:5])
    #
    # # 获取所有元数据
    # all_data = ncbi_tools.search_and_process("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]",
    #                                          max_results=10, process_method='all')
    # print("All metadata shape:", all_data.shape)
    #
    # # 获取特征数据
    # feature_data = ncbi_tools.search_and_process("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]",
    #                                              max_results=10, process_method='features')
    # print("Feature data shape:", feature_data.shape)

    # 自定义过滤
    custom_data = ncbi_tools.search_and_process("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]",
                                                max_results=10, process_method='custom',
                                                contains=['accession', 'organism'])
    print("Custom filtered data shape:", custom_data.shape)

    # 获取原始数据
    raw_data = ncbi_tools.get_raw_data("nucleotide", "SARS-CoV-2[Organism] AND complete genome[Title]", max_results=10)
    print("Number of raw records:", len(raw_data))
