from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import config
import datetime
from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from forms import RegistrationForm

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

login_manager = LoginManager(app)

@app.route('/')
def home():
    registrationform = RegistrationForm()
    return render_template('home.html', registrationform=registrationform)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    print("Login failed")
    return home()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    pw1 = request.form.get('password')
    pw2 = request.form.get('password2')

    if not pw1 == pw2:
        print("Passwords not equal")
        return redirect(url_for('home'))

    if DB.get_user(email):
        print("Email already in database")
        return redirect(url_for('home'))

    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    print("Sucessful")
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route('/newrequest/<tid>')
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return("Your request has been submitted - A waiter will be with you shortly")


@app.route('/account/createtable', methods=['POST'])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = BH.shorten_url(config.base_url + "newrequest/" + tableid)
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))


@app.route('/account/deletetable')
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))


@app.route('/account')
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route('/dashboard')
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now-req['time']).seconds
        req['wait_minutes'] = "{:.01f}".format((deltaseconds/60))
    return render_template("dashboard.html", requests=requests)


@app.route('/dashboard/resolve')
@login_required
def dashboard_resolve():
    request_id = request.args.get('request_id')
    print("Resolve request for id: ", request_id)
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
