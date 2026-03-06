from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import random

# --- GÜNCEL KİMLİK BİLGİLERİ ---
SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            target = data.get('target', '').replace('@', '').strip()
            message_text = data.get('message', 'Selam!')

            cl = Client()
            cl.request_timeout = 10
            
            # INSTAGRAM'I KANDIRAN TARAYICI BAŞLIKLARI (SENİN VERDİĞİN YAPI)
            cl.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36')
            
            # Ekstra Güvenlik Başlıkları
            headers = {
                "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "X-IG-App-ID": "936619743392459", # Gerçek Instagram Web App ID
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/",
                "Origin": "https://www.instagram.com"
            }
            cl.direct.headers.update(headers)

            # SIZMA VE GİRİŞ
            cl.login_by_sessionid(SESSION_ID)
            
            # Hız Sınırına Takılmamak İçin Hafif Rastgele Bekleme
            import time
            time.sleep(random.uniform(1, 3))

            # OPERASYON
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            cl.direct_send(message_text, [user_id])
            
            self._send_response(200, {"status": "success", "message": f"@{target} tamamlandı!"})

        except Exception as e:
            error_str = str(e)
            # Eğer IP engeli varsa veya boş dönüyorsa
            if "Expecting value" in error_str or "403" in error_str:
                self._send_response(429, {"status": "error", "message": "IP Limitine takıldık. Vercel projesini başka bir isimle tekrar açın (IP Değişimi için)."})
            else:
                self._send_response(500, {"status": "error", "message": f"Hata: {error_str}"})

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
