<h1>Splonko Reports</h1>

<h3> Tools I'm currently using- Pycharm, Cmder (terminal) </h3>
<h4> Referenced Book: "The New and Improved Flask Mega-Tutorial" by Miguel Grinberg
<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world"> Flask Mega Tutorial</a> </h4>

<h5>Day1: Hello World</h5>

1. Installed Python: https://www.python.org/downloads/
2. Created Directory for SplonkoReports in the terminal: mkdir <directory_name>
3. Changed directory to newly created directory
4. Created Virtual Environment: 'python -m venv venv'
5. Started up virtual environment
    * MAC: 'source venv/bin/activate'
    * Windows: 'venv\Scripts\activate.bat'
    
6. Installed Flask: 'pip install flask'
7. Created splonko_reports.py under the main directory
8. Created an app directed with __init__ and routes files as sub files
9. Exported splonko_reports.py into the virtual environment
   * MAC: 'export FLASK_APP=<application name>.py'
   * Windows: 'set FLASK_APP=<application name>.py'
   
10. In the virtual environment terminal, ran flask: 'flask run'
11. In browser, navigated to http://localhost:5000/ to see Hello, World!

```
Everything was straight forward getting the app going.  Didn't run into any hickups along the way.
```