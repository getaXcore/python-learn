import tkinter as tk
from tkinter import messagebox
from transformers import pipeline
import re
from langdetect import detect

# Load IndoBERT model
indo_bert = pipeline(
    "text-classification",
    model="w11wo/indonesian-roberta-base-sentiment-classifier",
    tokenizer="w11wo/indonesian-roberta-base-sentiment-classifier"
)

# Fungsi untuk validasi input
def is_valid_input(teks):
    # Bersihkan teks dari spasi berlebih
    teks = teks.strip()

    #Cek panjang minimal
    if len(teks) < 8:
        return False
    
    # Deteksi apakah bahasa indonesia?
    try:
        return detect(teks) == 'id'
    except:
        return False

# Fungsi analisis
def analisis_sentimen():
    teks = entry.get()
    if not teks.strip():
        hasil_label.config(text="Silahkan masukkan teks.")
        return
    if not is_valid_input(teks):
        hasil_label.config(text="Input tidak valid atau tidak bermakna", fg="orange")
        return
    
    try:    
        hasil = indo_bert(teks)[0]
        label = hasil['label'].lower()
        skor = hasil['score']

        warna = {
            "positive": "green",
            "negative": "red",
            "neutral": "gray"
        }.get(label, "black")

        hasil_label.config(text=f"Prediksi: {label.capitalize()} ({skor:.2f})", fg=warna)
    except Exception as e:
        messagebox.showerror("Error",f"Terjadi kesalahan saat analisis:\n{e}")

def on_teks_berubah(event):
    if not entry.get().strip():
        hasil_label.config(text="")

# Setup GUI
window = tk.Tk()
window.title("Analisis Sentimen Bahasa Indonesia (IndoBERT)")
window.geometry("500x250")

judul = tk.Label(window, text="Analisis Sentimen Bahasa Indonesia", font=("Helevatica", 14))
judul.pack(pady=10)

entry = tk.Entry(window, width=60)
entry.pack(pady=5)
entry.bind("<KeyRelease>", on_teks_berubah) # Tambahkan bind ke fungsi reset

btn = tk.Button(window, text="Analisis", command=analisis_sentimen)
btn.pack(pady=5)

hasil_label = tk.Label(window, text="", font=("Helevatica", 12))
hasil_label.pack(pady=20)

window.mainloop()