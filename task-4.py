import tkinter as tk
from tkinter import messagebox
from transformers import pipeline

# === LOAD 2 MODEL ===
# BERT (Inggris)
bert_en = pipeline("sentiment-analysis")

#IndoBERT (sudah fine-tuned untuk sentimen)
indo_bert = pipeline(
    "text-classification",
    model="w11wo/indonesian-roberta-base-sentiment-classifier",
    tokenizer="w11wo/indonesian-roberta-base-sentiment-classifier"
)

# === FUNGSI BANTUAN ===
def normalisasi_label(label):
    label = label.lower()
    if 'pos' in label:
        return 'positif'
    elif 'neg' in label:
        return 'negatif'
    elif 'neutral' in label or 'netral' in label:
        return 'netral'
    return label

def is_ambiguous(label_en, label_id, score_en, score_id, threshold=0.7):
    # Jika IndoBERT yakin (confidence tinggi), percaya pada IndoBERT
    if score_id >= threshold:
        return False
    #Jika IndoBERT ragu, dan label beda, atau dua-duanya ragu
    if label_en != label_id or (score_en < threshold and score_id < threshold):
        return True
    return False

def ensemble_sentimen(teks):
    hasil_en = bert_en(teks)[0]
    hasil_id = indo_bert(teks)[0]

    label_en = normalisasi_label(hasil_en['label'])
    score_en = hasil_en['score']

    label_id = normalisasi_label(hasil_id['label'])
    score_id= hasil_id['score']

    ambiguous = is_ambiguous(label_en, label_id, score_en, score_id)

    if not ambiguous:
        # Jika tidak ambigu, ambil label yang disepakati atau paling yakin
        if label_en == label_id:
            final_label = label_en
            final_score = max(score_en, score_id)
        else:
            if score_en > score_id:
                final_label = label_en
                final_score = score_en
            else:
                final_label = label_id
                final_score = score_id
    else:
        final_label = "ambiguous"
        final_score = None
        
    return {
        "bert_en": (label_en, score_en),
        "indo_bert": (label_id, score_id),
        "final": (final_label, final_score),
        "ambiguous": ambiguous
    }

# === FUNGSI GUI ===
def analisis_sentimen():
    teks = entry.get()
    if not teks.strip():
        messagebox.showwarning("Peringatan", "Silahkan masukkan kalimat terlebih dahulu.")
        return
    
    try:
        hasil = ensemble_sentimen(teks)

        # Tampilkan hasil model BERT (Inggris)
        label_bert_en.config(
            text=f"BERT (EN): {hasil['bert_en'][0].capitalize()} ({hasil['bert_en'][1]:.2f})"
        )

        # Tampilkan hasil IndoBERT
        label_indo_bert.config(
            text=f"IndoBERT: {hasil['indo_bert'][0].capitalize()} ({hasil['indo_bert'][1]:.2f})"
        )

        if hasil["ambiguous"]:
            label_hasil.config(
                text="? Kalimat Ambigu: Model tidak sepakat atau confidence rendah",
                fg="orange"
            )
        else:
            # Tampilkan hasil ensemble
            warna = {
                "positif": "green",
                "negatif": "red",
                "netral": "gray"
            }.get(hasil['final'][0], "black")

            label_hasil.config(
                text= f"Prediksi Akhir: {hasil['final'][0].capitalize()} ({hasil['final'][1]:.2f})",
                fg=warna
            )
    except Exception as e:
        messagebox.showerror("Error",f"Terjadi kesalahan saat analisis:\n{e}")

# === GUI SETUP ===
window = tk.Tk()
window.title("Analisis Sentimen Ensemble (BERT + IndoBERT)")
window.geometry("500x350")
window.resizable(True,False)

label_judul = tk.Label(window, text="Analisis Sentimen Bahasa Indonesia", font=("Arial", 16))
label_judul.pack(pady=10)

entry = tk.Entry(window, font=("Arial", 12), width=50)
entry.pack(pady=5)

btn = tk.Button(window, text="Analisis", font=("Arial", 12), command=analisis_sentimen)
btn.pack(pady=10)

label_bert_en = tk.Label(window, text="BERT (EN): -", font=("Arial", 12))
label_bert_en.pack()

label_indo_bert = tk.Label(window, text="IndoBERT: -", font=("Arial", 12))
label_indo_bert.pack()

label_hasil = tk.Label(window, text="", font=("Arial", 14))
label_hasil.pack(pady=15)

window.mainloop()