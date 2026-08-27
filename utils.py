import json
from pathlib import Path
from database import Database, Note

db = Database('notes')
def extract_route(request):
    lista = request.split(' ')
    resposta = lista[1][1:]
    return resposta

def read_file(filepath):
    # route = f'/{filepath}'
    arquivo = open(filepath, 'rb')
    conteudo = arquivo.read()
    arquivo.close()
    return conteudo

def load_data(filepath):
    caminho = "data/" + filepath
    arquivo = open(caminho, 'r')
    dados = json.load(arquivo)
    arquivo.close() #liberar o arquivo depois de usá-lo
    return dados

def load_template(arquivo):
    arq = open('templates/'+ arquivo, 'r', encoding='utf-8')
    conteudo = arq.read()
    arq.close()
    return conteudo
    

def add_note(nova_anotacao):
    nota = Note(title=nova_anotacao['titulo'], content=nova_anotacao['detalhes'])
    db.add(nota)

def delete_note(note_id):
    db.delete(note_id)

def get_notes():
    return db.get_all()

def get_note(note_id):
    return db.get_by_id(note_id)

def update_note(note_id, titulo, detalhes):
    nota = Note(id=note_id, title=titulo, content=detalhes)
    db.update(nota)

def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()

        cabecalho = f'HTTP/1.1 {code} {reason}\n'
        if headers:
            cabecalho += f'{headers}\n'
        cabecalho += '\n'

        return cabecalho.encode() + body