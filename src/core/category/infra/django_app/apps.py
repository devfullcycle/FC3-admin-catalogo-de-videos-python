from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.category.infra.django_app'
    label = 'category'
    verbose_name = 'Categorias'
