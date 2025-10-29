#!/usr/bin/env python3
"""
Simple HTTP server with URL rewriting for clean URLs (no .html extension)
"""
import os
import http.server
import socketserver
from urllib.parse import unquote

PORT = 8080

class RewriteHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Decode the URL
        self.path = unquote(self.path)
        
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        # If path doesn't have an extension and file doesn't exist
        elif '.' not in os.path.basename(self.path):
            # Try adding .html extension
            html_path = self.path + '.html'
            if os.path.isfile(self.directory + html_path):
                self.path = html_path
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Add cache control headers for development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    handler = RewriteHTTPRequestHandler
    handler.directory = os.getcwd()
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Serving files from: {os.getcwd()}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


