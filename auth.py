import csv
from getpass import getpass
from utils import hash_password, verify_password, validate_email, validate_password
from datetime import datetime
from sunrise_sunset import get_sunrise_sunset  # Correct import for the function
import bcrypt
LOG_FILE = 'log.csv'
USER_DATA_FILE = 'regno.csv'  # User data file

# Log user activity including login/logout details
def log_user_activity(email, action, sunrise=None, sunset=None, solar_noon=None, day_length=None, login_time=None):
    with open(LOG_FILE, 'a', newline='', encoding='utf-8-sig') as logfile:
        writer = csv.writer(logfile)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if action == 'login':
            writer.writerow([email, action, login_time, sunrise, sunset, solar_noon, day_length, ''])
        elif action == 'logout':
            logout_time = current_time
            session_duration = (datetime.now() - datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 60.0  # duration in minutes
            writer.writerow([email, action, login_time, '', '', '', '', logout_time, session_duration])

# Register new users
def register_user():
    email = input("Enter your email (example@gmail.com): ")
    if not validate_email(email):
        print("Invalid email format.")
        return False
    
    while True:
        password = getpass("Enter password (hidden): ")
        if not validate_password(password):
            print("Password must have at least 8 characters, one uppercase, one lowercase, one number, and one special character.")
            continue
        confirm_password = input(f"Confirm password (visible): {password}\nIs this correct? (y/n): ")
        if confirm_password.lower() != 'y':
            print("Passwords did not match. Registration failed.")
            return False
        break
    
    security_question = input("Enter a security question: ")
    security_answer = input("Enter the answer to the security question: ")
    
    hashed_pw = hash_password(password)
    print(f"Hashed password for {email}: {hashed_pw.decode('utf-8')}")
    with open(USER_DATA_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([email, hashed_pw.decode('utf-8'), security_question, security_answer])
    print("User registered successfully!")
    return True

# Login users with attempt tracking and logging
def login_with_attempts(max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        email = input("Enter email: ")
        password = getpass("Enter password (hidden): ")
        if login_user(email, password):
            login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            city = input("Enter city to get sunrise and sunset times: ")
            sunrise, sunset, solar_noon, day_length = get_sunrise_sunset(city, email, login_time)  # Use the correct function name

            # Log the login time and sunrise/sunset data
            log_user_activity(email, 'login', sunrise, sunset, solar_noon, day_length, login_time)

            # Return email and login_time for further use
            return email, login_time
        else:
            attempts += 1
            print(f"Attempt {attempts}/{max_attempts} failed. {max_attempts - attempts} attempts remaining.")
    print("Too many failed attempts. Locked out.")
    return None, None  # Return None for both if login fails

# Handle user login process
def login_user(email, password):
    with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # print(f"Checking row: {row}")
            if len(row) >= 4:
                if row[0] == email:
                    # print(f"Email matched: {row[0]}")
                    # print(f"Row password (hashed): {row[1]}")  # Debug: Print stored hashed password
                    # print(f"Entered password: {password}")  # Debug: Print entered password
                    if verify_password(row[1], password.strip()):
                        print("Login successful!")
                        return True   
                    else:
                        # print(f"Invalid password for email: {email}")
                        # print("Invalid password.")
                        print("Login failed. Please check your email and password.")
                        return False
    print("User not found.")
    return False

# Recover password for users
def recover_password(email):
    rows = []
    user_found = False
    updated_row = None

    try:
        # Read the CSV file and handle BOM if present
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 0:  # Skip empty rows
                    continue
                rows.append(row)

                # Check if the email matches
                if row[0] == email:
                    user_found = True
                    if len(row) < 4:
                        print("User data is incomplete. Cannot recover password.")
                        return False

                    # Security question and answer validation
                    print(f"Security question: {row[2]}")
                    user_answer = input("Enter your answer: ").strip().lower()

                    if user_answer != row[3].strip().lower():
                        print("Incorrect answer.")
                        return False

                    # Password validation and update process
                    while True:
                        new_password = getpass("Enter new password (hidden): ")
                        if not validate_password(new_password):
                            print("Password must have at least 8 characters, one uppercase, one lowercase, one number, and one special character.")
                            continue
                        
                        confirm_password = input(f"Confirm password (visible): {new_password}\nIs this correct? (y/n): ").strip().lower()
                        if confirm_password == 'y':
                            # Hash and update the password
                            row[1] = hash_password(new_password).decode('utf-8')
                            updated_row = row
                            print("Password reset successful.")
                            break
                        else:
                            print("Passwords did not match. Please try again.")
                    break

        if not user_found:
            print("User not found.")
            return False

        # If the password was updated, write the new data to the CSV
        if updated_row:
            with open(USER_DATA_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)

        return True

    except FileNotFoundError:
        print(f"Error: The file '{USER_DATA_FILE}' was not found.")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# Log user logout
def logout_user(email, login_time):
    log_user_activity(email, 'logout', login_time=login_time)
    print(f"{email} has been logged out.")


