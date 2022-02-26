import dijkstra

#Pasar el mapa a matriz de adyacencia
#Se podría parsear de json a matriz de adyacencia

wmat = [[0, 2, 0, 0, 0, 1, 0, 0],
        [2, 0, 2, 2, 4, 0, 0, 0],
        [0, 2, 0, 0, 3, 0, 0, 1],
        [0, 2, 0, 0, 4, 3, 0, 0],
        [0, 4, 3, 4, 0, 0, 7, 0],
        [1, 0, 0, 3, 0, 0, 5, 0],
        [0, 0, 0, 0, 7, 5, 0, 6],
        [0, 0, 1, 0, 0, 0, 6, 0]]


print (dijkstra.find_all(wmat,0))
print (dijkstra.find_shortest_path(wmat, 0)) #para esepcificar entre dos nodos a la derecha de 0, añadir , n. Siendo n el numero de dicho nodo.	
print (dijkstra.find_shortest_distance(wmat,0)) #aqui igual
