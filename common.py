import csv
from datetime import datetime
LOG_FILE ='log.csv'
def log_user_activity(email, action, sunrise=None, sunset=None):
    """Log user activity to a CSV file."""
    with open(LOG_FILE, 'a', newline='', encoding='utf-8-sig') as logfile:
        writer = csv.writer(logfile)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if action == 'login':
            writer.writerow([email, 'Login', current_time, sunrise, sunset, ''])
        elif action == 'logout':
            writer.writerow([email, 'Logout', current_time])