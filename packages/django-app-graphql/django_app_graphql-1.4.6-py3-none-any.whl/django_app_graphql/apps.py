from django.apps import AppConfig


class GraphqlSectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app_graphql'

    def ready(self):
        pass
