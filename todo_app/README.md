# Django TODO App

A full-featured Todo application built with Django featuring CRUD operations, due date tracking, and task completion management.

## Features

✅ **Complete CRUD Operations**
- Create, read, update, and delete todos
- Edit todo titles and descriptions
- Set due dates for tasks

✅ **Task Management**
- Mark todos as completed/incomplete
- Track overdue todos
- View creation and update timestamps
- Organize todos by creation date

✅ **User-Friendly Interface**
- Beautiful, responsive design with gradient background
- Intuitive forms for creating and editing todos
- Quick action buttons for completing, editing, and deleting tasks
- Empty state messaging

✅ **Comprehensive Testing**
- 21 unit tests covering models and views
- Test coverage for CRUD operations
- Tests for overdue detection and task resolution

✅ **Admin Panel**
- Django admin interface for managing todos
- Advanced filtering and search capabilities
- Bulk operations support

## Project Structure

```
django_todo/                 # Main Django project settings
  ├── settings.py          # Project configuration
  ├── urls.py              # Main URL configuration
  └── wsgi.py              # WSGI application
  
todos/                      # Main app
  ├── models.py            # Todo model definition
  ├── views.py             # View logic for CRUD operations
  ├── urls.py              # App URL patterns
  ├── admin.py             # Admin configuration
  ├── tests.py             # Comprehensive test suite
  ├── migrations/          # Database migrations
  └── templates/
      └── todos/
          ├── base.html           # Base template with styling
          ├── home.html           # Todo list view
          ├── create_todo.html    # Create todo form
          └── edit_todo.html      # Edit todo form

manage.py                   # Django management script
requirements.txt            # Python dependencies
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/dzumii/ai-dev-tools.git
cd ai-dev-tools
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional - for admin panel)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Access the Application
- **Main App**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

### Managing Todos

#### Create a Todo
1. Click "➕ Add New Todo" button
2. Enter the title (required)
3. Optionally add description and due date
4. Click "✓ Create Todo"

#### Edit a Todo
1. Click "✏️ Edit" button on the todo
2. Modify the title, description, or due date
3. Click "✓ Update Todo"

#### Complete a Todo
- Click "✓ Complete" to mark a todo as done
- Click "↩️ Undo" to revert completion status

#### Delete a Todo
1. Click "🗑️ Delete" button
2. Confirm the deletion

## Model Details

### Todo Model

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField(200) | Todo title (required) |
| `description` | TextField | Detailed description (optional) |
| `due_date` | DateTimeField | Due date and time (optional) |
| `completed` | BooleanField | Completion status (default: False) |
| `created_at` | DateTimeField | Creation timestamp (auto) |
| `updated_at` | DateTimeField | Last update timestamp (auto) |

### Model Methods

- `resolve()` - Mark todo as completed
- `unresolve()` - Mark todo as incomplete
- `is_overdue()` - Check if todo is past due date

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | List all todos |
| GET | `/create/` | Show create form |
| POST | `/create/` | Create new todo |
| GET | `/<id>/edit/` | Show edit form |
| POST | `/<id>/edit/` | Update todo |
| POST | `/<id>/delete/` | Delete todo |
| POST | `/<id>/resolve/` | Mark as completed |
| POST | `/<id>/unresolve/` | Mark as incomplete |

## Running Tests

Execute all tests with verbose output:
```bash
python manage.py test todos --verbosity=2
```

Test Results:
- ✅ 21 tests passing
- Coverage includes:
  - Model creation and properties
  - Todo resolution/unresolve functionality
  - Overdue date detection
  - CRUD operations
  - Error handling and edge cases

## Technologies Used

- **Django 5.2.8** - Web framework
- **Python 3.12** - Programming language
- **SQLite** - Database (default)
- **HTML5 & CSS3** - Frontend
- **Django Templates** - Template engine

## Configuration

### Settings (django_todo/settings.py)

Key configurations:
- **DEBUG**: True (development mode)
- **ALLOWED_HOSTS**: []
- **DATABASE**: SQLite (db.sqlite3)
- **INSTALLED_APPS**: Includes 'todos' app
- **TEMPLATES**: Django template backend with app directories

## Future Enhancements

- [ ] User authentication and per-user todos
- [ ] Categories/Tags for organizing todos
- [ ] Due date reminders/notifications
- [ ] Recurring todos
- [ ] Todo priority levels
- [ ] Collaboration features
- [ ] REST API with DRF
- [ ] Frontend framework (React/Vue)

## License

This project is open source and available under the MIT License.

## Author

**dzumii** - Django TODO App Developer

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open a GitHub issue in the repository.

---

**Made with ❤️ using Django**