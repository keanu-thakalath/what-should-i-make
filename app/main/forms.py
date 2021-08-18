from app.models import Recipe
from app import db
from flask import current_app
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, SelectField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError

class FilterForm(FlaskForm):
    query = StringField('Query')
    meal = SelectMultipleField('Meal of the Day', choices=[(c, c) for c in ['Breakfast', 'Lunch', 'Dinner', 'Snack']])
    cuisine = SelectMultipleField('Cuisine')
    meat = BooleanField('Meat')
    vegetarian = BooleanField('Vegetarian')
    vegan = BooleanField('Vegan')
    difficulty_rating = SelectField('Maximum Difficulty', choices=[(str(i), str(i)) for i in range(1, 6)], coerce=int)
    taste_rating = SelectField('Minimum Taste', choices=[(str(i), str(i)) for i in range(1, 6)], coerce=int)
    submit = SubmitField('Filter')

    def __init__(self):
        super().__init__()
        self.cuisine.choices = [(c, c) for c in current_app.config['CUISINES']]

    def validate_vegan(self, vegan):
        if (vegan.data and not self.vegetarian.data):
            raise ValidationError('The recipe must be vegetarian if it is vegan.')

    def validate_meat(self, meat):
        if (not meat.data and not self.vegetarian.data and not self.vegan.data):
            raise ValidationError('The results must have meat, be vegetarian or be vegan.')

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    meal = SelectField('Meal of the Day', choices=[(c, c) for c in ['Breakfast', 'Lunch', 'Dinner', 'Snack']])
    cuisine = SelectField('Cuisine')
    vegetarian = BooleanField('Vegetarian')
    vegan = BooleanField('Vegan')
    difficulty_rating = SelectField('Difficulty', choices=[(str(i), str(i)) for i in range(1, 6)], coerce=int)
    taste_rating = SelectField('Taste', choices=[(str(i), str(i)) for i in range(1, 6)], coerce=int)
    submit = SubmitField('Create Recipe')
    delete_submit = SubmitField('Delete Recipe')

    def __init__(self, user, editing=False, initial_name=None):
        super().__init__()
        self.user = user
        self.cuisine.choices = [(c, c) for c in current_app.config['CUISINES']]
        self.editing = editing
        self.initial_name = initial_name
        if editing:
            self.submit.label.text = 'Edit Recipe'

    def validate_vegan(self, vegan):
        if (vegan.data and not self.vegetarian.data):
            raise ValidationError('The recipe must be vegetarian if it is vegan.')

    def validate_name(self, name):
        recipe = Recipe.query.filter(func.lower(Recipe.name) == func.lower(name.data)).first()
        if self.editing:
            if recipe is not None and recipe.name != self.initial_name:
                raise ValidationError('You already have a recipe with this name.')
        elif recipe is not None:
            raise ValidationError('You already have a recipe with this name.')
