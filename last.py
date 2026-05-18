import datetime
from veritabani import json_oku, json_yaz

def odunc_al(kullanici_adi, isbn):
    kitaplar = json_oku("kitaplar.json")
    oduncler = json_oku("oduncler.json")
    
    if isbn in kitaplar and kitaplar[isbn]["stok"] > 0:
        kitaplar[isbn]["stok"] -= 1
        islem_id = f"{kullanici_adi}_{isbn}"
        bugun = datetime.date.today()
        
        oduncler[islem_id] = {
            "kullanici": kullanici_adi,
            "isbn": isbn,
            "durum": "aktif",
            "iade_tarihi": str(bugun + datetime.timedelta(days=15))
        }
        
        json_yaz("kitaplar.json", kitaplar)
        json_yaz("oduncler.json", oduncler)
        return True, f"Kitap verildi. İşlem ID: {islem_id}"
    return False, "Kitap bulunamadı veya stokta yok."

def iade_et(islem_id):
    oduncler = json_oku("oduncler.json")
    kitaplar = json_oku("kitaplar.json")
    
    if islem_id in oduncler and oduncler[islem_id]["durum"] == "aktif":
        oduncler[islem_id]["durum"] = "iade_edildi"
        isbn = oduncler[islem_id]["isbn"]
        
        if isbn in kitaplar:
            kitaplar[isbn]["stok"] += 1
            
        json_yaz("kitaplar.json", kitaplar)
        json_yaz("oduncler.json", oduncler)
        return True, "Kitap iade edildi ve stoka eklendi."
    return False, "Geçersiz veya zaten iade edilmiş İşlem ID."
{
    "emir_12345": {
        "kullanici": "emir",
        "isbn": "12345",
        "durum": "iade_edildi",
        "iade_tarihi": "2026-06-02"
    },
    "ceren_12345": {
        "kullanici": "ceren",
        "isbn": "12345",
        "durum": "iade_edildi",
        "iade_tarihi": "2026-06-02"
    }
}
import datetime
from veritabani import json_oku

def rapor_olustur():
    kitaplar = json_oku("kitaplar.json")
    kullanicilar = json_oku("kullanicilar.json")
    oduncler = json_oku("oduncler.json")
        
    aktif = sum(1 for v in oduncler.values() if v["durum"] == "aktif")
    
    rapor = f"====== KÜTÜPHANE İSTATİSTİK RAPORU ({datetime.date.today()}) ======\n\n"
    rapor += f" -> Toplam Kitap Çeşidi : {len(kitaplar)}\n"
    rapor += f" -> Kayıtlı Üye Sayısı  : {len(kullanicilar)}\n"
    rapor += f" -> Aktif Ödünç Sayısı  : {aktif}\n\n"
    rapor += "======================================================="
    return rapor
import json
import os
import hashlib

def dosyalari_baslat():
    dosyalar = {"kitaplar.json": {}, "kullanicilar.json": {}, "oduncler.json": {}}
    for dosya, bos_veri in dosyalar.items():
        if not os.path.exists(dosya):
            with open(dosya, "w", encoding="utf-8") as f:
                json.dump(bos_veri, f)
    
    with open("kullanicilar.json", "r", encoding="utf-8") as f:
        kullanicilar = json.load(f)
    
    # Varsayılan admin hesabı (Şifre: 1234)
    if "admin" not in kullanicilar:
        kullanicilar["admin"] = {
            "sifre_hash": hashlib.sha256("1234".encode('utf-8')).hexdigest(),
            "ad_soyad": "Sistem Yöneticisi",
            "rol": "yönetici"
        }
        json_yaz("kullanicilar.json", kullanicilar)

def json_oku(dosya_adi):
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def json_yaz(dosya_adi, veri):
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)
from veritabani import json_oku, json_yaz

