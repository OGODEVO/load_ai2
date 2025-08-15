from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import time

class SimpleNode(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Simulate processing time
        time.sleep(0.5)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "success", "node": self.server.server_address}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run_node(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleNode)
    print(f"Starting node on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    ports = [8001, 8002, 8003, 8004, 8005]
    threads = []
    for port in ports:
        thread = threading.Thread(target=run_node, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
