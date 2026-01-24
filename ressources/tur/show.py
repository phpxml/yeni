import requests
import re
import json
import urllib3

base_url = "[https://ciner.daioncdn.net/showtv/](https://ciner.daioncdn.net/showtv/)"

urllib3.disable_warnings()

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': '[https://www.showtv.com.tr/](https://www.showtv.com.tr/)'
    }

    try:
        response = requests.get(
            "[https://www.showtv.com.tr/canli-yayin](https://www.showtv.com.tr/canli-yayin)",
            headers=headers,
            verify=False,
            timeout=15
        )

        if response.status_code == 200:
            match = re.search(r'data-hope-video=["\'](.*?)["\']', response.text, re.DOTALL)

            if match:
                json_data_raw = match.group(1)
                json_data_valid = json_data_raw.replace("\\/", "/")
                ht_data = json.loads(json_data_valid)
                
                m3u8_list = ht_data.get('media', {}).get('m3u8', [])
                ht_stream_m3u8 = m3u8_list[0].get('src') if m3u8_list else None

                if ht_stream_m3u8:
                    content_response = requests.get(ht_stream_m3u8, headers=headers, timeout=10)

                    if content_response.status_code == 200:
                        lines = content_response.text.split("\n")
                        output = []

                        for line in lines:
                            line = line.strip()
                            if line.startswith("showtv"):
                                output.append(base_url + line)
                            elif line:
                                output.append(line)

                        print("\n".join(output))
    except:
        pass

if __name__ == "__main__":
    main()
