from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123456@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Bpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(255))
    blog_content = db.Column(db.Text)

    def __init__(self, blog_title, blog_content):
        self.blog_title = blog_title
        self.blog_content = blog_content

@app.route("/newpost", methods=['POST'])
def validate_new_post():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']
    title_error = ''
    body_error = ''
    return render_template("newpost.html", title="Create New Post", )

@app.route("/newpost")
def new_post():
    return render_template("newpost.html", title="Create New Post")

@app.route("/blog")
def main_blog():
    return render_template("blog.html", title="Demo Blog")

if __name__ == '__main__':
    app.run ()