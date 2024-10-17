"""NCBI Basic Configuration"""
import os
from configparser import ConfigParser

# Default configuration
DEFAULT_CONFIG = {
    'email': '',
    'api_key': '',
    'max_results': '20'
}

AVAILABLE_DATABASES = [
    'pubmed', 'protein', 'nuccore', 'ipg', 'nucleotide', 'structure', 'genome',
    'annotinfo', 'assembly', 'bioproject', 'biosample', 'blastdbinfo', 'books',
    'cdd', 'clinvar', 'gap', 'gapplus', 'grasp', 'dbvar', 'gene', 'gds',
    'geoprofiles', 'medgen', 'mesh', 'nlmcatalog', 'omim', 'orgtrack', 'pmc',
    'popset', 'proteinclusters', 'pcassay', 'protfam', 'pccompound', 'pcsubstance',
    'seqannot', 'snp', 'sra', 'taxonomy', 'biocollections', 'gtr'
]

def load_config():
    config = ConfigParser()

    # Set default values
    config['DEFAULT'] = DEFAULT_CONFIG

    # Load from config file if it exists
    config_file = os.path.expanduser('~/.ncbi_tools.ini')
    if os.path.exists(config_file):
        config.read(config_file)

    # Override with environment variables if set
    for key in DEFAULT_CONFIG:
        env_var = f'SEARCH_NCBI_{key.upper()}'
        if os.environ.get(env_var):
            config['DEFAULT'][key] = os.environ[env_var]

    return config['DEFAULT']

CONFIG = load_config()

EMAIL = CONFIG['email']
API_KEY = CONFIG['api_key']
MAX_RESULTS = int(CONFIG['max_results'])

DATABASES = AVAILABLE_DATABASES