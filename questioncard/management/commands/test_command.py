from datetime import datetime, date
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from app.models import Item

from questioncard.models import QuestionCard

class Command(BaseCommand):
    help = "テストコマンド"

    @transaction.atomic
    def handle(self, *args, **options):
        questionCard1 = QuestionCard.objects.get(pk=31)
        questionCard2 = QuestionCard.objects.get(pk=32)

        print([questionCard1.order, questionCard2.order])
        questionCard1.order, questionCard2.order = questionCard2.order, questionCard1.order
        #questionCard1.order, questionCard2.order = 0, 1
        questionCard1.save()
        questionCard2.save()
        print([questionCard1.order, questionCard2.order])
        print("hello_world")