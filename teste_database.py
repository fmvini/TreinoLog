from database import Database

db = Database()

db.conectar()
print("Conexão aberta!")

db.fechar()
print("Conexão fechada!")

db.conectar()
print("Nova conexão aberta!")

db.fechar()