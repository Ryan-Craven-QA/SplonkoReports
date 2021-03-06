<h1>Splonko Reports</h1>

<h3> Tools I'm currently using- Pycharm, Cmder (terminal) </h3>

<h4> Referenced Book: "The New and Improved Flask Mega-Tutorial" by Miguel Grinberg <br>
<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world"> Flask Mega Tutorial</a> </h4>

<h3> Getting Started </h3>
1. Install pip

*  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
*  python3 get-pip.py


2. Start Virtual Environment
* MAC: source venv/Scripts/activate
* Windows: venv\Scripts\activate.bat
    *   Terminal should should (venv) ...

<p> Once you have a virtual environment spun up and activated, <br>
3. Install requirements.txt file 

* pip install -r requirements.txt (or pip3 install -r requirements.txt)</p>

4. Starting the application (in terminal - type)
* flask run


** When the application starts **
* There should be a few APIs already loaded into the DB
* Login preloaded with:
  * Username: splonko
  * password: cat

  
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

Updating Flask DB: <br>
   * flask db migrate -m "insert message" <br>
   * flask db upgrade


Update Env variables to get emails: <br> ** Use set instead of export if on Windows ** <br>
* export MAIL_SERVER=smtp.googlemail.com
* export MAIL_PORT=587
* export MAIL_USE_TLS=1
* export MAIL_USERNAME=<your-gmail-username>
* export MAIL_PASSWORD=<your-gmail-password>
