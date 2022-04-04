from app import app, db
from app.models import Cart, Contact, Products, User 

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Products': Products, 'Contact': Contact, 'Cart': Cart }