from flask import Flask, render_template, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongo', 27017)
db = client.FlaskAppDocker
collection_movie = db['movies']

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/insert/", methods=['POST', 'GET'])
def insert_movie():
    if request.method == 'POST':
        nom  = request.form['nom']
        genre = request.form['genre']
        last_movie_id = get_last_movie_id()
        current_movie_id = last_movie_id + 1
        movie_dict = {         
            "movie_id": current_movie_id,         
            "nom"    : nom,         
            "genre"   : genre     
            }
        collection_movie.insert_one(movie_dict)
        success = True
        return render_template('index.html', success=success)
    return render_template('insert_movie.html')



def get_last_movie_id():
    last_movie_id  = collection_movie.find().sort([('movie_id', -1)]).limit(1)
    try:
        last_movie_id = last_movie_id[0]['movie_id']
    except:
        last_movie_id = 0
    return last_movie_id



@app.route("/get_all/", methods=['GET'])
def get_all_movie():
    movies = collection_movie.find()
    movies_list = []
    for item in movies:
        movie_dict = {
            "movie_id": item['movie_id'],
            "nom"    : item['nom'],
            "genre"   : item['genre']
        }
        movies_list.append(movie_dict)
    return render_template('list_movie.html', movies_list=movies_list)



@app.route('/edit/<int:movie_id>', methods=('GET', 'POST'))
def edit_movie(movie_id):

    if request.method == 'POST':
        nom  = request.form['nom']
        genre = request.form['genre']
        movie_dict = {
            "nom" : nom,
            "genre": genre
            }
        collection_movie.update_many({'movie_id': int(movie_id)}, {'$set': movie_dict})
        updated = True
        return render_template('index.html', updated=updated)
    movie_to_update = collection_movie.find_one({"movie_id":movie_id})
    return render_template('edit_movie.html', movie_to_update=movie_to_update)




@app.route("/delete/<movie_id>", methods=('GET', 'POST'))
def delete_one_movie(movie_id):
    collection_movie.delete_many({'movie_id': int(movie_id)})
    deleted = True
    return render_template('index.html', deleted=deleted)


if __name__ == "__main__":
    app.run(debug=True)