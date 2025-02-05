from django.core.management.base import BaseCommand
from todo.models import Todo
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 5 random tasks with random completion status'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Create or get a user
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'is_verified': True
            }
        )
        
        # Set password for demo_user
        user.set_password('demo1234')  # Sets password to 'demo1234'
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Demo user credentials:\nUsername: demo_user\nPassword: demo1234')
        )
        
        # Generate random dates between now and next 30 days
        today = datetime.now()
        
        for _ in range(5):
            due_date = today + timedelta(days=random.randint(1, 30))
            
            task = Todo.objects.create(
                user=user,  # Add the user here
                title=fake.sentence(nb_words=4)[:-1],  # Remove trailing period
                description=fake.paragraph(),
                due_date=due_date.date(),
                done=random.choice([True, False])
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created task: "{task.title}" (Due: {task.due_date}, Done: {task.done})'
                )
            )