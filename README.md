# AI Dev Tools Repository

A collection of AI-powered development projects and tools.

## Projects

### 📝 [todo_app](./todo_app/)
A full-featured Django TODO application with CRUD operations, due date tracking, and task management.

**Features:**
- ✅ Complete CRUD operations for todos
- ✅ Due date and overdue tracking
- ✅ Mark tasks as complete/incomplete
- ✅ Beautiful, responsive UI with gradient design
- ✅ Comprehensive test suite (21 tests, 100% pass rate)
- ✅ Django admin interface

**Tech Stack:** Django 5.2.8, SQLite, HTML5, CSS3

**Quick Start:**
```bash
cd todo_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Access at `http://localhost:8000`

---

## Repository Structure

```
ai-dev-tools/
├── todo_app/              # Django TODO application
│   ├── django_todo/       # Project configuration
│   ├── todos/             # Main app with models, views, templates
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies
│   ├── README.md          # Project documentation
│   ├── .gitignore         # Git ignore rules
│   └── db.sqlite3         # SQLite database
├── venv/                  # Virtual environment (not tracked)
└── README.md              # This file
```

## Getting Started

1. **Clone the repository:**
```bash
git clone https://github.com/dzumii/ai-dev-tools.git
cd ai-dev-tools
```

2. **Navigate to a project:**
```bash
cd todo_app
```

3. **Set up the environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Run the project:**
```bash
python manage.py migrate
python manage.py runserver
```

## Projects Status

| Project | Status | Type | Description |
|---------|--------|------|-------------|
| [todo_app](./todo_app/) | ✅ Complete | Django App | Full-stack TODO application |

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.

## License

This repository is open source and available under the MIT License.

---

**Repository:** dzumii/ai-dev-tools  
**Last Updated:** November 27, 2025
