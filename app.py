from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)
plants = mongo.db.plants
harvests = mongo.db.harvests

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    # TODO: Replace the following line with a database call to retrieve *all*
    # plants from the Mongo database's `plants` collection.
    plants_data = plants.find()
    

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # TODO: Get the new plant's name, variety, photo, & date planted, and 
        # store them in the object below.

        plant_name = request.form.get('plant_name')
        variety = request.form.get('variety')
        photo = request.form.get('photo')
        date_planted = request.form.get('date_planted')

        new_plant = {
            'name': plant_name,
            'variety': variety,
            'photo_url': photo,
            'date_planted': date_planted
        }
        # TODO: Make an `insert_one` database call to insert the object into the
        # database's `plants` collection, and get its inserted id. Pass the 
        # inserted id into the redirect call below.

        insert_plant_id = plants.insert_one(new_plant).inserted_id


        return redirect(url_for('detail', plant_id=insert_plant_id))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""

    # TODO: Replace the following line with a database call to retrieve *one*
    # plant from the database, whose id matches the id passed in via the URL.
    plant_to_show = plants.find_one({"_id": ObjectId(plant_id)})

    harvests_to_find = harvests.find()

    context = {
        'plant' : plant_to_show,
        'harvests': harvests_to_find
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """

    # TODO: Create a new harvest object by passing in the form data from the
    # detail page form.
    quantity = request.form.get('harvested_amount')
    date = request.form.get('date_planted')

    new_harvest = {
        'quantity': quantity, # e.g. '3 tomatoes'
        'date': date,
        'plant_id': plant_id
    }

    harvests.insert_one(new_harvest).inserted_id

    # TODO: Make an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    name = request.form.get("plant_name")
    variety = request.form.get("variety")
    photo_url = request.form.get("photo")
    date_planted = request.form.get("date_planted")

    if request.method == 'POST':
        # TODO: Make an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.

        current_edit = {
            "name": name,
            "variety": variety,
            "photo_url": photo_url,
            "date_planted": date_planted
        }
        new_edit = {"$set": current_edit}
        plants.update_one({"_id": ObjectId(plant_id)}, new_edit)

        
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # TODO: Make a `find_one` database call to get the plant object with the
        # passed-in _id.
        plant_to_show = plants.find_one({"_id": ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # TODO: Make a `delete_one` database call to delete the plant with the given
    # id.
    plants.delete_one({"_id": ObjectId(plant_id)}, plant_id)


    # TODO: Also, make a `delete_many` database call to delete all harvests with
    # the given plant id.
    delete_all_harvests = harvests.find({"plant_id": (plant_id)})
    for item in delete_all_harvests:
        harvests.delete_one(item)

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

