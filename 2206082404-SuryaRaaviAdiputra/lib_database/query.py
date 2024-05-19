from django.db import connection

def execute_query(query: str):
  with connection.cursor() as cursor:
    cursor.execute(query)
  
def get_data(query: str):
  with connection.cursor() as cursor:
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def select(query: str):
  return get_data(query)

def insert(query: str):
  execute_query(query)

def update(query: str):
  execute_query(query)

def delete(query: str):
  execute_query(query)