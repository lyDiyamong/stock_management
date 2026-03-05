"""
Contains all business logic for CRUD operations on stock products.

This module handles adding, viewing, updating, deleting, and searching
products. It operates on the in-memory product list and delegates
persistence to data_manager.py.
"""

from data_manager import generate_product_id


def add_product(products):
    """
    Prompt the user for product details and add a new product to the list.

    Collects product name, category, quantity, price, and reorder level
    from the user. Validates all numeric fields before accepting input.
    Generates a unique ID automatically.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None: Modifies the products list in place.
    """
    print("\n  --- Add New Product ---")

    name = input("  Product name: ").strip()
    if not name:
        print("  [ERROR] Product name cannot be empty.")
        return

    # Check for duplicate name (case-insensitive)
    for product in products:
        if product["name"].lower() == name.lower():
            print(f"  [ERROR] A product named '{name}' already exists (ID: {product['id']}).")
            return

    category = input("  Category: ").strip()
    if not category:
        print("  [ERROR] Category cannot be empty.")
        return

    quantity = get_valid_integer("  Initial quantity: ")
    if quantity is None:
        return

    price = get_valid_float("  Unit price ($): ")
    if price is None:
        return

    reorder_level = get_valid_integer("  Reorder alert level (min quantity): ")
    if reorder_level is None:
        return

    new_product = {
        "id": generate_product_id(products),
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": round(price, 2),
        "reorder_level": reorder_level
    }

    products.append(new_product)
    print(f"\n  [OK] Product '{name}' added with ID {new_product['id']}.")


def view_all_products(products):
    """
    Display all products in a formatted table.

    Prints a structured table of all products including their ID, name,
    category, quantity, price, and reorder level. Highlights products
    that are at or below their reorder level.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- All Products ---")

    if not products:
        print("  No products found.")
        return

    header = (
        f"  {'ID':<6} {'Name':<25} {'Category':<15} "
        f"{'Qty':>6} {'Price':>10} {'Reorder':>8}"
    )
    separator = "  " + "-" * 74

    print(separator)
    print(header)
    print(separator)

    for product in products:
        low_stock_flag = ""
        if product["quantity"] <= product["reorder_level"]:
            low_stock_flag = " [LOW]"

        print(
            f"  {product['id']:<6} {product['name']:<25} {product['category']:<15} "
            f"{product['quantity']:>6} {product['price']:>10.2f} "
            f"{product['reorder_level']:>8}{low_stock_flag}"
        )

    print(separator)
    print(f"  Total products: {len(products)}")


def search_products(products):
    """
    Search for products by name, category, or ID.

    Performs a case-insensitive partial match search on product names
    and categories, and an exact match search on product ID.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- Search Products ---")

    query = input("  Enter search term (name, category, or ID): ").strip()
    if not query:
        print("  [ERROR] Search term cannot be empty.")
        return

    query_lower = query.lower()
    results = []

    for product in products:
        if (query_lower in product["name"].lower() or
                query_lower in product["category"].lower() or
                query_lower == product["id"].lower()):
            results.append(product)

    if not results:
        print(f"  No products found matching '{query}'.")
        return

    print(f"\n  Found {len(results)} result(s):\n")
    header = (
        f"  {'ID':<6} {'Name':<25} {'Category':<15} "
        f"{'Qty':>6} {'Price':>10} {'Reorder':>8}"
    )
    separator = "  " + "-" * 74

    print(separator)
    print(header)
    print(separator)

    for product in results:
        low_stock_flag = ""
        if product["quantity"] <= product["reorder_level"]:
            low_stock_flag = " [LOW]"
        print(
            f"  {product['id']:<6} {product['name']:<25} {product['category']:<15} "
            f"{product['quantity']:>6} {product['price']:>10.2f} "
            f"{product['reorder_level']:>8}{low_stock_flag}"
        )

    print(separator)


def update_product(products):
    """
    Update fields of an existing product by ID.

    Prompts the user to enter a product ID, then presents a sub-menu
    to choose which field to update. Validates all numeric inputs.
    Pressing Enter without input skips a field update.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None: Modifies the products list in place.
    """
    print("\n  --- Update Product ---")

    product_id = input("  Enter product ID to update: ").strip().upper()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  [ERROR] Product with ID '{product_id}' not found.")
        return

    print(f"\n  Editing: {product['name']} (ID: {product['id']})")
    print("  Press Enter to keep the current value.\n")

    _update_product_name(product, products)
    _update_product_category(product)
    _update_product_quantity(product)
    _update_product_price(product)
    _update_product_reorder_level(product)

    print(f"\n  [OK] Product '{product['id']}' updated successfully.")


def delete_product(products):
    """
    Delete a product from the inventory by ID.

    Prompts the user for a product ID and asks for confirmation before
    permanently removing the product from the list.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None: Modifies the products list in place.
    """
    print("\n  --- Delete Product ---")

    product_id = input("  Enter product ID to delete: ").strip().upper()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  [ERROR] Product with ID '{product_id}' not found.")
        return

    print(f"\n  Product to delete: {product['name']} (ID: {product['id']})")
    confirm = input("  Are you sure? This cannot be undone. (yes/no): ").strip().lower()

    if confirm == "yes":
        products.remove(product)
        print(f"  [OK] Product '{product_id}' deleted.")
    else:
        print("  Deletion cancelled.")


