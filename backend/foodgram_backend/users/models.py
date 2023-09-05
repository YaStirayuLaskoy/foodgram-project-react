from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Follower(models.Model):
    """Модель фолловера."""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Автор рецепта",
                               related_name="following",
                               )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=False,
                             verbose_name="Фолловер",
                             related_name="follower",
                             )
