import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from models import Makanan, Transaksi
from tkinter import Button

# Set tema dan warna default
ctk.set_appearance_mode("light")  # Mode: dark, light
ctk.set_default_color_theme("blue")  # Tema: blue, dark-blue, green

# Fetch data menu dari API
def fetch_menu():
    response = requests.get("http://127.0.0.1:5000/menu")
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Gagal mengambil data menu dari server.")
        return []

# Aplikasi GUI
class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Restoran Khas Indonesia")
        self.root.geometry("1200x800")
        self.transaksi = Transaksi()
        self.pesanan_count = {}  # Untuk menyimpan jumlah pesanan per item

        # Frame utama
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Frame untuk tombol aksi di bagian atas
        self.action_frame = ctk.CTkFrame(self.main_frame)
        self.action_frame.pack(fill="x", padx=10, pady=5)

        # Tombol tambah ke pesanan di atas
        ctk.CTkButton(
            self.action_frame,
            text="Tambah ke Pesanan",
            command=self.tambah_ke_pesanan,
            font=ctk.CTkFont(size=14),
            height=40
        ).pack(side="left", padx=5)

        # Tombol Checkout di atas
        ctk.CTkButton(
            self.action_frame,
            text="Checkout",
            command=self.checkout,
            font=ctk.CTkFont(size=14),
            height=40
        ).pack(side="left", padx=5)

        # Frame untuk konten (menu dan pesanan)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame untuk Daftar Menu (kiri)
        self.menu_frame = ctk.CTkFrame(self.content_frame)
        self.menu_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        # Label judul dengan styling
        ctk.CTkLabel(
            self.menu_frame, 
            text="Daftar Menu", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=15)

        # Frame untuk gambar menu
        self.image_frame = ctk.CTkFrame(self.menu_frame)
        self.image_frame.pack(pady=10)
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.pack()

        # Tabel menu dengan styling
        self.menu_tree = ttk.Treeview(
            self.menu_frame, 
            columns=("id", "nama", "harga", "deskripsi"), 
            show="headings",
            style="Custom.Treeview"
            
        )
        
        # Styling treeview
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="black",
            fieldbackground="white",
            rowheight=30,
            font=('Arial', 12)  # Font size besar
        )
        style.configure(
            "Custom.Treeview.Heading",
            relief="flat",
            background="white", 
            foreground="black",
            fieldbackground="white",
            font=('Arial', 12, 'bold')  # Font size besar untuk heading
        )
        style.map("Custom.Treeview", background=[("selected", "#1f538d")])

        self.menu_tree.heading("id", text="ID", anchor="center")
        self.menu_tree.heading("nama", text="Nama", anchor="center")
        self.menu_tree.heading("harga", text="Harga", anchor="center")
        self.menu_tree.heading("deskripsi", text="Deskripsi", anchor="center")
        self.menu_tree.column("id", width=50, anchor="center")
        self.menu_tree.column("nama", width=200, anchor="center")
        self.menu_tree.column("harga", width=100, anchor="center")
        self.menu_tree.column("deskripsi", width=250, anchor="center")
        self.menu_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.menu_tree.bind('<<TreeviewSelect>>', self.tampilkan_gambar)

        # Frame untuk Pesanan (kanan)
        self.order_frame = ctk.CTkFrame(self.content_frame)
        self.order_frame.pack(side="right", fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(
            self.order_frame,
            text="Pesanan Anda",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=15)

        # Tabel pesanan
        self.pesanan_tree = ttk.Treeview(
            self.order_frame,
            columns=("nama", "jumlah", "harga"),
            show="headings",
            style="Custom.Treeview"
        )
        self.pesanan_tree.heading("nama", text="Nama", anchor="center")
        self.pesanan_tree.heading("jumlah", text="Jumlah", anchor="center")
        self.pesanan_tree.heading("harga", text="Harga", anchor="center")
        self.pesanan_tree.column("nama", width=200, anchor="center")
        self.pesanan_tree.column("jumlah", width=100, anchor="center")
        self.pesanan_tree.column("harga", width=100, anchor="center")
        self.pesanan_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame untuk total
        self.total_frame = ctk.CTkFrame(self.order_frame)
        self.total_frame.pack(fill="x", padx=10, pady=10)

        # Label total harga
        self.total_label = ctk.CTkLabel(
            self.total_frame,
            text="Total: Rp0",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.total_label.pack(side="left", padx=20)

        # Dictionary untuk menyimpan data menu
        self.menu_data = {}

        # Load menu
        self.load_menu()

    def load_menu(self):
        menu = fetch_menu()
        for item in menu:
            self.menu_data[item["id"]] = item
            self.menu_tree.insert("", "end", values=(item["id"], item["nama"], item["harga"], item["deskripsi"]))

    def tampilkan_gambar(self, event):
        selected_item = self.menu_tree.focus()
        if selected_item:
            item_data = self.menu_tree.item(selected_item, "values")
            menu_id = int(item_data[0])
            foto_path = self.menu_data[menu_id]["foto"]
            
            try:
                image = Image.open(f"images/{foto_path}")
                image = image.resize((300, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_label.configure(image=None)

    def tambah_ke_pesanan(self):
        selected_item = self.menu_tree.focus()
        if selected_item:
            item_data = self.menu_tree.item(selected_item, "values")
            item_id = item_data[0]
            nama, harga = item_data[1], int(item_data[2])
            
            # Cek apakah item sudah ada di pesanan
            if item_id in self.pesanan_count:
                # Update jumlah dan tampilan
                self.pesanan_count[item_id]["jumlah"] += 1
                jumlah = self.pesanan_count[item_id]["jumlah"]
                total_harga = harga * jumlah
                
                # Update tampilan di treeview
                for item in self.pesanan_tree.get_children():
                    if self.pesanan_tree.item(item)["values"][0] == nama:
                        self.pesanan_tree.item(item, values=(nama, jumlah, total_harga))
                        break
            else:
                # Tambah item baru
                menu_item = Makanan(item_id, nama, "", harga, "")
                self.transaksi.tambah_pesanan(menu_item)
                self.pesanan_count[item_id] = {
                    "jumlah": 1,
                    "harga": harga
                }
                self.pesanan_tree.insert("", "end", values=(nama, 1, harga))
            
            self.update_total()
        else:
            messagebox.showwarning("Peringatan", "Pilih menu terlebih dahulu!")

    def update_total(self):
        total = sum(item["jumlah"] * item["harga"] for item in self.pesanan_count.values())
        self.total_label.configure(text=f"Total: Rp{total:,}")

    def checkout(self):
        if self.transaksi.hitung_total() > 0:
            struk_window = ctk.CTkToplevel(self.root)
            struk_window.title("Struk Pembelian")
            struk_window.geometry("400x500")

            ctk.CTkLabel(
                struk_window,
                text="Struk Pembelian",
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=20)

            pesanan_frame = ctk.CTkFrame(struk_window)
            pesanan_frame.pack(fill="both", expand=True, padx=20, pady=10)

            total = 0
            for item_id, data in self.pesanan_count.items():
                nama = next(item["nama"] for item in self.menu_data.values() if str(item["id"]) == item_id)
                subtotal = data["jumlah"] * data["harga"]
                total += subtotal
                ctk.CTkLabel(
                    pesanan_frame,
                    text=f"{nama} x{data['jumlah']} - Rp{subtotal:,}",
                    font=ctk.CTkFont(size=14)
                ).pack(anchor="w", pady=5)

            ctk.CTkLabel(
                struk_window,
                text=f"Total: Rp{total:,}",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=20)

            ctk.CTkButton(
                struk_window,
                text="Tutup",
                command=struk_window.destroy,
                font=ctk.CTkFont(size=14),
                height=40
            ).pack(pady=20)

            # Reset pesanan
            self.transaksi = Transaksi()
            self.pesanan_count = {}
            self.pesanan_tree.delete(*self.pesanan_tree.get_children())
            self.update_total()
        else:
            messagebox.showwarning("Peringatan", "Belum ada pesanan yang dibuat.")

# Main program
if __name__ == "__main__":
    root = ctk.CTk()
    app = RestaurantApp(root)
    root.mainloop()
