from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '''<html><body>&#161Hola! <br> <a href = '/hello'> Back to Hello</a>'''
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return
        except IOError:
            self.send_error(404, "File not found %s" % self.path)
            return

    def do_POST(self):
        print("In POST")
        try:
            self.send_response(301)
            self.send_header('Content-type,', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers.get('content-type'))
            print("ctype: " + ctype)
            for x in pdict:
                print(x)
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(str(self.rfile, "utf-8"), pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)
            return


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('Web Server is running on port %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
