import bcrypt, pg8000, datetime
from flask import Flask, render_template, request

app = Flask(__name__)
app.template_folder ='/var/www/html' # point the flask framework to look in this directory for loading .html files

con = pg8000.connect(host='127.0.0.1',
user='postgres',
password='Geok2001@',
database='GDPR' # connection to postgresql GDPR database with the users credentials
)


@app.route('/')
def index():
    return render_template('index.html') # behavior on loadup, load in root the index.html file

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password') # gathering the data typed from the user
    cursor = con.cursor()
    cursor.execute("SELECT password, last_pwd_change FROM users WHERE username = %s", (username,)) 
    data = cursor.fetchone() # finding password that corresponds to the typed username and the last time the password changed
    cursor.close()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM logging WHERE username = %s AND success = false AND timestamp > (SELECT MAX(timestamp) FROM logging WHERE username = %s AND success = true)", (username,username))
    failed_attempts = cursor.fetchone()[0] # count failed login attempts starting the count from the last successful login
    cursor.close()
    if failed_attempts <= 4: # check if the user is not locked before you check for correct password
        if data:
            hashed_password, last_pwd_change = data # if we find the data
            if bcrypt.checkpw(password.encode(), hashed_password.encode()): # check typed password encoded to bytes if it matches hashed password encoded to bytes
                current_time = datetime.datetime.now() # gather the time right now
                time_passed = current_time - last_pwd_change # calculate time passed 
                if time_passed.days > 180: # if 6 months have passed inform user to change his password
                    return "Your password has been expired, please change it before logging in"
                else:
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO logging (username, success) VALUES (%s, %s)", (username, True)) # inserting correct data to logging
                    con.commit()
                    cursor.close()
                    return "Success, you are logged in"
            else:
                cursor = con.cursor()
                cursor.execute("INSERT INTO logging (username, success) VALUES (%s, %s)", (username, False)) # inserting correct data to logging
                con.commit()
                cursor.close()
                cursor = con.cursor()
                cursor.execute("SELECT COUNT(*) FROM logging WHERE username = %s AND success = false AND timestamp > (SELECT MAX(timestamp) FROM logging WHERE username = %s AND success = true)", (username,username))
                failed_attempts = cursor.fetchone()[0] # count failed login attempts starting the count from the last successful login
                cursor.close()
                if failed_attempts > 4: # check if this is the 5th time of incorrect password and lock the user
                    return "Too many failed login attempts, your account has been locked"
                return "Incorrect Password, go to the previous page and try again"
        else: # if not the user does not exist in our users table
            return "User not found, go to the previous page and try again"
    else: return "Too many failed login attempts, your account has been locked" # user is locked

if __name__ == '__main__':
    app.run(host='83.212.106.137', port=5000, debug=True) # start server