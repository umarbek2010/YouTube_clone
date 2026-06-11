from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Аталышы")
    description = models.TextField(blank=True, verbose_name="Сүрөттөмө")
    video_file = models.FileField(upload_to='videos/', verbose_name="Видео файлы")
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        verbose_name="Миниатюра"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name="Жүктөгөн колдонуучу"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Жүктөлгөн убакыт")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Акыркы өзгөртүү")
    views = models.PositiveIntegerField(default=0, verbose_name="Көрүүлөр саны")

    class Meta:
        ordering = ['-created_at']           # Жаңы видеолор алдыда
        verbose_name = "Видео"
        verbose_name_plural = "Видеолор"

    def __str__(self):
        return self.title

    def increment_views(self):
        """Көрүү санын көбөйтүү үчүн ыңгайлуу метод"""
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарийлер"

    def __str__(self):
        return f"{self.user.username} → {self.video.title}"


class Like(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')   # Бир колдонуучу бир видеого бир жолу лайк
        ordering = ['-created_at']
        verbose_name = "Лайк"
        verbose_name_plural = "Лайктар"

    def __str__(self):
        return f"{self.user.username} лайктады: {self.video.title}"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    channel = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')  # Бир эле каналга эки жолу подписка болбоо
        ordering = ['-created_at']
        verbose_name = "Подписка"
        verbose_name_plural = "Подпискалар"

    def clean(self):
        if self.subscriber == self.channel:
            raise ValidationError("Өзүңүзгө подписка боло албайсыз!")

    def __str__(self):
        return f"{self.subscriber.username} → {self.channel.username}"