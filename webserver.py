from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import os
import sys
# import art


class base_case:
    '''Parent for case handlers.'''

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = f"'{full_path}' cannot be read: {msg}"
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    # def test(self, handler):
    #     assert False, 'Not implemented.' # empty to be overriden

    # def act(self, handler):
    #     assert False, 'Not implemented.' # empty to be overriden

class ServerException(Exception):
    pass

class case_no_file:
    '''File or directory does not exist.'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException(f"'{handler.full_path}' not found")



class case_existing_file(base_case):
    '''File exists.'''

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)

class case_directory_index_file:
    '''Serve index.html page for a directory.'''

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.handle_file(self.index_path(handler))


class case_directory_no_index_file(case_directory_index_file):
    '''Serve listing for a directory without an index.html page.'''

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.list_files_in_dir(handler.full_path)



class case_always_fail:
    '''Base case if nothing else worked.'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException(f"Unknown object '{handler.full_path}'")



class RequestHandler(BaseHTTPRequestHandler):

    # dynamicaly generated error pages

    Error_Page = """
        <html>
        <body>
        <h1>Error accessing {full_path}</h1>
        <p>{msg}</p>
        </body>
        </html>

        """
    Listing_Page = '''
        <html>
        <body>
        <h2>There is no index.html in this directory</h2>
        <p>Create an index.html file or click on any of the files to serve</p>
        <ul>
        {0}
        </ul>
        </body>
        </html>
        '''

    # Classify and handle request.
    Cases = [case_no_file(),case_existing_file(),
             case_directory_index_file(),
             case_directory_no_index_file(),
             case_always_fail()]

    def do_GET(self):

        try:

            self.full_path = os.getcwd() + self.path

            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(full_path=self.path, msg=msg)
        self.send_content(content.encode(), 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{full_path}' cannot be read: {msg}"
            self.handle_error(msg)

    def list_files_in_dir(self, full_path):
        extensions = ('html','php','txt')
        try:
            entries = os.listdir(full_path)
            bullets = [f'<li><a href={e}>{e}</a></li>'
                for e in entries if e.endswith(extensions) and not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page.encode())
        except OSError as msg:
            msg = f"'{full_path}' cannot be listed: {msg}"
            self.handle_error(msg)



if __name__ == '__main__':
    banner = r"""
/ ___| (_) _ __ ___   _ __  | |  ___ / ___|   ___  _ __ __   __  ___  _ __ 
\___ \ | || '_ ` _ \ | '_ \ | | / _ \\___ \  / _ \| '__|\ \ / / / _ \| '__|
 ___) || || | | | | || |_) || ||  __/ ___) ||  __/| |    \ V / |  __/| |   
|____/ |_||_| |_| |_|| .__/ |_| \___||____/  \___||_|     \_/   \___||_|   
                             |_|                                                                        
"""

    print(banner)

    if len(sys.argv)< 2 or len(sys.argv) > 2:
        print(f"Usage : \n\t python3 {sys.argv[0]} <port>")
        sys.exit(2)

    port = int(sys.argv[1])
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
    server.socket =ssl.wrap_socket(server.socket, keyfile="key.pem",\
                                  certfile="cert.pem", server_side=True)
    ps = ''.join([str(l) + ":" for l in server.server_address])
    print(f'[+] server started at  {ps[:-1]}')
    server.serve_forever()