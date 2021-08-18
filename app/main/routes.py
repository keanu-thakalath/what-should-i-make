from app.main import bp
from app.main.forms import RecipeForm, FilterForm
from app.models import Recipe
from app import db
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
import random

def SA_OR(exp1, exp2):
    return (exp1 | exp2) if exp1 is not None else exp2

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = FilterForm()
    if request.method == 'GET':
        form.meal.data = [c[0] for c in form.meal.choices]
        form.cuisine.data = [c[0] for c in form.cuisine.choices]
        form.meat.data = True
        form.vegetarian.data = True
        form.vegan.data = True
        form.difficulty_rating.data = 5
        form.taste_rating.data = 1

    query = Recipe.query.filter_by(user=current_user)
    if form.validate_on_submit():
        query = query.whooshee_search(form.query.data) if form.query.data else query
        query = query.filter(Recipe.meal.in_(form.meal.data))
        query = query.filter(Recipe.cuisine.in_(form.cuisine.data))
        query = query.filter(Recipe.difficulty_rating <= form.difficulty_rating.data)
        query = query.filter(Recipe.taste_rating >= form.taste_rating.data)

        meat = (Recipe.vegetarian == False) & (Recipe.vegan == False)
        vegetarian = Recipe.vegetarian == True
        vegan = Recipe.vegan == True

        final_expression = (meat if form.meat.data else None)
        final_expression = SA_OR(final_expression, vegetarian if form.vegetarian.data else None)
        final_expression = SA_OR(final_expression, (vegan if form.vegan.data else None))

        query = query.filter(final_expression)

    recipes = query.all()
    random.shuffle(recipes)
    return render_template('main/index.html', title='Home', form=form, recipes=recipes)

@bp.route('/recipes/<int:id>', methods=['GET', 'POST'])
@login_required
def recipe(id):
    recipe = Recipe.query.get(id)
    if recipe is None or recipe.user != current_user:
        return redirect(url_for('main.index.html'))

    form = RecipeForm(current_user, True, recipe.name)
    if form.validate_on_submit():
        if form.delete_submit.data:
            db.session.delete(recipe)
        else:
            recipe.name = form.name.data
            recipe.meal = form.meal.data
            recipe.cuisine = form.cuisine.data
            recipe.vegetarian = form.vegetarian.data
            recipe.vegan = form.vegan.data
            recipe.difficulty_rating = form.difficulty_rating.data
            recipe.taste_rating = form.taste_rating.data
        db.session.commit()

        return redirect(url_for('main.index'))

    if request.method == 'GET':
        form.name.data = recipe.name
        form.meal.data = recipe.meal
        form.cuisine.data = recipe.cuisine
        form.vegetarian.data = recipe.vegetarian
        form.vegan.data = recipe.vegan
        form.difficulty_rating.data = recipe.difficulty_rating
        form.taste_rating.data = recipe.taste_rating
    return render_template('main/recipe.html', title=recipe.name, recipe=recipe, form=form)

@bp.route('/recipes/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm(current_user)
    if form.validate_on_submit():
        recipe = Recipe(name=form.name.data, meal=form.meal.data, cuisine=form.cuisine.data,
            vegetarian=form.vegetarian.data, vegan=form.vegan.data,
            difficulty_rating=form.difficulty_rating.data, taste_rating=form.taste_rating.data,
            user=current_user)
        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('main/new_recipe.html', title='New Recipe', form=form)


