
import json
import os

FILE_NAME = "products.json"


def load_products():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Error reading inventory file.")
        return []


def save_products(products):
    with open(FILE_NAME, "w") as file:
        json.dump(products, file, indent=4)


def display_products(products):
    if not products:
        print("\nNo products available.")
        return

    print("\n--- INVENTORY ---")
    print(f"{'ID':<8}{'Product':<15}{'Price':<10}{'Stock':<8}")

    for product in products:
        print(
            f"{product['id']:<8}"
            f"{product['name']:<15}"
            f"{product['price']:<10.2f}"
            f"{product['stock']:<8}"
        )


def add_product(products):
    product_id = input("Enter product ID: ").strip()

    if any(p["id"] == product_id for p in products):
        print("Product ID already exists.")
        return

    name = input("Enter product name: ").strip()

    try:
        price = float(input("Enter price: "))
        stock = int(input("Enter quantity: "))

        if not name or price < 0 or stock < 0:
            print("Enter valid product details.")
            return

        products.append({
            "id": product_id,
            "name": name,
            "price": price,
            "stock": stock
        })

        save_products(products)
        print("Product added successfully.")

    except ValueError:
        print("Invalid price or quantity.")


def update_stock(products):
    product_id = input("Enter product ID: ").strip()

    for product in products:
        if product["id"] == product_id:
            try:
                quantity = int(input("Enter quantity to add: "))

                if quantity <= 0:
                    print("Quantity must be positive.")
                    return

                product["stock"] += quantity
                save_products(products)
                print("Stock updated successfully.")
            except ValueError:
                print("Enter a valid quantity.")
            return

    print("Product not found.")


def sell_product(products):
    product_id = input("Enter product ID: ").strip()

    for product in products:
        if product["id"] == product_id:
            try:
                quantity = int(input("Enter quantity to sell: "))

                if quantity <= 0:
                    print("Quantity must be positive.")
                elif quantity > product["stock"]:
                    print("Not enough stock available.")
                else:
                    product["stock"] -= quantity
                    total = quantity * product["price"]

                    save_products(products)
                    print(f"Sale successful! Total: Rs. {total:.2f}")
            except ValueError:
                print("Enter a valid quantity.")
            return

    print("Product not found.")


def low_stock(products):
    print("\n--- LOW STOCK PRODUCTS ---")
    found = False

    for product in products:
        if product["stock"] <= 5:
            print(f"{product['name']} - Only {product['stock']} left")
            found = True

    if not found:
        print("No low-stock products.")


def main():
    products = load_products()

    while True:
        print("\n===== INVENTORY MANAGEMENT =====")
        print("1. View Products")
        print("2. Add Product")
        print("3. Add Stock")
        print("4. Sell Product")
        print("5. Check Low Stock")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            display_products(products)
        elif choice == "2":
            add_product(products)
        elif choice == "3":
            update_stock(products)
        elif choice == "4":
            sell_product(products)
        elif choice == "5":
            low_stock(products)
        elif choice == "6":
            print("Inventory system closed.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
