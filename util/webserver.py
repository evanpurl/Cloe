import socketserver
from http.server import SimpleHTTPRequestHandler


def run():
    httpd = socketserver.TCPServer(('0.0.0.0', 25565), SimpleHTTPRequestHandler)
    httpd.serve_forever()
