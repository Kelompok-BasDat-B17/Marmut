from lib_database.query import *
from datetime import datetime as dt


def search_user(email: str, password: str):
  query = f"SELECT email, password FROM AKUN WHERE email = '{email}' AND password = '{password}'"
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


