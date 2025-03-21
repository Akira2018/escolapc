from django.apps import AppConfig

class GestaoConfig(AppConfig):
<<<<<<< HEAD
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao'

    def ready(self):
        pass  # ✅ Remova qualquer consulta ao banco aqui






=======
    name = 'gestao'

    def ready(self):
        import gestao.signals  # Conecta os sinais
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
