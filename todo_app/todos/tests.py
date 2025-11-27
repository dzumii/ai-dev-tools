from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Todo


class TodoModelTests(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description"
        )

    def test_todo_creation(self):
        """Test that a todo is created successfully"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.completed)

    def test_todo_str_representation(self):
        """Test string representation of todo"""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_resolve_todo(self):
        """Test marking todo as completed"""
        self.assertFalse(self.todo.completed)
        self.todo.resolve()
        self.assertTrue(self.todo.completed)

    def test_unresolve_todo(self):
        """Test marking todo as incomplete"""
        self.todo.resolve()
        self.assertTrue(self.todo.completed)
        self.todo.unresolve()
        self.assertFalse(self.todo.completed)

    def test_is_overdue_with_no_due_date(self):
        """Test overdue check with no due date"""
        self.assertFalse(self.todo.is_overdue())

    def test_is_overdue_with_future_due_date(self):
        """Test overdue check with future due date"""
        self.todo.due_date = timezone.now() + timedelta(days=1)
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())

    def test_is_overdue_with_past_due_date(self):
        """Test overdue check with past due date"""
        self.todo.due_date = timezone.now() - timedelta(days=1)
        self.todo.save()
        self.assertTrue(self.todo.is_overdue())

    def test_is_overdue_when_completed(self):
        """Test overdue check when todo is completed"""
        self.todo.due_date = timezone.now() - timedelta(days=1)
        self.todo.completed = True
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())

    def test_todo_ordering(self):
        """Test that todos are ordered by creation date (newest first)"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0].id, todo2.id)
        self.assertEqual(todos[1].id, todo1.id)


class TodoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo1 = Todo.objects.create(
            title="Test Todo 1",
            description="Description 1"
        )
        self.todo2 = Todo.objects.create(
            title="Test Todo 2",
            description="Description 2",
            completed=True
        )

    def test_todo_list_view(self):
        """Test todo list view displays all todos"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/home.html')
        self.assertIn(self.todo1, response.context['todos'])
        self.assertIn(self.todo2, response.context['todos'])

    def test_create_todo_get_view(self):
        """Test create todo GET request"""
        response = self.client.get(reverse('create_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/create_todo.html')

    def test_create_todo_post_view(self):
        """Test create todo POST request"""
        data = {
            'title': 'New Todo',
            'description': 'New Description'
        }
        response = self.client.post(reverse('create_todo'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_create_todo_without_title(self):
        """Test create todo without title"""
        data = {
            'description': 'New Description'
        }
        response = self.client.post(reverse('create_todo'), data)
        # Should redirect with error message
        self.assertEqual(response.status_code, 302)

    def test_create_todo_with_due_date(self):
        """Test create todo with due date"""
        due_date = (timezone.now() + timedelta(days=1)).isoformat()
        data = {
            'title': 'Todo with Due Date',
            'description': 'Description',
            'due_date': due_date
        }
        response = self.client.post(reverse('create_todo'), data)
        self.assertTrue(Todo.objects.filter(title='Todo with Due Date').exists())

    def test_edit_todo_get_view(self):
        """Test edit todo GET request"""
        response = self.client.get(reverse('edit_todo', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/edit_todo.html')
        self.assertEqual(response.context['todo'], self.todo1)

    def test_edit_todo_post_view(self):
        """Test edit todo POST request"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        response = self.client.post(reverse('edit_todo', args=[self.todo1.id]), data)
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Title')
        self.assertEqual(self.todo1.description, 'Updated Description')

    def test_delete_todo(self):
        """Test delete todo"""
        todo_id = self.todo1.id
        response = self.client.post(reverse('delete_todo', args=[todo_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())

    def test_resolve_todo(self):
        """Test resolve todo"""
        self.assertFalse(self.todo1.completed)
        response = self.client.post(reverse('resolve_todo', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)

    def test_unresolve_todo(self):
        """Test unresolve todo"""
        self.assertTrue(self.todo2.completed)
        response = self.client.post(reverse('unresolve_todo', args=[self.todo2.id]))
        self.assertEqual(response.status_code, 302)
        self.todo2.refresh_from_db()
        self.assertFalse(self.todo2.completed)

    def test_delete_todo_nonexistent(self):
        """Test delete non-existent todo"""
        response = self.client.post(reverse('delete_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_edit_todo_nonexistent(self):
        """Test edit non-existent todo"""
        response = self.client.get(reverse('edit_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)
