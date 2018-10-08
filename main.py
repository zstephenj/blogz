from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'secretkeysecretkey'
db = SQLAlchemy(app)

class Bpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(255))
    blog_content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, blog_content, author_id):
        self.blog_title = blog_title
        self.blog_content = blog_content
        self.author_id = author_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(88))
    password = db.Column(db.String(88))
    blogs = db.relationship('Bpost', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        real_user = User.query.filter_by(username=username).first()
        if not real_user:
            flash('Username does not exist', 'error')
            return render_template('login.html', title='Login')
        if real_user and real_user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Incorrect password')
            return render_template('login.html', title='Login', username=username)
    else:
        return render_template('login.html', title='Login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        signup_error = False
        if not username:
            flash('Username field cannot be empty', 'error')
            signup_error = True
        if not password:
            flash('Password field cannot be empty', 'error')
            signup_error = True
        if not verify_password:
            flash('Verify Password field cannot be empty', 'error')
            signup_error = True
        if len(username) < 3:
            flash('Username must be at least three characters long', 'error')
            signup_error = True
        if len(password) < 3:
            flash('Password must be at least three characters long', 'error')
            signup_error = True
        if password != verify_password:
            flash('Passwords do not match', 'error')
            signup_error = True
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('An account with that username already exists.')
            signup_error = True
        if signup_error:
            return render_template('signup.html', title='Signup', username=username)
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
    else:
        return render_template('signup.html', title='Signup')

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = ''
        body_error = ''
        if not blog_title:
            title_error = 'Post title cannot be empty.'
        if not blog_body:
            body_error = 'Post body cannot be empty.'   
        if not title_error and not body_error:
            author_user = User.query.filter_by(username=session['username']).first()
            new_post = Bpost(blog_title, blog_body, author_user.id)
            db.session.add(new_post)
            db.session.commit()
            blog_id = new_post.id 
            return redirect('/blog?id={0}'.format(blog_id))
        else:
            return render_template("newpost.html", title="Create New Post", blog_title=blog_title, blog_body=blog_body, title_error=title_error, body_error = body_error)
    else:
        return render_template("newpost.html", title="Create New Post")

@app.route("/blog")
def blog():
    id = request.args.get('id')
    author_id = request.args.get('user')
    if not id == None:
        content = Bpost.query.filter_by(id=id).all()
        return render_template("blog.html", title="Demo Blog", content=content) 
    if not author_id == None:
        content = Bpost.query.filter_by(author_id=author_id).all()
        return render_template("blog.html", title="Demo Blog", content=content) 
    else:
        content = Bpost.query.all()
        return render_template("blog.html", title="Demo Blog", content=content)

@app.route('/')
def index():
    authors = User.query.all()
    return render_template('index.html', title='Blog Home', authors=authors)


if __name__ == '__main__':
    app.run ()