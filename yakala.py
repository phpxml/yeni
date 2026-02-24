import requests
import re

def star_yakala():
    # Ahmet'in Star TV gizli mutfağı
    url = "https://www.elahmad.com/tv/live/channels.php?id=83"
    
    # Ahmet'i kandırmak için gerçek bir tarayıcı gibi davranıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.elahmad.com/tv/canli-tv-live.php'
    }
    
    try:
        print("Star TV sayfasına gidiliyor...")
        response = requests.get(url, headers=headers, timeout=15)
        
        # Sayfa kodunun içinde imzayı arıyoruz
        # Ahmet ne kadar tam ekran yapsa da bu kod metni okur
        match = re.search(r'wmsAuthSign=([a-zA-Z0-9%=\-_&\.]+)', response.text)
        
        if match:
            token = match.group(0) # 'wmsAuthSign=...' kısmını alır
            # Tincat'ten aldığın sabit BozzTV link yapısı
            star_link = f"https://tgn.bozztv.com/gin-trn09/gin-startv/index.m3u8?{token}"
            
            # IPTV listenin içine yazıyoruz
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, Star TV\n{star_link}\n")
            print("BAŞARILI: Star TV imzası tazelendi ve liste.m3u dosyasına yazıldı.")
        else:
            print("HATA: İmza sayfa kaynağında bulunamadı. Ahmet korumayı artırmış olabilir.")
            
    except Exception as e:
        print(f"BAĞLANTI HATASI: {e}")

if __name__ == "__main__":
    star_yakala()
