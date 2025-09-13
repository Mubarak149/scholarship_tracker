# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scholarship
from .utils import summarize_description

@receiver(post_save, sender=Scholarship)
def summarize_on_save(sender, instance, created, **kwargs):
    if instance.description:  # only run if description exists
        summary = summarize_description(instance.description)
        if summary and summary != instance.summary:  # avoid infinite save loop
            Scholarship.objects.filter(pk=instance.pk).update(summary=summary)
