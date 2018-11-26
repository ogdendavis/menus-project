#!/usr/bin/env python

### Web server script! ###

# BaseHTTPServer is Python's basic HTTP server library
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# CGI helps with parsing POST requests so we can respond appropriately
import cgi

### How to process HTTP requests ###

# Inherit from BaseHTTPServer, and define methods for types of HTTP requests
class webserverHandler(BaseHTTPRequestHandler):
    # Override default do_GET with our custom responses
    def do_GET(self):
        try:
            # Test for sending back a basic response to a get request
            if self.path.endswith("/hello"):
                self.send_response(200) # GET success code
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Simple test output
                output = ""
                output += "<html><body>Hello!"
                # Adding form from do_POST (below)
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name = 'message' type = 'text'><input type = 'submit' value = 'Submit'></form>"
                # Close body and html tags!
                output += "</body></html>"

                # Write output to write file, thus sending to client
                self.wfile.write(output)
                # Print output in terminal for reference/debugging
                print(output)

            # A second test page -- this time, en espanol!
            if self.path.endswith("/hola"):
                self.send_response(200) # GET success cod
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Simple test output
                output = ""
                # &#161; is HTML entity for upside-down '!'. Also added link
                output += "<html><body>&#161;Hola! <a href='/hello'>Back to Hello</a>"
                # Adding form from do_POST (below)
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name = 'message' type = 'text'><input type = 'submit' value = 'Submit'></form>"
                # Close body and html tags!
                output += "</body></html>"

                # Write output to write file, thus sending to client
                self.wfile.write(output)
                # Print output in terminal for reference/debugging
                print(output)

        except IOError:
            # IOError is the error type for 'file not found' in Python 2
            # In Python 3, this is now an OSError, but IOError is an alias
            # for OSError, so either/both will work
            self.send_error(404, "File Not Found {}".format(self.path))


    # Override default do_POST to respond to input appropriately
    def do_POST(self):
        try:
            self.send_response(301) # Response for successful POST
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # I don't entirely get this part -- I'm using cgi to extract data
            # from the post request
            # Note that this 'self' refers to the post request that was sent,
            # so here we're getting the content-type header that was sent to
            # us from the client, NOT the content-type header we declared above
            # to send back
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # If the headers that were sent include form input data:
            if ctype == 'multipart/form-data':
                # Using the dictionary created (somehow) earlier to parse the
                # form fields that were sent
                fields = cgi.parse_multipart(self.rfile, pdict)
                # Getting the input from the 'message' field - it's an array
                messagecontent = fields.get('message')

                # Output will include info from message field above, and will
                # have the form that can be submitted to make this whole thing
                # happen!
                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this:</h2>"
                # Input from message field, as extracted into array above
                output += "<h1>{}<h1>".format(messagecontent[0])

                # Adding the form that we'll use to submit the info to start
                # Note that the form attributes correspond to how we parsed the
                # form data above -- it uses a POST, it sends a
                # multipart/form-data header, and it has an input field named
                # 'message'
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name = 'message' type = 'text'><input type = 'submit' value = 'Submit'></form>"

                # Close body and html tags!
                output += "</body></html>"

                # Send the output to the client
                self.wfile.write(output)
                # Print to terminal for debugging
                print(output)

        except:
            pass


### Instantiate server and set it up to listen on port ###
def main():
    try:
        port = 8080
        # Pass HTTP server a tuple with server name and port number, and then
        # the class to use for server requests (defined above)
        server = HTTPServer(('',port), webserverHandler)
        # Notify that server is running, and make it run until stopped
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        # If user stops server with keyboard interrupt, notify that it's
        # stopping, and stop it!
        print("^C entered, stopping web server...")
        server.socket.close()


# If the module is run, use the main function to set up the server!
if __name__ == '__main__':
    main()
