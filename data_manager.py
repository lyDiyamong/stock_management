"""
Handles all JSON file I/O operations for the Stock Management System.

This module is responsible for loading and saving stock data to disk,
ensuring data persistence between application sessions.
"""

import json
import os

DATA_FILE = "data.json"


def load_stock_data():
    """
    Load stock data from the JSON file.

    Reads the persisted stock records from disk. If the file does not
    exist (e.g., first run), returns an empty list so the application
    can start fresh without errors.

    Returns:
        list: A list of product dictionaries. Returns an empty list if
              the file does not exist or is empty/corrupted.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        print("  [WARNING] Could not read data file. Starting with empty inventory.")
        return []


def save_stock_data(products):
    """
    Save stock data to the JSON file.

    Serializes the in-memory product list to JSON format and writes it
    to disk. Called automatically before the application exits.

    Parameters:
        products (list): The list of product dictionaries to persist.

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)
        return True
    except IOError as error:
        print(f"  [ERROR] Failed to save data: {error}")
        return False


def generate_product_id(products):
    """
    Generate a unique product ID for a new product.

    Scans existing product IDs and returns the next available integer ID
    formatted as a zero-padded string (e.g., 'P001', 'P002').

    Parameters:
        products (list): The current list of product dictionaries.

    Returns:
        str: A unique product ID string in the format 'PXXX'.
    """
    if not products:
        return "P001"

    existing_ids = []
    for product in products:
        pid = product.get("id", "")
        if pid.startswith("P") and pid[1:].isdigit():
            existing_ids.append(int(pid[1:]))

    if not existing_ids:
        return "P001"

    next_id = max(existing_ids) + 1
    return f"P{next_id:03d}"