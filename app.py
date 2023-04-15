from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import psycopg2
conn = psycopg2.connect(YOUR_DATABASE_URL)

cursor = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    data = ''
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (ID SERIAL UNIQUE, TASKS varchar(200), CREATED_DATE varchar(200), DUE_DATE varchar(200)) ;''')
            cursor.execute('''SELECT * FROM USERS ;''')
            data = cursor.fetchall()
    return render_template('todo.html', tasks=data)

@app.route('/addtodo', methods=['POST'])
def add_todo():
        now = date.today()
        data = request.form
        task = data['task']
        duedate = data['duedate']
        with conn:
            with conn.cursor() as cursor:
                 cursor.execute('''INSERT INTO USERS (TASKS , CREATED_DATE , DUE_DATE) VALUES (%s, %s, %s);''' ,(task, now, duedate))
        
        return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
