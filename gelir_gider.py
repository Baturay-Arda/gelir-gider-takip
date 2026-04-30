import customtkinter as ctk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Gelir Gider Takip")
app.geometry("520x750")

DOSYA = "veriler.json"
kayitlar = []
secili_index = None

# GELİR kategorileri
KATEGORILER1 = ["Maaş", "Harçlık", "Burs", "Kredi", "Diğer"]

# GİDER kategorileri
KATEGORILER2 = ["Kira", "Yemek", "Ulaşım", "Fatura", "Eğlence", "Diğer"]

# ---------------- TARİH ----------------
def bugun():
    return datetime.now().strftime("%Y-%m-%d")

# ---------------- LOAD ----------------
def yukle():
    global kayitlar

    if os.path.exists(DOSYA):
        with open(DOSYA, "r", encoding="utf-8") as f:
            data = json.load(f)

            kayitlar = []

            for item in data:
                if len(item) == 2:
                    tur, miktar = item

                    if tur == "Gelir":
                        kategori = "Diğer"
                    else:
                        kategori = "Diğer"

                    kayitlar.append((tur, miktar, kategori, bugun()))

                elif len(item) == 3:
                    tur, miktar, kategori = item
                    kayitlar.append((tur, miktar, kategori, bugun()))

                else:
                    kayitlar.append(tuple(item))

# ---------------- SAVE ----------------
def kaydet_dosya():
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(kayitlar, f, ensure_ascii=False)

# ---------------- BAKİYE ----------------
def bakiye_guncelle():
    toplam = 0

    for tur, miktar, kategori, tarih in kayitlar:
        if tur == "Gelir":
            toplam += miktar
        else:
            toplam -= miktar

    bakiye_label.configure(text=f"Bakiye: {toplam} TL")

# ---------------- LİSTE ----------------
def kayitlari_guncelle():
    for w in liste_frame.winfo_children():
        w.destroy()

    for i, (tur, miktar, kategori, tarih) in enumerate(kayitlar):

        text = f"{tarih} | {tur} | {miktar} TL | {kategori}"

        btn = ctk.CTkButton(
            liste_frame,
            text=text,
            command=lambda i=i: sec(i)
        )
        btn.pack(pady=3)

# ---------------- SEÇ ----------------
def sec(i):
    global secili_index
    secili_index = i

# ---------------- SİL ----------------
def sil():
    global secili_index

    if secili_index is not None:
        kayitlar.pop(secili_index)
        secili_index = None

        kaydet_dosya()
        kayitlari_guncelle()
        bakiye_guncelle()

# ---------------- GRAFİK ----------------
def grafik_goster():
    data = {}

    for tur, miktar, kategori, tarih in kayitlar:
        if kategori not in data:
            data[kategori] = 0

        if tur == "Gelir":
            data[kategori] += miktar
        else:
            data[kategori] += miktar

    labels = list(data.keys())
    values = list(data.values())

    if len(values) == 0:
        return

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Kategori Bazlı Dağılım")
    plt.show()

# ---------------- GELİR EKLE ----------------
def gelir_ekle():
    pencere = ctk.CTkToplevel(app)
    pencere.title("Gelir Ekle")
    pencere.geometry("300x250")

    entry = ctk.CTkEntry(pencere, placeholder_text="Miktar")
    entry.pack(pady=10)

    kategori_menu = ctk.CTkOptionMenu(
        pencere,
        values=KATEGORILER1
    )
    kategori_menu.pack(pady=10)

    def kaydet():
        kayitlar.append(
            (
                "Gelir",
                int(entry.get()),
                kategori_menu.get(),
                bugun()
            )
        )

        kaydet_dosya()
        kayitlari_guncelle()
        bakiye_guncelle()
        pencere.destroy()

    ctk.CTkButton(
        pencere,
        text="Kaydet",
        command=kaydet
    ).pack(pady=10)

# ---------------- GİDER EKLE ----------------
def gider_ekle():
    pencere = ctk.CTkToplevel(app)
    pencere.title("Gider Ekle")
    pencere.geometry("300x250")

    entry = ctk.CTkEntry(pencere, placeholder_text="Miktar")
    entry.pack(pady=10)

    kategori_menu = ctk.CTkOptionMenu(
        pencere,
        values=KATEGORILER2
    )
    kategori_menu.pack(pady=10)

    def kaydet():
        kayitlar.append(
            (
                "Gider",
                int(entry.get()),
                kategori_menu.get(),
                bugun()
            )
        )

        kaydet_dosya()
        kayitlari_guncelle()
        bakiye_guncelle()
        pencere.destroy()

    ctk.CTkButton(
        pencere,
        text="Kaydet",
        command=kaydet
    ).pack(pady=10)

# ---------------- GÜNCELLE ----------------
def guncelle():
    global secili_index

    if secili_index is None:
        return

    tur, miktar, kategori, tarih = kayitlar[secili_index]

    pencere = ctk.CTkToplevel(app)
    pencere.title("Güncelle")
    pencere.geometry("300x250")

    entry = ctk.CTkEntry(pencere)
    entry.pack(pady=10)
    entry.insert(0, str(miktar))

    # Türe göre kategori listesi seç
    if tur == "Gelir":
        kategori_listesi = KATEGORILER1
    else:
        kategori_listesi = KATEGORILER2

    kategori_menu = ctk.CTkOptionMenu(
        pencere,
        values=kategori_listesi
    )
    kategori_menu.pack(pady=10)
    kategori_menu.set(kategori)

    def kaydet():
        kayitlar[secili_index] = (
            tur,
            int(entry.get()),
            kategori_menu.get(),
            tarih
        )

        kaydet_dosya()
        kayitlari_guncelle()
        bakiye_guncelle()
        pencere.destroy()

    ctk.CTkButton(
        pencere,
        text="Kaydet",
        command=kaydet
    ).pack(pady=10)

# ---------------- UI ----------------
ctk.CTkLabel(
    app,
    text="💰 Gelir Gider Takip",
    font=("Arial", 26)
).pack(pady=10)

bakiye_label = ctk.CTkLabel(
    app,
    text="Bakiye: 0 TL",
    font=("Arial", 20)
)
bakiye_label.pack(pady=10)

liste_frame = ctk.CTkScrollableFrame(
    app,
    width=460,
    height=350
)
liste_frame.pack(pady=10)

ctk.CTkButton(app, text="Gelir Ekle", command=gelir_ekle).pack(pady=5)
ctk.CTkButton(app, text="Gider Ekle", command=gider_ekle).pack(pady=5)
ctk.CTkButton(app, text="Sil", command=sil).pack(pady=5)
ctk.CTkButton(app, text="Güncelle", command=guncelle).pack(pady=5)
ctk.CTkButton(app, text="📊 Grafik", command=grafik_goster).pack(pady=5)

# ---------------- START ----------------
yukle()
kayitlari_guncelle()
bakiye_guncelle()

app.mainloop()