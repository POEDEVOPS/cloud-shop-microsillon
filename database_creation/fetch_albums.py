# script that inits the microsillon shop database with following info:
# - shop name
# - users : admin and buyer
# - albums and artists of selected style

import discogs_client
from discogs_client.exceptions import HTTPError
import psycopg2
import random
import time
import os

# utility functions
def downloadCover(image_uri, album) :
    content, resp= discogsclient._fetcher.fetch(None, "GET", image_uri, headers={"User-agent": discogsclient.user_agent})
    file = open(album, "wb")
    file.write(content)
    file.close()

def random_between(a, b):  
    return random.randint(a, b)

# search variables
shop_name = os.environ['SHOP_NAME']
total_albums = int(os.environ['TOTAL_ALBUMS'])
music_style= os.environ['MUSIC_STYLE']
print("Microsillon Shop Database Generator")
print("-----------------------------------")
print("")
print("Shop details : ")
print("Shop name : {}".format(shop_name))
print("Total albums : {}".format(str(total_albums)))
print("Music style : {}".format(music_style))
print("")

# API keys
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token= os.environ['ACCESS_TOKEN']
access_secret=os.environ['ACCESS_SECRET']

# DB keys
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

# Users passwords
USER_ADMIN_PW = os.environ['USER_ADMIN_PW']
USER_GUEST_PW = os.environ['USER_GUEST_PW']

# connecting to the database
print("Database setup")
print("--------------")
print("")
print("Connecting to database ...")
print("")
try:
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    print("Connection successful !")

    # Create a cursor object
    cursor = conn.cursor()

    # opening file
    file = open("microsillon.sql", "a")

    # Creating SHOP 
    print("Generating the tables ...")
    print("")

    print("Creating table SHOP")
    query="CREATE TABLE shop(id SERIAL PRIMARY KEY,name VARCHAR(255),style VARCHAR(255));"
    file.write("-- TABLE CREATE\n")
    file.write(query)
    file.write("\n")
    cursor.execute(query)

    # Creating USERS 
    print("Creating table USERS")
    query = "CREATE TABLE users(id SERIAL PRIMARY KEY,login VARCHAR(50),password VARCHAR(50),role VARCHAR(50),avatar VARCHAR(255));"
    file.write(query)
    file.write("\n")
    cursor.execute(query)

    # Creating ALBUMS 
    print("Creating table ALBUMS")
    query="CREATE TABLE albums(id SERIAL PRIMARY KEY,title VARCHAR(255),year VARCHAR(4),artist_id VARCHAR(255),labels VARCHAR(255),art VARCHAR(255),stock INTEGER,price INTEGER);"
    file.write(query)
    file.write("\n")
    cursor.execute(query)

    # Creating ARTISTS 
    print("Creating table ARTISTS")
    query="CREATE TABLE artists(id SERIAL PRIMARY KEY,name VARCHAR(255),style VARCHAR(255));"
    file.write(query)
    file.write("\n\n")
    cursor.execute(query)

    # Commiting changes
    conn.commit()

    # adding shop name
    print("Adding shop data")
    query="insert into shop (name,style) "
    query=query+"values ('{}','{}');".format(shop_name.replace("'", ""), music_style.replace("'", ""))

    file.write("-- SHOP INFO INSERT\n")
    file.write(query)
    file.write("\n\n")
    # Exec query
    cursor.execute(query)
    conn.commit()

    # adding users
    # adding admin
    print("")
    print("Creating users")
    print("")

    print("Adding user : admin")
    query="insert into users (id, login, password, role, avatar) "
    query=query+"values ({},'{}','{}', '{}', {});".format(1,"admin", USER_ADMIN_PW, "admin", "/avatars/admin.jpg" )
    file.write("-- USERS INSERT\n")
    file.write(query)
    file.write("\n")
    cursor.execute(query)
    conn.commit()
    # adding user
    print("Adding user : guest")
    query="insert into users (id, login, password, role, avatar) "
    query=query+"values ({},'{}','{}', '{}', {});".format(2,"guest", USER_GUEST_PW, "client", "/avatars/user.jpg" )
    file.write(query)
    file.write("\n\n")
    cursor.execute(query)
    conn.commit()
    print("")

    # instantiate our discogs_client object
    print("Connecting to the discogs API ...")
    print("")
    discogsclient = discogs_client.Client("discogs_api_example/2.0", consumer_key=consumer_key, consumer_secret=consumer_secret, token=access_token, secret=access_secret)
    print("Connection successful")

    # search
    print("Searching the discogs database ...")
    search_results = discogsclient.search(type="release", style=music_style)
    print("Search complete")

    # save results
    print("")
    print("Inserting albums and artists in the DB")
    print("")
    file.write("-- ALBUMS and ARTISTS insert\n")

    albums=1
    for release in search_results:
        # album data
        album_id=release.id
        album_artist_id="".join(str(artist.id) for artist in release.artists)
        album_title=release.title.replace("'", "")
        if "live" in album_title.lower() :
            continue
        album_year=release.year
        album_labels="".join(label.name for label in release.labels).replace("'", "")
        cover_filename="./covers/{}.jpg".format(album_title.replace(" ", "_")).replace("'", "")
        album_cover=downloadCover(release.images[0]["uri"], cover_filename)

        # artist data
        artist_name="".join(artist.name for artist in release.artists).replace("'", "")
        artist_style=music_style

        # inserting albums in the db
        query="insert into albums (id,title,artist_id,year,labels,art,stock,price) "
        query=query+"values ({},'{}',{},'{}','{}',{},{},{});".format(album_id, album_title, album_artist_id, album_year, album_labels, cover_filename , random_between(1,10), random_between(5,25))
        # Exec query
        print("inserting album {}/{}".format(albums, total_albums))
        file.write(query)
        file.write("\n")
        cursor.execute(query)
        conn.commit()

        # inserting artists in the db
        # checking existence
        query="select count(id) from artists where id={};".format(album_artist_id)
        cursor.execute(query)
        result=int(cursor.fetchall()[0][0])
        if result == 0:
            print("Inserting artist")
            query="insert into artists (id,name,style) "
            query=query+"values ({},'{}','{}');".format(album_artist_id, artist_name, music_style)
            # Exec query
            file.write(query)
            file.write("\n")
            cursor.execute(query)
            conn.commit()
        else:
            print("Existing artist")
        
        # checking for number of albums
        if albums >= total_albums:
            file.close()
            break
        albums=albums+1

except (Exception, psycopg2.Error) as error:
    print(error)