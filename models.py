import sqlite3
from database import DB_NAME


class Carrinho:

    def __init__(self,
                 nome,
                 modelo,
                 cor,
                 ano,
                 foto_path,
                 id=None):

        self.id = id
        self.nome = nome
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.foto_path = foto_path

    # -------- SALVAR --------
    def salvar(self):

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if self.id is None:

            cursor.execute("""
                INSERT INTO carrinhos
                (nome, modelo, cor, ano, foto_path)
                VALUES (?,?,?,?,?)
            """, (
                self.nome,
                self.modelo,
                self.cor,
                self.ano,
                self.foto_path
            ))

            self.id = cursor.lastrowid

        else:
            cursor.execute("""
                UPDATE carrinhos
                SET nome=?, modelo=?, cor=?, ano=?, foto_path=?
                WHERE id=?
            """, (
                self.nome,
                self.modelo,
                self.cor,
                self.ano,
                self.foto_path,
                self.id
            ))

        conn.commit()
        conn.close()

    # -------- EXCLUIR --------
    def excluir(self):

        if self.id is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM carrinhos WHERE id=?",
            (self.id,)
        )

        conn.commit()
        conn.close()

    # -------- LISTAR --------
    @staticmethod
    def listar(termo=""):

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, modelo, cor, ano, foto_path
            FROM carrinhos
            WHERE nome LIKE ?
        """, (f"%{termo}%",))

        dados = cursor.fetchall()
        conn.close()

        return [
            Carrinho(n, m, c, a, f, i)
            for i, n, m, c, a, f in dados
        ]