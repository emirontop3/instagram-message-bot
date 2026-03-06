from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json

SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"
USER_AGENT = "Instagram 269.1.0.18.231 Android (33/13.0; 450dpi; 1080x2340; samsung; SM-S911B; galaxy s23; qcom; en_US; 443213142)"

class handler(BaseHTTPRequestHandler):
    # Tarayıcıların güvenlik duvarını aşmak için CORS ayarları
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

            cl = Client()
            cl.request_timeout = 7 # 10 saniye limitine takılmamak için
            
            # Kimlik Bürüme ve Sızma
            cl.set_user_agent(USER_AGENT)
            cl.login_by_sessionid(SESSION_ID)
            
            # Operasyon
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            
            self._send_response(200, {"status": "success", "message": f"@{target} başarıyla takibe alındı!"})
        except Exception as e:
            self._send_response(500, {"status": "error", "message": f"Instagram Hatası: {str(e)}"})

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
