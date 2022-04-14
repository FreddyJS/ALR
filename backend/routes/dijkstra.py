import os
import json
from typing import List


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


def calculate_route(mapa: Mapa, inicio, fin) -> List[Nodo]:
    visitados = ListaNodos()
    frontera = ListaNodos()

    marca_inicio = mapa.getMarca(inicio)
    marca_fin = mapa.getMarca(fin)

    if (marca_fin == None or marca_inicio == None):
        raise ValueError("Número introducido no válido.")

    nodo = Nodo(marca_inicio, marca_inicio, 0)
    frontera.push(nodo)

    while (not frontera.vacia()):
        nodo: Nodo = frontera.pop()
        if (nodo.id == marca_fin):
            resultado = [nodo.padre, nodo.id]
            paso = nodo.padre
            while (paso != marca_inicio):
                paso = visitados.getPadre(paso)
                resultado.insert(0, paso)

            return resultado

        visitados.push(nodo)
        hijos: list[dict] = mapa.enlaces(nodo.id)
        for hijo in hijos:
            id = hijo.get("id")
            coste_acumulado = nodo.coste_acumulado + hijo.get("distancia")
            nodo_hijo = Nodo(id, nodo.id, coste_acumulado)
            if (not visitados.contiene(nodo_hijo)):
                frontera.push(nodo_hijo)


def appendNodeType(mapa: Mapa, ruta):
    aux = []
    for elemento in ruta:
        if (mapa.esCruce(elemento)):
            aux.append("_CRUCE_" + elemento)
        else:
            aux.append("_HABITACION_" + elemento)

    return (aux)


def get_direcciones(mapa: Mapa, ruta):
    direcciones = []
    i = 0

    for node_id in ruta:
        links: list[dict] = mapa.enlaces(node_id)

        for link in links:
            try:
                if (link.get("id") == ruta[i + 1]):
                    direcciones.append(link.get("direccion"))
                    i += 1
            except IndexError:
                pass

    return direcciones


def get_giros(ruta_absoluta, grados, colores):
    giros = []

    for d in ruta_absoluta:
        grados = grados % 360

        if (grados == 0):
            if ("norte" in d):
                grados += 0
                giros.append("recto.")

            elif ("oeste" in d):
                grados += 270
                giros.append("izquierda.")

            elif ("este" in d):
                grados += 90
                giros.append("derecha.")

            elif ("sur" in d):
                grados += 180
                giros.append("vuelta.")

        elif (grados == 90):
            if ("norte" in d):
                grados += 270
                giros.append("izquierda.")

            elif ("oeste" in d):
                grados += 180
                giros.append("vuelta.")

            elif ("este" in d):
                grados += 0
                giros.append("recto.")

            elif ("sur" in d):
                grados += 90
                giros.append("derecha.")

        elif (grados == 270):
            if ("norte" in d):
                grados += 90
                giros.append("derecha.")

            elif ("oeste" in d):
                grados += 0
                giros.append("recto.")

            elif ("este" in d):
                grados += 180
                giros.append("vuelta.")

            elif ("sur" in d):
                grados += 270
                giros.append("izquierda.")

        elif (grados == 180):
            if ("norte" in d):
                grados += 180
                giros.append("vuelta.")

            elif ("oeste" in d):
                grados += 90
                giros.append("derecha.")

            elif ("este" in d):
                grados += 270
                giros.append("izquierda.")

            elif ("sur" in d):
                grados += 0
                giros.append("recto.")

    giros.append(grados)

    if(giros[len(giros)-1] >= 360):
        giros[len(giros)-1] = giros[len(giros)-1] % 360

    counter = 0
    giros_final = []
    while True:
        if (counter == len(giros) - 1):
            giros_final.append(str(giros[counter]) + "." + colores[counter])
            break

        giros_final.append(str(giros[counter]) + str(colores[counter]))
        counter += 1

    return giros_final


def find_exit(mapa: Mapa, blocked_ids: List[str], current_id: str):
    links: list[dict] = mapa.enlaces(current_id)
    links = [link for link in links if link.get("id") not in blocked_ids]
    if (len(links) == 0):
        return False

    # print("Current id: " + current_id)
    # print("Blocked ids: " + str(blocked_ids))
    # print("Links: " + str(links))

    for link in links:
        link_node = mapa.getNodo(link.get("id"))
        if (link_node["tipo"] == "cruce"):
            print("Pasillo con salida: " + link_node["id"])
            return True
        else:
            blocked_ids.append(link.get("id"))
            return find_exit(mapa, blocked_ids, link.get("id"))

    print("Pasillo sin salida: " + current_id)
    return False


def get_rooms():
    map_path = os.path.join(os.path.dirname(__file__), 'mapa.json')
    rooms = []
    with open(map_path, 'r') as f:
        mapa = json.load(f)
        for node in mapa:
            if (node["tipo"] == "habitaciones"):
                for room in node["habitaciones"]:
                    rooms.append(room)

    return rooms


def has_exit(mapa: Mapa, giros: List[str]):
    giros.reverse()
    blocked_ids = []
    current_id = -1
    for giro in giros:
        if "CRUCE" in giro:
            blocked_ids.append(giro.split("_")[-1])
            break
        elif "HABITACION" in giro:
            id = giro.split("_")[-1]
            if current_id == -1:
                current_id = id

            blocked_ids.append(id)

    giros.reverse()
    return find_exit(mapa, blocked_ids=blocked_ids, current_id=current_id)


def route_to_room(origin_room: str, dest_room: str, grados: int = 0):
    map_path = os.path.join(os.path.dirname(__file__), 'mapa.json')
    map = Mapa(map_path)

    # Get the node id of the destiny room, it must be a rooms node
    destId = map.getMarca(dest_room)
    if (destId == None or map.getNodo(destId)["tipo"] != "habitaciones"):
        raise Exception("Destino no encontrado")

    # Get the node id of the origin room, it must be a rooms node
    originId = map.getMarca(origin_room)
    if (originId == None or map.getNodo(originId)["tipo"] != "habitaciones"):
        raise Exception("Origen no encontrado")

    # Calculate route to destiny room
    route = calculate_route(map, origin_room, dest_room)
    absolute_route = get_direcciones(map, route)
    colores = appendNodeType(map, route)
    giros: list[str] = get_giros(absolute_route, grados, colores)

    # Calculate route to from destiny room to origin room
    return_route = calculate_route(map, dest_room, origin_room)
    return_absolute_route = get_direcciones(map, return_route)
    return_types = appendNodeType(map, return_route)
    return_giros = get_giros(return_absolute_route, int(
        giros[-1].split(".")[0]), return_types)

    blocked = has_exit(map, giros)
    return_giros[0] = return_giros[0] + "." + str(blocked)

    return giros, return_giros


if __name__ == "__main__":
    print("From 'hall' to '03'")
    route, return_route = route_to_room("hall", "57")
    print(route, "\n")

    print("From '03' to 'hall'")
    print(return_route)
