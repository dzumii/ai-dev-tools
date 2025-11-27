from django.db import models
from django.utils import timezone


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Check if todo is overdue"""
        if self.completed or not self.due_date:
            return False
        return timezone.now() > self.due_date

    def resolve(self):
        """Mark todo as completed"""
        self.completed = True
        self.save()

    def unresolve(self):
        """Mark todo as not completed"""
        self.completed = False
        self.save()
