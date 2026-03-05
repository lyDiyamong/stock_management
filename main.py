"""
Entry point for the Stock Management System console application.

This module contains the main menu loop and top-level navigation logic.
It orchestrates all other modules: data_manager, product_manager, and
reports. The application loads data on startup and saves automatically
before exiting.

Usage:
    python3 main.py 

Modules:
    data_manager   - JSON file I/O and ID generation
    product_manager - CRUD and stock transaction operations
    reports        - Inventory analytics and report generation
"""

from data_manager import load_stock_data, save_stock_data
from product_manager import (
    add_product,
    view_all_products,
    search_products,
    update_product,
    delete_product,
    restock_product,
    sell_product
)
from reports import (
    report_low_stock,
    report_inventory_value,
    report_category_summary,
    report_full_summary
)


def display_main_menu():
    """
    Print the main navigation menu to the console.

    Displays numbered options for all available features. Called at
    the start of each iteration of the main loop.

    Returns:
        None
    """
    print("\n" + "=" * 50)
    print("       STOCK MANAGEMENT SYSTEM")
    print("=" * 50)
    print("  INVENTORY")
    print("    1. View All Products")
    print("    2. Add New Product")
    print("    3. Update Product")
    print("    4. Delete Product")
    print("    5. Search Products")
    print()
    print("  STOCK OPERATIONS")
    print("    6. Record Sale (Deduct Stock)")
    print("    7. Restock Product (Add Stock)")
    print()
    print("  REPORTS")
    print("    8. Low Stock Alert")
    print("    9. Inventory Valuation")
    print("   10. Category Summary")
    print("   11. Full Inventory Dashboard")
    print()
    print("    0. Save and Exit")
    print("=" * 50)


def get_menu_choice():
    """
    Prompt the user to enter a menu option and return it as a string.

    Does not validate the choice here; validation is handled in the
    main loop so that the error message is contextual.

    Returns:
        str: The raw input string from the user.
    """
    return input("  Select an option: ").strip()


def run_application():
    """
    Launch and run the main application loop.

    Loads data from disk on startup, then repeatedly displays the menu
    and dispatches to the appropriate handler based on user input.
    Saves all data to disk before exiting. The loop runs until the
    user selects option 0.

    Returns:
        None
    """
    print("\n  Loading inventory data...")
    products = load_stock_data()
    print(f"  {len(products)} product(s) loaded.")

    # Map of menu choices to handler functions that require the products list
    menu_actions = {
        "1": view_all_products,
        "2": add_product,
        "3": update_product,
        "4": delete_product,
        "5": search_products,
        "6": sell_product,
        "7": restock_product,
        "8": report_low_stock,
        "9": report_inventory_value,
        "10": report_category_summary,
        "11": report_full_summary,
    }

    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice == "0":
            # Save data and exit gracefully
            print("\n  Saving inventory data...")
            success = save_stock_data(products)
            if success:
                print("  Data saved successfully.")
            print("  Goodbye.\n")
            break
        elif choice in menu_actions:
            # Dispatch to the appropriate handler
            menu_actions[choice](products)
            input("\n  Press Enter to return to the main menu...")
        else:
            print(f"\n  [ERROR] '{choice}' is not a valid option. Please choose 0-11.")


if __name__ == "__main__":
    run_application()