from urllib.parse import unquote_plus
from utils import get_notes, get_note, update_note, load_template, build_response, add_note, delete_note, toggle_favorite

def render_index(mensagem_erro=''):
    erro_html = f'<p class="form-error">{mensagem_erro}</p>' if mensagem_erro else ''

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            title=nota.title, details=nota.content, id=nota.id,
            favorite_label='Favorita' if nota.favorite else 'Favoritar'
        )
        for nota in get_notes()
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes, error_message=erro_html)
    return build_response(body=body)


def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=', 1)
            params[chave] = unquote_plus(valor)

        titulo = params['titulo'].strip()
        detalhes = params['detalhes'].strip()

        if not titulo or not detalhes:
            return render_index('Preencha o título e o conteúdo antes de criar a anotação')

        nova_anotacao = {
            'titulo': titulo,
            'detalhes': detalhes,
        }
        add_note(nova_anotacao)

        return build_response(code=303, reason='See Other', headers='Location: /')
    return render_index()

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

def favorite(note_id):
    toggle_favorite(int(note_id))
    return build_response(code=303, reason='See Other', headers='Location: /')

def not_found():
    body = load_template('404.html')
    return build_response(body=body, code=404, reason='Not Found')