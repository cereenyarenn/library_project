import json
import customtkinter as ctk

JSON_DOSYASI = "kitaplar.json"

def json_oku():
    try:
        with open(JSON_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def json_yaz(veri):
    with open(JSON_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

class KitapYonetimModulu(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Kitap Envanter Yönetimi")
        self.geometry("450x600")
        
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#FFF0F5")
        
        self.ana_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ana_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.baslik_label = ctk.CTkLabel(self.ana_frame, text="Kitap Ekle / Güncelle / Sil", 
                                         font=("Helvetica", 20, "bold"), text_color="#5C88C4")
        self.baslik_label.pack(pady=(0, 20))

        self.entryler = {}
        alanlar = ["ISBN", "Ad", "Yazar", "Yayınevi", "Yayın Yılı", "Stok", "Konum"]
        
        for alan in alanlar:
            frame = ctk.CTkFrame(self.ana_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(frame, text=f"{alan}:", width=100, anchor="w", text_color="#333333", font=("Helvetica", 13, "bold"))
            lbl.pack(side="left")
            
            ent = ctk.CTkEntry(frame, width=250, border_color="#AEC6CF", fg_color="#FFFFFF", text_color="black")
            ent.pack(side="right", fill="x", expand=True)
            self.entryler[alan] = ent

        self.btn_frame = ctk.CTkFrame(self.ana_frame, fg_color="transparent")
        self.btn_frame.pack(pady=25)

        self.btn_ekle = ctk.CTkButton(self.btn_frame, text="Ekle", command=self.kitap_ekle, 
                                      fg_color="#FFB6C1", hover_color="#FF69B4", text_color="black", font=("Helvetica", 13, "bold"))
        self.btn_ekle.grid(row=0, column=0, padx=5)

        self.btn_guncelle = ctk.CTkButton(self.btn_frame, text="Güncelle", command=self.kitap_guncelle,
                                          fg_color="#AEC6CF", hover_color="#779ECB", text_color="black", font=("Helvetica", 13, "bold"))
        self.btn_guncelle.grid(row=0, column=1, padx=5)

        self.btn_sil = ctk.CTkButton(self.btn_frame, text="Sil", command=self.kitap_sil,
                                     fg_color="#FF9999", hover_color="#FF6666", text_color="black", font=("Helvetica", 13, "bold"))
        self.btn_sil.grid(row=0, column=2, padx=5)

        self.durum_label = ctk.CTkLabel(self.ana_frame, text="", font=("Helvetica", 13, "bold"))
        self.durum_label.pack(pady=10)

    def formu_temizle(self):
        for ent in self.entryler.values():
            ent.delete(0, 'end')

    def mesaj_goster(self, mesaj, renk):
        self.durum_label.configure(text=mesaj, text_color=renk)

    def kitap_ekle(self):
        isbn = self.entryler["ISBN"].get().strip()
        if not isbn:
            self.mesaj_goster("Hata: ISBN alanı zorunludur!", "red")
            return

        kitaplar = json_oku()
        if isbn in kitaplar:
            self.mesaj_goster("Hata: Bu ISBN zaten sistemde kayıtlı!", "red")
            return

        yeni_kitap = {
            "ad": self.entryler["Ad"].get().strip(),
            "yazar": self.entryler["Yazar"].get().strip(),
            "yayinevi": self.entryler["Yayınevi"].get().strip(),
            "yayin_yili": self.entryler["Yayın Yılı"].get().strip(),
            "stok": self.entryler["Stok"].get().strip(),
            "konum": self.entryler["Konum"].get().strip()
        }
        
        try:
            yeni_kitap["stok"] = int(yeni_kitap["stok"]) if yeni_kitap["stok"] else 0
            yeni_kitap["yayin_yili"] = int(yeni_kitap["yayin_yili"]) if yeni_kitap["yayin_yili"] else 0
        except ValueError:
            self.mesaj_goster("Hata: Stok ve Yayın Yılı rakamlardan oluşmalıdır!", "red")
            return

        kitaplar[isbn] = yeni_kitap
        json_yaz(kitaplar)
        
        self.mesaj_goster("Kitap başarıyla eklendi!", "green")
        self.formu_temizle()

    def kitap_guncelle(self):
        isbn = self.entryler["ISBN"].get().strip()
        if not isbn:
            self.mesaj_goster("Lütfen güncellenecek kitabın ISBN'ini girin!", "red")
            return

        kitaplar = json_oku()
        if isbn not in kitaplar:
            self.mesaj_goster("Hata: Sistemde bu ISBN'e ait kitap bulunamadı!", "red")
            return

        guncel_ad = self.entryler["Ad"].get().strip()
        guncel_yazar = self.entryler["Yazar"].get().strip()
        guncel_yayinevi = self.entryler["Yayınevi"].get().strip()
        guncel_yayin = self.entryler["Yayın Yılı"].get().strip()
        guncel_stok = self.entryler["Stok"].get().strip()
        guncel_konum = self.entryler["Konum"].get().strip()

        if guncel_ad: kitaplar[isbn]["ad"] = guncel_ad
        if guncel_yazar: kitaplar[isbn]["yazar"] = guncel_yazar
        if guncel_yayinevi: kitaplar[isbn]["yayinevi"] = guncel_yayinevi
        if guncel_konum: kitaplar[isbn]["konum"] = guncel_konum
        
        try:
            if guncel_yayin: kitaplar[isbn]["yayin_yili"] = int(guncel_yayin)
            if guncel_stok: kitaplar[isbn]["stok"] = int(guncel_stok)
        except ValueError:
            self.mesaj_goster("Hata: Stok ve Yayın Yılı rakamlardan oluşmalıdır!", "red")
            return

        json_yaz(kitaplar)
        self.mesaj_goster("Kitap bilgileri başarıyla güncellendi!", "green")
        self.formu_temizle()

    def kitap_sil(self):
        isbn = self.entryler["ISBN"].get().strip()
        if not isbn:
            self.mesaj_goster("Lütfen silinecek kitabın ISBN'ini girin!", "red")
            return

        kitaplar = json_oku()
        if isbn in kitaplar:
            del kitaplar[isbn] 
            json_yaz(kitaplar)
            self.mesaj_goster("Kitap sistemden başarıyla silindi!", "green")
            self.formu_temizle()
        else:
            self.mesaj_goster("Hata: Silinecek kitap bulunamadı!", "red")

if __name__ == "__main__":
    uygulama = KitapYonetimModulu()
    uygulama.mainloop()
