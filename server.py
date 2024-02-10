from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import json
from main import *

Jarvis = JarvisAI()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # get the content length of the post request
        content_length = int(self.headers['Content-Length'])

        # read the post data
        post_data = self.rfile.read(content_length)

        # decode the post data from bytes to string
        post_data = post_data.decode('utf-8')

        # parse the post data as a JSON object
        post_data = json.loads(post_data)

        # get the message text from the JSON object
        message_text = post_data['message']

        # send the message text to your chatbot and get the response
        sentence = str(message_text)

        ResponseOutput = Jarvis.say(sentence)
        with open("short_term_memory/current_class.json", "r") as file:
            intent_class = json.load(file)

        # Create a response JSON object
        response_data = {
            'response': ResponseOutput,
            'intent_class': intent_class
        }

        # Convert the response JSON object to a JSON string
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
