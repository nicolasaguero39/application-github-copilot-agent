from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone
from bson import ObjectId
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Borrar datos previos
        # Eliminar colecciones directamente con pymongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['user'].delete_many({})
        db['team'].delete_many({})
        db['activity'].delete_many({})
        db['leaderboard'].delete_many({})
        db['workout'].delete_many({})

        # Equipos
        marvel = Team.objects.create(id=str(ObjectId()), name='marvel', description='Marvel team')
        dc = Team.objects.create(id=str(ObjectId()), name='dc', description='DC team')

        # Usuarios superhéroes
        users = [
            User(id=str(ObjectId()), name='Iron Man', email='ironman@marvel.com', team='marvel'),
            User(id=str(ObjectId()), name='Captain America', email='cap@marvel.com', team='marvel'),
            User(id=str(ObjectId()), name='Spider-Man', email='spiderman@marvel.com', team='marvel'),
            User(id=str(ObjectId()), name='Batman', email='batman@dc.com', team='dc'),
            User(id=str(ObjectId()), name='Superman', email='superman@dc.com', team='dc'),
            User(id=str(ObjectId()), name='Wonder Woman', email='wonderwoman@dc.com', team='dc'),
        ]
        for user in users:
            user.save()

        # Actividades
        Activity.objects.create(id=str(ObjectId()), user=users[0], type='run', duration=30, date=timezone.now().date())
        Activity.objects.create(id=str(ObjectId()), user=users[3], type='swim', duration=45, date=timezone.now().date())

        # Leaderboard
        Leaderboard.objects.create(id=str(ObjectId()), team=marvel, points=150)
        Leaderboard.objects.create(id=str(ObjectId()), team=dc, points=120)

        # Workouts
        Workout.objects.create(id=str(ObjectId()), name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        Workout.objects.create(id=str(ObjectId()), name='Plank', description='Hold plank for 1 min', suggested_for='dc')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
