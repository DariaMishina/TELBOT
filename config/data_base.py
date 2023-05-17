import sqlite3 

conn = sqlite3.connect('./data/userbase.db', check_same_thread=False)
cursor = conn.cursor()

# Загрузка пользователя в таблицу
def db_table_val(user_id: int):
    cursor.execute('INSERT INTO user_base (user_id) VALUES (?)', (user_id,))
    conn.commit()
    
# Проверка на наличие пользователя в базе данных
def user_exists(user_id: int):
    cursor.execute("SELECT 1 FROM user_base WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result is not None

# Обновление запроса пользователя
def db_update_prompt(user_id: int, prompt: str):
    cursor.execute('UPDATE user_base \
                    SET prompt = ? WHERE user_id = ?', (prompt, user_id))
    conn.commit()
    
# Обновление времени 
def db_update_time(user_id: int, time:str):
    cursor.execute('UPDATE user_base \
                    SET time = ? WHERE user_id = ?', (time, user_id))
    conn.commit()

# Обновление ингредиента
def db_update_ingredient(user_id: int,ingredient:str):
    cursor.execute('UPDATE user_base \
                    SET ingredient = ? WHERE user_id = ?', (ingredient, user_id))
    conn.commit()
    
# Обновление блюда 
def db_update_dishes(user_id: int,dishes:str):
    cursor.execute('UPDATE user_base \
                    SET dishes = ? WHERE user_id = ?', (dishes, user_id))
    conn.commit()

# Обновление категории
def db_update_category(user_id: int, category:str):
    cursor.execute('UPDATE user_base \
                    SET category = ? WHERE user_id = ?', (category, user_id))
    conn.commit()

# Получение данных из записи
def get_db_value(user_id: int, column: str):
    result = cursor.execute(f'SELECT {column} FROM user_base WHERE user_id = {user_id}').fetchall()
    conn.commit()
    return result[0][0]

# Получение данных из записи
def get_db_all_value(user_id: int):
    result = cursor.execute(f'SELECT * FROM user_base WHERE user_id = {user_id}').fetchall()
    conn.commit()
    return result[0][2:]
    