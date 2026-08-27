import sqlite3
from dataclasses import dataclass


class Database():
    def __init__(self, nome_arquivo):
        self.conn = sqlite3.connect(nome_arquivo + '.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, favorite INTEGER NOT NULL DEFAULT 0);")

    def add(self, note):
        self.cur.execute(
            "INSERT INTO note (title,content) VALUES (?, ?)", (note.title, note.content)
        )
        self.conn.commit()
    
    def get_all(self):
        lista = []
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC")
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            lista.append(Note(id, title, content, bool(linha[3])))

        return lista
    
    def update(self, entry):
        self.cur.execute(
            "UPDATE note SET title = ?, content = ? WHERE id = ?",
            (entry.title, entry.content, entry.id)
        )
        self.conn.commit()

    def get_by_id(self, note_id):
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note WHERE id = ?", (note_id,))
        linha = cursor.fetchone()
        if linha:
            return Note(linha[0], linha[1], linha[2], bool(linha[3]))
        return None

    def delete(self, note_id):
        self.cur.execute(
            "DELETE FROM note WHERE id = ?",
            (note_id,)
        )
        self.conn.commit()

    def toggle_favorite(self, note_id):
        self.cur.execute(
            "UPDATE note SET favorite = NOT favorite WHERE id = ?",
            (note_id,)
        )
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorite: bool = False
