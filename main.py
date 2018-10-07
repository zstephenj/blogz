from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Bpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(255))
    blog_content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, blog_content, author):
        self.blog_title = blog_title
        self.blog_content = blog_content
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(88))
    password = db.Column(db.String(88))
    blogs = db.relationship('Bpost', backref='author')

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
            new_post = Bpost(blog_title, blog_body)
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
    if not id == None:
        content = Bpost.query.filter_by(id=id).all()
        return render_template("blog.html", title="Demo Blog", content=content) 
    else:
        content = Bpost.query.all()
        return render_template("blog.html", title="Demo Blog", content=content)

if __name__ == '__main__':
    app.run ()