# Import both of BaseHTTPServer's classes for implementing HTTP servers
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

# Import module for Common Gateway Interface support
# https://docs.python.org/2/library/cgi.html
import cgi

# import necessary tools to interface with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# Creates a staging zone for objects loaded into the database session object
# Use session.commit() or session.rollback() to add/revert changes
session = DBSession()



class webserverHandler(BaseHTTPRequestHandler):
    # Handle GET requests (overwrites default methods in BaseHTTPRequestHandler)
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                # Fetch all restaurants to get list of restaurant objects
                restaurants = session.query(Restaurant).all()
                # Get restaurant names by accessing the name instance attribute of restaurant objects
                for r in restaurants:
                    output += r.name
                    output += "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % r.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % r.id
                    output += "<br><br><br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                # Get restaurant id from path
                restaurant_id = self.path.split("/")[2]
                # Search db for id
                restaurant_query = session.query(Restaurant).filter_by(
                    id=restaurant_id).one()
                # If id exists
                if restaurant_id:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit %s </h1>" % restaurant_query.name
                    output += "<form method='POST' enctype='multipart/form-data' \
                              action = '/restaurants/%s/edit' >" % restaurant_id
                    output += "<input name = 'restaurant_name' type='text' \
                              placeholder = '%s' >" % restaurant_query.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(
                    id=restaurant_id).one()
                if restaurant_query:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % restaurant_query.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurant_id
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Create a new restaurant </h1>"
                output += '''<form method='POST' enctype='multipart/form-data' \
                          action='/restaurants/new'><h2>Enter restaurant name: \
                          </h2><input name="restaurant_name" type="text" > \
                          <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('restaurant_name')
                    restaurant_id = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(
                        id=restaurant_id).one()

                if restaurant_query:
                    restaurant_query.name = new_restaurant_name[0]
                    session.add(restaurant_query)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(
                    id=restaurant_id).one()
                if restaurant_query:
                    session.delete(restaurant_query)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/restaurants/new"):
                # Code 303 indicates a successful POST
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    formcontent = fields.get('restaurant_name')

                    # Create new restaurant and add to db
                    new_restaurant = Restaurant(name = formcontent[0])
                    session.add(new_restaurant)
                    session.commit()

                    output = ""
                    output += "<html><body>"
                    output += "Thanks, your request to create the restaurant '%s' has been received!" % formcontent[0]
                    # output += "<b>Your restaurant submission for %s has been received</b>" % messagecontent[0]
                    output += "<h1> Create a new restaurant </h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' \
                              action='/restaurants/new'><h2>Enter restaurant name below: \
                              </h2><input name="restaurant_name" type="text" > \
                              <input type="submit" value="Submit"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
        except:
            pass


# Indicate what code to execute based on HTTP request
def main():
    try:
        port = 8080
        # Create HTTP server: https://docs.python.org/2/library/basehttpserver.html
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        # Keep web server constantly listening
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, web server properly stopped"
        # Shut down server
        server.socket.close()

# Instantiate server and specify port to listen on
if __name__ == '__main__':
    main()
