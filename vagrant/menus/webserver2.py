from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base

# Create a DB Session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                for rest in restaurants:
                    output += "<h2> %s </h2>" % rest.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % rest.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a><br>" % rest.id

                output += "<br><h2><a href='/restaurants/new'>Add a New Restaurant</a></h2>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What is the new restaurant's Name?</h2><input name='rname' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_id = self.path[13:-5]

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "action='/restaurants/edit'>"
                output += "<h2>What is the New Name?</h2>"
                output += "<input name='uname' type='text' >"
                output += "<input type='hidden' name='id' value='%s'>" % rest_id
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            elif self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_id = self.path[13:-7]

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "action='/restaurants/delete'>"
                output += "<h2>Delete This Restaurant?</h2>"
                output += "<input name='delete_rest' type='checkbox' >"
                output += "<input type='hidden' name='id' value='%s'>" % rest_id
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            else:
                self.send_error(404, "I can't find %s." % self.path)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('rname', None)

                new_restaurant = Restaurant(name=new_name[0])
                session.add(new_restaurant)
                session.commit()

                output = ""
                output += "<html><body>"
                output += "<h1> Okay, %s has been added </h1>" % new_name[0]
                output += "<a href='/restaurants'>Return to Home Page</a>"
                output += "</body></html>"
                self.wfile.write(output)

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    up_name = fields.get('uname', None)
                    rest_id = fields.get('id', None)

                up_rest = session.query(Restaurant).filter_by(id=rest_id[0]).one()
                old_name = up_rest.name
                up_rest.name = up_name[0]
                session.add(up_rest)
                session.commit()

                output = ""
                output += "<html><body>"
                output += "<h1> Okay, the name %s " % old_name
                output += "has been updated to %s </h1>" % up_name[0]
                output += "<a href='/restaurants'>Return to Home Page</a>"
                output += "</body></html>"
                self.wfile.write(output)

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    d_rest = fields.get('delete_rest', [None])
                    rest_id = fields.get('id', None)

                rest = session.query(Restaurant).filter_by(id=rest_id[0]).one()
                old_name = rest.name
                output = ""
                output += "<html><body>"
                if d_rest[0] == 'on':
                    session.delete(rest)
                    session.commit()
                    output += "<h1> Okay, %s " % old_name
                    output += "has been removed from the database </h1>"
                    output += "<a href='/restaurants'>Return to Home Page</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                else:
                    output += "<h1> Okay, %s " % old_name
                    output += "will stay in the Database. For now... </h1>"
                    output += "<a href='/restaurants'>Return to Home Page</a>"
                    output += "</body></html>"
                    self.wfile.write(output)

        except:
            self.send_error(500, "Something's gone terribly wrong")


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
