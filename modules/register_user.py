
from flask import jsonify, request
from werkzeug.security import generate_password_hash


class UserRegistration:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def register_user(self):
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')

        if not phone or not email or not password or not name:
            return jsonify({'message': 'Invalid input data'}), 400


        try:

            database_connection = self.database_initializer.get_database_connection()

            cursor = database_connection.cursor() 

            # Check if a record with the provided phone_number or email exists
            cursor.execute("SELECT id FROM users WHERE phone_number = %s OR email = %s;", (phone, email))
            existing_record = cursor.fetchone()

            if existing_record:
                # Record with the provided phone_number or email already exists; update it
                update_query = """
                    UPDATE users
                    SET name = %s, phone_number = %s, email = %s, password_hash = %s
                    WHERE id = %s;
                """
                cursor.execute(update_query, (name, phone, email, generate_password_hash(password), existing_record[0]))
            else:
                # No existing record found; insert a new one
                insert_query = "INSERT INTO users (name, phone_number, email, password_hash) VALUES (%s, %s, %s, %s);"
                cursor.execute(insert_query, (name, phone, email, generate_password_hash(password)))

            database_connection.commit()
            
            return jsonify({'message': 'User registered successfully'})

        except Exception as e:
            #return jsonify({'message': 'An error occured. Please contact support.', 'error': str(e)}), 500
            return jsonify({'message': str(e), 'error': str(e)}), 500 # For testing only
        finally:
            cursor.close()
            database_connection.close()