import requests
import urllib3

urllib3.disable_warnings()

def main():
    base_url = "https://ciner.daioncdn.net/showtv/"
    master_url = "https://ciner.daioncdn.net/showtv/showtv.m3u8"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(master_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            lines = response.text.split("\n")
            output = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith("showtv"):
                    output.append(base_url + line)
                else:
                    output.append(line)
            
            print("\n".join(output))
        else:
            print("#EXTM3U")
            print("#EXT-X-STREAM-INF:BANDWIDTH=1200000,RESOLUTION=1280x720")
            print("https://ciner.daioncdn.net/showtv/showtv_720p.m3u8")

    except:
        print("#EXTM3U")
        print("https://ciner.daioncdn.net/showtv/showtv_720p.m3u8")

if __name__ == "__main__":
    main()
