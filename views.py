from flask import render_template, request, Blueprint
from features import extract, pd
from model import recommend_from_playlist
from main import *

views = Blueprint(__name__, "views")

# grab songDF and complete_feature_set
songDF = pd.read_csv("./data/allsong_data.csv")
complete_feature_set = pd.read_csv("./data/complete_feature.csv")


@views.route("/")
def home():
    # render the home page
    return render_template('home.html')


@views.route('/recommend', methods=['POST'])
def recommend():

    # requesting the URL form the HTML form
    URL = request.form['URL']

    # using the extract function to get a features dataframe
    df = extract(URL)

    # retrieve the results and get as many recommendations as the user requested
    top40 = recommend_from_playlist(songDF, complete_feature_set, df)

    number_of_recs = int(request.form['number-of-recs'])
    my_songs = []
    for i in range(number_of_recs):
        my_songs.append([str(top40.iloc[i, 0]) + ' - ' + '"' + str(top40.iloc[i, 2]) + '"',
                         "https://open.spotify.com/track/" + str(top40.iloc[i, 1])])

    templates = ['results.html', 'image.html']
    return render_template(templates, songs=my_songs)


@views.route('/top-artist')
def image():

    token = get_token()
    result = search_for_artist(token, "olivia")

    artist_name = result['name']
    artist_image = result['images'][0]

    image_parameters = {
        'height': artist_image['height'],
        'url': artist_image['url'],
        'width': artist_image['width']
    }

    # artist_id = result["id"]
    # songs = get_songs_by_artist(token, artist_id)

    # for idx, song in enumerate(songs):
    #     print(f"{idx + 1}. {song['name']}")

    return render_template('image.html', image_parameters=image_parameters, top_artist_name=artist_name)
