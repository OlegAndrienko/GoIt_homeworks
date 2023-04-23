from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
import urllib.parse
import urllib.request
import mimetypes
import pathlib 


class HttpHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        pr_url = urllib.parse.urlparse(self.path) # отримали URL рядок
        
        #Робимо маршрутизацію по сторінках
        
        if pr_url.path == '/':
            self.send_html_file('C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\\web_socket_module_4\\front-init\\index.html')
        elif pr_url.path == '/message':
            self.send_html_file('C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\\web_socket_module_4\\front-init\\message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                print('Ok static')
                self.send_static()
            else:
                self.send_html_file(
                'C:\\Users\\Oleg\\OneDrive\\GOIT_cloud\\web_socket_module_4\\front-init\\error.html', 404)
      
            

    def send_html_file(self, filename, status=200):
        
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
            

    
    def send_static(self, filename=None, status=200):
        
        self.send_response(status)
        mt = mimetypes.guess_type(self.path)
        print(mt)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        filename = f'.{self.path}'
        with open(filename, 'rb') as fb:
            self.wfile.write(fb.read())
        
        
    def do_POST(self):
        
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        print('_________________')
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        print('_________________')
        data_dict = {key: value for key, value in [
            el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


    # def parse_form_data(self, data):

    #     raw_params = data.split('&')
    #     data = {key: value for key, value in [param.split('=') for param in raw_params]}

#

def run(server_class=HTTPServer, handler_class=HttpHandler): #server 
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
