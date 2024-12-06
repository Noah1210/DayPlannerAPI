from django.test import TestCase
from dayplanner.models import Note, Task, Todo, User
from django.utils import timezone
from faker import Faker

fake = Faker()

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password=fake.password())
        self.note_content = fake.text()
        self.note = Note.objects.create(content=self.note_content, date=timezone.now().date(), user=self.user)

    def test_note_creation(self):
        self.assertTrue(self.note.content)
        self.assertEqual(self.note.user, self.user)

    def test_note_creation_empty_content(self):
        note = Note.objects.create(content='', date=timezone.now().date(), user=self.user)
        self.assertEqual(note.content, '', "Expected note content to be empty")

    def test_note_deletion(self):
        note_id = self.note.id
        self.note.delete()
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password=fake.password())
        self.task_title = fake.sentence()
        self.task_color = fake.color()
        self.task = Task.objects.create(
            title=self.task_title,
            date_start=timezone.now(),
            date_end=timezone.now() + timezone.timedelta(hours=1),
            color=self.task_color,
            user=self.user
        )

    def test_task_creation(self):
        self.assertTrue(self.task.title)
        self.assertEqual(self.task.user, self.user)


    def test_task_creation_empty_title(self):
        task = Task.objects.create(
            title='',
            date_start=timezone.now(),
            date_end=timezone.now() + timezone.timedelta(hours=1),
            color=self.task_color,
            user=self.user
        )
        self.assertEqual(task.title, '', "Expected task title to be empty")

    def test_task_deletion(self):
        task_id = self.task.id
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password=fake.password())
        self.todo_title = fake.sentence()
        self.todo_is_done = fake.boolean()
        self.todo_is_priority = fake.boolean()
        self.todo = Todo.objects.create(
            title=self.todo_title,
            date=timezone.now().date(),
            is_done=self.todo_is_done,
            is_priority=self.todo_is_priority,
            user=self.user
        )

    def test_todo_creation(self):
        self.assertTrue(self.todo.title)
        self.assertEqual(self.todo.user, self.user)

    def test_todo_creation_empty_title(self):
        todo = Todo.objects.create(
            title='',
            date=timezone.now().date(),
            is_done=self.todo_is_done,
            is_priority=self.todo_is_priority,
            user=self.user
        )
        self.assertEqual(todo.title, '', "Expected todo title to be empty")

    def test_todo_toggle_is_done(self):
        initial_status = self.todo.is_done
        print(f"Initial status: {initial_status}")
        self.todo.is_done = not initial_status
        print(f"New status: {self.todo.is_done}")
        self.todo.save()
        self.assertNotEqual(self.todo.is_done, initial_status, "Expected todo is_done status to be toggled")

    def test_todo_deletion(self):
        todo_id = self.todo.id
        self.todo.delete()
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=todo_id)