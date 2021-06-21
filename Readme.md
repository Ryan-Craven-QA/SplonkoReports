<h1>Splonko Reports</h1>

<h3> Tools I'm currently using- Pycharm, Cmder (terminal) </h3>

<h4> Referenced Book: "The New and Improved Flask Mega-Tutorial" by Miguel Grinberg <br>
<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world"> Flask Mega Tutorial</a> </h4>

<h3> The idea behind Splonko Reports is to provide an open source opportunity to show: </h3>

1. Status of APIs that run of a schedule (WIP) -- Main goal
2. Poll / Pull Test automation results -- Stretch goal (will be implemented later)

--Why?
    I got tired of consistently having to run a newman script to run a collection of postman and 
    having to manually update the test results.
        --This will not replace applications like POSTMAN - this isn't a test application.
        --Rather, you'll be able to see a status of your API requests and see if they're passing
          of failing.


Common commands needed and forgotten:

Starting virtual environment:
* MAC: source venv/bin/activate
* Windows: venv\Scripts\activate.bat

Updating Flask DB: <br>
   * flask db migrate -m "insert message" <br>
   * flask db upgrade


Update Env variables to get emails: <br> ** Use set instead of export if on Windows ** <br>
* export MAIL_SERVER=smtp.googlemail.com
* export MAIL_PORT=587
* export MAIL_USE_TLS=1
* export MAIL_USERNAME=<your-gmail-username>
* export MAIL_PASSWORD=<your-gmail-password>
