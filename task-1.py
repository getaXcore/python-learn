# Install dulu kalau belum ada: pip install scikit-learn

import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Data latih (training data)
data_teks = [
    "Saya sangat senang hari ini",
    "Ini adalah pengalaman yang menyenangkan",
    "Saya sedih dan kecewa",
    "Hari yang buruk dan menyebalkan",
    "Luar biasa! Aku suka sekali",
    "Ini sangat jelek dan tidak menyenangkan",
    "Aku benci hari ini",
    "Aku muak dengan semuanya",
    "Sangat menyebalkan dan bikin frustasi",
    "Aku malas menghadapi ini lagi",
    "Aku suka cuacanya",
    "Kamu sangat menyenangkan untuk diajak ngobrol",
    "Aku sangat kecewa dengan hasilnya",
    "Senang bisa ikut acara ini",
    "Benci banget sama suasananya",
    "Aku menikmati waktuku bersama kalian",
    "Aku marah dan kesal",
    "Aku sangat bersyukur hari ini",
    "Bersyukur atas keberuntungan yang kudapat",
    "Aku merasa bersyukur dan bahagia",
    "Aku merasa tidak bersukur",
    "Aku merasa tidak bahagia",
    "Melihat dia, diriku menjadi bahagia",
    "Mungkin kali ini aku ditakdirkan untuk bahagia"
]

label = ['positif', 'positif', 'negatif', 'negatif', 'positif', 'negatif',
    'negatif', 'negatif', 'negatif', 'negatif', 'positif', 'positif',
    'negatif', 'positif', 'negatif', 'positif', 'negatif', 'positif', 'positif', 'positif',
    'negatif', 'negatif', 'positif', 'positif']

# Buat pipeline: vectorizer + classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Latih model
model.fit(data_teks, label)

# ===== GUI ====
def analisis_sentimen():
    teks = entry.get()
    if not teks.strip():
        messagebox.showwarning("Peringatan", "Silahkan masukkan kalimat terlebih dahulu")
        return
    hasil = model.predict([teks])[0]
    label_hasil.config(text=f"Sentimen: {hasil.capitalize()}", fg='green' if hasil == 'positif' else 'red')


#Setup jendela utama
window = tk.Tk()
window.title("Analisis Sentimen Sederhana")
window.geometry("400x250")
window.resizable(False, False)

#Judul
label_judul = tk.Label(window, text="Analisis Sentimen Teks", font=("Arial",16))
label_judul.pack(pady=10)

#Input field
entry = tk.Entry(window, font=("Arial", 12), width=40)
entry.pack(pady=5)

#Tombol Analisis
btn = tk.Button(window, text="Analisis", font=("Arial", 12), command=analisis_sentimen)
btn.pack(pady=10)

#Hasil
label_hasil = tk.Label(window, text="", font=("Arial", 14))
label_hasil.pack(pady=10)

#Jalankan GUI
window.mainloop()

# # Input interaktif dari user
# print("=== Analisis Sentimen Teks ===")
# print("Ketik 'exit' untuk keluar")

# while True:
#     teks = input("Masukkan kalimat: ")
#     if teks.lower() in ['exit', 'quit', 'keluar']:
#         print("Terima kasih! Program selesai.")
#         break

#     hasil = model.predict([teks])[0]
#     print(f"Sentimen: {hasil}\n")

# # Uji model
# kalimat_uji = [
#     "Hari ini menyenangkan sekali",
#     "Aku benci semuanya",
#     "Senang bisa bertemu kalian",
#     "Hari ini sangat buruk",
#     "Aku marah dan kecewa",
#     "Sangat bersyukur atas segalanya"
# ]

# # Prediksi
# prediksi = model.predict(kalimat_uji)

# # Tampilkan hasil
# for teks, hasil in zip(kalimat_uji, prediksi):
#     print(f"Teks: {teks} => Sentimen: {hasil}")
