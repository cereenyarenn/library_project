import json
import datetime

# Dosya isimleri
DOSYA_KITAPLAR = "kitaplar.json"
DOSYA_KULLANICILAR = "kullanicilar.json"
DOSYA_ODUNCLER = "oduncler.json"

def json_oku(dosya_adi, varsayilan_tip=dict):
    """Dosyayı güvenli bir şekilde açar, hata durumunda varsayılan tipi döner."""
    try:
        # encoding="utf-8" Türkçe karakterlerin doğru okunmasını sağlar
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return varsayilan_tip()

def kutuphane_raporu_olustur():
    # 1. Veri Dosyalarını Yükle
    kitaplar = json_oku(DOSYA_KITAPLAR)
    kullanicilar = json_oku(DOSYA_KULLANICILAR)
    oduncler = json_oku(DOSYA_ODUNCLER)
    bugun = datetime.date.today()

    # 2. Temel Sayaçlar ve Değişkenler
    toplam_kitap_cesidi = len(kitaplar)
    toplam_stok_miktari = sum(int(k.get("stok", 0)) for k in kitaplar.values())
    toplam_kullanici = len(kullanicilar)
    
    aktif_odunc_sayisi = 0
    kitap_odunc_skorlari = {}  # Hangi ISBN kaç kez ödünç alındı?
    gecikmis_iadeler = []

    # 3. Ödünç Geçmişi ve Gecikme Analizi
    for islem_id, veri in oduncler.items():
        isbn = veri.get("isbn")
        
        # Popüler kitap istatistiği için her ödünç kaydını sayıyoruz
        kitap_odunc_skorlari[isbn] = kitap_odunc_skorlari.get(isbn, 0) + 1

        # Gecikme analizi sadece iade edilmemiş (aktif) kitaplar için geçerlidir
        if veri.get("durum") == "aktif":
            aktif_odunc_sayisi += 1
            try:
                # Verilen iade tarihini tarih nesnesine çevir (YYYY-MM-DD)
                iade_tarihi = datetime.date.fromisoformat(veri.get("iade_tarihi"))
                
                # Eğer iade tarihi bugünden önceyse süre geçmiş demektir
                if iade_tarihi < bugun:
                    gecikme_gunu = (bugun - iade_tarihi).days
                    gecikmis_iadeler.append({
                        "kullanici": veri.get("kullanici"),
                        "isbn": isbn,
                        "kitap_adi": kitaplar.get(isbn, {}).get("ad", "Bilinmeyen Kitap"),
                        "gecikme": gecikme_gunu
                    })
            except (ValueError, TypeError):
                pass

    # Popülerlik skorlarını çoktan aza doğru sırala
    sirali_populerlik = sorted(kitap_odunc_skorlari.items(), key=lambda x: x[1], reverse=True)


    # ================= TERMINAL RAPOR ÇIKTISI =================
    
    print("=" * 60)
    print(f"KÜTÜPHANE ENVANTER VE İSTATİSTİK RAPORU ({bugun})")
    print("=" * 60)
    
    # Bölüm 1: Genel Durum
    print("\n[1] GENEL SİSTEM ÖZETİ")
    print(f" - Toplam Benzersiz Kitap Çeşidi : {toplam_kitap_cesidi}")
    print(f" - Raflardaki Toplam Stok Adedi  : {toplam_stok_miktari}")
    print(f" - Sisteme Kayıtlı Üye Sayısı    : {toplam_kullanici}")
    print(f" - Okuyuculardaki Aktif Ödünç    : {aktif_odunc_sayisi}")
    
    # Bölüm 2: Popüler Kitaplar
    print("\n[2] EN POPÜLER KİTAPLAR (En Çok Ödünç Alınan İlk 5)")
    if sirali_populerlik:
        sira = 1
        for isbn, adet in sirali_populerlik[:5]:
            kitap_adi = kitaplar.get(isbn, {}).get("ad", "Bilinmeyen Kitap")
            print(f"  {sira}. {kitap_adi:<30} (ISBN: {isbn}) -> {adet} kez")
            sira += 1
    else:
        print("  - Henüz ödünç alınmış bir kitap kaydı bulunmuyor.")

    # Bölüm 3: Gecikmiş İadeler
    print("\n[3] GECİKMİŞ İADELER (Süresi Geçen Aktif Ödünçler)")
    if gecikmis_iadeler:
        for g in gecikmis_iadeler:
            print(f"  * Kullanıcı: {g['kullanici']:<10} | Kitap: {g['kitap_adi'][:25]:<25} | {g['gecikme']} Gün Gecikti!")
    else:
        print("  - Süresi geçmiş veya gecikmiş iade bulunmuyor.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    kutuphane_raporu_olustur()