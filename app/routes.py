import os
import sys
from datetime import datetime
from json import JSONDecodeError
from pytz import timezone
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db, requests_helper, stats_helper
from app.api_results import get_api_results
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, \
    CreateAPI
from app.models import User, Api, Stats

from app.report_generation import render_html


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    stat = Stats.query.all()
    lastStat = Stats.query.order_by(Stats.statid.desc()).first()
    return render_template('index.html', title='Home', stat=stat, lastStat=lastStat)


@app.route('/api_report', methods=['GET', 'POST'])
@login_required
def api_report():
    if request.method == 'POST':
        if 'pdf' in request.form:
            render_html()

    try:
        s = Api.query.all()
        apiPass = 0
        apiFail = 0
        apiWip = 0
        apiTotal = 0
        for x in s:
            requesttype = Api.get_requesttype(x)
            apiurl = Api.get_apiurl(x)
            apidata = Api.get_apidata(x)
            response = requests_helper.perform_request(requesttype, apiurl, apidata)
            try:
                if response.status_code < 300:
                    apiPass += 1
                    apiTotal += 1
                else:
                    apiFail += 1
                    apiTotal += 1
                Api.set_responsecode(x, response.status_code)
                Api.set_response(x, response.json())
                Api.set_reason(x, response.reason)
            except AttributeError:
                apiWip += 1
            except JSONDecodeError:
                Api.set_response(x, "{}")
        data = db.session.query(Api).all()

        stats_helper.updateStats(apiPass, apiFail, apiTotal, apiWip)

        stats = Stats.query.order_by(Stats.statid.desc()).first()
        return render_template('api_report.html', title='Home', data=data, stats=stats)
    except UnboundLocalError:
        return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/createAPI', methods=['GET', 'POST'])
def create_API():
    form = CreateAPI()
    if form.validate_on_submit():
        c_api = Api(apiname=form.apiname.data, requesttype=form.requesttype.data, apiurl=form.apiurl.data,
                    apidata=form.apidata.data)
        db.session.add(c_api)
        db.session.commit()
        flash('API added to DB')
        return render_template('createAPI.html', title='Create API', form=form)
    return render_template('createAPI.html', title='Create API', form=form)


@app.route('/displayAPIs', methods=['GET', 'POST'])
def display_api():
    info = db.session.query(Api).all()
    if request.method == 'POST':
        if 'edit' in request.form:
            api_id = request.form['edit']
            session['api_id'] = api_id
            return redirect(url_for('edit_api', api_id=api_id))
        else:
            api_id = request.form['delete']
            api_to_delete = Api.query.get_or_404(api_id)
            db.session.delete(api_to_delete)
            db.session.commit()
            return redirect(url_for('display_api'))
    else:
        return render_template('displayAPIs.html', title='API List', data=info)


@app.route('/edit_api', methods=['GET', 'POST'])
@login_required
def edit_api():
    api_id = session.get('api_id')
    data = Api.query.get(api_id)
    form = CreateAPI(obj=data)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('display_api'))
    if request.method == 'POST' and 'back' in request.form:
        return redirect(url_for('display_api'))
    return render_template('edit_api.html', title='Edit Api', form=form, data=data)
