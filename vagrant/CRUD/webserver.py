# Import both of BaseHTTPServer's classes for implementing HTTP servers
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

# Import module for Common Gateway Interface support
# https://docs.python.org/2/library/cgi.html
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    # Handle GET requests (overwrites default methods in BaseHTTPRequestHandler)
    def do_GET(self):
        try:
            # BaseHTTPRequestHandler provides the path variable which contains
            # the URL sent by the client to the server as a string
            if self.path.endswith("/hello"):
                # Send code 200, indicating successful GET request
                self.send_response(200)
                # Send header indicating HTML is being sent to client
                self.send_header('Content-type', 'text/html')
                # Sends a blank line indicating end of HTTP header
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' \
                          action='/hello'><h2>What would you like me to say? \
                          </h2><input name="message" type="text" > \
                          <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                # Send message back to the client
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body> &#161 Hola! <a href='/hello'> \
                Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' \
                          action='/hello'><h2>What would you like me to say? \
                          </h2><input name="message" type="text" > \
                          <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)

    def do_POST(self):
        try:
            # Code 303 indicates a successful POST
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this: </h2>"
                output += "<h1> %s <h1>" % messagecontent[0]

                output += '''<form method='POST' enctype='multipart/form-data' \
                          action='/hello'><h2>What would you like me to say? \
                          </h2><input name="message" type="text" > \
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
