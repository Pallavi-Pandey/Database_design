from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class ProductEntryForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    size_id = SelectField('Size', coerce=int, validators=[DataRequired()])
    color_id = SelectField('Color', coerce=int, validators=[DataRequired()])
    material_id = SelectField('Material', coerce=int, validators=[DataRequired()])
    sku = IntegerField('SKU', validators=[DataRequired()])
    qty = FloatField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Product Entry')
