import json
import hashlib
import datetime


def kullanici_girisi(kullanici_adi, sifre):
    # json dosyasını okuyoruz
    dosya = open("kullanicilar.json", "r", encoding="utf-8")
    kullanicilar = json.load(dosya)
    dosya.close()

   # güvenlik kısmı
    sifre_hash = hashlib.sha256(sifre.encode('utf-8')).hexdigest()

    if kullanici_adi in kullanicilar:
        if kullanicilar[kullanici_adi]["sifre_hash"] == sifre_hash:
            rol = kullanicilar[kullanici_adi]["rol"]
            print("Giriş başarılı!")
            return True, rol
        else:
            #hata çıkarsa bu komutla kontrol ediyoruz print("Yanlış şifre girdin.")
            return False, None
    else:
       #hata çıkarsa bu komutla kontrol ediyoruz print("Böyle bir kullanıcı yok.")
        return False, None


def kitap_odunc_al(kullanici_adi, isbn):
    # kitapları aç
    f = open("kitaplar.json", "r", encoding="utf-8")
    kitaplar = json.load(f)
    f.close()

    if isbn in kitaplar:
        if kitaplar[isbn]["stok"] > 0:
            # stoku 1 azalt
            kitaplar[isbn]["stok"] = kitaplar[isbn]["stok"] - 1 
            
            # ödünç dosyasını aç
            f2 = open("oduncler.json", "r", encoding="utf-8")
            oduncler = json.load(f2)
            f2.close()

            # 15 gün süre veriyoruz
            bugun = datetime.datetime.now()
            iade_tarihi = bugun + datetime.timedelta(days=15)
            
            # islem idsini birleştirdim kolay olsun diye
            islem_id = kullanici_adi + "_" + isbn 

            oduncler[islem_id] = {
                "kullanici": kullanici_adi,
                "isbn": isbn,
                "verilen_tarih": str(bugun.date()),
                "iade_tarihi": str(iade_tarihi.date()),
                "durum": "aktif"
            }

            # dosyaları kaydediyoruz
            f3 = open("kitaplar.json", "w", encoding="utf-8")
            json.dump(kitaplar, f3, indent=4)
            f3.close()

            f4 = open("oduncler.json", "w", encoding="utf-8")
            json.dump(oduncler, f4, indent=4)
            f4.close()
            
           # hata çıkarsa bu komutla kontrol ediyoruz print("Kitap verildi.")
            return islem_id
        else:
            # hata çıkarsa bu komutla kontrol ediyoruz print("Kitap kalmamış.")
            return None
    else:
      #hata çıkarsa bu komutla kontrol ediyoruz  print("Kütüphanede bu kitap yok.")
        return None

def kitap_iade_et(islem_id):
    # kayıtları aç
    dosya = open("oduncler.json", "r", encoding="utf-8")
    oduncler = json.load(dosya)
    dosya.close()

    if islem_id in oduncler:
        if oduncler[islem_id]["durum"] == "aktif":
            oduncler[islem_id]["durum"] = "iade_edildi"
            
            # kitabı bulup stoku geri ekliyoruz
            isbn = oduncler[islem_id]["isbn"]
            
            dosya2 = open("kitaplar.json", "r", encoding="utf-8")
            kitaplar = json.load(dosya2)
            dosya2.close()

            kitaplar[isbn]["stok"] = kitaplar[isbn]["stok"] + 1

            # dosyaları tekrar yaz
            dosya3 = open("kitaplar.json", "w", encoding="utf-8")
            json.dump(kitaplar, dosya3, indent=4)
            dosya3.close()

            dosya4 = open("oduncler.json", "w", encoding="utf-8")
            json.dump(oduncler, dosya4, indent=4)
            dosya4.close()

            # hata çıkarsa bu komutla kontrol ediyoruz print("Kitap başarıyla iade alındı.")
            return True
        else:
           # hata çıkarsa bu komutla kontrol ediyoruz print("Bu kitap zaten iade edilmiş.")
            return False
    else:
       # hata çıkarsa bu komutla kontrol ediyoruz print("Böyle bir işlem bulunamadı.")
        return False