import json
from pathlib import Path
from typing import Any, List



def read(path:Path=Path('mock_inventory.json'), key:str=None, values:List=None) -> List[dict]:
    """
    Reads and optionally filters inventory data from a JSON file.

    This function represents the 'Read' operation in CRUD. It loads data from a
    specified JSON file. If both 'key' and 'values' are provided, it filters the
    data to return only the items where the value of the specified key exists
    in the 'values' list. If neither is provided, it returns the entire dataset.

    Args:
        path (Path): The file path to the JSON document containing the inventory data.
        key (str, optional): The dictionary key used for filtering (e.g., 'code', 'name'). Defaults to None.
        values (List, optional): A list of acceptable values for the specified key. Defaults to None.

    Returns:
        List[dict]: A list of dictionaries representing the filtered (or complete) inventory items.

    Raises:
        ValueError: If only one of `key` or `values` is provided (both are required for filtering).
        ValueError: If the provided `key` does not exist in any of the dictionaries within the data.

    Todo:
        * Replace JSON file reading with a proper SQLAlchemy database query once the DB is established.
    """
    with path.open() as file:
        content = json.load(file)#TODO: remove reading from the json file after establishing the database
    if (key and (not values)) or (values and (not key)):
        raise ValueError("both key and values should be provided to filter out the data")
    elif key and (not any([key in item.keys() for item in content])):
        raise ValueError(f"key {key} not found in content")
    elif not key and not values:
        return content
    else:
        content = [item for item in content if item.get(key) in values] #TODO:we gotta make it a proper SQL query
        return content






