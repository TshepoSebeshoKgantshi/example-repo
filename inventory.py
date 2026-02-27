# ========= The beginning of the class =========
from __future__ import annotations

import os
from typing import Optional

# Ensure inventory.txt is always accessed from the same folder as this file
BASE_DIR = os.path.dirname(__file__)
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.txt")


class Shoe:
    def __init__(self, country: str, code: str, product: str, cost: float, quantity: int):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self) -> float:
        """Returns the cost of the shoes."""
        return self.cost

    def get_quantity(self) -> int:
        """Returns the quantity of the shoes."""
        return self.quantity

    def __str__(self) -> str:
        """Returns a string representation of the Shoe object."""
        return (
            f"Country: {self.country} | Code: {self.code} | Product: {self.product} | "
            f"Cost: {self.cost} | Quantity: {self.quantity}"
        )


# ============= Shoe list ===========
# Required: empty list to store Shoe objects
shoes_list: list[Shoe] = []


def read_shoes_data() -> None:
    """
    Open inventory.txt, read the data, create Shoe objects, and append them to shoes_list.
    Must use try-except for error handling and skip the first line (header).
    """
    shoes_list.clear()

    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            print("inventory.txt is empty.")
            return

        # Skip header
        for line_no, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 5:
                print(f"Skipping invalid line {line_no}: {line}")
                continue

            country, code, product, cost_str, qty_str = parts

            try:
                cost = float(cost_str)
                quantity = int(qty_str)
            except ValueError:
                print(f"Skipping line {line_no} (bad number): {line}")
                continue

            shoes_list.append(Shoe(country, code, product, cost, quantity))

        print(f"Loaded {len(shoes_list)} shoes from inventory.txt.")

    except FileNotFoundError:
        print("Error: inventory.txt not found. Make sure it is in the same folder as inventory.py.")
    except PermissionError:
        print("Error: Permission denied when reading inventory.txt.")
    except Exception as e:
        print(f"Unexpected error while reading inventory.txt: {e}")


def capture_shoes() -> None:
    """
    Allow a user to capture data about a shoe and append a new Shoe object to shoes_list.
    """
    country = input("Country: ").strip()
    code = input("Code: ").strip()
    product = input("Product: ").strip()

    while True:
        try:
            cost = float(input("Cost: ").strip())
            break
        except ValueError:
            print("Invalid cost. Please enter a number (e.g. 2300 or 2300.50).")

    while True:
        try:
            quantity = int(input("Quantity: ").strip())
            break
        except ValueError:
            print("Invalid quantity. Please enter a whole number (e.g. 10).")

    shoes_list.append(Shoe(country, code, product, cost, quantity))
    print("Shoe captured and added to the list.")


def view_all() -> None:
    """
    Iterate over shoes_list and print the details of the shoes returned from __str__.
    """
    if not shoes_list:
        print("No shoes loaded. Choose option 1 first (read_shoes_data).")
        return

    print("\n--- ALL SHOES ---")
    for shoe in shoes_list:
        print(shoe)


def _update_quantity_in_file(target_code: str, new_quantity: int) -> bool:
    """
    Update ONLY the quantity field for the shoe with target_code in inventory.txt.
    Returns True if an update was made, otherwise False.
    """
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            return False

        header = lines[0]
        updated_lines = [header]
        updated = False

        for line in lines[1:]:
            raw = line.rstrip("\n")
            if not raw.strip():
                updated_lines.append(line)
                continue

            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 5:
                updated_lines.append(line if line.endswith("\n") else line + "\n")
                continue

            country, code, product, cost, quantity = parts

            if code == target_code:
                updated_lines.append(f"{country},{code},{product},{cost},{new_quantity}\n")
                updated = True
            else:
                updated_lines.append(line if line.endswith("\n") else line + "\n")

        if not updated:
            return False

        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

        return True

    except FileNotFoundError:
        print("Error: inventory.txt not found.")
        return False
    except PermissionError:
        print("Error: Permission denied when updating inventory.txt.")
        return False
    except Exception as e:
        print(f"Error updating inventory.txt: {e}")
        return False


def re_stock() -> None:
    """
    Find the shoe object with the lowest quantity, ask the user if they want to add stock,
    update the quantity, and update that shoe's quantity in the file.
    """
    if not shoes_list:
        print("No shoes loaded. Choose option 1 first (read_shoes_data).")
        return

    lowest_shoe = min(shoes_list, key=lambda s: s.quantity)

    print("\nLowest stock item:")
    print(lowest_shoe)

    choice = input("Do you want to add stock to this item? (y/n): ").strip().lower()
    if choice != "y":
        print("Restock cancelled.")
        return

    while True:
        try:
            add_qty = int(input("How many units do you want to add? ").strip())
            if add_qty <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number.")

    lowest_shoe.quantity += add_qty

    # Required: update quantity on the file for this shoe
    updated = _update_quantity_in_file(lowest_shoe.code, lowest_shoe.quantity)
    if not updated:
        print("Warning: Could not update the file line for this shoe (code not found).")

    print("Stock updated:")
    print(lowest_shoe)


def search_shoe() -> Optional[Shoe]:
    """
    Search for a shoe from the list using the shoe code and return the object.
    """
    if not shoes_list:
        print("No shoes loaded. Choose option 1 first (read_shoes_data).")
        return None

    code = input("Enter shoe code to search: ").strip()
    for shoe in shoes_list:
        if shoe.code == code:
            return shoe

    return None


def value_per_item() -> None:
    """
    Calculate the total value for each item and print it.
    value = cost * quantity
    """
    if not shoes_list:
        print("No shoes loaded. Choose option 1 first (read_shoes_data).")
        return

    print("\n--- VALUE PER ITEM ---")
    for shoe in shoes_list:
        value = shoe.cost * shoe.quantity
        print(f"Product: {shoe.product} | Code: {shoe.code} | Value: {value}")


def highest_qty() -> None:
    """
    Determine the product with the highest quantity and print this shoe as being for sale.
    """
    if not shoes_list:
        print("No shoes loaded. Choose option 1 first (read_shoes_data).")
        return

    highest_shoe = max(shoes_list, key=lambda s: s.quantity)
    print("\n--- FOR SALE (HIGHEST STOCK) ---")
    print(highest_shoe)


def main() -> None:
    # Required: menu inside a while loop
    while True:
        print(
            "\n===== NIKE WAREHOUSE MENU =====\n"
            "1. Read shoes data\n"
            "2. Capture a new shoe\n"
            "3. View all shoes\n"
            "4. Restock (lowest quantity)\n"
            "5. Search shoe by code\n"
            "6. Value per item\n"
            "7. Highest quantity (for sale)\n"
            "0. Exit\n"
        )

        choice = input("Choose an option: ").strip()

        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            view_all()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            found = search_shoe()
            if found is None:
                print("Shoe not found.")
            else:
                print("Shoe found:")
                print(found)
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()