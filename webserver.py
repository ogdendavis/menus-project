#!/usr/bin/env python

# Web server script!

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

### How to process HTTP requests ###
# Inherit from BaseHTTPServer, and define methods for types of HTTP requests
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Test for sending back a basic response to a get request
            if self.path.endswith("/hello"):
                self.send_response(200) # GET success code
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Simple test output
                output = ""
                output += "<html><body>Hello!</body></html>"
                # Write output to write file, thus sending to client
                self.wfile.write(output)
                # Print output in terminal for reference/debugging
                print(output)
                
        except IOError:
            # IOError is the error type for 'file not found' in Python 2
            # In Python 3, this is now an OSError, but IOError is an alias
            # for OSError, so either/both will work
            self.send_error(404, "File Not Found {}".format(self.path))


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
