#!/usr/bin/env python

### Web server script! Rewritten from original (example) to perform
### CRUD functions on restaurantmenu.db

# BaseHTTPServer is Python's basic HTTP server library
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# CGI helps with parsing POST requests so we can respond appropriately
import cgi
# db_queries holds functions that perform SQL queries on the database and
# return the results in ways that can be used in this Python server code
from db_queries import get_restaurants, get_restaurant_by_id, add_restaurant, edit_restaurant, delete_restaurant

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

                # Use get_restaurants to get list of restaurant names
                restaurants = get_restaurants()

                output = ""
                # HTML document setup
                output += """<html lang='en'>
                                <head>
                                    <title>Restaurants</title>
                                    <meta charset='utf-8'>
                                </head>
                                <body>"""
                output += "<h1>Restaurants!</h1>"
                # Link to add new restaurant
                output += "<a href='/restaurants/new'>Add a new restaurant</a>"
                # Put restaurant names in an unordered list
                output += "<ul>"
                for restaurant in restaurants:
                    edit_link = "/restaurants/{}/edit".format(restaurant.id)
                    delete_link = "/restaurants/{}/delete".format(restaurant.id)
                    output += "<li>{}".format(restaurant.name)
                    # Sub-list to hold Edit and Delete links
                    output += "<ul>"
                    output += "<li><a href='{}'>Edit</a>".format(edit_link)
                    output += "</li><li><a href='{}'>Delete</a></li>".format(delete_link)
                    # Close sub-list ul and restaurant li
                    output += "</ul></li>"
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

            # Page to edit existing restaurant
            if self.path.endswith("/edit"):
                # Display page to edit restaurant entry
                self.send_response(200) # GET success code
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Get ID of restaurant to be edited from URL
                restaurant_id = self.path.split('/')[2]
                # Use ID to get restaurant name with db_queries function
                restaurant_name = get_restaurant_by_id(restaurant_id).name

                output = ""
                # HTML document setup
                output += "<html lang='en'><head>"
                output += "<title>Edit {}</title>".format(restaurant_name)
                output += "<meta charset='utf-8'></head><body>"
                output += "<h1>Edit {}</h1>".format(restaurant_name)
                # Form to edit this restaurant
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '{}'>".format(self.path)
                output += """New name: <input name = 'new_name' type = 'text' placeholder = "{}">""".format(restaurant_name)
                output += "<input type = 'submit' value = 'Submit'></form>"
                # Close body and html tags!
                output += "</body></html>"

                # Write to response and print to terminal for reference
                self.wfile.write(output)
                print(output)

            if self.path.endswith("/delete"):
                # Confirmation page for restaurant deletion
                self.send_response(200) # GET success code
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Get ID of restaurant to be deleted
                restaurant_id = self.path.split('/')[2]
                # Use ID to get restaurant name with db_queries function
                restaurant_name = get_restaurant_by_id(restaurant_id).name

                output = ""
                # HTML document setup
                output += "<html lang='en'><head>"
                output += "<title>Delete {}</title>".format(restaurant_name)
                output += "<meta charset='utf-8'></head><body>"
                output += "<h1>DELETE CONFIRMATION</h1>"
                output += "<p>Are you sure you want to delete {}?".format(restaurant_name)
                # Form to edit this restaurant
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '{}'>".format(self.path)
                output += """<input type = 'submit' value = "Yes, delete {}"></form>""".format(restaurant_name)
                output += "<form method = 'GET' action = '/restaurants'><input type = 'submit' value = 'Cancel'></form>"
                # Close body and html tags!
                output += "</body></html>"

                # Write to response and print to terminal for reference
                self.wfile.write(output)
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
                # Use cgi to extract data from the post request
                # self.headers.getheader gets header sent from client
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # If the headers that were sent include form input data:
                if ctype == 'multipart/form-data':
                    # Parse the form fields and get the 'restaurant' field,
                    # which is a list with 1 item (the text entered)
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant')
                # Use function from db_queries to add restaurant to database
                add_restaurant(restaurant_name[0])

                # Once DB function is completed, send back headers
                self.send_response(301) # Response for successful POST
                self.send_header("Content-type", "text/html")
                # Redirect header -- causes client to go to restaurant list
                self.send_header("Location", "/restaurants")
                self.end_headers()

            if self.path.endswith("edit"):
                # Use cgi to extract data from the post request
                # self.headers.getheader gets header sent from client
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # If the headers that were sent include form input data:
                if ctype == 'multipart/form-data':
                    # Parse the form fields and get the 'restaurant' field,
                    # which is a list with 1 item (the text entered)
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get("new_name")[0]

                # Form used the edit page's URL as action, so get restaurant
                # id from that
                id = self.path.split('/')[2]

                # Use name and ID to update restaurant in db_queries
                edit_restaurant(id, new_name)

                # Once DB function is completed, send back headers
                self.send_response(301) # Response for successful POST
                self.send_header("Content-type", "text/html")
                # Redirect header -- causes client to go to restaurant list
                self.send_header("Location", "/restaurants")
                self.end_headers()

            if self.path.endswith("/delete"):
                # We're not reading any form data, so no need for cgi here

                # Form used the delete page's URL as action, so get restaurant
                # id from that and delete it
                id = self.path.split('/')[2]
                delete_restaurant(id)

                # Once DB function is completed, send back headers
                self.send_response(301) # Response for successful POST
                self.send_header("Content-type", "text/html")
                # Redirect header -- causes client to go to restaurant list
                self.send_header("Location", "/restaurants")
                self.end_headers()

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
        print(" Keyboard interrupt, stopping web server...")
        server.socket.close()


# If the module is run, use the main function to set up the server!
if __name__ == '__main__':
    main()
