from django.apps import AppConfig

class GestaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao'

    def ready(self):
        pass  # ✅ Remova qualquer consulta ao banco aqui






