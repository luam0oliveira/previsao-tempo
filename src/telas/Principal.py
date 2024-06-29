import datetime
import time

from typing import Tuple
from wsgiref import validate
import customtkinter
from tkinter import Tk, messagebox
import ttkbootstrap as tb

from Banco import Banco
from telas.Login import Login
from util import criaPrevisao

# Classe Principal
class Principal(customtkinter.CTk):
	def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
		super().__init__(fg_color, **kwargs)
		self.geometry("1000x600")
		self.title("TESTE")
		self.banco = Banco()
		self.usuario = None
		self.container = customtkinter.CTkFrame(self)
		self.container.pack(expand = True, fill = "both")
		self.container.configure(fg_color = "yellow")
		self.__add_widgets(self.container)
		self.mainloop()
		

	def regerar(self):
		print(self.usuario)
		for child in self.container.grid_slaves():
			child.destroy()
		self.__add_widgets(self.container)
		self.container.update()

	def __add_widgets(self, master):
		if not self.usuario:
			master.grid_rowconfigure(0, weight=1)
			master.grid_columnconfigure(0, weight=1)
			customtkinter.CTkButton(master, text="É necessario logar", fg_color="red", command=self.logar).grid()
			return
		
		self.container.columnconfigure(0, weight = 1)
		self.container.rowconfigure(0, weight=1)
		self.container.rowconfigure((1,2,3,4), weight = 3)
		containerEscolha = customtkinter.CTkFrame(self.container, height= 0)
		containerEscolha.grid(column = 0, row = 0, sticky = "WESN")

		containerEscolha.columnconfigure((0,1,2,3,4,5), weight= 1)
		containerEscolha.rowconfigure((0,1), weight=1)

		# Adiciona cidade
		self.cidadeEntry = customtkinter.CTkEntry(containerEscolha, )
		self.cidadeEntry.grid(row=1, column=0, padx=20, pady=10, sticky="EW")

		# Adiciona estado
		self.estadoEntry = customtkinter.CTkEntry(containerEscolha)
		self.estadoEntry.grid(row=1, column=1, padx=20, pady=10, sticky="EW")

		# DataInicial
		self.dataInicial = tb.DateEntry(containerEscolha)
		self.dataInicial.grid(column=2, row= 1)
		
		self.dataFinal = tb.DateEntry(containerEscolha)
		self.dataFinal.grid(column=3, row= 1)

		customtkinter.CTkLabel(containerEscolha, text="Data Final", height=0, width=0).grid(column = 3, row=0)
		customtkinter.CTkLabel(containerEscolha, text="Data Inicial").grid(column = 2, row=0)
		customtkinter.CTkLabel(containerEscolha, text="Cidade: ").grid(row = 0, column = 0)
		customtkinter.CTkLabel(containerEscolha, text="Estado: ").grid(row = 0, column = 1)
		customtkinter.CTkButton(containerEscolha, text="CONSULTAR", command=self.validaData).grid(column=4,columnspan = 2, row= 0, rowspan = 2)

		self.containerPrevisoes = customtkinter.CTkFrame(self.container, fg_color="white")
		self.containerPrevisoes.rowconfigure((0,1,2,3,4,5,6), weight=1)
		self.containerPrevisoes.columnconfigure(0, weight=1)
		self.containerPrevisoes.grid(column = 0, row = 1, rowspan = 4, sticky = "NSWE")

	def validaData(self):
		dataInit = list(map(int,self.dataInicial.entry.get().split('/')))
		dataInit = datetime.date(dataInit[2], dataInit[1], dataInit[0])
		maximo = datetime.date.today() + datetime.timedelta(days=7)
		minimo = datetime.date.today()

		dataFim = list(map(int,self.dataFinal.entry.get().split('/')))
		dataFim = datetime.date(dataFim[2], dataFim[1], dataFim[0])

		if dataInit < minimo or dataInit > maximo:
			messagebox.showinfo("Imp", "Data inicial incorreta.")
			return
		
		if dataFim < dataInit or dataFim > maximo:
			messagebox.showinfo("Imp", "Data final incorreta.")
			return
		
		# CHAMADA REQUEST
		dados = criaPrevisao(self.cidadeEntry.get(), self.estadoEntry.get())

		if not dados:
			messagebox.showinfo("Imp", "Não foi possivel encontrar a cidade.")
			return
		
		for slave in self.containerPrevisoes.slaves():
			slave.destroy()

		cont = 0
		for data in dados:
			data1 = list(map(int,data.split('-')))
			print(data1)
			data1 = datetime.date(data1[0], data1[1], data1[2])
			if data1 < dataInit or data1 > dataFim:
				continue
			
			contain = customtkinter.CTkFrame(self.containerPrevisoes, fg_color="green")
			contain.columnconfigure((0,1,2,3,4,5), weight=1)
			contain.rowconfigure(0, weight=1)

			customtkinter.CTkLabel(contain, text=f"DATA: {data1.strftime('%d/%m/%Y')}").grid(column=0, row=0, )
			customtkinter.CTkLabel(contain, text=f"CIDADE: {dados[data].cidade}").grid(column=1, row=0, )
			customtkinter.CTkLabel(contain, text=f"PAIS: {dados[data].pais}").grid(column=2, row=0, )
			customtkinter.CTkLabel(contain, text=f"MINIMA: {dados[data].minTemp}").grid(column=3, row=0, )
			customtkinter.CTkLabel(contain, text=f"MAXIMA: {dados[data].maxTemp}").grid(column=4, row=0, )
			customtkinter.CTkLabel(contain, text=f"DESC,: {dados[data].descricao}").grid(column=5, row=0, )
			contain.grid(row = cont, column = 0, sticky = "NSWE")
			cont+=1
		self.containerPrevisoes.update()
		
		
	def logar(self):
		login = Login(self, self.banco)
		login.mainloop()

	