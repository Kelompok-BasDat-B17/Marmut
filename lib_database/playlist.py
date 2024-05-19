from lib_database.query import *
from datetime import datetime as dt
import uuid

class Playlist():
  list_playlist = []
  def __init__(self, id_playlist, judul: str, jumlah_lagu: str, deskripsi: str, total_durasi, tanggal_dibuat):
    self.id_playlist = id_playlist
    self.judul = judul
    self.jumlah_lagu = jumlah_lagu
    self.deskripsi = deskripsi
    self.total_durasi = total_durasi
    self.tanggal_dibuat = tanggal_dibuat
    Playlist.list_playlist.append(self)

class Songs():
  list_song = []
  def __init__(self, judul, nama, durasi, id_lagu):
    self.judul = judul
    self.nama = nama
    self.durasi = durasi
    self.id_lagu = id_lagu
    Songs.list_song.append(self)

def get_song(id_playlist: str):
  query = f"SELECT k.id, k.judul, k.tanggal_rilis, k,tahun, k.durasi FROM PLAYLIST_SONG AS ps JOIN KONTEN AS k ON ps.id_song = k.id WHERE ps.id_playlist = '{id_playlist}'"
  song_list = get_data(query)
  return song_list

def get_user_detail(id_playlist: str):
  for playlist in Playlist.list_playlist:
    if str(playlist.id_playlist) == id_playlist:
      return playlist

def get_playlist(email: str):
  query = f"""
      SELECT 
        up.id_playlist, 
        up.judul, 
        COUNT(k.id) AS jumlah_lagu,  
        up.deskripsi, 
        SUM(k.durasi) AS total_durasi,  
        up.tanggal_dibuat 
    FROM 
        USER_PLAYLIST AS up 
    LEFT JOIN 
        PLAYLIST_SONG AS sp ON up.id_playlist = sp.id_playlist 
    LEFT JOIN 
        KONTEN AS k ON k.id = sp.id_song 
    WHERE 
        up.email_pembuat = '{email}' 
    GROUP BY 
        up.id_playlist, up.judul, up.deskripsi, up.tanggal_dibuat 
    ORDER BY 
        up.tanggal_dibuat DESC;"""
  playlist = get_data(query)
  return playlist

def get_pembuat(email: str):
  query = f"SELECT nama FROM AKUN WHERE email = '{email}'"
  return get_data(query)

def get_detail_playlist(id_playlist: str):
  list_detail_song = get_data(f"SELECT k.judul, a.nama, k.durasi, ps.id_song FROM PLAYLIST_SONG AS ps JOIN SONG AS s ON ps.id_song = s.id_konten JOIN KONTEN AS k ON ps.id_song = k.id JOIN ARTIST AS ar ON s.id_artist = ar.id JOIN AKUN AS a ON ar.email_akun = a.email WHERE ps.id_playlist = '{id_playlist}'")
  return list_detail_song

def get_id_user_playlist():
  user_playlist = get_data(f"SELECT id_user_playlist FROM USER_PLAYLIST")
  return user_playlist

def get_id_playlist(email: str):
  id_playlist = get_data(f"SELECT id_playlist FROM USER_PLAYLIST WHERE email = '{email}'")
  return id_playlist

def insert_playlist(id_playlist: uuid, judul: str, deskripsi: str, email: str, id_user_playlist: uuid):
  insert(f"INSERT INTO PLAYLIST VALUES ('{id_playlist}');")
  insert(f"INSERT INTO USER_PLAYLIST VALUES ('{email}', '{id_user_playlist}', '{judul}', '{deskripsi}', {0}, '{dt.now()}', '{id_playlist}', {0})")

def del_playlist(id_playlist: str):
  delete(f"DELETE FROM PLAYLIST WHERE id = '{id_playlist}'")

def get_list_lagu():
  return get_data(f"SELECT s.id_konten, k.judul, a.nama FROM SONG AS s JOIN KONTEN AS k ON s.id_konten = k.id JOIN ARTIST AS ar ON s.id_artist = ar.id JOIN AKUN AS a ON ar.email_akun = a.email ORDER BY k.judul ASC")

def add_song(id_playlist: uuid, id_song: uuid):
  insert(f"INSERT INTO PLAYLIST_SONG VALUES ('{id_playlist}', '{id_song}')")

def del_song(id_playlist, id_song):
  delete(f"DELETE FROM PLAYLIST_SONG WHERE id_playlist = '{id_playlist}' AND id_song = '{id_song}'")