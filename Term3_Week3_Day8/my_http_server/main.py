import http.server
import socketserver

class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": "home.html",
            "/anythingyouwant": "greeting.py"
        }
        
        try:
            self.path = routes[self.path]
        except:
            self.path = "404.html"

        return super().do_GET()

        
PORT = 8000
Handler = CustomRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()