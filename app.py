from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  "apiKey": "AIzaSyBrQoyeN6xoQtOmpD0WsfA9EfGiHH2jMIg",
  "authDomain": "project1-a869b.firebaseapp.com",
  "projectId": "project1-a869b",
  "storageBucket": "project1-a869b.appspot.com",
  "messagingSenderId": "221693419654",
  "appId": "1:221693419654:web:37c0e61efe4492015d3107",
  "measurementId": "G-2SWJJ8CWTD",
  "databaseURL":"https://project1-a869b-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user={"username":username}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            print("yo")
            # return redirect(url_for('home'))
            db.child("Users").child(login_session["user"]["localId"]).set(user)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/home', methods= ['GET', 'POST'])
def home():
    error=''
    stories=db.child("stories").get().val()
    return render_template('home.html',stories=stories, user=login_session["user"]["localId"] )


@app.route('/add_story', methods=['GET', 'POST'])
def add_story():
    error=""
    if request.method == 'POST':
        story = request.form['story']
        title = request.form['title']
        print (login_session)
        post={"story":story , "title":title,"UID":login_session["user"]["localId"]}
        try:
            db.child("stories").push(post)
            # stories_len= stories.len()

            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
        return render_template("add_story.html")

    return render_template('add_story.html')

@app.route('/my_stories')
def my_stories():
    error=''
    stories=db.child("stories").get().val()
    return render_template('my_stories.html',stories=stories, user=login_session["user"]["localId"] )



@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)