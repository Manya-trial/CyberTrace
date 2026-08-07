import requests
import time

API_KEY = "7d9cae9e84191a6334c4313bc816bfaf7c085d08374c3aacf634994ceafb081e"

def scan_url(url):
    try:
        headers = {"x-apikey": API_KEY}

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )
        result = response.json()
        scan_id = result['data']['id']

        time.sleep(3)

        analysis = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{scan_id}",
            headers=headers
        ).json()

        stats = analysis['data']['attributes']['stats']
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        harmless = stats.get('harmless', 0)
        undetected = stats.get('undetected', 0)
        total = malicious + suspicious + harmless + undetected

        verdict = "DANGEROUS" if malicious > 2 else \
                  "SUSPICIOUS" if malicious > 0 or suspicious > 0 else "SAFE"

        return {
            'url': url,
            'verdict': verdict,
            'malicious': malicious,
            'suspicious': suspicious,
            'harmless': harmless,
            'total_engines': total,
            'status': 'success'
        }

    except Exception as e:
        return {'status': 'error', 'message': str(e)}