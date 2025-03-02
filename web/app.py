import os
import random
from datetime import datetime
from mysql.connector import Error
from flask import Flask, redirect, url_for, render_template, session, request, send_from_directory , jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functions import create_db_connection

import hashlib
import hmac
import os


# Your bot's token
BOT_TOKEN = '6425402449:AAGOkDCJMOQ4-t-1q8icX82WKQCJMAyIyC4'
# Your bot's username
BOT_USERNAME = 'HurryTutor_bot'
# Your secret key for creating a secure hash
SECRET_KEY = os.environ.get('SECRET_KEY', '5498603Ma.')


app = Flask(__name__)
app.secret_key = 'a9f3b9a7cfda4b3b9a8df9e23f67b8cd'


def check_telegram_authentication(bot_token, request_data):
    check_hash = request_data.pop('hash')
    token_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(request_data.items(), key=lambda x: x[0])])
    secret_key = hashlib.sha256(bot_token.encode('utf-8')).digest()
    hmac_string = hmac.new(secret_key, token_check_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac_string == check_hash


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')















@app.route('/courses')
def courses():

    username = session.get('username')

    connection = create_db_connection()
    if connection is None:
        return "Error connecting to the database"

    cursor = connection.cursor()

    # Check if there is any phone number of user in Table
    cursor.execute("SELECT phone_number FROM users WHERE telegram_id = %s", (username,))
    result = cursor.fetchone()  # This will fetch the first row of results

    # result will be None if there are no rows returned or a tuple of the values of the selected columns
    if result and result[0] is not None:
        # If the result is not None and the first item (which is phone_number) is also not None
        return render_template('project.html')
    else:
        # If the result is None (no such user) or the phone_number of the user is None
        return redirect(url_for('register_details'))


    connection.commit()
    cursor.close()
    connection.close()















@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')


def is_registered():
    return 'username' in session

@app.route('/login', methods=['GET'])
def login():

    if is_registered():
        return redirect(url_for('courses'))

    if 'id' in request.args:
        # Extract user credentials from Telegram authentication data
        telegram_id = request.args.get('id')
        name = request.args.get('first_name')
        surname = request.args.get('last_name')
        telegram_username = request.args.get('username')
        photo = request.args.get('photo_url')

        # Connect to the database
        connection = create_db_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        if cursor.fetchone():
            session['username'] = telegram_id
            return redirect(url_for('courses'))

        # Insert new user into the database
        insert_query = """
        INSERT INTO users (telegram_id, name, surname, telegram_username, photo)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (telegram_id, name, surname, telegram_username, photo))
        connection.commit()
        cursor.close()
        connection.close()

        session['username'] = telegram_id


        return redirect(url_for('courses'))

    # If no Telegram parameters, render the standard registration page
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register():

    if is_registered():
        return redirect(url_for('courses'))

    if 'id' in request.args:
        # Extract user credentials from Telegram authentication data
        telegram_id = request.args.get('id')
        name = request.args.get('first_name')
        surname = request.args.get('last_name')
        telegram_username = request.args.get('username')
        photo = request.args.get('photo_url')

        # Connect to the database
        connection = create_db_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        if cursor.fetchone():
            session['username'] = telegram_id
            return redirect(url_for('courses'))

        # Insert new user into the database
        insert_query = """
        INSERT INTO users (telegram_id, name, surname, telegram_username, photo)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (telegram_id, name, surname, telegram_username, photo))
        connection.commit()
        cursor.close()
        connection.close()

        session['username'] = telegram_id


        return redirect(url_for('courses'))

    # If no Telegram parameters, render the standard registration page
    return render_template('sign-up.html')



@app.route('/register/details', methods=['GET', 'POST'])
def register_details():
    if request.method == 'POST':
        username = session.get('username')

        phone_number = request.form['phone_number']

        # Connect to the database
        connection = create_db_connection()

        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor()

        update_query = "UPDATE users SET phone_number = %s WHERE telegram_id = %s"

        cursor.execute(update_query, (phone_number, username))
        connection.commit()
        cursor.close()
        connection.close()

        # Retrieve stored Telegram data if needed


        return redirect(url_for('courses'))

    # Render a form for additional details including a phone number field
    return render_template('register_details.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/img/<path:filename>')
def get_image(filename):
    return send_from_directory('static/img', filename)

if __name__ == '__main__':
    app.run(debug=True)