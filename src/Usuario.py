from Pessoa import Pessoa
from bcrypt import hashpw, gensalt, checkpw


class Usuario(Pessoa):
	def __init__(self, nome: str, email: str, senha: str, hashed: bool = False, id: str = 0) -> None:
		super().__init__(nome)
		self.id = id
		self.email = email
		if hashed:
			self.hash_senha = senha
		else:
			self.hash_senha = hashpw(senha.encode(), gensalt())

	# ligar banco de dados com isso 
	def verifica_login(self, email:str, senha: str):
		return email == self.email and checkpw(senha.encode(), self.hash_senha)
	

	def __str__(self) -> str:
		return super().__str__() + f" {self.id} {self.email} {self.hash_senha}"
