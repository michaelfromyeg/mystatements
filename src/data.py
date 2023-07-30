# Add an entry to the savings.json file

import json
from pprint import pprint
from typing import Tuple, Dict

DATA_FOLDER = 'data'

def build_object() -> Tuple[str, Dict]:
    '''
    Build a savings object to append to savings.json
    
    Need:
        - key: str
        - kind: str
        - date: int
        - amount: int
        - description: str
        - tags: List[str]
        - metadata: Dict
    '''

    which = input('> Is this for savings or chequing? Enter \'savings\' or \'chequing\'.\n') # TODO: refactor into selection
    key = input('> What is the "identifying" string for this data?\n')

    obj = {}
    
    kind = input('> What kind of transaction is this? Psst... see transaction.py for help.\n')
    obj['kind'] = kind

    date = input('> Where can the date field be found? e.g., 0, 1, 2, 3\n')
    try:
        obj['date'] = int(date)
    except Exception:
        print("Invalid date entered. Exiting.")
        exit(1)

    amount = input('> Where can the amount field be found? e.g., 0, 1, 2, 3\n')
    try:
        obj['amount'] = int(amount)
    except Exception:
        print("Invalid amount entered. Exiting.")
        exit(1)

    description = input('> What description would you like to give this entry?\n')
    obj['description'] = description

    tags = input('> What tags would you like to add? Enter a comma-separated list.\n')
    obj['tags'] = tags.split(',')

    metadata = input('> Would you like to add metadata? Enter \'yes\' or \'no\'.\n')
    o_metadata = {}
    while (metadata == 'yes'):
        key_val = input('> Input your metadata as a key-value pair, with a colon separating them. e.g., key:value\n')
        key, val = key_val.split(':')
        o_metadata[key] = val
        metadata = input('> Would you like to add more? Enter \'yes\' or \'no\'.\n')
    obj['metadata'] = o_metadata

    if validate_object(obj):
        return (which, key, obj)
    else:
        print("Invalid arguments supplied to object. Exiting.")
        exit(1)


def write_json(key: str, obj: Dict, filename: str) -> None:
    '''
    Append object to correct file
    '''
    data = None
    with open(filename) as f:
        data = json.load(f)
        data[key] = obj
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return None

def validate_object(obj: Dict) -> bool:
    '''
    Check if the user entered valid values
    '''
    # raise NotImplementedException
    return True

# Driver code
if __name__ == '__main__':
    which, key, obj = build_object()
    write_json(key, obj, f"{DATA_FOLDER}/{'savings' if which == 'savings' else 'chequing'}.json")