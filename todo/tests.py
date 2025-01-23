from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo

class TodoCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.todo = Todo.objects.create(user=self.user, title='Test Todo', description='Test Description', due_date='2023-12-31', done=False)

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo:todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')
        self.assertContains(response, self.todo.title)

    def test_todo_detail_view(self):
        response = self.client.get(reverse('todo:todo_detail', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_detail.html')
        self.assertContains(response, self.todo.title)
        self.assertContains(response, self.todo.description)

    def test_todo_create_view(self):
        response = self.client.get(reverse('todo:todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_form.html')

        response = self.client.post(reverse('todo:todo_create'), {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': '2023-12-31',
            'done': False
        })
        self.assertRedirects(response, reverse('todo:todo_list'))
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view(self):
        response = self.client.get(reverse('todo:todo_update', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_form.html')

        response = self.client.post(reverse('todo:todo_update', args=[self.todo.pk]), {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'due_date': '2023-12-31',
            'done': True
        })
        self.assertRedirects(response, reverse('todo:todo_list'))
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertTrue(self.todo.done)

    def test_todo_delete_view(self):
        response = self.client.get(reverse('todo:todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_confirm_delete.html')

        response = self.client.post(reverse('todo:todo_delete', args=[self.todo.pk]))
        self.assertRedirects(response, reverse('todo:todo_list'))
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
