# gestao/mixins.py
import requests
from django.core.exceptions import ValidationError

class CepMixin:
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')

        if not cep:
            raise ValidationError("Por favor, insira um CEP válido.")

        # Faz a consulta do CEP usando a API do ViaCEP
        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            raise ValidationError("Erro ao conectar à API de CEP.")

        if response.status_code == 200:
            dados = response.json()
            if 'erro' in dados:
                raise ValidationError("CEP não encontrado.")
            self.cleaned_data['logradouro'] = dados.get('logradouro', '')
            self.cleaned_data['bairro'] = dados.get('bairro', '')
            self.cleaned_data['cidade'] = dados.get('localidade', '')
            self.cleaned_data['estado'] = dados.get('uf', '')
        else:
            raise ValidationError("CEP não encontrado.")

        return cep


