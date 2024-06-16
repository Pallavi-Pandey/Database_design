from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import ProductForm, ProductEntryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'product'  # Replace with your actual secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models here (same as before)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    entries = db.relationship('ProductEntry', backref='product', lazy=True)

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size_value = db.Column(db.String(50), nullable=False)

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_value = db.Column(db.String(50), nullable=False)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_value = db.Column(db.String(50), nullable=False)

class ProductEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    sku = db.Column(db.Integer, nullable=False, unique=True)
    qty = db.Column(db.Float, nullable=False)

    size = db.relationship('Size', backref=db.backref('entries', lazy=True))
    color = db.relationship('Color', backref=db.backref('entries', lazy=True))
    material = db.relationship('Material', backref=db.backref('entries', lazy=True))

def insert_initial_data():
    sizes = ['Small', 'Medium', 'Large']
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Purple', 'Orange', 'Pink', 'Brown']
    materials = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Leather', 'Linen', 'Denim', 'Nylon', 'Suede', 'Velvet']

    for size in sizes:
        if not Size.query.filter_by(size_value=size).first():
            db.session.add(Size(size_value=size))
    
    for color in colors:
        if not Color.query.filter_by(color_value=color).first():
            db.session.add(Color(color_value=color))

    for material in materials:
        if not Material.query.filter_by(material_value=material).first():
            db.session.add(Material(material_value=material))

    db.session.commit()

with app.app_context():
    db.create_all()
    insert_initial_data()

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('add_product_entry', product_id=product.id))
    return render_template('add_product.html', form=form)

@app.route('/add_product_entry', methods=['GET', 'POST'])
def add_product_entry():
    form = ProductEntryForm()
    form.product_id.choices = [(product.id, product.name) for product in Product.query.all()]
    form.size_id.choices = [(size.id, size.size_value) for size in Size.query.all()]
    form.color_id.choices = [(color.id, color.color_value) for color in Color.query.all()]
    form.material_id.choices = [(material.id, material.material_value) for material in Material.query.all()]

    # Preselect product if product_id is provided in the query string
    selected_product_id = request.args.get('product_id')
    if selected_product_id:
        form.product_id.data = int(selected_product_id)
    
    if form.validate_on_submit():
        product_entry = ProductEntry(
            product_id=form.product_id.data,
            size_id=form.size_id.data,
            color_id=form.color_id.data,
            material_id=form.material_id.data,
            sku=form.sku.data,
            qty=form.qty.data
        )
        db.session.add(product_entry)
        db.session.commit()
        flash('Product entry added successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('add_product_entry.html', form=form)

@app.route('/')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
