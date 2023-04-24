import pathlib
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import json
import socket


BASE_DIR = pathlib.Path()
BUFFER_SIZE = 1024



class MyHTTPHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        print(route)
        match route.path:
            case "/":
               self.send_html('C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\\web_socket_module_4\\front-init\\index.html')
            case "/message":
               self.send_html('C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\web_socket_module_4\\front-init\\message.html')
            case _:
                print('ROUTE:', BASE_DIR / route.path[1:])
                file_path = BASE_DIR / route.path[1:]
                print(file_path.exists())
                if file_path.exists():
                    self.send_static(file_path)
                else:
                    self.send_html('C:\\Users\\Oleg\OneDrive\\GOIT_cloud\\web_socket_module_4\\front-init\\error.html', 404)
     
    def do_POST(self):
        # self.send_html('C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\web_socket_module_4\\front-init\\message.html')
        
        body = self.rfile.read(int(self.headers['Content-Length'])) 
        body = urllib.parse.unquote_plus(body.decode()) # пробирає пробіли
        payload = {key: value for key, value in [el.split('=') for el in body.split('&')]}
        with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as fd:
            json.dump(payload, fd, ensure_ascii=False)
       
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
                                 
        
    def send_html(self, filename, status_code=200): 
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())
            
    
    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
             self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain'
                             )
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())
     
     
def save_data_from_http_server( data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    dict_parse = {key: value for key, value in [el.split('=' for el in parse_data.split('&'))] }    
        

def run_socket_server(host, port):
    # host = '127.0.0.1'
    # port = 5000

    s_socket = socket.socket()
    s_socket.bind((host, port))
    s_socket.listen(1)

    # conn, addr = s_socket.accept()
    # print(f"Connection from {addr}")
    try:
        while True:
            msg, address = s_socket.recvfrom(BUFFER_SIZE)
            save_data_from_http_server(msg)
    except KeyboardInterrupt:
        print('socket server stopped')
    finally:     
        s_socket.close()
    

def run(server=HTTPServer, handler=MyHTTPHandler):
    address = ('', 3000)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
            
            
if __name__ == '__main__':
   
    run()