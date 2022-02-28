#! /usr/bin/env python3

import sys
import json
import os

from sqlalchemy import false

class Nodo:
    def __init__(self, id, padre, coste_acumulado):
        self.id = id
        self.padre = padre
        self.coste_acumulado = coste_acumulado


class ListaNodos:
    def __init__(self):
        self.nodos = []

    def push(self, nodo):
        self.nodos.append(nodo)

    def pop(self):
        coste = float("inf")
        resultado = None
        for n in self.nodos:
            if (n.coste_acumulado < coste):
                resultado = n
                coste = n.coste_acumulado
        
        self.nodos.remove(resultado)
        return resultado

    def getPadre(self, id):
        for n in self.nodos:
            if (n.id == id):
                return n.padre
        
        return None

    def vacia(self):
        if (len(self.nodos) == 0):
            return True
        else:
            return False


    def contiene(self, nodo):
        for n in self.nodos:
            if (n.id == nodo.id):
                return True
        
        return False

    def imprime(self):
        print("------------- FRONTERA -----------")
        for n in self.nodos:
            print("MARCA: " + n.id + ", COSTE ACUMULADO: " + str(n.coste_acumulado))




class Mapa:
    def __init__(self,fichero):
        with open(fichero, 'r') as f:
            data=f.read()
            f.close()

        self.mapa = json.loads(data)


    def enlaces(self, id):
        for marca in self.mapa:
            if (marca["id"] == id):
                return marca["enlaces"]

        return []
    
    def esCruce(self, id):
        for marca in self.mapa:
            if (marca["id"] == id):
                if (marca["tipo"] == "cruce"):
                    return True
                else:
                    return false

    def getNodo(self, id):
        for marca in self.mapa:
            if (marca["id"] == id):
                return marca

    def getMarca(self, habitacion_id):
        for marca in self.mapa:
            if (marca["tipo"] == "habitaciones"):
                if (habitacion_id in marca["habitaciones"]):
                    return marca["id"]
            
            elif (marca["tipo"] == "cruce"):
                #print("La marca con id " + habitacion_id + ", es un cruce.")
                if(habitacion_id in marca["id"]):
                    return marca["id"]

    
        return None



def get_ruta(mapa, inicio, fin):

    mapa = Mapa(mapa)
    visitados = ListaNodos()
    frontera = ListaNodos()
    direcciones = []

    marca_inicio = mapa.getMarca(inicio)
    marca_fin = mapa.getMarca(fin)

    if (marca_fin == None or marca_inicio == None):
        print("Número introducido no válido.")
        exit(-1)


    nodo = Nodo(marca_inicio,marca_inicio,0)
    frontera.push(nodo)

    while (not frontera.vacia()):
        #frontera.imprime()
        nodo = frontera.pop()
        if (nodo.id == marca_fin):
            resultado = [nodo.padre, nodo.id]
            paso = nodo.padre
            while (paso != marca_inicio):
                paso = visitados.getPadre(paso)
                resultado.insert(0,paso)
        
            return resultado

        visitados.push(nodo)
        hijos = mapa.enlaces(nodo.id)
        for hijo in hijos:
            id = hijo.get("id")
            coste_acumulado = nodo.coste_acumulado + hijo.get("distancia")
            nodo_hijo = Nodo(id, nodo.id, coste_acumulado)
            if (not visitados.contiene(nodo_hijo)):
                frontera.push(nodo_hijo)


def get_direcciones(mapa, ruta):
    mapa = Mapa(mapa)
    i = 0
    direcciones = []
    try:
        while True:
            e = mapa.enlaces(ruta[i])
            for enl in e:
                if(enl.get("id") == ruta[i+1]):
                    if(mapa.getNodo(ruta[i+1])["tipo"] in "cruce"):
                       # print(ruta[i+1] + " es un: " + mapa.getNodo(ruta[i+1])["tipo"] +  " - ", end="")
                        direcciones.append(enl.get("direccion"))
        
            i+=1
    except IndexError as error:  
        #se añade ultimo enlace, no se añadió antes puesto que para el utlimo enlace lee que el siguiente nodo es de habnitaciones ->
        #no entra if, no lo añade
        n = len(ruta)-2
        for enlace in mapa.enlaces(ruta[n]):
            if(enlace.get("id") == ruta[n+1]):
                direcciones.append(enlace.get("direccion"))

        print("Cálculo de ruta finalizado.")
    return direcciones


if __name__ == "__main__":

    if (len(sys.argv) != 4):
        print("\nSintaxis: python3 ruta.py nombre_mapa.json origen destino\n")
        exit(-1)

    if (os.path.exists("./rutas/" + sys.argv[2] + "_" +  sys.argv[3] + ".txt")):
        print("Ruta de " + sys.argv[2] + " a " + sys.argv[3] + " ya calculada anteriormente.")
        exit(-2)

    #print(str(get_direcciones(sys.argv[1], get_ruta(sys.argv[1], sys.argv[2], sys.argv[3]))))
    ruta = get_direcciones(sys.argv[1], get_ruta(sys.argv[1], sys.argv[2], sys.argv[3]))
    
    try:
        outputFile = open ("./rutas/" + sys.argv[2] + "_" +  sys.argv[3] + ".txt", "w")
    except:
        os.system("mkdir rutas")
        outputFile = open ("./rutas/" + sys.argv[2] + "_" +  sys.argv[3] + ".txt", "w")
    finally:
        for cruce in ruta:
            outputFile.write(str(cruce) + "\n")
        exit(0)
