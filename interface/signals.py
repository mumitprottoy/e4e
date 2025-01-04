from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core import exceptions
from profiles import models as profile_models, operations
from stuff import models as stuff_models
from library import models as lib_models
from payment import models as payment_models


@receiver(pre_save, sender=User)
def ensure_unique_email(instance: User, *args, **kwargs):
    user = instance
    if  (not user.pk) and User.objects.filter(email=user.email).exists():
        raise exceptions.ValidationError('Email already exists')


@receiver(post_save, sender=User)
def add_profile_pic(instance: User, created: bool, *args, **kwargs):
    user = instance
    if created:
        profile_models.Picture(user=user).save()


@receiver(post_save, sender=User)
def set_user_status(instance: User, created: bool, *args, **kwargs):
    user = instance
    if created:
        profile_models.UserStatus(user=user).save()


@receiver(post_save, sender=payment_models.PurchaseV3)
def update_user_status(instance: payment_models.PurchaseV3, *args, **kwargs):
    purchase = instance
    if purchase.is_closed:
        purchase.user.status.update_to_premium()


@receiver(post_save, sender=User)
def assign_full_name(instance: User, created: bool, *args, **kwargs):
    user = instance
    if created and (not (user.first_name and user.last_name)):
        user.first_name, user.last_name = stuff_models.Name.get_random_name()
        user.save()


@receiver(post_save, sender=lib_models.Learner)
def set_up_levels(instance: lib_models.Learner, created: bool, *args, **kwargs):
    learner = instance
    if created:
        for topic in learner.chapter.topics.all().order_by('id'):
            level = lib_models.Level(
                learner=learner, topic=topic)
            level.save()
            quiz = lib_models.Quiz(level=level); quiz.save()
            for question in topic.questions.all():
                lib_models.Answer(quiz=quiz, question=question).save()


@receiver(post_save, sender=User)
def set_up_codes(instance: User, created: bool, *args, **kwargs):
    user = instance
    if created:
        profile_models.SixDigitCode(user=user).save()
