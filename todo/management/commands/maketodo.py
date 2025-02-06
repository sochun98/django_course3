import sys
from django.core.management import BaseCommand
from todo.models import Todo
from random import choice


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("make todo start :)")
        
        for i in range(1, 101):
            todo, created = Todo.objects.get_or_create(name=f"테스트 todo {i}", complete=choice([True, False]))
            if created:
                print(f"{i}번째 todo 생성 완료")
            else:
                print(f"{i}번째 todo 이미 존재")
        
        sys.stdout.write(self.style.SUCCESS("make todo end :)"))