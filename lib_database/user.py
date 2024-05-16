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
  query2 = f"INSERT INTO PEMILIK_HAK_CIPTA VALUES ('{id_pemilik_hak_cipta}', '{0}')"
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
  query = f"SELECT * FROM FIND_ALBUMS_BY_SONGWRITER_EMAIL('{email}');"
  data = get_data(query)
  return data

def get_album_list_songwriter(email: str):
  query = f"SELECT * FROM FIND_ALBUMS_BY_SONGWRITER_EMAIL('{email}');"
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
  query = f"SELECT id FROM ALBUM WHERE nama_album = '{album_name}'"
  album_id = get_data(query)
  if album_id == []:
    return False
  album_id = album_id[0][0]
  query = f"DELETE FROM ALBUM WHERE id = '{album_id}'"
  delete(query)
  return True

def delete_song_by_name(song_name: str):
  query = f"SELECT id FROM LAGU WHERE nama_lagu = '{song_name}'"
  song_id = get_data(query)
  if song_id == []:
    return False
  song_id = song_id[0][0]
  query = f"DELETE FROM LAGU WHERE id = '{song_id}'"
  delete(query)
  return True