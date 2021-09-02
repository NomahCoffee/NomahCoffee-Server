# Nomah Coffee - Server

This repository holds the backend code for the Nomah Coffee website and iOS mobile application.

## Built With

The server is written in Django / Python. It uses DjangoRestFramework to serialize models into JSON for API call responses and Djoser to handle basic authentication actions such as registration, login, logout, password reset and account activation.
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Djoser](https://djoser.readthedocs.io/en/latest/#)

## Getting Started

Make sure you have all of the prerequisites and then follow the steps to get the server running locally on your machine.

## Prerequisites

* Python - Run the following command. If you see a response like `Python 3.9.1`, then you are set to continue. If not, make sure you download the latest stable version of Python
  ```
  python3 --version
  ```

## Installation

1. Clone the repo
   ```
   git clone https://github.com/NomahCoffee/NomahCoffee-Server.git
   ```
2. Create and then activate your virtual environment.
If both of these steps are completed properly, you should see your command line start with your virtual environemnt (i.e. `(myvirtenv)`)
   ```
   python3 -m venv venv
   
   ## For Mac / Linux users
   source venv/bin/activate
   
   ## For Windows users
   venv\Scripts\activate
   ```
3. Make sure to change directory into the repository
   ```
   cd NomahCoffee-Server
   ```
4. Install all of the required libraries
   ```
   pip install -r requirements.txt
   ```
5. Set environment variables by creating a `.env` file in the top level directory and add the environment variables. You will need to contact a project administrator to obtain the variables. WARNING: You cannot properly run this project without the environment variables.
   ```
   📦 NomahCoffee-Server
      📂 apiapp
      📂 authapp
      📂 nomahcoffee
      📄 .env <- Add this file
      📄 .gitignore
      📄 db.sqlite3
      📄 manage.py
      📄 README.md
      📄 requirements.txt
   ```
   You're `.env` file should look like this
   ```
   SECRET_KEY=[secret key here]
   DEBUG=[debug value here]
   ```
6. Setup the database schema
   ```
   python manage.py migrate
   ```
7. Populate the database with sample data
   ```
   python manage.py loaddata apiapp/fixtures/coffee.json
   python manage.py loaddata apiapp/fixtures/storehours.json
   python manage.py loaddata apiapp/fixtures/storelocations.json
   python manage.py loaddata authapp/fixtures/users.json
   ```
8. Create a super user to access the admin dashboard
   ```
   python manage.py createsuperuser
   ```
9. Run the server and then login to the admin dashboard at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) with your newly created super user
   ```
   python manage.py runserver
   ```

## Contributing
If you have interest in contributing to this project, be sure to complete the following steps.
1. Fork the project
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add some amazing feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request
---
## Contact

Caleb Rudnicki - calebrudnicki@gmail.com

📍 Made in BOS
