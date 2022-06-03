from app import app, db
from flask import redirect, render_template, url_for, flash


@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html',  title=title)

@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html',  title=title)

@app.route('/contact')
def contact():
    title = 'Contact'
    return render_template('contact.html',  title=title)

@app.route('/shop')
def shop():
    title = 'Shop'
    return render_template('shop.html',  title=title)



            
    











    
    



