from app import app, db
from flask import redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm
from app.models import User, Products, Cart

@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html',  title=title)

@app.route('/shop')
def shop():
    title = 'Shop'
    # products = products.query.all()

    return render_template('shop.html',  title=title)


@app.route('/cart')
def cart():
    title = 'Cart'

    #VIEWING ITEMS IN CART 
    cart = current_user.cart
    subtotal = 0
    for item in cart:
        subtotal+=int(item.price)*int(item.quantity)
    

    if request.method == "POST":
        cartitem = Cart.query.filter_by(product_id=idpd).first()
        cartitem.quantity = qty
        db.session.commit()
        cart=current_user.cart 
        subtotal = 0
        for item in cart:
            subtotal+=int(item.price)*int(item.quantity)

    return render_template('cart.html', cart=cart, noOfItems=noOfItems, subtotal=subtotal, title=title)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    
    if form.validate_on_submit():
        
        email = form.email.data
        username = form.username.data
        password = form.password.data
        
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all() 
        if users_with_that_info:
            flash(f"There is already a user with that username and/or email. Please try again", "danger")
            return render_template('signup.html', title=title, form=form)

        
        new_user = User(email=email, username=username, password=password)
        
        flash(f"{new_user.username} has succesfully signed up.", "success")
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            
            login_user(user)
            
            flash(f'{user} has successfully logged in', 'success')
            
            return redirect(url_for('index'))
        else:
            flash('Username and/or password is incorrect', 'danger')
            
    return render_template('login.html', title=title, form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))

##ADD TO CART 
@app.route("/add_to_Cart/<product_id>")
@login_required
def addToCart(product_id):
    title= 'Add to Cart'

    item_to_add = Cart(product_id=product_id, user_id=current_user.id)
    db.session.add(item_to_add)
    db.session.commit()
    
    repeat_item = Cart.query.filter_by(product_id=product_id, buyer=current_user).first()
    if repeat_item:
        
        repeat_item.quantity += 1
        db.session.commit()
        flash('This item is already in your cart, add again!', 'success')
        
    else:
        user = User.query.get(current_user.id)
        user.add_to_cart(product_id)

        return redirect(url_for('shop'))

    return render_template('addtocart.html', title=title)

##REMOVE FROM CART 
@app.route("/removeFromCart/<product_id>")
@login_required
def removeFromCart(product_id):

    item_to_remove = Cart.query.filter_by(product_id=product_id, buyer=current_user).first()
    db.session.delete(item_to_remove)
    db.session.commit()

    flash('Your item has been removed from your cart!', 'success')
    return redirect(url_for('cart'))


@app.route("/single_product")
def single_product(product_id):
    title = 'Product'
    product = Products.query.get_or_404(product_id)

    return render_template('single_product.html', product=product, title=title)

    
    



