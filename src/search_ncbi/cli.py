import argparse
import sys
import pandas as pd
from .search_ncbi import NCBITools


def main():
    parser = argparse.ArgumentParser(description="NCBI Tools Command Line Interface")
    parser.add_argument("--email", required=True, help="Your email address for NCBI queries")
    parser.add_argument("--api-key", help="Your NCBI API key (optional)")
    parser.add_argument("-d", "--db", required=True, help="NCBI database to search")
    parser.add_argument("-t", "--term", required=True, help="Search term")
    parser.add_argument("-m", "--max-results", type=int, default=None, help="Maximum number of results to return")
    parser.add_argument("-b", "--batch-size", type=int, default=500, help="Number of results to process in each batch")
    parser.add_argument("-o", "--output", default="output.csv", help="Output file name (CSV format)")
    parser.add_argument("-a", "--action", choices=["metadata", "custom", "raw", "count", "id_list"], default="metadata",
                        help="Action to perform: process all metadata, custom metadata extraction, get raw data, get count, or get ID list")
    parser.add_argument("--include", nargs="*", help="List of column names to include (for custom filtering)")
    parser.add_argument("--exclude", nargs="*", help="List of column names to exclude (for custom filtering)")
    parser.add_argument("--contains", nargs="*",
                        help="List of strings that column names should contain (for custom filtering)")
    parser.add_argument("--regex", help="Regular expression for filtering column names (for custom filtering)")

    args = parser.parse_args()

    ncbi = NCBITools(args.email, args.api_key)

    try:
        if args.action == "metadata":
            result = ncbi.search_and_process(args.db, args.term, max_results=args.max_results,
                                             batch_size=args.batch_size, process_method='all')
            result.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")
        elif args.action == "custom":
            result = ncbi.search_and_process(args.db, args.term, max_results=args.max_results,
                                             batch_size=args.batch_size, process_method='custom',
                                             include=args.include, exclude=args.exclude, contains=args.contains, regex=args.regex)
            result.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")
        elif args.action == "raw":
            result = ncbi.get_raw_data(args.db, args.term, max_results=args.max_results, batch_size=args.batch_size)
            pd.DataFrame(result).to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")
        elif args.action == "count":
            count = ncbi.search_count(args.db, args.term)
            print(f"Total number of results: {count}")
        elif args.action == "id_list":
            id_list = ncbi.get_id_list(args.db, args.term, max_results=args.max_results, batch_size=args.batch_size)
            output_file = args.output if args.output.endswith('.txt') else args.output.rsplit('.', 1)[0] + '.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                for id in id_list:
                    f.write(f"{id}\n")
            print(f"ID List saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()