# Django Todo App

This is a simple Django-based Todo application that allows users to create, update, and delete tasks. The application also includes user authentication, password reset functionality, pagination, and search functionality.

## Features

- User authentication (login, logout, signup)
- Password reset functionality
- Create, update, and delete tasks
- Pagination for the todo list
- Search functionality for todos
- Improved UI/UX design

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/MahdiSiamaki/Django-TodoApp.git
cd Django-TodoApp
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Apply the database migrations:

```bash
python manage.py migrate
```

5. Create a superuser (admin) account:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open your web browser and navigate to `http://127.0.0.1:8000` to access the application.

## Docker Setup Instructions

1. Build the Docker image:

```bash
docker-compose build
```

2. Run the Docker containers:

```bash
docker-compose up
```

3. Open your web browser and navigate to `http://127.0.0.1:8000` to access the application.

## Usage

1. Register a new user account or log in with an existing account.
2. Create, update, and delete tasks using the provided forms.
3. Use the search bar to filter tasks based on their title or description.
4. Navigate through the paginated todo list using the pagination controls.
5. Reset your password using the password reset functionality if needed.

## Technologies Used

- Django
- SQLite
- HTML/CSS
- JavaScript
- Bootstrap

## Project Structure

- `accounts/`: Contains user authentication-related files (models, views, forms, etc.)
- `core/`: Contains project-wide settings and configurations
- `todo/`: Contains todo-related files (models, views, forms, etc.)
- `templates/`: Contains HTML templates for the project
- `static/`: Contains static files (CSS, JavaScript, images, etc.)
- `manage.py`: Django's command-line utility for administrative tasks

## API Endpoints

### User Authentication

- `POST /accounts/login/`: Log in a user
- `POST /accounts/logout/`: Log out a user
- `POST /accounts/signup/`: Sign up a new user
- `POST /accounts/password_reset/`: Request a password reset
- `POST /accounts/password_reset/done/`: Confirm password reset request
- `POST /accounts/reset/<uidb64>/<token>/`: Confirm new password
- `POST /accounts/reset/done/`: Complete password reset
- `POST /api/v1/login/`: Token-based login
- `POST /api/v1/logout/`: Token-based logout

### Todo Operations

- `GET /api/v1/todos/`: List all todos for the authenticated user
- `POST /api/v1/todos/`: Create a new todo
- `GET /api/v1/todos/<id>/`: Retrieve a specific todo
- `PUT /api/v1/todos/<id>/`: Update a specific todo
- `DELETE /api/v1/todos/<id>/`: Delete a specific todo

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```

## Deployment

To deploy the application to a production environment, follow these steps:

1. Set the `DEBUG` setting to `False` in `core/settings.py`.
2. Configure the `ALLOWED_HOSTS` setting with your domain name or IP address.
3. Set up a production-ready database (e.g., PostgreSQL) and update the `DATABASES` setting in `core/settings.py`.
4. Collect static files using the following command:

```bash
python manage.py collectstatic
```

5. Configure a web server (e.g., Nginx) and a WSGI server (e.g., Gunicorn) to serve the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
