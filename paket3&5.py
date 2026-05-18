import json

#3. soru
def kullanici_ekle(kullanici_adi, sifre, ad_soyad, rol):
    try:
        with open("kullanicilar.json", "r", encoding="utf-8") as dosya:
            kullanicilar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        kullanicilar = [] 
    bilgi = {
        "kullanici_adi": kullanici_adi,
        "sifre": sifre,
        "ad_soyad": ad_soyad,
        "rol": rol
    }
    kullanicilar.append(bilgi)
    with open("kullanicilar.json", "w", encoding="utf-8") as dosya:
        json.dump(kullanicilar, dosya, ensure_ascii=False, indent=4)   
    print(f"'{kullanici_adi}' adlı kullanıcı sisteme başarıyla eklendi.")


def kullanici_silme(silinecek_kullanici_adi):
    try:
        with open("kullanicilar.json", "r", encoding="utf-8") as dosya:
            kullanicilar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        kullanicilar = []
    silindi_mi = False
    guncel_kullanicilar = []
    for kullanici in kullanicilar:
        mevcut_kullanici = kullanici["kullanici_adi"]
        if mevcut_kullanici != silinecek_kullanici_adi:
            guncel_kullanicilar.append(kullanici)
        else:
            silindi_mi = True      
    with open("kullanicilar.json", "w", encoding="utf-8") as dosya:
        json.dump(guncel_kullanicilar, dosya, ensure_ascii=False, indent=4) 
    if silindi_mi:
        print(f"'{silinecek_kullanici_adi}' kullanıcı adlı kişi başarıyla silindi.")
    else:
        print(f"'{silinecek_kullanici_adi}' adlı kullanıcı bulunamadı.")


def kullanici_guncelleme(guncellenecek_kullanici_adi, yeni_sifre, yeni_ad_soyad, yeni_rol):
    try:
        with open("kullanicilar.json", "r", encoding="utf-8") as dosya:
            kullanicilar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        kullanicilar = []
    guncellendi_mi = False
    for kullanici in kullanicilar:
        mevcut_kullanici = kullanici["kullanici_adi"].strip().replace(" ", "")
        hedef_kullanici = guncellenecek_kullanici_adi.strip().replace(" ", "")
        if mevcut_kullanici == hedef_kullanici:
            kullanici["sifre"] = yeni_sifre
            kullanici["ad_soyad"] = yeni_ad_soyad
            kullanici["rol"] = yeni_rol
            guncellendi_mi = True
            break
            
    with open("kullanicilar.json", "w", encoding="utf-8") as dosya:
        json.dump(kullanicilar, dosya, ensure_ascii=False, indent=4)  
    if guncellendi_mi:
        print(f"'{guncellenecek_kullanici_adi}' adlı kullanıcının bilgileri güncellendi.")
    else:
        print(f"'{guncellenecek_kullanici_adi}' adlı kullanıcı bulunamadı.")



#5. soru
def kitap_arama(aranan_kitap):
    bulundu_mu = False
    print(f"\n'{aranan_kitap}' İçin Arama Sonuçları")
    
    try:
        with open("kitaplar.json", "r", encoding="utf-8") as dosya:
            raflar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Kütüphane sistemi boş (Kitaplar dosyası bulunamadı).")
        return
        
    for raf in raflar:
        kitap_isim = raf["isim"].lower()
        yazar_isim = raf["yazar"].lower()
        aranan = aranan_kitap.lower()
        if (aranan in kitap_isim) or (aranan in yazar_isim):
            print(f"ISBN: {raf['isbn']}")
            print(f"İsim: {raf['isim']}")
            print(f"Yazar: {raf['yazar']}")
            print(f"Yayınevi: {raf['yayinevi']}")
            print(f"Yayın Yılı: {raf['yayinyili']}")
            print(f"Stok: {raf['stok']}")
            print(f"Raf Konumu: {raf['konum']}")
            print("-" * 30)
            bulundu_mu = True
            
    if not bulundu_mu:
        print("Aranan kriterlere uygun kitap bulunamadı.")


def kitap_listele():
    print("\nKütüphanedeki Tüm Kitaplar")
    
    try:
        with open("kitaplar.json", "r", encoding="utf-8") as dosya:
            raflar = json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Kütüphane sistemi boş (Kitaplar dosyası bulunamadı).")
        return
        
    if len(raflar) == 0:
        print("Kütüphanede şu an hiç kitap bulunmuyor.")
    else:
        for raf in raflar:
            print(f"ISBN: {raf['isbn']} | İsim: {raf['isim']} | Yazar: {raf['yazar']} | Stok: {raf['stok']}")
