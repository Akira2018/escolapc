#utils.py

import requests
from django.core.exceptions import ValidationError

def buscar_endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        return {
            'logradouro': dados.get('logradouro', ''),
            'bairro': dados.get('bairro', ''),
            'cidade': dados.get('cidade', ''),
            'estado': dados.get('estado', ''),
        }
    else:
        raise ValidationError("CEP não encontrado.")
