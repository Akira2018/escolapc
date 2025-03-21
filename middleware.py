from django.utils.deprecation import MiddlewareMixin

class AccessibilityMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Verifique se a resposta é uma página HTML
        if 'text/html' in response.get('Content-Type', ''):
            # Adicione suas verificações de acessibilidade aqui
            content = response.content.decode('utf-8')

            # Exemplo: Verificar se há imagens sem texto alternativo
            if '<img ' in content and 'alt="' not in content:
                print("Alerta de Acessibilidade: Imagem sem texto alternativo detectada.")

            # Exemplo: Forçar o foco no elemento principal da página
            if '<main' in content and 'tabindex="-1"' not in content:
                content = content.replace('<main', '<main tabindex="-1"')
                response.content = content.encode('utf-8')
                
        return response
