from urllib.parse import unquote_plus
from utils import get_notes, get_note, update_note, load_template, build_response, add_note, delete_note

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=', 1)
            params[chave] = unquote_plus(valor)

        nova_anotacao = {
            'titulo': params['titulo'],
            'detalhes': params['detalhes'],
        }
        add_note(nova_anotacao)

        return build_response(code=303, reason='See Other', headers='Location: /')

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=nota.title, details=nota.content, id=nota.id)
        for nota in get_notes()
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(body=body)

def delete(note_id):
    nota = get_note(int(note_id))
    body = load_template('confirm-delete.html').format(id=nota.id, title=nota.title, details=nota.content)
    return build_response(body=body)

def confirm_delete(note_id):
    delete_note(int(note_id))
    return build_response(code=303, reason='See Other', headers='Location: /')

def edit(request, note_id):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=', 1)
            params[chave] = unquote_plus(valor)

        update_note(int(note_id), params['titulo'], params['detalhes'])
        return build_response(code=303, reason='See Other', headers='Location: /')

    nota = get_note(int(note_id))
    body = load_template('edit.html').format(id=nota.id, title=nota.title, details=nota.content)
    return build_response(body=body)