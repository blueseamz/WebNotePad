from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os


class Resquest(BaseHTTPRequestHandler):
    def get_html(self, msg=''):
        return f'''
        <html>
        <head>
            <meta charset="utf-8">
            <title>Web NotePad</title>
        </head>
        <body>
            <form name="input" method="post">
                <input type="submit" value="Save"><br><br>
                <textarea rows="20" cols="80" name="msg">{msg}</textarea>
            </form>
        </body>
        </html>
        '''

    def do_GET(self):
        print(self.requestline)
        msg = ''
        if os.path.isfile('notefile.txt'):
            notefile = open('notefile.txt', 'r')
            msg = notefile.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.get_html(msg).encode())
        notefile.close()

    def do_POST(self):
        # print(self.headers)
        # print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))
        msgtext = urllib.parse.unquote(req_datas.decode())
        print(msgtext)
        notefile = open('notefile.txt', 'w')
        notefile.write(msgtext[4:])
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.get_html(msgtext[4:]).encode())


if __name__ == '__main__':
    host = ('', 5000)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
