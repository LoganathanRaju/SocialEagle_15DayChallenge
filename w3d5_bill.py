import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os

class RestaurantBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spice Garden - Indian Restaurant Billing System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        # Updated color scheme with more visible buttons
        self.colors = {
            "primary": "#d32f2f",  # Red
            "secondary": "#ffa000",  # Amber
            "accent": "#388e3c",  # Green
            "background": "#f5f5f5",
            "text": "#212121",
            "light_text": "#757575",
            "header_bg": "#d32f2f",
            "header_fg": "white",
            "button_bg": "#ff5722",  # Bright orange for better visibility
            "button_fg": "white",
            "button_hover": "#e64a19",  # Darker orange for hover
            "menu_button_bg": "#4caf50",  # Green for menu buttons
            "menu_button_fg": "white",
            "menu_button_hover": "#388e3c",  # Darker green for menu buttons hover
            "tree_header_bg": "#e0e0e0",
            "tree_odd_row": "#f5f5f5",
            "tree_even_row": "#eeeeee"
        }
        
        # Menu items with prices in SGD
        self.menu_items = {
            "Starters": {
                "Samosa (2 pcs)": 5.90,
                "Paneer Tikka": 8.90,
                "Chicken 65": 9.90,
                "Vegetable Pakora": 6.50,
                "Aloo Tikki": 5.50
            },
            "Main Course - Vegetarian": {
                "Paneer Butter Masala": 15.90,
                "Palak Paneer": 14.90,
                "Chana Masala": 12.90,
                "Dal Makhani": 13.50,
                "Mixed Vegetable Curry": 12.50,
                "Malai Kofta": 16.50
            },
            "Main Course - Non-Vegetarian": {
                "Butter Chicken": 18.90,
                "Chicken Tikka Masala": 17.90,
                "Lamb Rogan Josh": 21.90,
                "Fish Curry": 19.50,
                "Chicken Biryani": 16.90,
                "Mutton Biryani": 22.50
            },
            "Breads & Rice": {
                "Garlic Naan": 4.50,
                "Butter Naan": 3.90,
                "Tandoori Roti": 3.50,
                "Plain Rice": 4.50,
                "Jeera Rice": 5.50,
                "Kashmiri Pulao": 8.90
            },
            "Desserts": {
                "Gulab Jamun (2 pcs)": 6.50,
                "Rasmalai": 7.50,
                "Kheer": 5.90,
                "Mango Lassi": 5.50,
                "Masala Chai": 3.50
            },
            "Beverages": {
                "Mango Lassi": 5.50,
                "Sweet Lassi": 4.50,
                "Salted Lassi": 4.50,
                "Masala Chai": 3.50,
                "Fresh Lime Juice": 4.50,
                "Mineral Water": 2.50
            }
        }
        
        self.current_order = {}
        self.tax_rate = 0.09  # 9% GST for Singapore
        self.currency = "SGD"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for widgets
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabel", background=self.colors["background"], foreground=self.colors["text"])
        style.configure("Header.TLabel", background=self.colors["header_bg"], foreground=self.colors["header_fg"], font=("Arial", 16, "bold"))
        style.configure("Title.TLabel", background=self.colors["background"], foreground=self.colors["primary"], font=("Arial", 18, "bold"))
        style.configure("Subtitle.TLabel", background=self.colors["background"], foreground=self.colors["secondary"], font=("Arial", 12, "italic"))
        
        # Configure button styles
        style.configure("Action.TButton", 
                       background=self.colors["button_bg"],
                       foreground=self.colors["button_fg"],
                       font=("Arial", 10, "bold"),
                       padding=(10, 5))
        style.map("Action.TButton", 
                 background=[('active', self.colors["button_hover"])])
        
        style.configure("Menu.TButton", 
                       background=self.colors["menu_button_bg"],
                       foreground=self.colors["menu_button_fg"],
                       font=("Arial", 9, "bold"),
                       padding=(5, 3))
        style.map("Menu.TButton", 
                 background=[('active', self.colors["menu_button_hover"])])
        
        style.configure("Treeview", 
                        background=self.colors["tree_odd_row"],
                        foreground=self.colors["text"],
                        fieldbackground=self.colors["tree_odd_row"])
        style.configure("Treeview.Heading", 
                        background=self.colors["tree_header_bg"],
                        foreground=self.colors["text"],
                        font=("Arial", 10, "bold"))
        style.map("Treeview", background=[('selected', self.colors["primary"])])
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Restaurant header
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(0, weight=1)
        
        ttk.Label(header_frame, text="Spice Garden", style="Title.TLabel").grid(row=0, column=0, pady=5)
        ttk.Label(header_frame, text="Authentic Indian Cuisine", style="Subtitle.TLabel").grid(row=1, column=0, pady=(0, 10))
        
        # Menu section
        menu_frame = ttk.LabelFrame(main_frame, text="Menu", padding="10")
        menu_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=5)
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.rowconfigure(0, weight=1)
        
        # Create notebook for menu categories
        notebook = ttk.Notebook(menu_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create frames for each category
        self.category_frames = {}
        for category in self.menu_items:
            frame = ttk.Frame(notebook, padding="10")
            notebook.add(frame, text=category)
            self.category_frames[category] = frame
            self.populate_category(frame, category)
            frame.columnconfigure(0, weight=1)
        
        # Order section
        order_frame = ttk.LabelFrame(main_frame, text="Current Order", padding="10")
        order_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=5)
        order_frame.columnconfigure(0, weight=1)
        order_frame.rowconfigure(0, weight=1)
        order_frame.rowconfigure(2, weight=1)
        
        # Selected item display
        selected_frame = ttk.Frame(order_frame)
        selected_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        selected_frame.columnconfigure(1, weight=1)
        
        ttk.Label(selected_frame, text="Selected Item:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.selected_item_var = tk.StringVar(value="No item selected")
        ttk.Label(selected_frame, textvariable=self.selected_item_var, foreground=self.colors["primary"], 
                 font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Quantity controls
        quantity_frame = ttk.Frame(order_frame)
        quantity_frame.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(quantity_frame, text="Quantity:", font=("Arial", 10)).grid(row=0, column=0)
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(quantity_frame, from_=1, to=20, textvariable=self.quantity_var, width=8)
        quantity_spinbox.grid(row=0, column=1, padx=5)
        
        # Order treeview with improved column alignment
        tree_frame = ttk.Frame(order_frame)
        tree_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        columns = ("Item", "Quantity", "Price", "Total")
        self.order_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure column widths and alignment
        self.order_tree.column("Item", width=220, anchor=tk.W)
        self.order_tree.column("Quantity", width=80, anchor=tk.CENTER)
        self.order_tree.column("Price", width=100, anchor=tk.E)
        self.order_tree.column("Total", width=100, anchor=tk.E)
        
        for col in columns:
            self.order_tree.heading(col, text=col)
        
        # Scrollbar for order tree
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=scrollbar.set)
        
        self.order_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bill summary
        bill_frame = ttk.Frame(order_frame, style="TFrame")
        bill_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(bill_frame, text="Subtotal:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        self.subtotal_var = tk.StringVar(value=f"{self.currency} 0.00")
        ttk.Label(bill_frame, textvariable=self.subtotal_var, font=("Arial", 10)).grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        
        ttk.Label(bill_frame, text="GST (9%):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W)
        self.tax_var = tk.StringVar(value=f"{self.currency} 0.00")
        ttk.Label(bill_frame, textvariable=self.tax_var, font=("Arial", 10)).grid(row=1, column=1, sticky=tk.E, padx=(10, 0))
        
        ttk.Label(bill_frame, text="Total:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.total_var = tk.StringVar(value=f"{self.currency} 0.00")
        ttk.Label(bill_frame, textvariable=self.total_var, font=("Arial", 12, "bold"), 
                 foreground=self.colors["primary"]).grid(row=2, column=1, sticky=tk.E, padx=(10, 0), pady=(5, 0))
        
        # Buttons with improved visibility
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Add to Order", command=self.add_to_order, 
                  style="Action.TButton", width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_from_order, 
                  style="Action.TButton", width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Order", command=self.clear_order, 
                  style="Action.TButton", width=15).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Generate PDF Invoice", command=self.generate_pdf, 
                  style="Action.TButton", width=18).grid(row=0, column=3, padx=5, pady=5)
        
        # Configure weights for resizing
        menu_frame.rowconfigure(0, weight=1)
        menu_frame.columnconfigure(0, weight=1)
        order_frame.rowconfigure(2, weight=1)
        order_frame.columnconfigure(0, weight=1)
        
    def populate_category(self, frame, category):
        row = 0
        col = 0
        max_cols = 2  # Number of columns for menu items
        
        for item, price in self.menu_items[category].items():
            # Use ttk buttons for better styling consistency
            btn = ttk.Button(frame, 
                           text=f"{item}\n{self.currency} {price:.2f}", 
                           style="Menu.TButton",
                           command=lambda i=item, p=price: self.select_item(i, p))
            btn.grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=3)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def select_item(self, item, price):
        self.selected_item = item
        self.selected_price = price
        self.selected_item_var.set(f"{item} - {self.currency} {price:.2f}")
        
    def add_to_order(self):
        if not hasattr(self, 'selected_item'):
            messagebox.showwarning("Warning", "Please select an item from the menu first!")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be at least 1!")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity!")
            return
        
        if self.selected_item in self.current_order:
            self.current_order[self.selected_item]['quantity'] += quantity
        else:
            self.current_order[self.selected_item] = {
                'price': self.selected_price,
                'quantity': quantity
            }
        
        self.update_order_display()
    
    def remove_from_order(self):
        selected_item = self.order_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return
        
        item = self.order_tree.item(selected_item[0])['values'][0]
        if item in self.current_order:
            del self.current_order[item]
            self.update_order_display()
    
    def clear_order(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the entire order?"):
            self.current_order = {}
            self.update_order_display()
    
    def update_order_display(self):
        # Clear current display
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # Add items to display with alternating row colors
        for i, (item, details) in enumerate(self.current_order.items()):
            total = details['price'] * details['quantity']
            tags = ('even',) if i % 2 == 0 else ('odd',)
            self.order_tree.insert("", "end", values=(
                item, details['quantity'], f"{self.currency} {details['price']:.2f}", f"{self.currency} {total:.2f}"
            ), tags=tags)
        
        # Configure tag colors
        self.order_tree.tag_configure('odd', background=self.colors["tree_odd_row"])
        self.order_tree.tag_configure('even', background=self.colors["tree_even_row"])
        
        # Update bill summary
        self.update_bill_summary()
    
    def update_bill_summary(self):
        subtotal = sum(details['price'] * details['quantity'] for details in self.current_order.values())
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        
        self.subtotal_var.set(f"{self.currency} {subtotal:.2f}")
        self.tax_var.set(f"{self.currency} {tax:.2f}")
        self.total_var.set(f"{self.currency} {total:.2f}")
    
    def generate_pdf(self):
        if not self.current_order:
            messagebox.showwarning("Warning", "No items in the order to generate invoice!")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Invoice As"
        )
        
        if not file_path:
            return
        
        try:
            # Create PDF with better formatting
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                alignment=1,  # Center aligned
                textColor=colors.HexColor(self.colors["primary"])
            )
            title = Paragraph("SPICE GARDEN", title_style)
            elements.append(title)
            
            # Add subtitle
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=20,
                alignment=1,
                textColor=colors.HexColor(self.colors["secondary"])
            )
            subtitle = Paragraph("Authentic Indian Cuisine", subtitle_style)
            elements.append(subtitle)
            
            # Add restaurant info
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=20,
                alignment=1
            )
            info_text = "123 Little India Road, Singapore 123456<br/>Tel: +65 6123 4567 | Email: info@spicegarden.sg"
            info = Paragraph(info_text, info_style)
            elements.append(info)
            
            # Add invoice title
            invoice_title_style = ParagraphStyle(
                'InvoiceTitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=20,
                alignment=0,  # Left aligned
                textColor=colors.HexColor(self.colors["primary"])
            )
            invoice_title = Paragraph("INVOICE", invoice_title_style)
            elements.append(invoice_title)
            
            # Add invoice details
            details_style = ParagraphStyle(
                'DetailsStyle',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=30
            )
            details_text = f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}<br/>Invoice #: SG{datetime.now().strftime('%Y%m%d%H%M%S')}"
            details = Paragraph(details_text, details_style)
            elements.append(details)
            
            # Create table data
            table_data = [['Item', 'Qty', 'Price', 'Total']]
            
            subtotal = 0
            for item, details in self.current_order.items():
                item_total = details['price'] * details['quantity']
                subtotal += item_total
                table_data.append([
                    item,
                    str(details['quantity']),
                    f"{self.currency} {details['price']:.2f}",
                    f"{self.currency} {item_total:.2f}"
                ])
            
            tax = subtotal * self.tax_rate
            total = subtotal + tax
            
            # Add summary rows
            table_data.append(['', '', 'Subtotal:', f"{self.currency} {subtotal:.2f}"])
            table_data.append(['', '', 'GST (9%):', f"{self.currency} {tax:.2f}"])
            table_data.append(['', '', 'Total:', f"{self.currency} {total:.2f}"])
            
            # Create table
            table = Table(table_data, colWidths=[280, 60, 80, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors["tree_header_bg"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -4), colors.white),
                ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -4), 10),
                ('BACKGROUND', (0, -3), (-1, -1), colors.HexColor('#f5f5f5')),
                ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
                ('LINEABOVE', (0, -3), (-1, -3), 1, colors.black),
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 30))
            
            # Add thank you message
            thanks_style = ParagraphStyle(
                'ThanksStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=10,
                alignment=1,
                textColor=colors.HexColor(self.colors["primary"])
            )
            thanks = Paragraph("Thank you for dining at Spice Garden!", thanks_style)
            elements.append(thanks)
            
            # Build PDF
            doc.build(elements)
            messagebox.showinfo("Success", f"Invoice saved as: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")

def main():
    root = tk.Tk()
    app = RestaurantBillingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()