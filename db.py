import mariadb

conn = mariadb.connect(
        user="root",
        password="12345678",
        host="localhost",
        port=3306,
        database="test"
    )

# SQL-запрос для добавления значения
sql_query = """
INSERT INTO tree (path, size, attr, date_c, date_u, date_l, id_task, flag_t, flag_e)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def connect_db():
  try:
      # Connect to the database
      global conn

  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")

def disconnect_db():
  try:
      global conn
      conn.close()

  except mariadb.Error as e:
      print(f"Error disconnecting from MariaDB: {e}")


def print_table_db(name):
  try:
      global conn
      cur = conn.cursor()
      # Execute a query
      cur.execute(f"SELECT * FROM {name}")

      # Fetch and display the result
      for row in cur.fetchall():
        print(row)

      cur.close()

  except mariadb.Error as e:
      print(f"Error print table {name} MariaDB: {e}")


def take_path_db(task_type):
  try:
      global conn
      cur = conn.cursor()
      cur.execute(f"SELECT * FROM task WHERE task.`type` = {task_type}")
      data = cur.fetchall()
      #print(data)
      data_path = []
      cur.close()
      for path,type in data:
        data_path.append(path)
      return data_path

  except mariadb.Error as e:
      print(f"Error take path from MariaDB task: {e}")


def add_to_db(data):
  try:
      global conn
      cur = conn.cursor()
      # Выполнение запроса
      cur.execute(sql_query, data)

      # Коммит изменений
      conn.commit()
      print("Value added successfully")

  except mariadb.Error as e:
    # Откат транзакции при ошибке
    conn.rollback()
    print(f"An error occurred: {e}")




# connect_db()
# #print_table_db("task")
# test = take_path_db(2)
# print(test)
# disconnect_db()