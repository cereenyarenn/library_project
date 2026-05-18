**library_project**

Bu proje, İzmir Bakırçay Üniversitesi Bilgisayar Mühendisliği Bölümü BIL1203 Mühendislikte Proje Yönetimi dersi kapsamında geliştirilmiş konsol tabanlı bir Kütüphane Envanter Yönetim Sistemidir.

Sistem: kütüphanedeki kitapların dijital ortamda takip edilmesini, kullanıcı yetkilendirmelerini (yönetici, personel, öğrenci) ve envanterin güvenli bir şekilde kalıcı dosyalarda (JSON) saklanmasını amaçlamaktadır.

**Özellikler**

**İş Paketi 1: Kullanıcı Girişi ve Yetkilendirme**
- Giriş Sistemi: Yönetici, personel ve öğrenci rolleriyle sisteme güvenli giriş yapılması.
- Erişim Kontrolü: Kullanıcı türüne (rolüne) göre sistemdeki yetkilerin ve menülerin kısıtlanması.

**İş Paketi 2 ve 5: Kitap Yönetimi ve Arama**
- Kitap Ekleme: ISBN, kitap adı, yazar, yayınevi, yayın yılı, stok ve raf konumu bilgileriyle sisteme yeni kitap kaydı.
- Kitap Silme ve Güncelleme: Eşsiz ISBN numarası üzerinden mevcut kitapların bilgilerini düzenleme veya envanterden çıkarma.
- Gelişmiş Arama: Kullanıcının girdiği anahtar kelimeye göre hem kitap adında hem de yazar adında çok kriterli filtreleme.
- Listeleme: Kütüphanedeki tüm kitapların envanter özetini görüntüleme.

**İş Paketi 3: Kullanıcı Yönetimi**
- Kullanıcı İşlemleri: Sisteme yeni kullanıcı ekleme, silme ve bilgilerini güncelleme.
- Rol Bazlı Yapı: Kullanıcıları yönetici, personel ve öğrenci yetki düzeylerine göre kategorize etme.

**İş Paketi 4: Ödünç Alma ve İade İşlemleri**
- İşlem Takibi: Kitap ödünç alma ve iade etme süreçlerinin yönetilmesi.
- Gecikme Yönetimi: Ödünç alma süresi, iade tarihi ve geciken kitapların sistem üzerinden takibi.

**İş Paketi 6: Raporlama ve İstatistikler**
- Envanter Özeti: Kütüphanenin genel durumunun raporlanması.
- Analiz: Popüler kitapların ve gecikmiş iadelerin istatistiksel olarak listelenmesi.

**Kullanılan Teknolojiler:**
- Programlama Dili: Python 3
- Veri Saklama: JSON
- Geliştirme Ortamı: VS Code ve OrbStack

**Geliştirici Ekip:**
- Ceren Yaren
- Ece Yiğit
- Emir Küçük
- Emir Nadiroğlu
