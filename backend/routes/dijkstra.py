import os
import json


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
            print("MARCA: " + n.id + ", COSTE ACUMULADO: " +
                  str(n.coste_acumulado))


class Mapa:
    def __init__(self, fichero):
        with open(fichero, 'r') as f:
            data = f.read()
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
                if (marca["tipo"] in "cruce"):
                    return True
                else:
                    return False

    def getNodo(self, id):
        for marca in self.mapa:
            if (marca["id"] == id):
                return marca

    def getMarca(self, habitacion_id):
        for marca in self.mapa:
            if (marca["tipo"] == "habitaciones"):
                if (habitacion_id in marca["habitaciones"]):
                    return marca["id"]
                if(habitacion_id in marca["id"]):
                    return marca["id"]

            elif (marca["tipo"] == "cruce"):
                #print("La marca con id " + habitacion_id + ", es un cruce.")
                if(habitacion_id in marca["id"]):
                    return marca["id"]

        return None


def get_ruta(mapa, inicio, fin):
    visitados = ListaNodos()
    frontera = ListaNodos()

    marca_inicio = mapa.getMarca(inicio)
    marca_fin = mapa.getMarca(fin)

    if (marca_fin == None or marca_inicio == None):
        raise ValueError("Número introducido no válido.")

    nodo = Nodo(marca_inicio, marca_inicio, 0)
    frontera.push(nodo)

    while (not frontera.vacia()):
        # frontera.imprime()
        nodo = frontera.pop()
        if (nodo.id == marca_fin):
            resultado = [nodo.padre, nodo.id]
            paso = nodo.padre
            while (paso != marca_inicio):
                paso = visitados.getPadre(paso)
                resultado.insert(0, paso)

            return resultado

        visitados.push(nodo)
        hijos = mapa.enlaces(nodo.id)
        for hijo in hijos:
            id = hijo.get("id")
            coste_acumulado = nodo.coste_acumulado + hijo.get("distancia")
            nodo_hijo = Nodo(id, nodo.id, coste_acumulado)
            if (not visitados.contiene(nodo_hijo)):
                frontera.push(nodo_hijo)


def color(mapa, ruta):
    aux = []
    for elemento in ruta:
        if (mapa.esCruce(elemento)):
            aux.append("_CRUCE.")
        else:
            aux.append("_HABITACION.")

    return (aux)


def get_direcciones(mapa, ruta):
    i = 0
    direcciones = []
    try:
        while True:
            e = mapa.enlaces(ruta[i])
            for enl in e:
                if(enl.get("id") == ruta[i+1]):
                    if(mapa.getNodo(ruta[i+1])["tipo"] in "cruce" or mapa.getNodo(ruta[i+1])["tipo"] in "habitaciones"):
                       # print(ruta[i+1] + " es un: " + mapa.getNodo(ruta[i+1])["tipo"] +  " - ", end="")
                        direcciones.append(enl.get("direccion"))

            i += 1
    except IndexError as _:
        # se añade ultimo enlace, no se añadió antes puesto que para el utlimo enlace lee que el siguiente nodo es de habnitaciones ->
        # no entra if, no lo añade
        n = len(ruta)-2
        for enlace in mapa.enlaces(ruta[n]):
            if(enlace.get("id") == ruta[n+1]):
                direcciones.append(enlace.get("direccion"))

        print("Cálculo de ruta finalizado.\n")
        ctr = 0
        ult_cruce = -1

        for elemento in ruta:
            if (mapa.esCruce(elemento)):
                ult_cruce = ctr
            ctr += 1

        # se le añade esta string a la direccion para saber que es el ultimo cruce
        direcciones[ult_cruce -
                    1] = str(direcciones[ult_cruce - 1]) + "-Este es el último cruce."
        direcciones.pop()  # se quita el ultimo elemento porque se repite
    return direcciones


