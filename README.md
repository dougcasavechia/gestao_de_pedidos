Digital Order Management System

This is a digital system designed to eliminate the need for paper usage and simplify the process of order management. It utilizes the Google Drive API and Trello API for storing and organizing orders, respectively.

Features
- Paper Elimination: Digitizes the order management process, reducing the need for paper usage.
- Ease of Locating Orders: All orders are stored digitally, making it easy to search and locate them.
- Integration with Google Drive: Utilizes the Google Drive API to store and organize orders in specific folders.
- Integration with Trello: Utilizes the Trello API to manage orders, allowing visualization and updates on a Kanban board.

HOW TO USE
Requirements
1. Google Drive account.
2. Trello account.
  
Configuration
1. Clone this repository to your local environment.

2. Install the required packages by running the following command:
-pip install -r requirements.txt

3. Configure the Google Drive and Trello credentials:

- Create a project in Google Developer Console.
- Enable the Google Drive API for your project.
- Create authentication credentials (JSON) and download it.
- Rename the credentials file to credentials.json and place it in the root of the project.
- Access the Trello Developer and create a Trello application.
- Obtain the application key and access token.
- Update the variables TRELLO_API_KEY and TRELLO_API_TOKEN in the config.py file with your credentials.

Execution
1. Run the executable main.exe to start the system.
2. Follow the provided instructions to add, view, update, and delete orders.

Contributions
Contributions are welcome! Feel free to open issues or send pull requests to improve this system.

License
This project is licensed under the MIT License.
