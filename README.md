# poly-p2-crawler

This script automates fetching, paginating, and storing transaction data from the Optimism Sepolia Blockscout API into a CSV file for analysis, specifically targeting transactions of the PolyP2 Contract.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)

## Instructions

1. Ensure you have Python 3.x installed on your system.
2. Install the Requests library by running `pip install requests` in your terminal or command prompt.
3. Replace the value of `current_params_file` with the path to your `current_params.txt` file.
4. Execute the script.

## Usage

``` python
python3 crawler.py
```
### Script flow
- The script will read parameters from the `current_params.txt` file, construct the API URL, and fetch transaction data.
- Transaction data will be saved to `./data/transaction.csv`.
- If the file size exceeds 50 MB, the current transaction file will be archived, and a new one will be created using the template `transaction.csv`.
- Archived transaction files will be stored in the `./data/` directory.
- Progress and API URLs will be printed during execution.
- The script will continue fetching data until there are no more pages to retrieve.

## Notes

- Ensure proper network connectivity to access the Optimism Sepolia Blockscout API.
- Customize the field names in the `fieldnames` list of the `save_to_csv` function according to your requirements.
- Review and adjust the API URL construction logic (`api_url_base`) if necessary.
- Modify file paths and names as needed to match your directory structure and preferences.

## Disclaimer 

This script is provided as-is without any warranty. Use it at your own risk. Ensure compliance with API usage policies and data protection regulations.
