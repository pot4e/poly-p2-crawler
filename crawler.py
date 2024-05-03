import os
import json
import requests
import csv
import shutil

def flatten_item(item):
    flat_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                flat_item[f"{key}.{subkey}"] = subvalue
        elif isinstance(value, list):
            flat_item[key] = json.dumps(value)
        else:
            flat_item[key] = value
    return flat_item

def save_to_csv(items, filename):
    fieldnames = [
        'timestamp',
        'fee.type',
        'fee.value',
        'gas_limit',
        'block',
        'status',
        'method',
        'confirmations',
        'type',
        'exchange_rate',
        'to.ens_domain_name',
        'to.hash',
        'to.implementation_name',
        'to.is_contract',
        'to.is_verified',
        'to.metadata',
        'to.name',
        'to.private_tags',
        'to.public_tags',
        'to.watchlist_names',
        'tx_burnt_fee',
        'max_fee_per_gas',
        'result',
        'hash',
        'gas_price',
        'priority_fee',
        'base_fee_per_gas',
        'from.ens_domain_name',
        'from.hash',
        'from.implementation_name',
        'from.is_contract',
        'from.is_verified',
        'from.metadata',
        'from.name',
        'from.private_tags',
        'from.public_tags',
        'from.watchlist_names',
        'token_transfers',
        'tx_types',
        'gas_used',
        'created_contract',
        'position',
        'nonce',
        'has_error_in_internal_txs',
        'actions',
        'decoded_input',
        'decoded_input.method_id',
        'decoded_input.method_call',
        'decoded_input.parameters',
        'decoded_input.raw',
        'token_transfers_overflow',
        'raw_input',
        'value',
        'max_priority_fee_per_gas',
        'revert_reason',
        'revert_reason.method_id',
        'revert_reason.method_call',
        'revert_reason.parameters',
        'revert_reason.raw',
        'confirmation_duration',
        'tx_tag'
    ]
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in items:
            flat_item = flatten_item(item)
            writer.writerow(flat_item)

def get_data(api_url):
    response = requests.get(api_url)
    data = response.json()
    next_page_params = data.get('next_page_params', {})
    items = data.get('items', [])
    return next_page_params, items

def write_params_to_file(params, filename):
    with open(filename, 'w') as file:
        file.write(json.dumps(params))

def append_params_to_file(params, filename):
    with open(filename, 'a') as file:
        file.write(json.dumps(params) + '\n')

def check_file_size(filename):
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        # Chuyển đổi kích thước từ byte sang megabyte
        file_size_mb = file_size / (1024 * 1024)
        return file_size_mb > 50
    else:
        return False

# Đường dẫn tới tệp current_params.txt
current_params_file = "current_params.txt"

# Đọc thông tin từ tệp current_params.txt
with open(current_params_file, 'r') as file:
    next_page_params = json.loads(file.read())

print(next_page_params)
# Xây dựng URL API từ thông tin trong current_params.txt
api_url_base = "https://optimism-sepolia.blockscout.com/api/v2/addresses/0x5c48ab8DFD7abd7D14027FF65f01887F78EfFE0F/transactions"
api_url_params = "&".join([f"{key}={value}" for key, value in next_page_params.items()])
api_url = f"{api_url_base}?{api_url_params}"


called_params_file = "called_params.txt"
template_transaction_file = "transaction.csv"
transaction_file = "./data/transaction.csv"

while api_url:
    
    print("-------- API_URL --------")
    print(api_url)
    next_page_params, items = get_data(api_url)
    print("--------- Next Paramt")
    print(next_page_params)
    write_params_to_file(next_page_params, current_params_file)
    append_params_to_file(next_page_params, called_params_file)
    
    save_to_csv(items, transaction_file)

    # Kiểm tra kích thước của tệp transaction.csv
    if check_file_size(transaction_file):
        # Đổi tên tệp transaction
        archive_transaction_file = f"./data/transaction_{len(os.listdir('./data')) + 1}.csv"
        os.rename(transaction_file, archive_transaction_file)
        # Copy template thành transaction và tiếp tục
        shutil.copy(template_transaction_file, transaction_file)
    
    # Xây dựng URL cho trang tiếp theo
    api_url_params = "&".join([f"{key}={value}" for key, value in next_page_params.items()])
    api_url = f"{api_url_base}?{api_url_params}"

    print("Calling params:", next_page_params)

print("Done.")