def get_giros(ruta_absoluta, grados, colores):
    giros = []

    for d in ruta_absoluta:
        grados = grados % 360

        if (grados == 0):
            if ("norte" in d):
                grados += 0
                if("cruce" not in d):
                    giros.append("Recto.")
                else:
                    giros.append("Recto. Llegando al último cruce")

            elif ("oeste" in d):
                grados += 270
                if("cruce" not in d):
                    giros.append("Izquierda.")
                else:
                    giros.append("Izquierda. Llegando al último cruce")

            elif ("este" in d):
                grados += 90
                if("cruce" not in d):
                    giros.append("Derecha.")
                else:
                    giros.append("Derecha. Llegando al último cruce")

            elif ("sur" in d):
                grados += 180
                if("cruce" not in d):
                    giros.append("Dar vuelta.")
                else:
                    giros.append("Dar vuelta. Llegando al último cruce")

        elif (grados == 90):
            if ("norte" in d):
                grados += 270
                if("cruce" not in d):
                    giros.append("Izquierda.")
                else:
                    giros.append("Izquierda. Llegando al último cruce")

            elif ("oeste" in d):
                grados += 180
                if("cruce" not in d):
                    giros.append("Dar la vuelta.")
                else:
                    giros.append("Dar la vuelta. Llegando al último cruce")

            elif ("este" in d):
                grados += 0
                if("cruce" not in d):
                    giros.append("Recto.")
                else:
                    giros.append("Recto. Llegando al último cruce")

            elif ("sur" in d):
                grados += 90
                if("cruce" not in d):
                    giros.append("Derecha.")
                else:
                    giros.append("Derecha. Llegando al último cruce")

        elif (grados == 270):
            if ("norte" in d):
                grados += 90
                if("cruce" not in d):
                    giros.append("Derecha.")
                else:
                    giros.append("Derecha. Llegando al último cruce")

            elif ("oeste" in d):
                grados += 0
                if("cruce" not in d):
                    giros.append("Recto.")
                else:
                    giros.append("Recto. Llegando al último cruce")

            elif ("este" in d):
                grados += 180
                if("cruce" not in d):
                    giros.append("Dar la vuelta.")
                else:
                    giros.append("Dar la vuelta. Llegando al último cruce")

            elif ("sur" in d):
                grados += 270
                if("cruce" not in d):
                    giros.append("Izquierda.")
                else:
                    giros.append("Izquierda. Llegando al último cruce")

        elif (grados == 180):
            if ("norte" in d):
                grados += 180
                if("cruce" not in d):
                    giros.append("Dar la vuelta.")
                else:
                    giros.append("Dar la vuelta. Llegando al último cruce")

            elif ("oeste" in d):
                grados += 90
                if("cruce" not in d):
                    giros.append("Derecha.")
                else:
                    giros.append("Derecha. Llegando al último cruce")

            elif ("este" in d):
                grados += 270
                if("cruce" not in d):
                    giros.append("Izquierda.")
                else:
                    giros.append("Izquierda. Llegando al último cruce")

            elif ("sur" in d):
                grados += 0
                if("cruce" not in d):
                    giros.append("Recto.")
                else:
                    giros.append("Recto. Llegando al último cruce")

    giros.append(grados)

    if(giros[len(giros)-1] >= 360):
        giros[len(giros)-1] = giros[len(giros)-1] % 360

    counter = 0
    giros_final = []
    try:
        while True:
            giros_final.append(str(giros[counter]) + str(colores[counter+1]))
            counter += 1
    except Exception:
        pass

    giros_final.append(giros.pop())
    return giros


def get_final_route(origin: str, dest: str, grados: int = 0):
    map_path = os.path.join(os.path.dirname(__file__), 'mapa.json')
    map = Mapa(map_path)

    route = get_ruta(map, origin, dest)
    absolute_route = get_direcciones(map, route)
    colores = color(map, route)
    giros = get_giros(absolute_route, grados, colores)

    return giros
