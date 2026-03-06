from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json

# --- SABİT KİMLİK BİLGİLERİ ---
SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"
USER_AGENT = "Instagram 269.1.0.18.231 Android (33/13.0; 450dpi; 1080x2340; samsung; SM-S911B; galaxy s23; qcom; en_US; 443213142)"

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
            message_text = data.get('message', 'Selam! Bu otomatik bir mesajdır.') # Panelden mesaj gelmezse bu gider

            cl = Client()
            cl.request_timeout = 9 # Vercel limitine yakın ama güvenli
            
            # Instagram'ı kandırma katmanı
            cl.set_user_agent(USER_AGENT)
            
            # SIZMA OPERASYONU
            cl.login_by_sessionid(SESSION_ID)
            
            # 1. ADIM: Hedef Kullanıcıyı Bul
            user_id = cl.user_id_from_username(target)
            
            # 2. ADIM: Takip Et
            cl.user_follow(user_id)
            
            # 3. ADIM: Mesaj Gönder (DM)
            # İstersen buraya küçük bir bekleme ekleyebilirsin: import time; time.sleep(1)
            cl.direct_send(message_text, [user_id])
            
            res_msg = f"@{target} takibe alındı ve mesaj gönderildi!"
            self._send_response(200, {"status": "success", "message": res_msg})

        except Exception as e:
            # Hata detayını temizle ve gönder
            error_detail = str(e)
            if "Expecting value" in error_detail:
                error_detail = "Instagram bağlantıyı kesti (IP Engeli). Lütfen 5 dk sonra tekrar dene."
            
            self._send_response(500, {"status": "error", "message": f"Hata: {error_detail}"})

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
