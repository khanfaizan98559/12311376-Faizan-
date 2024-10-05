from auth import login_with_attempts, register_user, recover_password, logout_user
from sunrise_sunset import get_sunrise_sunset
from datetime import datetime
def main():
    print("Welcome to the Sunset and Sunrise Times Console Application with Secure Login!")
    
    logged_in_user = None  # Track logged-in user
    login_time = None
    while True:
        if not logged_in_user:
            # Display main menu for unauthenticated users
            print("\nPlease choose an option:")
            print("1. Login")
            print("2. Register")
            print("3. Recover Password")
            print("4. Exit")
            
            choice = input("Enter your choice: ")

            if choice == '1':
                # Attempt to log in
                email, login_time = login_with_attempts()
                if email:
                    logged_in_user = email  # Set the logged-in user
                    print(f"Logged in as: {logged_in_user}")

            elif choice == '2':
                # Register a new user
                register_user()

            elif choice == '3':
                # Recover password process
                email = input("Enter your registered email: ")
                recover_password(email)

            elif choice == '4':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice, please try again.")

        else:
            # Display menu for authenticated users
            print("\nWhat would you like to do?")
            print("1. Get Sunrise and Sunset times")
            print("2. Logout")
            print("3. Exit")
            
            logged_in_choice = input("Enter your choice: ")

            if logged_in_choice == '1':
                # Fetch sunrise and sunset times for the logged-in user
                city = input("Enter city to get sunrise and sunset times: ")
                try:
                    sunrise, sunset, solar_noon, (day_hours, day_minutes) = get_sunrise_sunset(city, logged_in_user, login_time)
                    print(f"Sunrise: {sunrise}")
                    print(f"Sunset: {sunset}")
                    print(f"Solar Noon: {solar_noon}")
                    print(f"Day Length: {day_hours, day_minutes}")
                except Exception as e:
                    print(f"An error occurred while fetching sunrise and sunset times: {e}")    
            
            elif logged_in_choice == '2':
                # Logout process
                logout_user(logged_in_user, login_time)
                logged_in_user = None# Clear the session after logout
                login_time = None
                print("You have been logged out.")

            elif logged_in_choice == '3':
                print("Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
