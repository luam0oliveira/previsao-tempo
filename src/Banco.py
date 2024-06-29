import sqlite3
import os

from Usuario import Usuario

class Banco:
	def __init__(self) -> None:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		database_path = dir_path + "/../banco.db"
		
		if not os.path.isfile(database_path):
			self.con = sqlite3.connect(database_path)
			self.__cria_banco()
		else:
			self.con = sqlite3.connect(database_path)
		self.con.row_factory = sqlite3.Row

	def __cria_banco(self):
		cursor = self.con.cursor()
		self.__cria_tabela_usuario(cursor)
	
	def __cria_tabela_usuario(self, cursor: sqlite3.Cursor):
		cursor.execute(
			"CREATE TABLE usuario( \
				id INTEGER PRIMARY KEY AUTOINCREMENT, \
				nome TEXT NOT NULL, \
				email TEXT UNIQUE NOT NULL, \
				senha_hash TEXT NOT NULL)")
		
	def ler_usuario_por_email(self, email):
		cursor = self.con.cursor()
		try:
			res = cursor.execute("SELECT * FROM usuario WHERE email = ?",(email,))
			usuario = res.fetchone()
			self.con.commit()
			if usuario:
				usuario = Usuario(usuario['nome'], usuario['email'], usuario['senha_hash'], True, usuario['id'])
			return usuario
		except Exception as e:
			print(e)
			print("Email não encontrado.")

	def cria_usuario(self, usuario: Usuario):
		cursor = self.con.cursor()
		try:
			res = cursor.execute("INSERT INTO usuario (nome, email, senha_hash) VALUES (?, ?, ?) RETURNING *",
						(usuario.nome, usuario.email, usuario.hash_senha))
			dadosUsuario = res.fetchone()
			self.con.commit()
			if dadosUsuario:
				usuario = Usuario(dadosUsuario['nome'], dadosUsuario['email'], dadosUsuario['senha_hash'], True, dadosUsuario['id'])
			return usuario
		except Exception as e:
			print(e)
			print("Email já está sendo utilizado.")
		
	def exclui_usuario(self, usuario: Usuario):
		cursor = self.con.cursor()
		try:
			res = cursor.execute("DELETE FROM usuario WHERE id = ?",(usuario.id))
			self.con.commit()
		except Exception as e:
			print(e)
			print("ID não encontrado.")
