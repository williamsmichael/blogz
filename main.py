from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'J@+2x\LEQqBMw`*S'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, title, body):
        self.title = title
        self.body = body 



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    post_title, post_body = '', ''
    
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']

        if post_title and post_body:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()

            post_id = str(new_post.id)
            return redirect('/blog?id=' + post_id)

        if not post_title:
            flash('Please fill in the title', 'error_title')

        if not post_body:
            flash('Please fill in the body', 'error_body')

    return render_template('newpost.html', title='newpost', post_title=post_title, post_body=post_body)


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    post_id = request.args.get('id')

    if post_id:
        post = Blog.query.get(post_id)
        return render_template('viewpost.html', title='viewpost', post=post)

    posts = Blog.query.order_by(Blog.created.desc()).all()   
    return render_template('posts.html', title='posts', posts=posts)  


@app.route('/')
def index():
    return redirect('/blog')  


if __name__ == '__main__':
    app.run()
