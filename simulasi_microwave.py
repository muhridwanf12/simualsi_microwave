import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class MicrowaveSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi Microwave")

        # Frame utama
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Frame untuk pintu microwave
        self.door_frame = ttk.Frame(self.main_frame, width=300, height=200, relief="ridge", borderwidth=5)
        self.door_frame.grid(column=0, row=0, rowspan=4, padx=10, pady=10)
        self.door_frame.grid_propagate(False)

        # Frame untuk kontrol microwave
        self.control_frame = ttk.Frame(self.main_frame, padding="10", relief="raised", borderwidth=5)
        self.control_frame.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Label dan input untuk waktu memasak
        self.time_label = ttk.Label(self.control_frame, text="Waktu Memasak (detik):")
        self.time_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

        self.time_entry = ttk.Entry(self.control_frame)
        self.time_entry.grid(column=1, row=0, padx=10, pady=5, sticky=tk.E)

        # Label dan dropdown untuk jenis masakan
        self.food_label = ttk.Label(self.control_frame, text="Jenis Masakan:")
        self.food_label.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)

        self.food_var = tk.StringVar()
        self.food_dropdown = ttk.Combobox(self.control_frame, textvariable=self.food_var)
        self.food_dropdown['values'] = ('Popcorn', 'Pizza', 'Ayam')
        self.food_dropdown.grid(column=1, row=1, padx=10, pady=5, sticky=tk.E)

        # Tombol untuk memulai memasak
        self.start_button = ttk.Button(self.control_frame, text="Mulai Masak", command=self.start_cooking)
        self.start_button.grid(column=0, row=2, columnspan=2, padx=10, pady=5)

        # Label untuk menampilkan status masakan
        self.status_label = ttk.Label(self.control_frame, text="Status: Menunggu", relief="sunken", width=30)
        self.status_label.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

        # Buat label hitung mundur dalam pintu microwave
        self.countdown_label = ttk.Label(self.door_frame, text="", font=("Helvetica", 48), background="black", foreground="green")
        self.countdown_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Frame untuk grafik matplotlib
        self.graph_frame = ttk.Frame(self.main_frame, padding="10", relief="sunken", borderwidth=5)
        self.graph_frame.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        # Variabel animasi
        self.anim = None

        self.canvas = None  # Initial canvas holder

    def start_cooking(self):
        try:
            self.cook_time = int(self.time_entry.get())
            self.food_type = self.food_var.get()

            if self.food_type == '':
                self.status_label.config(text="Pilih jenis masakan!")
                return

            self.reset_simulation()  # Reset animasi

            self.status_label.config(text=f"Memasak {self.food_type} selama {self.cook_time} detik")
            self.root.after(1000, self.update_timer)
            self.update_countdown()
            self.simulate_electric_field()

        except ValueError:
            self.status_label.config(text="Masukkan waktu memasak yang valid!")

    def reset_simulation(self):
        if self.anim:
            self.anim.event_source.stop()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

    def update_timer(self):
        if self.cook_time > 0:
            self.cook_time -= 1
            self.status_label.config(text=f"Memasak {self.food_type}... {self.cook_time} detik tersisa")
            self.root.after(1000, self.update_timer)
            self.update_countdown()
        else:
            self.status_label.config(text=f"{self.food_type} Selesai Dimasak!")
            self.countdown_label.config(text="")
            if self.anim:
                self.anim.event_source.stop()

    def update_countdown(self):
        self.countdown_label.config(text=str(self.cook_time))

    def simulate_electric_field(self):
        frekuensi = 2.45e9  # Frekuensi microwave dalam Hz (2.45 GHz untuk microwave)
        kecepatan_cahaya = 3e8  # Kecepatan cahaya dalam vacuum dalam m/s
        panjang_gelombang = kecepatan_cahaya / frekuensi  # Panjang gelombang microwave

        def distribusi_medan(x, y, panjang_gelombang, waktu):
            return np.sin(2 * np.pi * x / panjang_gelombang - waktu) * np.cos(2 * np.pi * y / panjang_gelombang)

        ukuran_grid = 100
        x = np.linspace(-1, 1, ukuran_grid)
        y = np.linspace(-1, 1, ukuran_grid)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection='3d')

        def update_frame(frame):
            waktu = frame / 10.0  # Mengatur kecepatan animasi
            medan_listrik = distribusi_medan(X, Y, panjang_gelombang, waktu)
            ax.clear()
            ax.plot_surface(X, Y, medan_listrik, cmap='viridis')
            ax.set_title('Distribusi Medan Listrik Microwave')
            ax.set_xlabel('Posisi X (m)')
            ax.set_ylabel('Posisi Y (m)')
            ax.set_zlabel('Medan Listrik')
            ax.set_zlim(-1, 1)

        self.anim = FuncAnimation(fig, update_frame, frames=200, interval=50, blit=False)

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MicrowaveSimulator(root)
    root.mainloop()
