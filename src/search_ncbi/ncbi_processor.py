"""process ncbi metadata information"""
import re
import pandas as pd
from typing import List, Dict, Any, Union

class NCBIMetadataProcessor:
    @staticmethod
    def extract_all_metadata(detailed_results: Union[List[Dict[str, Any]], pd.DataFrame]):
        """
        Extract all metadata from detailed results without filtering.

        Args:
        detailed_results (List[Dict[str, Any]]): List of detailed results from NCBI search.

        Returns:
        pd.DataFrame: DataFrame containing all extracted metadata.
        """
        if isinstance(detailed_results, pd.DataFrame):
            return detailed_results

        if not detailed_results:
            raise ValueError("No detailed results provided to process.")

        all_data = [NCBIMetadataProcessor._flatten_dict(record) for record in detailed_results]
        return pd.DataFrame(all_data)

    @staticmethod
    def _flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten a nested dictionary.

        Args:
        d (Dict[str, Any]): The dictionary to flatten.
        parent_key (str): The string to prepend to dictionary keys.
        sep (str): The separator between flattened keys.

        Returns:
        Dict[str, Any]: Flattened dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(NCBIMetadataProcessor._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(NCBIMetadataProcessor._flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", str(item)))
            else:
                items.append((new_key, str(v)))
        return dict(items)

    @staticmethod
    def extract_features(detailed_results: Union[List[Dict[str, Any]], pd.DataFrame],
                         include: Union[List[str], None] = None,
                         exclude: Union[List[str], None] = None,
                         contains: Union[List[str], None] = None,
                         regex: Union[str, None] = None) -> pd.DataFrame:
        """
        Filter the all_metadata DataFrame based on specified criteria.

        Args:
        all_metadata (pd.DataFrame): DataFrame containing all metadata.
        include (List[str], optional): List of column names to include. If None, all columns are included initially.
        exclude (List[str], optional): List of column names to exclude.
        contains (List[str], optional): List of strings that column names should contain.

        Returns:
        pd.DataFrame: Filtered DataFrame based on the specified criteria.
        """
        all_metadata = NCBIMetadataProcessor.extract_all_metadata(detailed_results)

        if include is None:
            filtered_columns = all_metadata.columns
        else:
            filtered_columns = [col for col in all_metadata.columns if col in include]

        if exclude:
            filtered_columns = [col for col in filtered_columns if col not in exclude]

        if contains:
            filtered_columns = [col for col in filtered_columns if any(substr in col for substr in contains)]

        if regex:
            pattern = re.compile(regex)
            filtered_columns = [col for col in filtered_columns if pattern.search(col)]

        if not filtered_columns:
            raise ValueError("No columns remain after applying filters.")

        return all_metadata[filtered_columns]

