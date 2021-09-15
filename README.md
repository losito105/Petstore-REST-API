# Petstore-REST-API

<h2>Setup:</h2>

This API requires Flask and its dependencies to run. For information regarding Flask and/or dependency installation, see:
https://flask.palletsprojects.com/en/1.1.x/installation/#installation 

Once you have Flask and the required dependencies installed, clone this repo to get the <pre>api.py</pre>source file.
Using your terminal, redirect into the cloned project directory. 

Once you are in the project directory, run the command <pre>export FLASK_APP=api.py</pre>
If you would like to run the API in debug mode, run the command 
<pre>export FLASK_ENV=development</pre>
Now just run <pre>flask run</pre> and the API should start up.
  
<h2>Testing / Use:</h2>

I would recommend installing the Chrome Extension "Advanced REST Client" to test or use this API.
This tool allows you to manually change the HTTP request method you are using, as well as manually
input a JSON request body and URL parameters. 

<h3>Sample Request:</h3>
<pre>
1. Within Advanced REST Client, select HTTP POST request method.
2. Add a request body with body content type "application/json" and switch the Editor view to "Raw input".
3. Paste the following in the text box below:
    {
      "id": 10,
      "username": "theUser",
      "firstName": "John",
      "lastName": "James",
      "email": "john@email.com",
      "password": "12345",
      "phone": "12345",
      "userStatus": 1
    }
4. In your terminal, copy the URL following the words "Running on:" and paste it into the "Request URL" section of the Advanced REST Client.
5. Concatenate "/user" onto the end of this URL.
6. Click "Send" and at the bottom of the Advanced REST Client, you should see a JSON response indicating that a new user was successfully created.
7. From here, you may want to log this user in/out, update their info, or delete them. You can also create multiple users at once. 
(See https://petstore3.swagger.io/ for instructions on how to complete steps 6 and 7.)
</pre>
  
<h2>Reference:</h2>
  
This API is an implementation of the Swagger Petstore - OpenAPI 3.0.
For information regarding JSON body input format, expected JSON response format, and Petstore API methods see:
https://petstore3.swagger.io/
  
While this is an implementation of the Petstore API, some implementation details may vary.
Any variation from the Petstore API should be well documented in comments in "api.py".
