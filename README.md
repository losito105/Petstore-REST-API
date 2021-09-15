# Petstore-REST-API

<h2>Setup:</h2>

This API requires Flask and its dependencies to run. For information regarding Flask and/or dependency installation, see:
https://flask.palletsprojects.com/en/1.1.x/installation/#installation 

Once you have Flask and the required dependencies installed, clone this repo to get the "api.py" source file.
Using your terminal, redirect into the cloned project directory. 

Once you are in the project directory, run the command "export FLASK_APP=api.py"
If you would like to run the API in debug mode, run the command "export FLASK_ENV=development"
Now just run "flask run" and the API should start up.
  
This API uses a static data source so there is no need to connect to an external database.
  
<h2>Testing / Use:</h2>

I would recommend installing the Chrome Extension "Advanced REST Client" to test or use this API.
This tool allows you to manually change the HTTP request method you are using, as well as manually
input a JSON request body and URL parameters. 
  
<h2>Reference:</h2>
  
This API is an implementation of the Swagger Petstore - OpenAPI 3.0.
For information regarding JSON body input format, expected JSON response format, and Petstore API methods see:
https://petstore3.swagger.io/
  
While this is an implementation of the Petstore API, some implementation details may vary.
Any variation from the Petstore API should be well documented in comments in "api.py".
