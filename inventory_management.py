import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()

def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?', (name, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    rows = c.fetchall()
    conn.close()
    return rows

def get_low_stock_alert(threshold):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE quantity < ?', (threshold,))
    rows = c.fetchall()
    conn.close()
    return rows

# GUI Setup
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.init_ui()

    def init_ui(self):
        # Create buttons for functionalities
        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_button.pack(pady=10)

        self.edit_button = tk.Button(self.root, text="Edit Product", command=self.edit_product)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_button.pack(pady=10)

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.pack(pady=10)

    def add_product(self):
        name = simpledialog.askstring("Input", "Product Name:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        price = simpledialog.askfloat("Input", "Price:")
        if name and quantity is not None and price is not None:
            add_product(name, quantity, price)
            messagebox.showinfo("Info", "Product added successfully!")
        else:
            messagebox.showwarning("Warning", "Invalid input!")

    def edit_product(self):
        product_id = simpledialog.askinteger("Input", "Enter Product ID to Edit:")
        product = self.get_product_by_id(product_id)
        if product:
            name = simpledialog.askstring("Input", "New Product Name:", initialvalue=product[1])
            quantity = simpledialog.askinteger("Input", "New Quantity:", initialvalue=product[2])
            price = simpledialog.askfloat("Input", "New Price:", initialvalue=product[3])
            if name and quantity is not None and price is not None:
                update_product(product_id, name, quantity, price)
                messagebox.showinfo("Info", "Product updated successfully!")
            else:
                messagebox.showwarning("Warning", "Invalid input!")
        else:
            messagebox.showwarning("Warning", "Product not found!")

    def delete_product(self):
        product_id = simpledialog.askinteger("Input", "Enter Product ID to Delete:")
        if product_id:
            delete_product(product_id)
            messagebox.showinfo("Info", "Product deleted successfully!")

    def generate_report(self):
        threshold = simpledialog.askinteger("Input", "Low Stock Threshold:")
        if threshold:
            low_stock_products = get_low_stock_alert(threshold)
            report = "\n".join([f"ID: {p[0]}, Name: {p[1]}, Quantity: {p[2]}, Price: ${p[3]:.2f}" for p in low_stock_products])
            if report:
                messagebox.showinfo("Low Stock Report", report)
            else:
                messagebox.showinfo("Low Stock Report", "No items below the threshold.")

    def get_product_by_id(self, product_id):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = c.fetchone()
        conn.close()
        return product

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
