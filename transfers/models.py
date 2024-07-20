import uuid
from django.db import models
from django.utils.text import slugify

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from name if not provided, and add first 4 characters of id to ensure uniqueness
            self.slug = slugify(self.name + str(self.id)[:4])
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.balance}"
    
    class Meta:
        ordering = ['created_at']