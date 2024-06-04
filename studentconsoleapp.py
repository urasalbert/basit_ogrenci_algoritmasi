import json
import os

class Ogrenci:
    def __init__(self, isim, soyisim, kayit_yili, ogretim_turu_kodu, bolum, ogrenci_numarasi=None):
        self.isim = isim
        self.soyisim = soyisim
        self.kayit_yili = kayit_yili
        self.ogretim_turu_kodu = ogretim_turu_kodu
        self.bolum = bolum
        self.ogrenci_numarasi = ogrenci_numarasi

def verileri_yukle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ogrenciler.json")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Ogrenci(**ogrenci) for ogrenci in data]
    return []

def verileri_kaydet(ogrenciler):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ogrenciler.json")

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump([ogrenci.__dict__ for ogrenci in ogrenciler], file, ensure_ascii=False, indent=4)

    print(f"Veriler {file_path} konumuna kaydedildi.")

def yeni_ogrenci_ekle(ogrenciler):
    isim = input("İsim: ").strip()
    if not isim.isalpha():
        print("İsim sadece harflerden oluşmalıdır.")
        return

    soyisim = input("Soyisim: ").strip()
    if not soyisim.isalpha():
        print("Soyisim sadece harflerden oluşmalıdır.")
        return

    kayit_yili = input("Kayıt Yılı (4 haneli): ").strip()
    if not kayit_yili or len(kayit_yili) != 4 or not kayit_yili.isdigit():
        print("Geçersiz kayıt yılı.")
        return

    uc_haneli_kayit_yili = kayit_yili[1:4]

    ogretim_turu_input = input("Öğretim Türü (1: İlk Öğretim, 2: İkinci Öğretim): ").strip()
    if ogretim_turu_input not in ['1', '2']:
        print("Geçersiz öğretim türü.")
        return

    ogretim_turu_kodu = "122" if ogretim_turu_input == '1' else "223"

    bolumler = [
        "Bilgisayar Mühendisliği", "Tıp", "Hukuk", "Mühendislik",
        "İşletme", "İktisat", "Eğitim", "Güzel Sanatlar", "Dil Bilimleri"
    ]

    for i, bolum in enumerate(bolumler, 1):
        print(f"{i}. {bolum}")

    bolum_secim = input("Bölüm: ").strip()
    if not bolum_secim.isdigit() or int(bolum_secim) not in range(1, len(bolumler) + 1):
        print("Geçersiz bölüm.")
        return

    bolum = bolumler[int(bolum_secim) - 1]

    ogrenciler.append(Ogrenci(isim, soyisim, uc_haneli_kayit_yili, ogretim_turu_kodu, bolum))
    print("Öğrenci eklendi.")

def mevcut_ogrencileri_goruntule(ogrenciler):
    if not ogrenciler:
        print("Görüntülenecek öğrenci yok.")
        return

    ogrenciler.sort(key=lambda x: (x.kayit_yili, x.ogretim_turu_kodu))

    for i, ogrenci in enumerate(ogrenciler):
        ogrenci_sira = str(i + 1).zfill(3)
        ogrenci.ogrenci_numarasi = f"{ogrenci.kayit_yili}{ogrenci.ogretim_turu_kodu}{ogrenci_sira}"

        print(f"İsim: {ogrenci.isim}, Soyisim: {ogrenci.soyisim}, Bölüm: {ogrenci.bolum}, Öğrenci Numarası: {ogrenci.ogrenci_numarasi}")

def ogrenci_ara(ogrenciler):
    print("Arama Kriteri Seçiniz:")
    print("1. İsim")
    print("2. Soyisim")
    print("3. Bölüm")
    print("4. Kayıt Yılı")
    kriter = input("Seçiminiz: ").strip()

    deger = input("Arama Değeri: ").strip()

    sonuc = [ogrenci for ogrenci in ogrenciler if
             (kriter == '1' and deger.lower() in ogrenci.isim.lower()) or
             (kriter == '2' and deger.lower() in ogrenci.soyisim.lower()) or
             (kriter == '3' and deger.lower() in ogrenci.bolum.lower()) or
             (kriter == '4' and deger in ogrenci.kayit_yili)]

    for ogrenci in sonuc:
        print(f"İsim: {ogrenci.isim}, Soyisim: {ogrenci.soyisim}, Bölüm: {ogrenci.bolum}, Öğrenci Numarası: {ogrenci.ogrenci_numarasi}")

def ogrenci_guncelle(ogrenciler):
    numara = input("Güncellemek istediğiniz öğrencinin numarasını girin: ").strip()

    ogrenci = next((o for o in ogrenciler if o.ogrenci_numarasi == numara), None)
    if ogrenci is None:
        print("Öğrenci bulunamadı.")
        return

    yeni_isim = input("Yeni İsim (boş geçmek için Enter'a basın): ").strip()
    if yeni_isim and not yeni_isim.isalpha():
        print("İsim sadece harflerden oluşmalıdır.")
        return
    if yeni_isim:
        ogrenci.isim = yeni_isim

    yeni_soyisim = input("Yeni Soyisim (boş geçmek için Enter'a basın): ").strip()
    if yeni_soyisim and not yeni_soyisim.isalpha():
        print("Soyisim sadece harflerden oluşmalıdır.")
        return
    if yeni_soyisim:
        ogrenci.soyisim = yeni_soyisim

    yeni_bolum = input("Yeni Bölüm (boş geçmek için Enter'a basın): ").strip()
    if yeni_bolum:
        ogrenci.bolum = yeni_bolum

    print("Öğrenci bilgileri güncellendi.")

def ogrenci_sil(ogrenciler):
    numara = input("Silmek istediğiniz öğrencinin numarasını girin: ").strip()

    ogrenci = next((o for o in ogrenciler if o.ogrenci_numarasi == numara), None)
    if ogrenci is None:
        print("Öğrenci bulunamadı.")
        return

    ogrenciler.remove(ogrenci)
    print("Öğrenci silindi.")

def main():
    ogrenciler = verileri_yukle()

    while True:
        print("1. Yeni Öğrenci Ekle")
        print("2. Mevcut Öğrencileri Görüntüle")
        print("3. Öğrenci Ara")
        print("4. Öğrenci Güncelle")
        print("5. Öğrenci Sil")
        print("6. Verileri Kaydet ve Çıkış")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            yeni_ogrenci_ekle(ogrenciler)
        elif secim == "2":
            mevcut_ogrencileri_goruntule(ogrenciler)
        elif secim == "3":
            ogrenci_ara(ogrenciler)
        elif secim == "4":
            ogrenci_guncelle(ogrenciler)
        elif secim == "5":
            ogrenci_sil(ogrenciler)
        elif secim == "6":
            verileri_kaydet(ogrenciler)
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
