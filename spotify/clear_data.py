import sqlite3

conn = sqlite3.connect('stupk_spotify.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Track;'
            'DROP TABLE IF EXISTS ARTIST;'
            'DROP TABLE IF EXISTS ALBUM')
conn.commit()
cur.close()