#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import config

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def _set_headers(s):
            s.send_response(200)
            s.send_header('Content-type', 'text/html')
            s.end_headers()
  def do_GET(s):
        
        def home_page(s):
            s._set_headers()
            message = ('''
            <!doctype html>
            <html>
            <a href = "/forum"> forum </a>
            <h1>Tal</h1>
            </html>
            ''')
            s.wfile.write(bytes(message, "utf8"))

        def forum_home(s):
            s._set_headers()
            message = '''
            <!doctype html>
            <html>
            <ol>
            '''
            posts = config.top_theme_db()
            for x in posts:
                message+="<li><a href = '/%s'>%s</li>"%(x[0], x[0])
            message+='''
            </ol>
            </html>
            '''
            s.wfile.write(bytes(message, "utf8"))
        if s.path == "/":
            print(home_page(s))
        elif s.path == "/forum":
            print(forum_home(s))
        else:
            s.send_error(404, "Nic tu nie ma", "Zły adres strony")
        
 
def run():
  config.create_db_connection("_db/forum.sqlite")  
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()