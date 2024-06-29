from tkinter import messagebox
import customtkinter

from Banco import Banco
from Usuario import Usuario

# CLasse login
class Login(customtkinter.CTkToplevel):
	def __init__(self, master, banco:Banco):
		super().__init__(master)
		
		self.title("TTT")
		self.registro = True
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.container = customtkinter.CTkFrame(self)
		self.__add_widgets(self.container)
		self.container.pack(expand= True)
		self.banco = banco
		self.parent = master
	
	def __reconstroi(self):
		for child in self.container.grid_slaves():
			child.destroy()
		self.__add_widgets(self.container)

	def __add_widgets(self, master):
		add = 0
		if self.registro:
			add = 1
			self.nomeLabel = customtkinter.CTkLabel(master, text="Nome: ")
			self.nomeLabel.grid(row = 0, column = 0,  padx=20, pady=10)
			self.nomeEntry = customtkinter.CTkEntry(master, )
			self.nomeEntry.grid(row=0, column=1, padx=20, pady=10, sticky="EW")

		# Adiciona email
		self.emailLabel = customtkinter.CTkLabel(master, text="Email: ")
		self.emailLabel.grid(row = 0 + add, column = 0,  padx=20, pady=10)
		self.emailEntry = customtkinter.CTkEntry(master, )
		self.emailEntry.grid(row=0 + add, column=1, padx=20, pady=10, sticky="EW")

		# Adiciona senha
		self.senhaLabel = customtkinter.CTkLabel(master, text="Senha: ")
		self.senhaLabel.grid(row = 1 + add, column = 0, padx=20, pady=10)
		self.senhaEntry = customtkinter.CTkEntry(master)
		self.senhaEntry.grid(row=1 + add, column=1, padx=20, pady=10, sticky="EW")

		# Botao login
		self.buttonLogin = customtkinter.CTkButton(master, text="Logar",  command=self.__button_login)
		self.buttonLogin.grid(row=2 + 2*add, column=0, columnspan=2, padx=20, pady=10)

		# Botao registro
		self.buttonRegistro = customtkinter.CTkButton(master, text="Registrar",   command=self.__button_registro)
		self.buttonRegistro.grid(row=3, column=0, columnspan=2)


		# add methods to app
	def __button_login(self):
		if self.registro:
			self.registro = not self.registro
			return self.__reconstroi()
		senha = self.senhaEntry.get()
		email = self.emailEntry.get()

		usuario = self.banco.ler_usuario_por_email(email)
		
		if usuario:
			if (usuario.verifica_login(email, senha)):
				self.parent.usuario = usuario
				self.parent.regerar()
				self.destroy()
				self.update()
				return
			
		messagebox.showinfo("Imp", "Usuario nao encontrado.")
		
		
	
	def __button_registro(self):
		if not self.registro:
			self.registro = not self.registro
			return self.__reconstroi()

		nome = self.nomeEntry.get()
		senha = self.senhaEntry.get()
		email = self.emailEntry.get()

		email = email.lower().strip()
		nome = nome.capitalize().strip()

		if not (email and nome and senha):
			messagebox.showinfo("Imp", "Preencha todos os campos.")
			return

		usuario = Usuario(nome, email, senha)

		usuario = self.banco.cria_usuario(usuario)
		if usuario:
			self.parent.usuario = usuario
			self.parent.regerar()
			self.destroy()
			self.update()
			return
		messagebox.showinfo("Imp", " incorreta.")
