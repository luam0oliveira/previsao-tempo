class Previsao:
	def __init__(self, cidade: str, pais: str, minTemp: int, maxTemp: int, descricao: str) -> None:
		self.cidade = cidade
		self.pais = pais
		self.minTemp = int(minTemp)
		self.maxTemp = int(maxTemp)
		self.descricao = descricao