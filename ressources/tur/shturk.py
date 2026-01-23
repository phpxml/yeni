
import requests
import re
import json
import urllib3
import sys

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_stream():
    base_url = "[https://ciner-live.ercdn.net/showturk/](https://ciner-live.ercdn.net/showturk/)"
    target_url = "[https://www.showturk.com.tr/canli-yayin](https://www.showturk.com.tr/canli-yayin)"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(target_url, verify=False, timeout=15, headers=headers)
        if response.status_code != 200:
            return

        site_content = response.text
        match = re.search(r"data-hope-video='(.*?)'", site_content, re.DOTALL)

        if match:
            json_data_raw = match.group(1)
            json_data_valid = json_data_raw.replace("\\/", "/")
            ht_data = json.loads(json_data_valid)

            m3u8_list = ht_data.get('media', {}).get('m3u8', [])
            ht_stream_m3u8 = m3u8_list[0].get('src') if m3u8_list else None

            if ht_stream_m3u8:
                content_response = requests.get(ht_stream_m3u8, timeout=10)
                if content_response.status_code == 200:
                    lines = content_response.text.split("\n")
                    modified_content = []

                    for line in lines:
                        if line.startswith("showturk"):
                            modified_content.append(base_url + line)
                        else:
                            modified_content.append(line)

                    # Çıktıyı ekrana bas (Workflow bunu m3u8 dosyasına yazar)
                    print("\n".join(modified_content))
                
    except Exception as e:
        # Hata durumunda boş çıktı vererek workflow'un bozulmasını engeller
        sys.exit(0)

if __name__ == "__main__":
    get_stream()