def restock_product(products):
    """
    Add stock to an existing product's quantity.

    Allows quick restocking without going through the full update flow.
    Useful for receiving new shipments and updating quantity on hand.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None: Modifies the products list in place.
    """
    print("\n  --- Restock Product ---")

    product_id = input("  Enter product ID to restock: ").strip().upper()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  [ERROR] Product with ID '{product_id}' not found.")
        return

    print(f"  Product: {product['name']} | Current stock: {product['quantity']}")

    amount = get_valid_integer("  Quantity to add: ")
    if amount is None:
        return

    if amount <= 0:
        print("  [ERROR] Amount to add must be greater than zero.")
        return

    product["quantity"] += amount
    print(f"  [OK] New stock level for '{product['name']}': {product['quantity']}")


def sell_product(products):
    """
    Deduct sold units from a product's quantity.

    Records a sale by reducing the stock quantity. Warns if the resulting
    quantity falls below the reorder level. Prevents selling more than
    the available stock.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None: Modifies the products list in place.
    """
    print("\n  --- Record Sale ---")

    product_id = input("  Enter product ID: ").strip().upper()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  [ERROR] Product with ID '{product_id}' not found.")
        return

    print(f"  Product: {product['name']} | Current stock: {product['quantity']}")

    amount = get_valid_integer("  Quantity sold: ")
    if amount is None:
        return

    if amount <= 0:
        print("  [ERROR] Quantity sold must be greater than zero.")
        return

    if amount > product["quantity"]:
        print(
            f"  [ERROR] Insufficient stock. Available: {product['quantity']}, "
            f"Requested: {amount}."
        )
        return

    product["quantity"] -= amount
    total_value = amount * product["price"]
    print(f"  [OK] Sold {amount} unit(s) of '{product['name']}'. Sale value: ${total_value:.2f}")

    if product["quantity"] <= product["reorder_level"]:
        print(
            f"  [ALERT] Stock for '{product['name']}' is now at {product['quantity']} "
            f"(reorder level: {product['reorder_level']}). Please reorder soon."
        )


# ---------------------------------------------------------------------------
# Field Update Helper Functions (used by update_product)
# ---------------------------------------------------------------------------

def _update_product_name(product, products):
    """Update product name with duplicate check."""
    new_name = input(f"  Name [{product['name']}]: ").strip()
    if not new_name or new_name.lower() == product["name"].lower():
        return
    
    if _product_name_exists(products, new_name, product["id"]):
        print(f"  [ERROR] Another product named '{new_name}' already exists. Name not changed.")
    else:
        product["name"] = new_name


def _update_product_category(product):
    """Update product category."""
    new_category = input(f"  Category [{product['category']}]: ").strip()
    if new_category:
        product["category"] = new_category


def _update_product_quantity(product):
    """Update product quantity with validation."""
    new_qty_str = input(f"  Quantity [{product['quantity']}]: ").strip()
    if not new_qty_str:
        return
    
    new_qty = parse_integer(new_qty_str)
    if new_qty is None:
        print("  [WARNING] Invalid quantity input. Quantity not changed.")
    else:
        product["quantity"] = new_qty


def _update_product_price(product):
    """Update product price with validation."""
    new_price_str = input(f"  Price [{product['price']:.2f}]: ").strip()
    if not new_price_str:
        return
    
    new_price = parse_float(new_price_str)
    if new_price is None:
        print("  [WARNING] Invalid price input. Price not changed.")
    else:
        product["price"] = round(new_price, 2)


def _update_product_reorder_level(product):
    """Update product reorder level with validation."""
    new_reorder_str = input(f"  Reorder level [{product['reorder_level']}]: ").strip()
    if not new_reorder_str:
        return
    
    new_reorder = parse_integer(new_reorder_str)
    if new_reorder is None:
        print("  [WARNING] Invalid reorder level input. Reorder level not changed.")
    else:
        product["reorder_level"] = new_reorder


def _product_name_exists(products, name, exclude_product_id):
    """Check if a product name already exists (case-insensitive), excluding a specific product."""
    for p in products:
        if p["id"] != exclude_product_id and p["name"].lower() == name.lower():
            return True
    return False


# ---------------------------------------------------------------------------
# Helper / Utility Functions
# ---------------------------------------------------------------------------

def find_product_by_id(products, product_id):
    """
    Find and return a product dictionary by its ID.

    Performs a case-insensitive exact match on the product ID field.

    Parameters:
        products (list): The in-memory list of product dictionaries.
        product_id (str): The product ID to search for.

    Returns:
        dict or None: The matching product dictionary, or None if not found.
    """
    for product in products:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def get_valid_integer(prompt):
    """
    Prompt the user repeatedly until a valid non-negative integer is entered.

    Parameters:
        prompt (str): The input prompt to display to the user.

    Returns:
        int or None: The validated integer, or None if the user types 'cancel'.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "cancel":
            print("  Operation cancelled.")
            return None
        result = parse_integer(raw)
        if result is not None and result >= 0:
            return result
        print("  [ERROR] Please enter a valid whole number (0 or greater). Type 'cancel' to abort.")


def get_valid_float(prompt):
    """
    Prompt the user repeatedly until a valid non-negative float is entered.

    Parameters:
        prompt (str): The input prompt to display to the user.

    Returns:
        float or None: The validated float, or None if the user types 'cancel'.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "cancel":
            print("  Operation cancelled.")
            return None
        result = parse_float(raw)
        if result is not None and result >= 0:
            return result
        print("  [ERROR] Please enter a valid number (e.g., 9.99). Type 'cancel' to abort.")


def parse_integer(value):
    """
    Attempt to parse a string as an integer without raising an exception.

    Parameters:
        value (str): The string to parse.

    Returns:
        int or None: The parsed integer, or None if parsing fails.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_float(value):
    """
    Attempt to parse a string as a float without raising an exception.

    Parameters:
        value (str): The string to parse.

    Returns:
        float or None: The parsed float, or None if parsing fails.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None