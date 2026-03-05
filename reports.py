"""
Generates summary reports and analytics for the stock inventory.

This module provides reporting features such as low-stock alerts,
inventory valuation, category breakdowns, and full inventory summaries.
All functions are read-only and do not modify the product list.
"""

NO_PRODUCTS_MESSAGE = "  No products in inventory."


def report_low_stock(products):
    """
    Display all products that are at or below their reorder level.

    Scans the full product list and prints any items whose current
    quantity is less than or equal to their defined reorder threshold.
    This helps purchasing staff identify what needs to be restocked.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- Low Stock Report ---")

    if not products:
        print(NO_PRODUCTS_MESSAGE)
        return

    low_stock_items = [
        p for p in products if p["quantity"] <= p["reorder_level"]
    ]

    if not low_stock_items:
        print("  All products are above their reorder levels. No action needed.")
        return

    print(f"\n  {len(low_stock_items)} product(s) require attention:\n")

    separator = "  " + "-" * 65
    header = (
        f"  {'ID':<6} {'Name':<25} {'Category':<15} "
        f"{'Current':>7} {'Reorder':>8}"
    )

    print(separator)
    print(header)
    print(separator)

    for product in low_stock_items:
        shortage = product["reorder_level"] - product["quantity"]
        print(
            f"  {product['id']:<6} {product['name']:<25} {product['category']:<15} "
            f"{product['quantity']:>7} {product['reorder_level']:>8}  "
            f"(short by {shortage})"
        )

    print(separator)


def report_inventory_value(products):
    """
    Display the total monetary value of the current inventory.

    Calculates the value of each product line (quantity x price) and
    shows a breakdown table followed by the grand total. Useful for
    financial reporting and auditing purposes.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- Inventory Valuation Report ---")

    if not products:
        print(NO_PRODUCTS_MESSAGE)
        return

    separator = "  " + "-" * 68
    header = (
        f"  {'ID':<6} {'Name':<25} {'Qty':>6} "
        f"{'Unit Price':>10} {'Line Value':>12}"
    )

    print(separator)
    print(header)
    print(separator)

    total_value = 0.0

    for product in products:
        line_value = product["quantity"] * product["price"]
        total_value += line_value
        print(
            f"  {product['id']:<6} {product['name']:<25} {product['quantity']:>6} "
            f"  {product['price']:>9.2f}   {line_value:>11.2f}"
        )

    print(separator)
    print(f"  {'TOTAL INVENTORY VALUE':>56}  ${total_value:>10.2f}")
    print(separator)


def report_category_summary(products):
    """
    Display a breakdown of inventory statistics grouped by category.

    Groups all products by their category field and calculates per-category
    totals for quantity, total value, and product count. Helps managers
    understand stock distribution across different product types.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- Category Summary Report ---")

    if not products:
        print(NO_PRODUCTS_MESSAGE)
        return

    # Build a dictionary grouped by category
    categories = {}
    for product in products:
        cat = product["category"]
        if cat not in categories:
            categories[cat] = {
                "count": 0,
                "total_quantity": 0,
                "total_value": 0.0
            }
        categories[cat]["count"] += 1
        categories[cat]["total_quantity"] += product["quantity"]
        categories[cat]["total_value"] += product["quantity"] * product["price"]

    separator = "  " + "-" * 65
    header = (
        f"  {'Category':<20} {'Products':>9} {'Total Qty':>10} {'Total Value':>13}"
    )

    print(separator)
    print(header)
    print(separator)

    grand_total_value = 0.0

    for category, stats in sorted(categories.items()):
        grand_total_value += stats["total_value"]
        print(
            f"  {category:<20} {stats['count']:>9} "
            f"{stats['total_quantity']:>10} {stats['total_value']:>13.2f}"
        )

    print(separator)
    print(f"  {'GRAND TOTAL':>30} {'':>10} {grand_total_value:>13.2f}")
    print(separator)


def report_full_summary(products):
    """
    Display a comprehensive overview of the entire inventory.

    Combines high-level statistics (total products, total units,
    total value, low-stock count) in a single dashboard-style view.
    Intended as a quick health-check for the inventory.

    Parameters:
        products (list): The current in-memory list of product dictionaries.

    Returns:
        None
    """
    print("\n  --- Inventory Summary Dashboard ---")

    if not products:
        print(NO_PRODUCTS_MESSAGE)
        return

    total_products = len(products)
    total_units = sum(p["quantity"] for p in products)
    total_value = sum(p["quantity"] * p["price"] for p in products)
    low_stock_count = sum(1 for p in products if p["quantity"] <= p["reorder_level"])
    out_of_stock = sum(1 for p in products if p["quantity"] == 0)

    categories = {p["category"] for p in products}

    separator = "  " + "=" * 45

    print(separator)
    print(f"  {'Stock Management System - Summary':^43}")
    print(separator)
    print(f"  Total product lines    : {total_products}")
    print(f"  Total categories       : {len(categories)}")
    print(f"  Total units in stock   : {total_units}")
    print(f"  Total inventory value  : ${total_value:,.2f}")
    print(f"  Products needing reorder: {low_stock_count}")
    print(f"  Out-of-stock items     : {out_of_stock}")
    print(separator)