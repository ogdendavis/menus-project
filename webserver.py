#!/usr/bin/env python

### Web server script! Rewritten from original (example) to perform
### CRUD functions on restaurantmenu.db

# BaseHTTPServer is Python's basic HTTP server library
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# CGI helps with parsing POST requests so we can respond appropriately
import cgi
# db_queries holds functions that perform SQL queries on the database and
# return the results in ways that can be used in this Python server code
from db_queries import read_names, add_restaurant

### How to process HTTP requests ###

# Inherit from BaseHTTPServer, and define methods for types of HTTP requests
class webserverHandler(BaseHTTPRequestHandler):
    # Override default do_GET with our custom responses
    def do_GET(self):
        try:
            # Restaurant list page
            if self.path.endswith("/restaurants"):
                self.send_response(200) # GET success code
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Use read_names to get list of restaurant names
                restaurants = read_names()

                output = ""
                # HTML document setup
                output += """<html lang='en'>
                                <head>
                                    <title>Restaurants</title>
                                    <meta charset='utf-8'>
                                </head>
                                <body>"""
                output += "<h1>Restaurants!</h1>"
                # Put restaurant names in an unordered list
                output += "<ul>"
                for name in restaurants:
                    output += "<li>{}".format(name)
                    # Sub-list to hold Edit and Delete links
                    output += "<ul><li><a href='#'>Edit</a></li><li><a href='#'>Delete</a></li></ul>"
                    output += "</li>"
                output += "</ul>"
                # Close body and html tags!
                output += "</body></html>"

                # Write output to write file, thus sending to client
                self.wfile.write(output)
                # Print output in terminal for reference/debugging
                print(output)

            # Page to add new restaurants
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                # HTML document setup
                output += """<html lang='en'>
                                <head>
                                    <title>Add a Restaurant</title>
                                    <meta charset='utf-8'>
                                </head>
                                <body>"""
                output += "<h1>Add a Restaurant!</h1>"
                # Form to add a restaurant
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>Restaurant name: <input name = 'restaurant' type = 'text'> <input type = 'submit' value = 'Submit'></form>"
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
            if self.path.endswith("/restaurants/new"):
                self.send_response(301) # Response for successful POST
                self.send_header("Content-type", "text/html")
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
                    # form fields that were sent and get the 'restaurant' field,
                    # which is a list with 1 item (the text entered)
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant')
                    # Use function from db_queries to add restaurant to database
                    add_restaurant(restaurant_name[0])

                    # Output mostly copied from do_GET for /restaurants/new
                    output = ""
                    output += "<html lang='en'><head><title>Add a Restaurant</title><meta charset='utf-8'></head><body>"
                    # Only change from do_GET -- confirm that restaurant was added
                    output += "<i>{} added!</i>".format(restaurant_name[0])
                    output += "<h1>Add a Restaurant!</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>Restaurant name: <input name = 'restaurant' type = 'text'> <input type = 'submit' value = 'Submit'></form>"
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
