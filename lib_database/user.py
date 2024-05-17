from lib_database.query import *
from datetime import datetime as dt


def search_user(email: str, password: str):
  query = f"SELECT email, password FROM AKUN WHERE email = '{email}' AND password = '{password}'"
  data = get_data(query)
  return data

def search_label(email: str, password: str):
  query = f"SELECT email, password FROM LABEL WHERE email = '{email}' AND password = '{password}'"
  data = get_data(query)
  return data

def get_account(email: str):
  query = f"SELECT * FROM AKUN WHERE email = '{email}'"
  data = get_data(query)
  return data

def get_subscription(email: str):
  query = f"SELECT * FROM PREMIUM WHERE email = '{email}'"
  data = get_data(query)
  if len(data) == 0:
    return False
  return True

def check_subscription(email: str):
  is_premium = get_subscription(email)
  if is_premium == True:
    expired = get_data(f"SELECT check_subscription('{email}')")
    print(expired)
    if expired[0] == True:
      delete(f"DELETE FROM PREMIUM WHERE email = '{email}'")
      insert(f"INSERT INTO NON_PREMIUM VALUES ('{email}')")
      return "nonpremium"
    return "premium"
  return "nonpremium"

def get_role(email: str):
  list_role = []
  query1 = f"SELECT * FROM PODCASTER WHERE email = '{email}'"
  query2 = f"SELECT * FROM SONGWRITER WHERE email_akun = '{email}'"
  query3 = f"SELECT * FROM ARTIST WHERE email_akun = '{email}'"
  is_podcaster = get_data(query1)
  is_songwriter = get_data(query2)
  is_artist = get_data(query3) 
  if (len(is_podcaster) != 0): list_role.append("Podcaster")
  if (len(is_songwriter) != 0): list_role.append("Songwriter")
  if (len(is_artist) != 0): list_role.append("Artist")
  return list_role

def check_user(email: str):
  query = f"SELECT email FROM LABEL WHERE email = '{email}'"
  is_pengguna = get_data(query)
  if len(is_pengguna) != 0:
    return False
  else: 
    return True
  
def get_label(email: str):
  query = f"SELECT * FROM LABEL WHERE email = '{email}'"
  label = get_data(query)
  return label
def get_royalty_list(email: str):  
  id_pemilik_hak_cipta = get_id_pemilik_hak_cipta_label(email)
  if id_pemilik_hak_cipta == []:
    id_pemilik_hak_cipta = get_id_pemilik_hak_cipta_artist(email)
  if id_pemilik_hak_cipta == []:
    id_pemilik_hak_cipta = get_id_pemilik_hak_cipta_songwriter(email)
  id_pemilik_hak_cipta = id_pemilik_hak_cipta[0][0]
  query = f"SELECT * FROM GetRoyaltiesByCopyrightOwner('{id_pemilik_hak_cipta}');"
  data = get_data(query)
  return data

def get_id_pemilik_hak_cipta_label(email: str):
  query = f"SELECT id_pemilik_hak_cipta FROM LABEL WHERE email = '{email}'"
  data = get_data(query)
  return data

def get_id_pemilik_hak_cipta_artist(email: str):
  query = f"SELECT id_pemilik_hak_cipta FROM ARTIST WHERE email_akun = '{email}'"
  data = get_data(query)
  return data

def get_id_pemilik_hak_cipta_songwriter(email: str):
  query = f"SELECT id_pemilik_hak_cipta FROM SONGWRITER WHERE email_akun = '{email}'"
  data = get_data(query)
  return data

def get_user_name(email: str):
  query = f"SELECT nama FROM AKUN WHERE email = '{email}'"
  data = get_data(query)
  if data == []:
    query = f"SELECT nama FROM LABEL WHERE email = '{email}'"
    data = get_data(query)
  return data[0][0]

def get_label_name(email: str):
  query = f"SELECT nama FROM LABEL WHERE email = '{email}'"
  data = get_data(query)
  return data[0][0]

def get_user_type(email):
    user_type = None
    if check_in_artist(email):
        user_type = "Artist"
    elif check_in_songwriter(email):
        user_type = "Songwriter"
    elif check_in_label(email):
        user_type = "Label"
    
    return user_type

def check_in_songwriter(email):
    query = f"SELECT COUNT(*) FROM SONGWRITER WHERE email_akun = '{email}'"
    result = get_data(query)
    return result[0][0] > 0

def check_in_label(email):
    result = f"SELECT COUNT(*) FROM LABEL WHERE email = '{email}'"
    result = get_data(result)
    return result[0][0] > 0

def check_in_artist(email):
    query = f"SELECT COUNT(*) FROM ARTIST WHERE email_akun = '{email}'"
    result = get_data(query)
    return result[0][0] > 0

