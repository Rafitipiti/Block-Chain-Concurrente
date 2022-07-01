import os
import time
import threading
import multiprocessing
import hashlib
from collections import OrderedDict
import copy

Dict_Usuarios = OrderedDict()
Dict_Bloques = OrderedDict()

class Usuario:
    def __init__(self, nombre, dni, dinero):
        self.nombre = nombre
        self.dni = dni
        self.dinero = dinero
        
    def mostrar_dinero(self):
        print(self.nombre + " tiene " + str(self.dinero) + " soles.")

    def set_dinero(self, dinero):
        self.dinero = dinero

    def perdida(self,cnt):
        self.dinero -= cnt

    def ganancia(self,cnt):
        self.dinero += cnt

class NeuralCoinBlock:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.usuarios = copy.deepcopy(Dict_Usuarios)
        if(self.previous_block_hash != "Primer bloque"):
            self.usuarios = copy.deepcopy(Dict_Bloques[self.previous_block_hash].usuarios)
        self.transaction_list = transaction_list
        self.block_data = self.Recibe_lista(transaction_list)
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        Dict_Bloques[self.block_hash] = self 

    def Recibe_lista(self,transaction_list):
        List_trans = []
        for i in transaction_list:
            """
            * [u_s] transfiere [cnt] soles a [u_r]
            * last_hash: Referencia al ultimo bloque que conoce esta transaccion 
            """
            # Se declara la intencion de transaccion
            t_str = "%s transfiere %s soles a %s"%(i[0].nombre, i[2], i[1].nombre) # String de transaccion
            List_trans.append(t_str)
            self.Execute_actual_T(i[0],i[1],i[2])     
        return " - ".join(List_trans) + " <- PREV BLOCK: " + self.previous_block_hash 
    
    def Execute_actual_T(self,emisor,receptor,dinero):
        self.usuarios[emisor.dni].dinero = self.usuarios[emisor.dni].dinero - dinero
        self.usuarios[receptor.dni].dinero = (self.usuarios[receptor.dni].dinero + dinero)

#REGISTRO DE USUARIOS
Dict_Usuarios[70254688] = Usuario("Camila",70254688,0.0)
Dict_Usuarios[75968222] = (Usuario("Miguel",75968222,0.0))
Dict_Usuarios[70369878] = (Usuario("Karla",70369878,0.0))
Dict_Usuarios[75852344] = (Usuario("Patricio",75852344,0.0))

# Intentar Transacciones
def Nuevo_bloque(List_trans, last_hash):
    new_block = NeuralCoinBlock(last_hash, List_trans)
    global last_transaction_hash
    last_transaction_hash = new_block.block_hash
    return 1

def tracking(hash):
    if hash not in Dict_Bloques:
        print("El hash no existe")
        return 0
    bloque = Dict_Bloques[hash]
    print("INFORMACION DE LA TRANSACCION: " + hash)
    for i in bloque.usuarios:
       bloque.usuarios[i].mostrar_dinero()

Nuevo_bloque([[Dict_Usuarios[70254688],Dict_Usuarios[75968222],5.5],[Dict_Usuarios[70254688],Dict_Usuarios[75968222],4.5]], "Primer bloque")
Nuevo_bloque([[Dict_Usuarios[70369878],Dict_Usuarios[75852344],4.0]], last_transaction_hash)
Nuevo_bloque([[Dict_Usuarios[70254688],Dict_Usuarios[75852344],2.8]],last_transaction_hash)

print("\nBLOQUES EXISTENTES:")
for i in Dict_Bloques:
    print(Dict_Bloques[i].block_data + " | HASH -> " + Dict_Bloques[i].block_hash)

print("\n")
tracking("1d1d23c3a6cd0c39de6f22a69b58c9e9fe863b54490ee6d1cdb0d1019cb0720b")