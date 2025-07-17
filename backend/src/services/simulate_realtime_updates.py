import sqlite3
import random
import time

DB_PATH = "e-commerce-data/olist.sqlite/olist.sqlite"

# Value ranges for simulation
def random_price():
    return round(random.uniform(10, 500), 2)

def random_discount():
    return round(random.uniform(0, 50), 2)  # up to 50% discount

def random_in_stock():
    return random.randint(0, 1)  # 0 = out of stock, 1 = in stock

def update_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]
    for pid in product_ids:
        price = random_price()
        discount = random_discount()
        in_stock = random_in_stock()
        cursor.execute(
            "UPDATE products SET current_price=?, discount_percent=?, in_stock=? WHERE product_id=?",
            (price, discount, in_stock, pid)
        )
    conn.commit()
    conn.close()
    print(f"Updated {len(product_ids)} products with new simulated values.")

def run_periodic_updates(interval_sec=10):
    while True:
        update_products()
        time.sleep(interval_sec)

if __name__ == "__main__":
    print("Starting real-time simulation of product data...")
    run_periodic_updates() 