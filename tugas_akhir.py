import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import shutil

# Kelas Senjata
class Senjata:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

# Kelas Pengguna
class Pengguna:
    def __init__(self, username, email, password, saldo, is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.saldo = saldo
        self.is_admin = is_admin
        self.senjata_dibeli = []  
        self.riwayat_pembelian = []

# Sistem Pembelian Senjata
class SistemPembelianSenjata:
    def __init__(self):
        self.pengguna_terdaftar = []
        self.senjata_tersedia = []
        self.load_users_from_file()  # Membaca pengguna dari file
        self.senjata_tersedia.extend([
            {"nama": "AK-47", "harga": 10, "gambar": "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\AK-47.png"},
            {"nama": "Desert Eagle", "harga": 5, "gambar": "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\Desert Eagle.png"},
            {"nama": "MP5", "harga": 7, "gambar": "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\MP5.png"},
            {"nama": "AWM", "harga": 20, "gambar": "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\AWM.png"},
            {"nama": "M4A1", "harga": 15, "gambar": "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\M4A1.png"}
        ])


    def register(self, username, email, password, saldo=0, is_admin=False):
        # Mengecek apakah username atau email sudah ada
        for pengguna in self.pengguna_terdaftar:
            if pengguna.username == username or pengguna.email == email:
                return False
        
        # Menambahkan pengguna baru
        new_user = Pengguna(username, email, password, saldo, is_admin)
        self.pengguna_terdaftar.append(new_user)
        self.save_users_to_file()  # Menyimpan pengguna ke file
        return True

    def login(self, username_or_email, password):
        for pengguna in self.pengguna_terdaftar:
            if (pengguna.username == username_or_email or pengguna.email == username_or_email) and pengguna.password == password:
                return pengguna
        return None

    def beli_senjata(self, pengguna, senjata):
        if pengguna.saldo >= senjata.harga:
            pengguna.saldo -= senjata.harga
            pengguna.senjata_dibeli.append(senjata)
            pengguna.riwayat_pembelian.append(senjata)  # Menambahkan senjata ke riwayat pembelian
            return True
        return False

    def tambah_senjata(self, nama, harga, gambar):
        senjata_baru = {"nama": nama, "harga": harga, "gambar": gambar}
        self.senjata_tersedia.append(senjata_baru)

    def isi_saldo(self, pengguna, jumlah):
        pengguna.saldo += jumlah

    def load_users_from_file(self):
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                for pengguna_data in data:
                    username = pengguna_data['username']
                    email = pengguna_data['email']
                    password = pengguna_data['password']
                    saldo = pengguna_data['saldo']
                    is_admin = pengguna_data['is_admin']
                    pengguna_dibuat = Pengguna(username, email, password, saldo, is_admin)

                    # Memasukkan senjata yang dibeli
                    senjata_dibeli_list = pengguna_data.get('senjata_dibeli', [])
                    for nama_senjata in senjata_dibeli_list:
                        senjata_obj = next((s for s in self.senjata_tersedia if s.nama == nama_senjata), None)
                        if senjata_obj:
                            pengguna_dibuat.senjata_dibeli.append(senjata_obj)
                    self.pengguna_terdaftar.append(pengguna_dibuat)
        except FileNotFoundError:
            with open("users.json", "w") as file:
                json.dump([], file)  # Create an empty JSON array if not found

    def save_users_to_file(self):
        try:
            data = []
            for pengguna in self.pengguna_terdaftar:
                senjata_dibeli_list = [senjata.nama for senjata in pengguna.senjata_dibeli]
                pengguna_data = {
                    'username': pengguna.username,
                    'email': pengguna.email,
                    'password': pengguna.password,
                    'saldo': pengguna.saldo,
                    'is_admin': pengguna.is_admin,
                    'senjata_dibeli': senjata_dibeli_list
                }
                data.append(pengguna_data)

            with open("users.json", "w") as file:
                json.dump(data, file, indent=4)  # Menyimpan data dalam format JSON dengan indentasi
        except Exception as e:
            print(f"Error saving user data: {e}")

# GUI Pembelian Senjata
class GUIPembelianSenjata:
    def __init__(self, root, sistem):
        self.root = root
        self.sistem = sistem
        self.current_user = None
        self.root.title("Sistem Pembelian Senjata")
        self.main_frame = tk.Frame(self.root, bg="#121212")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menunggu window selesai dimuat
        self.root.update_idletasks()
        
        # Inisialisasi background image setelah window dimuat
        self.update_background()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        
        # Menampilkan login frame setelah background siap
        self.root.after(100, self.login_frame)

    def update_background(self):
        # Memuat dan resize background image sesuai ukuran window
        self.bg_image = Image.open("C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\gunbg.jpg")
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        self.bg_image = self.bg_image.resize((window_width, window_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

    def on_resize(self, event):
        # Update background saat window diresize
        if event.widget == self.root:
            self.update_background()
            self.set_background()

    def set_background(self):
        # Hapus background lama jika ada
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Label) and hasattr(widget, 'is_background'):
                widget.destroy()
                
        # Tambah background baru
        bg_label = tk.Label(self.main_frame, image=self.bg_photo)
        bg_label.is_background = True  # Tandai sebagai background label
        bg_label.place(relwidth=1, relheight=1)
        
        # Pastikan background ada di belakang
        bg_label.lower()

    def login_frame(self):
        self.clear_frame()
        self.set_background()
        
        #Menampilkan 𝕯𝖎𝖕𝖘𝕲𝖚𝖓 𝕾𝖙𝖔𝖗𝖊 agar bisa kedap kedip
        self.toko_kedap_kedip = tk.Label(self.main_frame, text="𝕯𝖎𝖕𝖘𝕲𝖚𝖓 𝕾𝖙𝖔𝖗𝖊", font=("Arial", 50, "bold"), bg="#484848", fg="#39FF14")
        self.toko_kedap_kedip.pack(pady=(200,0))
        self.kedap_kedip_label(self.toko_kedap_kedip)

        tk.Label(self.main_frame, text="Login", font=("Arial", 24, "bold"), bg="#484848", fg="#39FF14").pack(pady=10)

        tk.Label(self.main_frame, text="Username / Email", bg="#484848", fg="#39FF14").pack(pady=(10, 0))
        self.username_or_email_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.username_or_email_entry.pack(pady=(0, 10))

        tk.Label(self.main_frame, text="Password", bg="#484848", fg="#39FF14").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.main_frame, show="*", bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.password_entry.pack(pady=(0, 10))

        tk.Button(self.main_frame, text="Login", command=self.login, width=10, bg="#39FF14", fg="#121212", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.main_frame, text="Register", command=self.register_frame, width=10, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

    def register_frame(self):
        self.clear_frame()
        self.set_background()

        self.toko_kedap_kedip = tk.Label(self.main_frame, text="𝕯𝖎𝖕𝖘𝕲𝖚𝖓 𝕾𝖙𝖔𝖗𝖊", font=("Arial", 50, "bold"), bg="#484848", fg="#39FF14")
        self.toko_kedap_kedip.pack(pady=(200,0))
        self.kedap_kedip_label(self.toko_kedap_kedip)

        tk.Label(self.main_frame, text="Register", font=("Arial", 24, "bold"), bg="#484848", fg="#39FF14").pack(pady=10)
        tk.Label(self.main_frame, text="Username", bg="#484848", fg="#39FF14").pack()
        self.username_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.username_entry.pack()
        tk.Label(self.main_frame, text="Email", bg="#484848", fg="#39FF14").pack()
        self.email_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.email_entry.pack()
        tk.Label(self.main_frame, text="Password", bg="#484848", fg="#39FF14").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*", bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.password_entry.pack(pady=(0,10))
        tk.Button(self.main_frame, text="Register", command=self.register, width=10, bg="#39FF14", fg="#121212", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Login", command=self.login_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

    def main_menu_frame(self):
        self.clear_frame()
        self.set_background()

        tk.Label(self.main_frame, text="𝕯𝖎𝖕𝖘𝕲𝖚𝖓 𝕾𝖙𝖔𝖗𝖊", font=("Arial", 50, "bold"), bg="#484848", fg="#39FF14").pack(pady=(150,0))

        tk.Label(self.main_frame, text=f"Hi 👋🏻, {self.current_user.username}", font=("Arial", 14), bg="#484848", fg="#39FF14").pack(pady=10)

        if self.current_user.is_admin:
            tk.Button(self.main_frame, text="Tambah Senjata", command=self.tambah_senjata_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Lihat Pengguna", command=self.lihat_pengguna_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Edit Saldo Pengguna", command=self.edit_saldo_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Lihat Senjata yang Dibeli", command=self.lihat_senjata_dibeli_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.main_frame, text="Lihat dan Beli Senjata", command=self.lihat_dan_beli_senjata_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

        if not self.current_user.is_admin:
            tk.Button(self.main_frame, text="Lihat Senjata yang Dibeli", command=self.lihat_senjata_dibeli_frame, width=20, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.main_frame, text="Logout", command=self.logout, width=10, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(side="left", anchor="w", padx=10, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def login(self):
        username_or_email = self.username_or_email_entry.get()
        password = self.password_entry.get()
        pengguna = self.sistem.login(username_or_email, password)
        if pengguna:
            self.current_user = pengguna
            self.main_menu_frame()
        else:
            messagebox.showerror("Error", "Username, email, atau password salah!")

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        is_admin = email.endswith('@admin.com')  # Menganggap email admin berakhiran @admin.com
        saldo = 0  # Saldo diatur 0 karena hanya admin yang bisa mengedit saldo

        # Validasi bahwa semua input harus terisi
        if not username or not email or not password:
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return

        if self.sistem.register(username, email, password, saldo, is_admin):
            messagebox.showinfo("Sukses", "Registrasi berhasil!")
            self.login_frame()
        else:
            messagebox.showerror("Error", "Username atau email sudah ada!")


    def lihat_dan_beli_senjata_frame(self):
        self.clear_frame()
        self.set_background()

        tk.Label(self.main_frame, text="𝕯𝖆𝖋𝖙𝖆𝖗 𝕾𝖊𝖓𝖏𝖆𝖙𝖆", font=("Arial", 50), bg="#484848", fg="#39FF14").pack(pady=(150,0))

        self.saldo_anda = tk.Label(self.main_frame, text=f"Saldo Anda: ${self.current_user.saldo}", font=("Arial", 14), bg="#484848", fg="#39FF14")
        self.saldo_anda.pack(pady=10)
        
        self.kedap_kedip_label(self.saldo_anda)
        
        senjata_container = tk.Frame(self.main_frame, bg="#121212")
        senjata_container.pack(pady=10)

        # Loop untuk setiap senjata
        for index, senjata in enumerate(self.sistem.senjata_tersedia):
            senjata_frame = tk.Frame(senjata_container, bg="#1c1c1c", bd=2, relief=tk.RAISED, padx=10, pady=10)
            senjata_frame.grid(row=index // 6, column=index % 6, padx=10, pady=10)

            try:
                # Memuat gambar
                image = Image.open(senjata['gambar'])
                image = image.resize((100, 100), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                img_label = tk.Label(senjata_frame, image=img, bg="#1c1c1c")
                img_label.image = img  # Menyimpan referensi gambar
                img_label.pack(pady=5)
            except Exception as e:
                print(f"Error loading image for {senjata['nama']}: {e}")
                img_label = tk.Label(senjata_frame, text="Image not found", bg="#1c1c1c", fg="red")
                img_label.pack(pady=5)

            # Menampilkan nama dan harga senjata
            tk.Label(senjata_frame, text=senjata['nama'], font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(pady=5)
            tk.Label(senjata_frame, text=f"${senjata['harga']}", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(pady=5)

            # Tombol beli
            beli_button = tk.Button(
                senjata_frame,
                text="Beli",
                command=lambda n=senjata['nama'], h=senjata['harga']: self.beli_senjata(Senjata(n, h)),
                width=10,
                bg="#444444",
                fg="#39FF14"
            )
            beli_button.pack(pady=5)

        tk.Button(self.main_frame, text="Back", command=self.main_menu_frame, width=7, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack(pady=5)

    def beli_senjata(self, senjata):
        if self.sistem.beli_senjata(self.current_user, senjata):
            messagebox.showinfo("Sukses", f"Anda telah membeli {senjata.nama}")
        else:
            messagebox.showerror("Error", "Saldo Anda tidak mencukupi!")

    def lihat_senjata_dibeli_frame(self):
        self.clear_frame()
        self.set_background()

        tk.Label(self.main_frame, text="𝕾𝖊𝖓𝖏𝖆𝖙𝖆 𝖞𝖆𝖓𝖌 𝕯𝖎𝖇𝖊𝖑𝖎", font=("Arial", 50), bg="#484848", fg="#39FF14").pack(pady=(150,0))

        # Membuat frame untuk menampung semua senjata yang dibeli
        senjata_container = tk.Frame(self.main_frame, bg="#121212")
        senjata_container.pack(pady=10)

        # Jika pengguna telah membeli senjata
        if self.current_user.senjata_dibeli:
            for index, senjata in enumerate(self.current_user.senjata_dibeli):
                # Membuat frame untuk setiap senjata
                senjata_frame = tk.Frame(senjata_container, bg="#1c1c1c", bd=2, relief=tk.RAISED, padx=10, pady=10)
                senjata_frame.grid(row=index // 3, column=index % 3, padx=10, pady=10)  # Mengatur posisi dalam grid

                # Memuat gambar senjata
                try:
                    image_path = f"C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir\\{senjata.nama}.png"  # Path gambar
                    image = Image.open(image_path)  # Memuat gambar dari path
                    image = image.resize((100, 100), Image.LANCZOS)  # Mengubah ukuran gambar
                    img = ImageTk.PhotoImage(image)
                    img_label = tk.Label(senjata_frame, image=img, bg="#1c1c1c")
                    img_label.image = img  # Menyimpan referensi gambar
                    img_label.pack(pady=5)
                except Exception as e:
                    print(f"Error loading image for {senjata.nama}: {e}")
                    img_label = tk.Label(senjata_frame, text="Image not found", bg="#1c1c1c", fg="red")
                    img_label.pack(pady=5)

                # Menampilkan nama dan harga senjata
                tk.Label(senjata_frame, text=senjata.nama, font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(pady=5)
                tk.Label(senjata_frame, text=f"${senjata.harga}", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(pady=5)
        else:
            tk.Label(self.main_frame, text="Anda belum membeli senjata", bg="#484848", fg="#39FF14").pack(pady=5)

        tk.Button(self.main_frame, text="Back", command=self.main_menu_frame, width=7, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack()

    def tambah_senjata_frame(self):
        self.clear_frame()
        self.set_background()

        tk.Label(self.main_frame, text="𝔗𝔞𝔪𝔟𝔞𝔥 𝔖𝔢𝔫𝔧𝔞𝔱𝔞", font=("Arial", 50), bg="#484848", fg="#39FF14").pack(pady=(200,10))

        tk.Label(self.main_frame, text="Nama Senjata", bg="#484848", fg="#39FF14").pack(pady=(10,0))
        self.senjata_nama_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.senjata_nama_entry.pack(pady=(0,10))

        tk.Label(self.main_frame, text="Harga Senjata", bg="#484848", fg="#39FF14").pack(pady=(10,0))
        self.senjata_harga_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.senjata_harga_entry.pack(pady=(0,10))

        tk.Label(self.main_frame, text="Gambar Senjata", bg="#484848", fg="#39FF14").pack(pady=(10,0))
        self.senjata_gambar_path = tk.StringVar()
        tk.Entry(self.main_frame, textvariable=self.senjata_gambar_path, width=50, bg="#484848", fg="#121212", font=("Arial", 14), state="readonly").pack(pady=(0,10))
        tk.Button(self.main_frame, text="Pilih Gambar", command=self.pilih_gambar, width=10, bg="#39FF14", fg="#121212", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.main_frame, text="Tambah", command=self.tambah_senjata, width=7, bg="#39FF14", fg="#121212", font=("Arial", 12, "bold")).pack(pady=(10,5))
        tk.Button(self.main_frame, text="Back", command=self.main_menu_frame, width=7, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack()

    def pilih_gambar(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            # Salin file ke folder default
            destination = "C:\\Users\\danie\\Downloads\\Teknik Komputer Undip\\tugas_akhir"
            try:
                file_name = file_path.split("/")[-1]  # Ambil nama file
                dest_path = f"{destination}\\{file_name}"
                shutil.copy(file_path, dest_path)  # Salin file ke folder
                self.senjata_gambar_path.set(dest_path)  # Set path baru
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")

    def tambah_senjata(self):
        nama = self.senjata_nama_entry.get()
        harga = int(self.senjata_harga_entry.get())
        gambar = self.senjata_gambar_path.get()
        if not gambar:
            messagebox.showerror("Error", "Silakan pilih gambar!")
            return
        self.sistem.tambah_senjata(nama, harga, gambar)
        messagebox.showinfo("Sukses", f"Senjata {nama} telah ditambahkan!")

    def lihat_pengguna_frame(self):
        self.clear_frame()
        self.set_background()

        tk.Label(self.main_frame, text="𝕯𝖆𝖋𝖙𝖆𝖗 𝕻𝖊𝖓𝖌𝖌𝖚𝖓𝖆", font=("Arial", 50), bg="#484848", fg="#39FF14").pack(pady=(225,0))

        for pengguna in self.sistem.pengguna_terdaftar:
            tk.Label(self.main_frame, text=f"{pengguna.username} - Saldo: ${pengguna.saldo}", bg="#484848", fg="#39FF14", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.main_menu_frame, width=7, bg="#444444", fg="#39FF14", font=("Arial", 12)).pack()

    def edit_saldo_frame(self):
        self.clear_frame()
        self.set_background()
        
        tk.Label(self.main_frame, text="𝕰𝖉𝖎𝖙 𝕾𝖆𝖑𝖉𝖔 𝕻𝖊𝖓𝖌𝖌𝖚𝖓𝖆", font=("Arial", 50), bg="#484848", fg="#39FF14").pack(pady=(225,15))

        tk.Label(self.main_frame, text="Username Pengguna", bg="#484848", fg="#39FF14").pack(pady=(10,0))
        self.username_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.username_entry.pack(pady=(0,10))

        tk.Label(self.main_frame, text="Jumlah Saldo yang ingin ditambahkan", bg="#484848", fg="#39FF14").pack(pady=(10,0))
        self.saldo_entry = tk.Entry(self.main_frame, bg="#333333", fg="#ffffff", font=("Arial", 14))
        self.saldo_entry.pack(pady=(0,10))

        tk.Button(self.main_frame, text="Edit Saldo", command=self.edit_saldo, width=10, bg="#39FF14", fg="#121212", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.main_menu_frame, width=10, bg="#444444", fg="#39FF14", font=("Arial", 12, "bold")).pack(pady=5)

    def edit_saldo(self):
        username = self.username_entry.get()
        jumlah_saldo = int(self.saldo_entry.get())
        pengguna = next((p for p in self.sistem.pengguna_terdaftar if p.username == username), None)
        if pengguna:
            self.sistem.isi_saldo(pengguna, jumlah_saldo)
            self.sistem.save_users_to_file()
            messagebox.showinfo("Sukses", f"Saldo {username} telah diperbarui!")
        else:
            messagebox.showerror("Error", "Pengguna tidak ditemukan!")

    def kedap_kedip_label(self, label):
        # Ubah warna label antara terlihat (fg="#39FF14") dan tidak terlihat (fg sama dengan bg)
        current_color = label.cget("fg")
        next_color = "#FF3131" if current_color == "#484848" else "#484848"
        label.config(fg=next_color)

        # Panggil metode ini lagi setelah 100ms
        label.after(500, lambda: self.kedap_kedip_label(label))

    def logout(self):
        self.current_user = None
        self.login_frame()

# Program Utama
def main():
    root = tk.Tk()
    root.state('zoomed')
    sistem = SistemPembelianSenjata()
    gui = GUIPembelianSenjata(root, sistem)
    root.mainloop()

if __name__ == "__main__":
    main()
