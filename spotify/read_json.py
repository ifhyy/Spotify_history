import sqlite3
import json
from functions import milliseconds_to_ms

conn = sqlite3.connect('stupk_spotify.sqlite')
cur = conn.cursor()

#Create Tables
cur.executescript('''
        CREATE TABLE IF NOT EXISTS Album(id INTEGER PRIMARY KEY, Name TEXT UNIQUE, Artist_id INTEGER);
        CREATE TABLE IF NOT EXISTS Artist(id INTEGER PRIMARY KEY, Name TEXT UNIQUE);
        CREATE TABLE IF NOT EXISTS Track(id INTEGER PRIMARY KEY, Name TEXT, Artist_id INTEGER, Album_id INTEGER,
        Duration TEXT, Times_Played INTEGER)''')


filename = 'endsong_'+input('Chose which file to open: 0 or 1\n')+'.json'
data = open(filename, encoding='utf8').read()
json_data = json.loads(data)

for j in json_data:
    track_name = j["master_metadata_track_name"]
    # track_name = track_name[:track_name.find('(')]
    artist_name = j["master_metadata_album_artist_name"]
    album_name = j["master_metadata_album_album_name"]
    if j["reason_end"] == "trackdone":
        duration = int(j["ms_played"])
        duration = milliseconds_to_ms(duration)
        print(duration)
    else:
        duration = '0'

    #Check if entry is a track
    if not track_name: continue

    # Check if Track is already in a base
    cur.execute('SELECT Artist.Name, Track.Name, Track.Times_played, Artist.id FROM Track JOIN Artist ON Track.Artist_id = Artist.id '
                'WHERE Track.Name = ? and Artist.Name = ?', (track_name, artist_name))
    info = cur.fetchone()
    if info:
        cur.execute('UPDATE Track SET Times_played=? WHERE Name=? and Artist_id=?',
                    (info[2] + 1, track_name, info[3]))
        if j["reason_end"] == "trackdone":
            cur.execute('UPDATE OR IGNORE Track SET duration=? WHERE Name=? and Artist_id=?', (duration, info[1], info[3]))
        conn.commit()
        print(info[1])
        continue


    # Inserting data into database
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist_name, ))
    cur.execute('SELECT id FROM Artist WHERE name=?', (artist_name, ))
    artist_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Album (name, artist_id) VALUES (?, ?)', (album_name, artist_id))
    cur.execute('SELECT id FROM Album WHERE name=? and artist_id=?', (album_name, artist_id))
    # Chech if track got no album information
    try:album_id = cur.fetchone()[0]
    except: album_id = 'no album'
    cur.execute('INSERT OR IGNORE INTO Track (name, artist_id, album_id, duration, times_played) '
                'VALUES (?, ?, ?, ?, ?)', (track_name, artist_id, album_id, duration, 1))

    conn.commit()
    print(track_name)
cur.execute('UPDATE Track SET duration= ? WHERE duration=?', ('3:00', 0))
conn.commit()
cur.close()
