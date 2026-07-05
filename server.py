#!/usr/bin/env python3
"""
Simple HTTP Server for ZKAS Website
Serves the website on http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
ZKAS_DIR = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        return super().end_headers()

if __name__ == '__main__':
    os.chdir(ZKAS_DIR)
    
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print("🌐 ZKAS Website Server Running")
        print("=" * 60)
        print(f"\n✓ Server URL: {url}")
        print(f"✓ Press Ctrl+C to stop\n")
        
        try:
            webbrowser.open(url)
            print("Opening browser...\n")
        except:
            print("Please open your browser and go to: " + url + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped")
            print("=" * 60)
