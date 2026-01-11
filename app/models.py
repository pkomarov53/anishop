from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.String(50))
    title = db.Column(db.String(200))
    fandom = db.Column(db.String(100))
    tags = db.Column(db.Text)
    price = db.Column(db.String(50))
    image = db.Column(db.Text)
    status = db.Column(db.String(50))
    stock = db.Column(db.String(100))
    delivery = db.Column(db.String(100))