## Definitely Not A Filmweb

DNAF is a web app for managing movies, reviews, and articles. Users can view and review movies, read articles, and more.

## Features

- User registration and authentication
- User movie management (add)
- Staff user movie management (approve, reject)
- Review management (add, edit, delete)
- User article management (add)
- Staff user article management (approve, reject)
- Genre management
- Average rating calculation for movies based on user reviews

## Requirements

- Python 3.x
- Django 3.x or higher
- PostgreSQL

## Installation

### Clone the Repository

```bash
git clone https://github.com/Madejowski98/DEFINITELY_NOT_A_FILMWEB.git
cd DEFINITELY_NOT_A_FILMWEB
```

### Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up PostgreSQL

```bash
https://www.postgresql.org
```

#### After successfully setting up database 
### Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

## Usage
### Accessing the Admin Interface
Navigate to http://127.0.0.1:8000/admin and log in with your superuser credentials to manage movies, reviews, and articles.
- You might need to set staff checkbox of an user in order to be able to view pending movies and articles to approve / reject them

### User Registration and Authentication
- Visit http://127.0.0.1:8000/accounts/register/ to register a new user.
- Visit http://127.0.0.1:8000/accounts/login/ to log in.
- Visit http://127.0.0.1:8000/accounts/my_profile/ to check and update your user profile

### Adding movies, reviews and articles
- Authenticated users are able to add movies, reviews and articles
- Users can add reviews on movie detail page, they can only edit / delete their own reviews
- Movies and articles need approval by staff user

## Contributing 
Contributions are welcome! Please create a pull request with detailed information about the changes.

## Contact
If you have any questions, feel free to contact the project maintainer at abno9444@gmail.com

