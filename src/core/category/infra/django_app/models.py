from django.db import models

class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'categories'
