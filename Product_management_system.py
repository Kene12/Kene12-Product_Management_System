import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime
import requests

class ProductManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management System")
        if not os.path.exists("products.txt"):
            with open("products.txt", "w", encoding="utf-8") as file:
                file.write("")
        if not os.path.exists("category.txt"):
            # Add default categories to the category.txt file
            default_categories = ["Electronics", "Clothing", "Books", "Food", "Toys", "Sports"]
            with open("category.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(default_categories))
        
        # Create images directory if not exists
        if not os.path.exists("images"):
            os.makedirs("images")
        
        self.initialize_ui()

    def initialize_ui(self):

        try:
            with open("category.txt", "r", encoding="utf-8") as cat_file:
                categories = cat_file.read().splitlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "Categories file not found.")
            categories = []

        # Frame for input fields
        self.frame_input = tk.Frame(self.root)
        self.frame_input.pack(padx=50, pady=10)

        # Labels and entry fields
        tk.Label(self.frame_input, text="Product ID:").grid(row=0, column=0, sticky="w")
        self.entry_product_id = tk.Entry(self.frame_input)
        self.entry_product_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frame_input, text="Name Product:").grid(row=1, column=0, sticky="w")
        self.entry_name = tk.Entry(self.frame_input)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frame_input, text="Price Product:").grid(row=2, column=0, sticky="w")
        self.entry_price = tk.Entry(self.frame_input)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frame_input, text="Product Description:").grid(row=3, column=0, sticky="w")
        self.text_description = tk.Text(self.frame_input, width=30, height=5)
        self.text_description.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frame_input, text="Stock Quantity:").grid(row=4, column=0, sticky="w")
        self.entry_stock_quantity = tk.Entry(self.frame_input)
        self.entry_stock_quantity.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frame_input, text="Category:").grid(row=5, column=0, sticky="w")
        self.selected_category = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.frame_input, textvariable=self.selected_category, values=categories)
        self.category_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.entry_search = tk.Entry(self.frame_input)
        self.entry_search.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        # Treeview widget to display products in a table format
        self.tree = ttk.Treeview(self.frame_input, columns=("Product ID", "Name", "Price", "Product Description", "Stock Quantity", "Category", "Date Added", "Last Updated"), show="headings")
        self.tree.grid(row=7, column=0, columnspan=4, rowspan=6, pady=1)

        # Define columns
        self.tree.heading("Product ID", text="Product ID", anchor="center")
        self.tree.column("Product ID", width=100, anchor="center")

        self.tree.heading("Name", text="Name", anchor="center")
        self.tree.column("Name", width=150, anchor="center")

        self.tree.heading("Price", text="Price", anchor="center")
        self.tree.column("Price", width=100, anchor="center")

        self.tree.heading("Product Description", text="Product Description", anchor="center")
        self.tree.column("Product Description", width=200, anchor="center")

        self.tree.heading("Stock Quantity", text="Stock Quantity", anchor="center")
        self.tree.column("Stock Quantity", width=100, anchor="center")

        self.tree.heading("Category", text="Category", anchor="center")
        self.tree.column("Category", width=100, anchor="center")

        self.tree.heading("Date Added", text="Date Added", anchor="center")
        self.tree.column("Date Added", width=150, anchor="center")

        self.tree.heading("Last Updated", text="Last Updated", anchor="center")
        self.tree.column("Last Updated", width=150, anchor="center")

        # Buttons for operations
        self.button_add = tk.Button(self.frame_input, text="Add Product", command=self.add_product)
        self.button_add.grid(row=7, column=4, padx=0, pady=0)

        self.button_edit = tk.Button(self.frame_input, text="Edit Product", command=self.edit_product)
        self.button_edit.grid(row=8, column=4, padx=0, pady=0)

        self.button_delete = tk.Button(self.frame_input, text="Delete Product", command=self.delete_product)
        self.button_delete.grid(row=9, column=4, padx=0, pady=0)

        self.button_select = tk.Button(self.frame_input, text="Select Product", command=self.select_product)
        self.button_select.grid(row=10, column=4, padx=0, pady=0)
        
        self.button_clear_all = tk.Button(self.frame_input, text="Clear All", command=self.clear)
        self.button_clear_all.grid(row=11, column=4, padx=0, pady=0)

        # Button for adding image
        self.button_add_image = tk.Button(self.frame_input, text="Add Image", command=self.add_image)
        self.button_add_image.grid(row=0, column=4, columnspan=2, pady=5)

        # Button for managing categories
        self.button_manage_categories = tk.Button(self.frame_input, text="Manage Categories", command=self.manage_categories)
        self.button_manage_categories.grid(row=12, column=4, padx=5, pady=5, sticky="w")

        self.button_search = tk.Button(self.frame_input, text="Search", command=self.search_product)
        self.button_search.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Label to display image
        self.image_label = tk.Label(self.frame_input)
        self.image_label.grid(row=0, column=2, columnspan=2, rowspan=6, pady=5)

        # Initialize images
        self.initialize_images()

        # Display initial image
        initial_image_path = os.path.join("images", "empty_image.jpg")
        self.display_image(initial_image_path)

        # Load products from file
        self.load_products()

    def initialize_images(self):
        # URL of the image to download
        image_url = "https://cdn.discordapp.com/attachments/795709879234854932/1211785714568798228/icon.ico?ex=65ef7664&is=65dd0164&hm=72ae87a0c7de371617c8e0ca2feb4f7fa90847969c07396eff3196ec1d64a116&"
        image_url2 = "https://cdn.discordapp.com/attachments/795709879234854932/1211786700506931221/empty_image.jpg?ex=65ef774f&is=65dd024f&hm=b0b65a87aec207690c4ef22d9a84b7a5ddd940c7c116467113dea1534869f54d&"
        target_folder = "images"
        target_path = os.path.join(target_folder, "icon.ico")
        target_path2 = os.path.join(target_folder, "empty_image.jpg")

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save the image file to the 'images' folder
            with open(target_path, 'wb') as f:
                f.write(response.content)
        response = requests.get(image_url2)
        if response.status_code == 200:
            # Save the image file to the 'images' folder
            with open(target_path2, 'wb') as f:
                f.write(response.content)

    def add_product(self):
         product_id = self.entry_product_id.get()
         name = self.entry_name.get()
         price = self.entry_price.get()
         description = self.text_description.get("1.0", "end-1c")
         stock_quantity = self.entry_stock_quantity.get()
         category = self.selected_category.get()
         date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         last_updated = ""

         if product_id and name and price and description and stock_quantity and category:
             image_path = ""  # Default to empty string if image path is not set
             if hasattr(self, 'image_path'):
                 image_path = self.image_path
                 # Clear the attribute to prevent reusing the same path
                 delattr(self, 'image_path')

             if image_path and os.path.exists(image_path):
                 # Copy the image file to the 'images' folder
                 image_filename = os.path.basename(image_path)
                 target_folder = "images"
                 if not os.path.exists(target_folder):
                     os.makedirs(target_folder)
                 target_path = os.path.join(target_folder, image_filename)
                 shutil.copy(image_path, target_path)
                 image_path = target_path

             with open("products.txt", "a", encoding="utf-8") as file:
                 file.write(f"{product_id},{name},{price},{description},{stock_quantity},{category},{date_added},{last_updated},{image_path}\n")

             self.tree.insert("", tk.END, values=(product_id, name, price, description, stock_quantity, category, date_added, last_updated, image_path))
             self.clear_entries()
             self.clear_image()  # Clear image after adding product
             self.display_image("images/empty_image.jpg")
             self.category_dropdown.set("")
         else:
             messagebox.showerror("Error", "Please fill in all fields.")

    def edit_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to edit.")
            return

        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        old_product_id = values[0]

        # Retrieve new product information from the entry fields
        new_product_id = self.entry_product_id.get()
        new_name = self.entry_name.get()
        new_price = self.entry_price.get()
        new_description = self.text_description.get("1.0", "end-1c")  # Get text from the Text widget
        new_stock_quantity = self.entry_stock_quantity.get()
        new_category = self.selected_category.get()  # Get selected category
        new_date_added = values[6]
        new_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not new_product_id or not new_name or not new_price or not new_description or not new_stock_quantity or not new_category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Retrieve the existing image path
        old_image_path = values[8]

        # Check if a new image is selected
        if hasattr(self, 'image_path'):
            new_image_path = self.image_path  # Get the new image path
            if old_image_path and old_image_path != "images/empty_image.jpg":
                if os.path.exists(old_image_path):  # Check if old image still exists
                    os.remove(old_image_path)  # Delete the old image if it exists
                else:
                    old_image_path = ""  # If old image does not exist, treat as if it's empty

            # Copy the new image file to the 'images' folder
            if os.path.exists(new_image_path):
                image_filename = os.path.basename(new_image_path)
                target_folder = "images"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                target_path = os.path.join(target_folder, image_filename)
                shutil.copy(new_image_path, target_path)
                new_image_path = target_path

            # Clear the attribute to prevent reusing the same path
            delattr(self, 'image_path')

        else:
            new_image_path = old_image_path  # Keep the existing image path if no new image is selected

        # Update product information in the Treeview
        self.tree.item(item, values=(new_product_id, new_name, new_price, new_description, new_stock_quantity, new_category, new_date_added, new_last_updated, new_image_path))

        # Update product information in the products.txt file
        with open("products.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open("products.txt", "w", encoding="utf-8") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == old_product_id:
                    file.write(f"{new_product_id},{new_name},{new_price},{new_description},{new_stock_quantity},{new_category},{new_date_added},{new_last_updated},{new_image_path}\n")
                else:
                    file.write(line)

        # Clear entries and display empty image after editing
        self.clear_entries()
        self.clear_image()
        self.display_image("images/empty_image.jpg")
        self.category_dropdown.set("")


    def delete_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        product_id = values[0]

        # Delete the product from the Treeview
        self.tree.delete(item)

        # Remove the product from the products.txt file
        with open("products.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open("products.txt", "w", encoding="utf-8") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[0] != product_id:
                    file.write(line)
                else:
                    # Delete the image file associated with the product
                    image_path = data[-1]
                    if image_path and image_path != "images/empty_image.jpg":
                        if os.path.exists(image_path):
                            os.remove(image_path)

        messagebox.showinfo("Success", "Product deleted successfully.")

    def select_product(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product.")
            return

        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")

        # Set values of entry fields to selected product's information
        self.entry_product_id.delete(0, tk.END)
        self.entry_product_id.insert(tk.END, values[0])

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(tk.END, values[1])

        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(tk.END, values[2])

        self.text_description.delete("1.0", tk.END)
        self.text_description.insert(tk.END, values[3])

        self.entry_stock_quantity.delete(0, tk.END)
        self.entry_stock_quantity.insert(tk.END, values[4])

        self.category_dropdown.set(values[5])

        # Display selected product's image
        image_path = values[8] if values[8] else "images/empty_image.jpg"
        self.display_image(image_path)

    def clear_entries(self):
        self.entry_product_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.text_description.delete("1.0", tk.END)
        self.entry_stock_quantity.delete(0, tk.END)
        self.category_dropdown.set("")

    def add_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])

        if file_path:
            self.image_path = file_path
            self.display_image(file_path)

    def display_image(self, path):
        # Open the image file
        image = Image.open(path)
        # Resize the image
        image = image.resize((200, 200))
        # Convert image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(image)
        # Update the image label
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to the image to prevent garbage collection

    def clear_image(self):
        # Clear the image label
        self.image_label.configure(image="")

    def search_product(self):
        search_query = self.entry_search.get().lower()

        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load products from file
        with open("products.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(",")
                if search_query in ",".join(data).lower():
                    self.tree.insert("", tk.END, values=data)

    def load_products(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load products from file
        with open("products.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(",")
                self.tree.insert("", tk.END, values=data)

    def clear(self):
        self.clear_entries()
        self.clear_image()
        self.display_image("images/empty_image.jpg")
        self.category_dropdown.set("")

    def manage_categories(self):
        # Open a new window for managing categories
        category_window = tk.Toplevel(self.root)
        category_window.title("Manage Categories")

        # Load categories from file
        try:
            with open("category.txt", "r", encoding="utf-8") as cat_file:
                categories = cat_file.read().splitlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "Categories file not found.")
            categories = []

        def save_categories():
            # Save categories to file
            with open("category.txt", "w", encoding="utf-8") as cat_file:
                cat_file.write("\n".join(category_listbox.get(0, tk.END)))

            # Update values in the main application
            self.category_dropdown.config(values=category_listbox.get(0, tk.END))
            self.category_dropdown.set("")  # Clear selection

            # Close the category management window
            category_window.destroy()

        def add_category():
            new_category = simpledialog.askstring("Add Category", "Enter new category:")
            if new_category:
                category_listbox.insert(tk.END, new_category)

        def edit_category():
            selection = category_listbox.curselection()
            if selection:
                index = selection[0]
                old_category = category_listbox.get(index)
                new_category = simpledialog.askstring("Edit Category", f"Edit category \"{old_category}\":", initialvalue=old_category)
                if new_category:
                    category_listbox.delete(index)
                    category_listbox.insert(index, new_category)

        def delete_category():
            selection = category_listbox.curselection()
            if selection:
                index = selection[0]
                category_listbox.delete(index)

        # Create a listbox to display categories
        category_listbox = tk.Listbox(category_window, selectmode=tk.SINGLE)
        category_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate the listbox with categories
        for category in categories:
            category_listbox.insert(tk.END, category)

        # Buttons for managing categories
        button_add = tk.Button(category_window, text="Add", command=add_category)
        button_add.pack(side=tk.LEFT, padx=5, pady=5)

        button_edit = tk.Button(category_window, text="Edit", command=edit_category)
        button_edit.pack(side=tk.LEFT, padx=5, pady=5)

        button_delete = tk.Button(category_window, text="Delete", command=delete_category)
        button_delete.pack(side=tk.LEFT, padx=5, pady=5)

        button_save = tk.Button(category_window, text="Save", command=save_categories)
        button_save.pack(side=tk.RIGHT, padx=5, pady=5)
        
# Create the main application window
root = tk.Tk()
app = ProductManagementApp(root)
root.mainloop()