def insert_label(uuid: str, nama: str, email: str, password: str, kontak: str, id_pemilik_hak_cipta: str):
  query2 = f"INSERT INTO PEMILIK_HAK_CIPTA VALUES ('{id_pemilik_hak_cipta}', '{100}')"
  insert(query2)
  query1 = f"INSERT INTO LABEL VALUES ('{uuid}', '{nama}', '{email}', '{password}', '{kontak}', '{id_pemilik_hak_cipta}')"
  insert(query1)

def get_data_label(email: str):
  query = f"SELECT * FROM LABEL WHERE email = '{email}'"
  data = get_data(query)
  return data

def get_album_list_label(uu_id: str):
  query = f"SELECT * FROM FindAlbumsByLabelId('{uu_id}');"
  data = get_data(query)
  return data

def get_user_uu_id(email: str):
  query = f"SELECT id FROM LABEL WHERE email = '{email}'"
  data = get_data(query)
  return data[0][0]

def get_album_list_artist(email: str):
  query = f"SELECT * FROM get_album_details();"
  data = get_data(query)
  return data

def get_album_list_songwriter(email: str):
  query = f"SELECT * FROM get_album_details();"
  data = get_data(query)
  return data

def get_song_detail(song_name: str):
  query = f"SELECT * FROM GET_SONG_DETAIL('{song_name}');"
  data = get_data(query)
  return data

def get_song_album(album_name: str):
  query = f"SELECT * FROM SHOW_SONG_STATS_BY_ALBUM('{album_name}');"
  data = get_data(query)
  return data

def delete_album_by_name(album_name: str):
  query = f"SELECT id FROM ALBUM WHERE judul = '{album_name}'"
  album_id = get_data(query)
  if album_id == []:
    return False
  album_id = album_id[0][0]
  query = f"DELETE FROM ALBUM WHERE id = '{album_id}'"
  delete(query)
  return True

def delete_song_by_name(song_name: str):
  query = f"SELECT id FROM KONTEN WHERE judul = '{song_name}'"
  song_id = get_data(query)
  if song_id == []:
    return False
  song_id = song_id[0][0]
  query = f"DELETE FROM KONTEN WHERE id = '{song_id}'"
  delete(query)
  return True

def get_label_list():
  query = "SELECT nama FROM LABEL"
  data = get_data(query)
  return data

def get_label_uuid_by_name(nama: str):
  query = f"SELECT id FROM LABEL WHERE nama = '{nama}'"
  data = get_data(query)
  return data[0][0]

def insert_album(album_id: str, album_name: str, jumlah_lagu: int, album_label_id: str, total_durasi: int):
  query = f"INSERT INTO ALBUM VALUES ('{album_id}', '{album_name}', '{jumlah_lagu}', '{album_label_id}', '{total_durasi}')"
  insert(query)

def get_songwriter_name(email: str):
  query = f"SELECT nama FROM AKUN WHERE email = '{email}'"
  data = get_data(query)
  return data[0][0]

def get_artist_name(email: str):
  query = f"SELECT nama FROM AKUN WHERE email = '{email}'"
  data = get_data(query)
  return data[0][0]

def get_artist_list():
  query = "SELECT * FROM get_artist_names()"
  data = get_data(query)
  return data

def add_song_songwriter(song_id, song_name, song_artist_id, song_writer, song_genre, song_duration, album_name):
  date = dt.now().strftime("%Y-%m-%d")
  year = date.split("-")[0]
  album_id = get_album_id_by_name(album_name)
  # KONTEN
  query = f"INSERT INTO KONTEN VALUES ('{song_id}', '{song_name}', CURRENT_DATE, {year}, {song_duration})"
  insert(query)
  
  # SONG
  query = f"INSERT INTO SONG VALUES ('{song_id}', '{song_artist_id}', '{album_id}', '{0}', '{0}')"
  insert(query)
  
  # ROYALTI
  id_phc_artist = get_id_phc_artist_by_id(song_artist_id)
  query = f"INSERT INTO ROYALTI VALUES ('{id_phc_artist}', '{song_id}', '{0}')"
  insert(query)
  
  id_phc_songwriter = get_id_phc_songwriter_by_name(song_writer)
  query = f"INSERT INTO ROYALTI VALUES ('{id_phc_songwriter}', '{song_id}', '{0}')"
  insert(query)
  
  id_phc_label = get_id_phc_label_by_album(album_name)
  query = f"INSERT INTO ROYALTI VALUES ('{id_phc_label}', '{song_id}', '{0}')"
  insert(query)
  
  # GENRE
  for genre in song_genre:
    query = f"INSERT INTO GENRE VALUES ('{song_id}', '{genre}')"
    insert(query)
  
  # SONGWRITER_WRITE_SONG
  song_writer_id = get_songwriter_id(song_writer)
  query = f"INSERT INTO SONGWRITER_WRITE_SONG VALUES ('{song_writer_id}', '{song_id}')"

  # Tambah Durasi dan Jumlah Lagu Album
  durasi_album_baru = get_album_duration(album_id) + int(song_duration)
  jumlah_lagu_baru = get_album_song_count(album_id) + 1
  query = f"UPDATE ALBUM SET total_durasi = {durasi_album_baru}, jumlah_lagu = {jumlah_lagu_baru} WHERE id = '{album_id}'"

