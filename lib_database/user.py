from lib_database.query import *
from datetime import datetime as dt


def search_user(email: str, password: str):
  query = f"SELECT email, password FROM AKUN WHERE email = '{email}' AND password = '{password}'"
  data = get_data(query)
  return data

def search_label(email: str, password: str):
  query = f"SELECT email, password FROM LABEL WHERE email = '{email}' AND password = '{password}'"
  data = get_data(query)
  print(data)
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
    if expired[0] == True:
      delete(f"DELETE FROM PREMIUM WHERE email = '{email}'")
      insert(f"INSERT INTO NON_PREMIUM VALUES ('{email}')")
      return "nonpremium"
    return "premium"
  return "nonpremium"

def get_royalty_list(email: str):
  query = f"SELECT * FROM SHOW_ROYALTY_LIST_BY_EMAIL('{email}')"
  data = get_data(query)
  return data

def get_user_name(email: str):
  query = f"SELECT nama FROM AKUN WHERE email = '{email}'"
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

def insert_label(email: str, password: str, nama: str, kontak: str):
  query = f"INSERT INTO LABEL VALUES ('{email}', '{password}', '{nama}', '{kontak}')"
  insert(query)