# Install dulu kalau belum ada: pip install scikit-learn

import tkinter as tk
from tkinter import messagebox
from transformers import pipeline

# === LOAD MODEL BERT ===
#ini akan otomatis download model pertama kali (bert-base-uncased fine-tuned for sentiment)
sentimen_model = pipeline("sentiment-analysis")


# ===== GUI ====
def analisis_sentimen():
    teks = entry.get()
    if not teks.strip():
        messagebox.showwarning("Peringatan", "Silahkan masukkan kalimat terlebih dahulu")
        return
    try: 
        hasil = sentimen_model(teks)[0]
        label = hasil['label'] # POSITIVE atau NEGATIF
        score = hasil['score'] # Confidence score
        warna = 'green' if label == 'POSITIVE' else 'red'
        label_hasil.config(
            text=f"Sentimen: {label.capitalize()} ({score:.2f})",
            fg=warna
        )
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menganalisis: {e}")


# === GUI SETUP ===
window = tk.Tk()
window.title("Analisis Sentimen dengan BERT")
window.geometry("400x250")
window.resizable(False, False)

#Judul
label_judul = tk.Label(window, text="Analisis Sentimen (BERT)", font=("Arial",16))
label_judul.pack(pady=10)

#Input teks
entry = tk.Entry(window, font=("Arial", 12), width=50)
entry.pack(pady=5)

#Tombol analisis
btn = tk.Button(window, text="Analisis", font=("Arial", 12), command=analisis_sentimen)
btn.pack(pady=10)

#Label hasil
label_hasil = tk.Label(window, text="", font=("Arial", 14))
label_hasil.pack(pady=10)

#Jalankan GUI
window.mainloop()