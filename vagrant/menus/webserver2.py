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
                    output += "<a href='/edit'>Delete</a><br>"

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
                print rest_id

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "action='/restaurants/edit'>"
                output += "<h2>What is the restaurant's New Name?</h2>"
                output += "<input name='uname' type='text' >"
                output += "<input type='hidden' name='id' value='%s'>" % rest_id
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            else:
                self.send_error(404, "I can't find %s. try harder" % self.path)

                '''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                for rest in restaurants:
                    output += "<h2> %s </h2>" % rest.name
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
                '''

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
            '''
            if new_name:
                new_restaurant = Restaurant(name=new_name[0])
                session.add(new_restaurant)
            if up_name:
                u_rest =session.query(Restaurant).filter_by(name="")
                u_rest = Restaurant(name=up_name[0])
                session.add(new_restaurant)

            session.commit()
            '''

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