def get_songwriter_id(song_writer):
  query = f"SELECT get_songwriter_id_by_name('{song_writer}')"
  data = get_data(query)
  return data[0][0]

def get_album_id_by_name(album_name):
  query = f"SELECT id FROM ALBUM WHERE judul = '{album_name}'"
  data = get_data(query)
  return data[0][0]

def get_id_phc_artist_by_id(artist_id):
  query = f"SELECT id_pemilik_hak_cipta FROM ARTIST WHERE id = '{artist_id}'"
  data = get_data(query)
  return data[0][0]

def get_id_phc_songwriter_by_name(songwrtier_name):
  songwriter_email = get_akun_email_by_name(songwrtier_name)
  query = f"SELECT id_pemilik_hak_cipta FROM SONGWRITER WHERE email_akun = '{songwriter_email}'"
  data = get_data(query)
  return data[0][0]

def get_akun_email_by_name(artist_name):
  query = f"SELECT email FROM AKUN WHERE nama = '{artist_name}'"
  data = get_data(query)
  return data[0][0]

def get_id_phc_label_by_album(album_name):
  query = f"SELECT id_label FROM ALBUM WHERE judul = '{album_name}'"
  data = get_data(query)
  id_phc_label = get_id_phc_label_by_id(data[0][0])
  return id_phc_label

def get_id_phc_label_by_id(label_id):
  query = f"SELECT id_pemilik_hak_cipta FROM LABEL WHERE id = '{label_id}'"
  data = get_data(query)
  return data[0][0]

def get_album_duration(album_id):
  query = f"SELECT total_durasi FROM ALBUM WHERE id = '{album_id}'"
  data = get_data(query)
  return data[0][0]

def get_album_song_count(album_id):
  query = f"SELECT jumlah_lagu FROM ALBUM WHERE id = '{album_id}'"
  data = get_data(query)
  return data[0][0]

def get_songwriter_list():
  query = "SELECT * FROM get_songwriter_names()"
  data = get_data(query)
  return data

def add_song_artist(song_id, song_name, song_artist_id, song_writers, song_genres, song_duration, album_name):
  date = dt.now().strftime("%Y-%m-%d")
  year = date.split("-")[0]
  album_id = get_album_id_by_name(album_name)
  # KONTEN
  query = f"INSERT INTO KONTEN VALUES ('{song_id}', '{song_name}', CURRENT_DATE, {year}, {song_duration})"
  insert(query)

  # SONG
  query = f"INSERT INTO SONG VALUES ('{song_id}', '{song_artist_id}', '{album_id}', '{0}', '{0}')"
  insert(query)

  # ROYALTI
  id_phc_artist = get_id_phc_artist_by_id(song_artist_id)
  query = f"INSERT INTO ROYALTI VALUES ('{id_phc_artist}', '{song_id}', '{0}')"
  insert(query)

  for song_writer in song_writers:
    id_phc_songwriter = get_id_phc_songwriter_by_name(song_writer)
    query = f"INSERT INTO ROYALTI VALUES ('{id_phc_songwriter}', '{song_id}', '{0}')"
    insert(query)
  
  id_phc_label = get_id_phc_label_by_album(album_name)
  query = f"INSERT INTO ROYALTI VALUES ('{id_phc_label}', '{song_id}', '{0}')"
  insert(query)
  
  # GENRE

  for genre in song_genres:
    query = f"INSERT INTO GENRE VALUES ('{song_id}', '{genre}')"
    insert(query)
  
  # SONGWRITER_WRITE_SONG
  for song_writer in song_writers:
    song_writer_id = get_songwriter_id(song_writer)
    query = f"INSERT INTO SONGWRITER_WRITE_SONG VALUES ('{song_writer_id}', '{song_id}')"
    insert(query)

  # Tambah Durasi dan Jumlah Lagu Album
  durasi_album_baru = get_album_duration(album_id) + int(song_duration)
  jumlah_lagu_baru = get_album_song_count(album_id) + 1
  query = f"UPDATE ALBUM SET total_durasi = {durasi_album_baru}, jumlah_lagu = {jumlah_lagu_baru} WHERE id = '{album_id}'"

def get_artist_id_by_name(artist_name):
  # Get Email From AKUN
  query = f"SELECT email FROM AKUN WHERE nama = '{artist_name}'"
  data = get_data(query)
  artist_email = data[0][0]
  # Get ID From ARTIST
  query = f"SELECT id FROM ARTIST WHERE email_akun = '{artist_email}'"
  data = get_data(query)
  return data[0][0]