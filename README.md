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

## Usage

1. Register a new user account or log in with an existing account.
2. Create, update, and delete tasks using the provided forms.
3. Use the search bar to filter tasks based on their title or description.
4. Navigate through the paginated todo list using the pagination controls.
5. Reset your password using the password reset functionality if needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
