
you can main.exe which is in dist folder
i added the screenshot over here



Sunset and Sunrise Times Console Application with Secure Login

Problem Statement: Create a Python-based console application that allows users to log in and retrieve sunset and sunrise times for any city they specify. The application should include secure login functionality, password recovery options, and enforce a limit on login attempts. Upon successful login, the system will fetch and display sunset and sunrise times using a public API for a user-specified location.
Requirements:
1. Login System:
•	User Credentials:
o	Store user credentials in a CSV file (regno.csv), containing fields such as email, hashed password, and security_question.
o	Hash the password (e.g., using bcrypt) for secure storage and comparison.
•	Login Process:
o	The user is prompted to enter their email and password.
o	Authenticate the credentials by comparing the input with the stored information in the CSV file.
2. Input Validation:
•	Email Validation:
o	Ensure that the email is in a valid format (e.g., user@example.com).
•	Password Validation:
o	The password must meet the following requirements:
	Minimum of 8 characters.
	At least one uppercase letter, one lowercase letter, one digit, and one special character.
o	Hash the input password for comparison with the stored hashed password.
3. Forgot Password:
•	Provide a "forgot password" option on the login screen.
•	Password Reset Process:
o	Prompt the user to enter their registered email.
o	If the email exists in the CSV file, ask them to correctly answer the security question stored with their profile.
o	Upon correctly answering the security question, allow them to reset the password, ensuring it follows the same password validation rules.
o	Update the CSV file with the newly hashed password.
4. Login Attempts:
•	Attempt Limitation:
o	Limit the user to 5 login attempts. After 5 failed attempts, deny further attempts until the application is restarted.
•	Security Measures:
o	Notify the user of how many attempts remain after each failed login.
o	Lock the user out and terminate the application upon exceeding the attempt limit.
5. API Integration (Sunset and Sunrise Data):
•	API Usage:
o	After successful login, prompt the user to enter the city or location for which they want to retrieve sunset and sunrise times.
o	Use the Sunrise-Sunset API (or similar free API) to fetch sunset and sunrise data.
o	Display the following information:
	Sunrise Time: The time the sun rises at the specified location.
	Sunset Time: The time the sun sets at the specified location.
	Day Length: The total duration of daylight.
	Solar Noon: The time at which the sun is at its highest point in the sky.

6. Error Handling:
•	Invalid API Key: Handle cases where the API key is invalid or expired, and show an appropriate error message.
•	Network Errors: If there is no internet connection or the API cannot be reached, display a meaningful error message and suggest checking the connection.
•	Invalid Location: If no data is available for the specified city, handle it gracefully by informing the user and suggesting they verify the location name or try another location.
•	Time Zone Considerations: Ensure the displayed times are adjusted to the user’s local time zone (if required).
![Interface](https://github.com/user-attachments/assets/c1f15d7d-159a-4f3b-92eb-166685169d23)
![Registration](https://github.com/user-attachments/assets/23537c2a-5f02-4144-b552-ae5d8a500fc6)
![login](https://github.com/user-attachments/assets/5c3cb2eb-83a5-42f7-9487-94e8f196f53c)
![logout](https://github.com/user-attachments/assets/18f872ca-ceb7-4553-b948-135a4fa3947f)
![recover password](https://github.com/user-attachments/assets/3c9ba15a-b508-444f-966f-0f29829eb2ee)
![wrong Attempts](https://github.com/user-attachments/assets/1dd69ec5-47f3-4e42-9734-391f5a9b3496)