def kitap_ekle(isbn, ad, yazar, yayinevi, yayin_yili, stok, konum):
    kitaplar = json_oku("kitaplar.json")
    if isbn in kitaplar:
        return False, "Bu ISBN zaten kayıtlı!"
    
    try:
        kitaplar[isbn] = {
            "ad": ad, "yazar": yazar, "yayinevi": yayinevi,
            "yayin_yili": int(yayin_yili or 0), "stok": int(stok or 0), "konum": konum
        }
        json_yaz("kitaplar.json", kitaplar)
        return True, "Kitap eklendi!"
    except ValueError:
        return False, "Stok ve Yıl rakam olmalıdır!"

def kitap_sil(isbn):
    kitaplar = json_oku("kitaplar.json")
    if isbn in kitaplar:
        del kitaplar[isbn]
        json_yaz("kitaplar.json", kitaplar)
        return True, "Kitap silindi!"
    return False, "Kitap bulunamadı!"

def kitap_ara(aranan):
    kitaplar = json_oku("kitaplar.json")
    aranan = aranan.lower()
    sonuc = ""
    for isbn, b in kitaplar.items():
        if aranan in b["ad"].lower() or aranan in b["yazar"].lower():
            sonuc += f"ISBN: {isbn} | Ad: {b['ad']} | Stok: {b['stok']}\n"
    return sonuc if sonuc else "Kitap bulunamadı."

def tum_kitaplari_listele():
    kitaplar = json_oku("kitaplar.json")
    sonuc = ""
    for isbn, b in kitaplar.items():
        sonuc += f"ISBN: {isbn} | Ad: {b['ad']} | Stok: {b['stok']}\n"
    return sonuc if sonuc else "Kütüphane boş."
{
    "12345": {
        "ad": "Python Programlama",
        "yazar": "Guido van Rossum",
        "stok": 5
    },
    "98765": {
        "ad": "Veri Yapıları ve Algoritmalar",
        "yazar": "Ahmet Yılmaz",
        "stok": 2
    },
    "45678": {
        "ad": "The C Programming Language",
        "yazar": "Brain W. Kernighan",
        "yayinevi": "Prentice Hall",
        "yayin_yili": 1988,
        "stok": 3,
        "konum": "Müh-Raf1"
    },
    "": {
        "ad": "",
        "yazar": "",
        "yayinevi": "",
        "yayin_yili": 0,
        "stok": 0,
        "konum": ""
    }
}
import hashlib
from veritabani import json_oku, json_yaz

def giris_yap(kullanici_adi, sifre):
    kullanicilar = json_oku("kullanicilar.json")
    sifre_hash = hashlib.sha256(sifre.encode('utf-8')).hexdigest()
    
    if kullanici_adi in kullanicilar and kullanicilar[kullanici_adi]["sifre_hash"] == sifre_hash:
        return True, kullanicilar[kullanici_adi]["rol"]
    return False, None

def kullanici_ekle(k_adi, sifre, ad_soyad, rol):
    kullanicilar = json_oku("kullanicilar.json")
    if k_adi in kullanicilar:
        return False, "Kullanıcı zaten mevcut!"
        
    sifre_hash = hashlib.sha256(sifre.encode('utf-8')).hexdigest()
    kullanicilar[k_adi] = {"sifre_hash": sifre_hash, "ad_soyad": ad_soyad, "rol": rol}
    json_yaz("kullanicilar.json", kullanicilar)
    return True, "Kullanıcı eklendi!"

def kullanici_sil(k_adi):
    kullanicilar = json_oku("kullanicilar.json")
    if k_adi in kullanicilar:
        del kullanicilar[k_adi]
        json_yaz("kullanicilar.json", kullanicilar)
        return True, "Kullanıcı silindi!"
    return False, "Kullanıcı bulunamadı!"

