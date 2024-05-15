from query import *
from datetime import datetime as dt


def search_user(email: str, password: str):
  query = f"SELECT email, password FROM AKUN WHERE email = '{email}' AND password = '{password}'"
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
    if expired[0] == True:
      delete(f"DELETE FROM PREMIUM WHERE email = '{email}'")
      insert(f"INSERT INTO NON_PREMIUM VALUES ('{email}')")
      return "nonpremium"
    return "premium"
  return "nonpremium"



