from django.core.management.base import BaseCommand

from mbq import env, pubsub


class Command(BaseCommand):
    def handle(self, *args, **options):
        pubsub.publish_json("pubsub.json", {"foo": "bar"}, env.get("SNS_ARN"), use_atomiq=False)