def kullanici_guncelle(k_adi, yeni_sifre, yeni_ad_soyad, yeni_rol):
    kullanicilar = json_oku("kullanicilar.json")
    if k_adi not in kullanicilar:
        return False, "Kullanıcı bulunamadı!"
    
    if yeni_sifre:
        kullanicilar[k_adi]["sifre_hash"] = hashlib.sha256(yeni_sifre.encode('utf-8')).hexdigest()
    if yeni_ad_soyad:
        kullanicilar[k_adi]["ad_soyad"] = yeni_ad_soyad
    if yeni_rol:
        kullanicilar[k_adi]["rol"] = yeni_rol
        
    json_yaz("kullanicilar.json", kullanicilar)
    return True, "Kullanıcı bilgileri güncellendi!"
{
    "admin": {
        "sifre_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        "rol": "yönetici"
    },
    "emir": {
        "sifre_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        "rol": "yönetici",
        "ad_soyad": "emir küçükkaynarpınar"
    },
    "ece": {
        "sifre_hash": "9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0",
        "ad_soyad": "ece",
        "rol": "yönetici"
    },
    "yyy": {
        "sifre_hash": "f2afd1cacb5441a5e65a7a460a5f9898b7b98b08aa6323a2e53c8b9a9686cd86",
        "ad_soyad": "yyy",
        "rol": "personel"
    },
    "ceren": {
        "sifre_hash": "90ae1a764e32daa9bd620702bbabded089798e967c1e1d59b8828fd994ed6cba",
        "ad_soyad": "ceren",
        "rol": "yönetici"
    }
}
import tkinter as tk
from tkinter import ttk, messagebox
from veritabani import dosyalari_baslat
from kullanici import giris_yap, kullanici_ekle, kullanici_sil, kullanici_guncelle
from kitap import kitap_ekle, kitap_sil, kitap_ara, tum_kitaplari_listele
from odunc import odunc_al, iade_et
from rapor import rapor_olustur

# Ortak Renkler (Soft Pink & Blue Teması)
BG_COLOR = "#FFF0F5" 
BTN_BLUE = "#AEC6CF"
BTN_PINK = "#FFB6C1"
BTN_RED = "#FF9999"

class KutuphaneUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Kütüphane Yönetim Sistemi")
        self.root.geometry("750x650")
        self.root.configure(bg=BG_COLOR)
        
        dosyalari_baslat()
        self.aktif_kullanici = None
        self.aktif_rol = None
        
        self.giris_ekrani()

    # --- 1. GİRİŞ VE KAYIT EKRANI ---
    def giris_ekrani(self):
        self.frame_giris = tk.Frame(self.root, bg=BG_COLOR)
        self.frame_giris.pack(expand=True)
        
        tk.Label(self.frame_giris, text="Sisteme Giriş / Kayıt", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg="#5C88C4").pack(pady=20)
        
        tk.Label(self.frame_giris, text="Kullanıcı Adı:", bg=BG_COLOR, font=("Helvetica", 10, "bold")).pack()
        self.ent_kullanici = tk.Entry(self.frame_giris, width=30, font=("Helvetica", 12))
        self.ent_kullanici.pack(pady=5)
        
        tk.Label(self.frame_giris, text="Şifre:", bg=BG_COLOR, font=("Helvetica", 10, "bold")).pack()
        self.ent_sifre = tk.Entry(self.frame_giris, width=30, show="*", font=("Helvetica", 12))
        self.ent_sifre.pack(pady=5)
        
        tk.Label(self.frame_giris, text="Hesap Rolü (Kayıt İçin Seçin):", bg=BG_COLOR, font=("Helvetica", 10, "bold")).pack(pady=(5, 0))
        self.cmb_giris_rol = ttk.Combobox(self.frame_giris, values=["öğrenci", "personel", "yönetici"], state="readonly", font=("Helvetica", 11), width=28)
        self.cmb_giris_rol.current(0) 
        self.cmb_giris_rol.pack(pady=5)
        
        btn_f = tk.Frame(self.frame_giris, bg=BG_COLOR)
        btn_f.pack(pady=20)
        
        tk.Button(btn_f, text="Giriş Yap", command=self.giris_kontrol, bg=BTN_BLUE, font=("Helvetica", 12, "bold"), width=12).pack(side="left", padx=10)
        tk.Button(btn_f, text="Kayıt Ol", command=self.kayit_kontrol, bg=BTN_PINK, font=("Helvetica", 12, "bold"), width=12).pack(side="left", padx=10)

    def giris_kontrol(self):
        k_adi = self.ent_kullanici.get().strip()
        sifre = self.ent_sifre.get().strip()
        
        basarili, rol = giris_yap(k_adi, sifre)
        if basarili:
            self.aktif_kullanici = k_adi
            self.aktif_rol = rol 
            self.frame_giris.destroy()
            self.ana_ekran()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

    def kayit_kontrol(self):
        k_adi = self.ent_kullanici.get().strip()
        sifre = self.ent_sifre.get().strip()
        secilen_rol = self.cmb_giris_rol.get() 
        
        if not k_adi or not sifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş bırakılamaz!")
            return
            
        durum, mesaj = kullanici_ekle(k_adi, sifre, k_adi, secilen_rol)
        if durum:
            messagebox.showinfo("Başarılı", f"Kayıt oluşturuldu!\nHesap Türü: {secilen_rol.upper()}\nŞimdi 'Giriş Yap' butonuna basabilirsiniz.")
        else:
            messagebox.showerror("Hata", mesaj)

    # --- HESAPTAN ÇIKIŞ İŞLEMİ ---
    def cikis_yap(self):
        # Kullanıcı bilgilerini sıfırla
        self.aktif_kullanici = None
        self.aktif_rol = None
        
        # Ana ekran elementlerini sil
        self.ust_bilgi_frame.destroy()
        self.notebook.destroy()
        
        # Giriş ekranını tekrar çağır
        self.giris_ekrani()

    # --- 2. ANA SEKMELER VE YETKİLENDİRME SÜRECİ ---
    def ana_ekran(self):
        # Üst bilgi alanı (Hoş geldin yazısı ve Çıkış Butonu)
        self.ust_bilgi_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.ust_bilgi_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(self.ust_bilgi_frame, text=f"Hoş Geldiniz, {self.aktif_kullanici} ({self.aktif_rol.capitalize()})", font=("Helvetica", 14, "bold"), bg=BG_COLOR, fg="#5C88C4").pack(side="left")
        
        tk.Button(self.ust_bilgi_frame, text="Çıkış Yap", command=self.cikis_yap, bg=BTN_RED, font=("Helvetica", 10, "bold"), width=10).pack(side="right")
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Helvetica', 11, 'bold'), padding=[10, 5])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Herkes görebilir
        self.tab_arama = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.tab_arama, text="Arama & Ödünç İşlemleri")
        self.kur_arama_sekmesi()

        # Personel ve Yönetici görebilir
        if self.aktif_rol in ["personel", "yönetici"]:
            self.tab_kitap = tk.Frame(self.notebook, bg="#FFFFFF")
            self.notebook.add(self.tab_kitap, text="Kitap Ekle/Sil")
            self.kur_kitap_sekmesi()
            
            self.tab_rapor = tk.Frame(self.notebook, bg="#FFFFFF")
            self.notebook.add(self.tab_rapor, text="İstatistik Raporları")
            self.kur_rapor_sekmesi()

        # Sadece Yönetici görebilir
        if self.aktif_rol == "yönetici":
            self.tab_kullanici = tk.Frame(self.notebook, bg="#FFFFFF")
            self.notebook.add(self.tab_kullanici, text="Kullanıcı Yönetimi (Admin)")
            self.kur_kullanici_sekmesi()

    # --- 3. KİTAP SEKME TASARIMI ---
    def kur_kitap_sekmesi(self):
        self.entryler = {}
        alanlar = ["ISBN", "Ad", "Yazar", "Yayınevi", "Yayın Yılı", "Stok", "Konum"]
        for alan in alanlar:
            f = tk.Frame(self.tab_kitap, bg="#FFFFFF")
            f.pack(fill="x", pady=5, padx=50)
            tk.Label(f, text=f"{alan}:", width=15, anchor="w", bg="#FFFFFF", font=("Helvetica", 11, "bold")).pack(side="left")
            ent = tk.Entry(f, width=40, font=("Helvetica", 11))
            ent.pack(side="left")
            self.entryler[alan] = ent
            
        btn_f = tk.Frame(self.tab_kitap, bg="#FFFFFF")
        btn_f.pack(pady=20)
        tk.Button(btn_f, text="Kitap Ekle", command=self.btn_ekle, bg=BTN_PINK, width=15, font=("Helvetica", 11, "bold")).pack(side="left", padx=10)
        tk.Button(btn_f, text="Kitap Sil", command=self.btn_sil, bg=BTN_RED, width=15, font=("Helvetica", 11, "bold")).pack(side="left", padx=10)

    def btn_ekle(self):
        durum, mesaj = kitap_ekle(
            self.entryler["ISBN"].get().strip(), self.entryler["Ad"].get().strip(),
            self.entryler["Yazar"].get().strip(), self.entryler["Yayınevi"].get().strip(),
            self.entryler["Yayın Yılı"].get(), self.entryler["Stok"].get(), self.entryler["Konum"].get().strip()
        )
        messagebox.showinfo("Sonuç", mesaj) if durum else messagebox.showerror("Hata", mesaj)

    def btn_sil(self):
        durum, mesaj = kitap_sil(self.entryler["ISBN"].get().strip())
        messagebox.showinfo("Sonuç", mesaj) if durum else messagebox.showerror("Hata", mesaj)

    # ARAMA & ÖDÜNÇ TASARIMI
    def kur_arama_sekmesi(self):
        ust_f = tk.Frame(self.tab_arama, bg="#F0F8FF", pady=10)
        ust_f.pack(fill="x")
        self.ent_arama = tk.Entry(ust_f, width=30, font=("Helvetica", 11))
        self.ent_arama.pack(side="left", padx=10)
        tk.Button(ust_f, text="Ara", command=self.btn_ara, bg=BTN_BLUE, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        tk.Button(ust_f, text="Tümünü Listele", command=self.btn_listele, bg=BTN_PINK, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        
        self.txt_sonuc = tk.Text(self.tab_arama, width=70, height=12, font=("Courier", 10))
        self.txt_sonuc.pack(pady=10)
        
        alt_f = tk.Frame(self.tab_arama, bg=BG_COLOR, pady=10)
        alt_f.pack(fill="x")
        tk.Label(alt_f, text="İşlem ISBN/ID:", bg=BG_COLOR, font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        self.ent_islem = tk.Entry(alt_f, width=25, font=("Helvetica", 11))
        self.ent_islem.pack(side="left")
        tk.Button(alt_f, text="Ödünç Al", command=self.btn_odunc, bg=BTN_BLUE, font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        tk.Button(alt_f, text="İade Et", command=self.btn_iade, bg=BTN_RED, font=("Helvetica", 10, "bold")).pack(side="left")

    def txt_yaz(self, metin):
        self.txt_sonuc.delete("1.0", tk.END)
        self.txt_sonuc.insert(tk.END, metin)

    def btn_ara(self): self.txt_yaz(kitap_ara(self.ent_arama.get().strip()))
    def btn_listele(self): self.txt_yaz(tum_kitaplari_listele())
    def btn_odunc(self):
        durum, mesaj = odunc_al(self.aktif_kullanici, self.ent_islem.get().strip())
        messagebox.showinfo("Sonuç", mesaj) if durum else messagebox.showerror("Hata", mesaj)
    def btn_iade(self):
        durum, mesaj = iade_et(self.ent_islem.get().strip())
        messagebox.showinfo("Sonuç", mesaj) if durum else messagebox.showerror("Hata", mesaj)

    # --- 5. RAPOR SEKME TASARIMI ---
    def kur_rapor_sekmesi(self):
        tk.Button(self.tab_rapor, text="İstatistikleri Yenile", command=self.btn_rapor, bg=BTN_PINK, font=("Helvetica", 12, "bold")).pack(pady=20)
        self.txt_rapor = tk.Text(self.tab_rapor, width=60, height=15, font=("Courier", 12))
        self.txt_rapor.pack()

    def btn_rapor(self):
        self.txt_rapor.delete("1.0", tk.END)
        self.txt_rapor.insert(tk.END, rapor_olustur())

    # --- 6. ADMIN PANELI SEKME TASARIMI ---
    def kur_kullanici_sekmesi(self):
        f_yonetim = tk.LabelFrame(self.tab_kullanici, text="Kullanıcı Yönetim Paneli", bg="#FFFFFF", font=("Helvetica", 11, "bold"), pady=10)
        f_yonetim.pack(fill="both", expand=True, pady=15, padx=50)
        
        tk.Label(f_yonetim, text="Kullanıcı Adı:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=20, pady=8, sticky="w")
        ent_k = tk.Entry(f_yonetim, font=("Helvetica", 11), width=25)
        ent_k.grid(row=0, column=1, padx=20, pady=8)
        
        tk.Label(f_yonetim, text="Şifre:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=20, pady=8, sticky="w")
        ent_s = tk.Entry(f_yonetim, font=("Helvetica", 11), width=25)
        ent_s.grid(row=1, column=1, padx=20, pady=8)

        tk.Label(f_yonetim, text="Ad Soyad:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=20, pady=8, sticky="w")
        ent_a = tk.Entry(f_yonetim, font=("Helvetica", 11), width=25)
        ent_a.grid(row=2, column=1, padx=20, pady=8)
        
        tk.Label(f_yonetim, text="Yetki Rolü:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=20, pady=8, sticky="w")
        cmb_rol = ttk.Combobox(f_yonetim, values=["öğrenci", "personel", "yönetici"], state="readonly", font=("Helvetica", 11), width=23)
        cmb_rol.current(0)
        cmb_rol.grid(row=3, column=1, padx=20, pady=8)
        
        btn_f = tk.Frame(f_yonetim, bg="#FFFFFF")
        btn_f.grid(row=4, column=0, columnspan=2, pady=20)
        
        def btn_usr_ekle():
            d, m = kullanici_ekle(ent_k.get().strip(), ent_s.get().strip(), ent_a.get().strip(), cmb_rol.get())
            messagebox.showinfo("Sonuç", m) if d else messagebox.showerror("Hata", m)

        def btn_usr_guncelle():
            k_adi = ent_k.get().strip()
            if not k_adi:
                messagebox.showerror("Hata", "Lütfen işlem yapılacak kullanıcı adını girin!")
                return
            d, m = kullanici_guncelle(k_adi, ent_s.get().strip(), ent_a.get().strip(), cmb_rol.get())
            messagebox.showinfo("Sonuç", m) if d else messagebox.showerror("Hata", m)

        def btn_usr_sil():
            k_adi = ent_k.get().strip()
            if k_adi == self.aktif_kullanici:
                messagebox.showerror("Hata", "Kendi yönetici hesabınızı silemezsiniz!")
                return
            d, m = kullanici_sil(k_adi)
            messagebox.showinfo("Sonuç", m) if d else messagebox.showerror("Hata", m)

        tk.Button(btn_f, text="Ekle", command=btn_usr_ekle, bg=BTN_BLUE, font=("Helvetica", 10, "bold"), width=10).pack(side="left", padx=8)
        tk.Button(btn_f, text="Güncelle", command=btn_usr_guncelle, bg=BTN_PINK, font=("Helvetica", 10, "bold"), width=10).pack(side="left", padx=8)
        tk.Button(btn_f, text="Sil", command=btn_usr_sil, bg=BTN_RED, font=("Helvetica", 10, "bold"), width=10).pack(side="left", padx=8)

if __name__ == "__main__":
    root = tk.Tk()
    app = KutuphaneUygulamasi(root)
    root.mainloop()
