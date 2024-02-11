from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import json
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        post_data = json.loads(post_data)
        message_text = post_data['message']
        sentence = str(message_text)
        os.system(f"./AI/classifier.out '{sentence}'")
        os.system(f"./AI/choose_response.out '{sentence}'")

        with open("short_term_memory/current_class.json", "r") as file:
            intent_class = json.load(file)
        
        with open("short_term_memory/output.txt", "r") as output:
            ResponseOutput = output.read()
        
        response_data = {
            'response': ResponseOutput,
            'intent_class': intent_class
        }

        response_json = json.dumps(response_data)
        response_bytes = response_json.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')  # Set content type to JSON
        self.send_header('Content-length', len(response_bytes))
        self.end_headers()

        self.wfile.write(response_bytes)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('8000')
    httpd.serve_forever()