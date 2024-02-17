class Grafo:
    def __init__(self):
        self.matriz_adj = []
        self.lista_adj = {}
        self.num_vertices = 0

    def carregar_grafo_do_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            self.num_vertices = int(linhas[0].strip())
            self.matriz_adj = [[int(x) for x in linha.split()] for linha in linhas[1:]]
            self.construir_lista_adj()

    def construir_lista_adj(self):
        self.lista_adj = {i: [] for i in range(1, self.num_vertices + 1)}
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.matriz_adj[i][j] == 1:
                    self.lista_adj[i + 1].append(j + 1)

    def imprimir_matriz_adj(self):
        for linha in self.matriz_adj:
            print(' '.join(str(celula) for celula in linha))

    def imprimir_lista_adj(self):
        for vertice, vizinhos in self.lista_adj.items():
            print(f'{vertice}: {vizinhos}')

    def calcular_graus_min_max(grafo):
        grau_minimo = float('inf')
        grau_maximo = 0

        for linha in grafo.matriz_adj:
            grau_vertice = sum(linha)
            if grau_vertice < grau_minimo:
                grau_minimo = grau_vertice
            if grau_vertice > grau_maximo:
                grau_maximo = grau_vertice

        return grau_minimo, grau_maximo
    
    def sequencia_de_graus(grafo):
        sequencia = []

        for linha in grafo.matriz_adj:
            grau_vertice = sum(linha)
            sequencia.append(grau_vertice)

        return sequencia
    
    def grau_e_vizinhanca(grafo, vertice):
        grau = sum(grafo.matriz_adj[vertice - 1])
        vizinhanca_aberta = [i + 1 for i in range(grafo.num_vertices) if grafo.matriz_adj[vertice - 1][i] == 1]
        vizinhanca_fechada = [i + 1 for i in range(grafo.num_vertices) if i != vertice - 1 and grafo.matriz_adj[vertice - 1][i] == 1]

        return grau, vizinhanca_aberta, vizinhanca_fechada
    
    def adjacencia(self, u, v):
        if u == v or u < 1 or v < 1 or u > self.num_vertices or v > self.num_vertices:
            return False  # Vértices iguais ou inválidos não são vizinhos

        return self.matriz_adj[u - 1][v - 1] == 1
    
    def regularidade(self):
        grau_min, grau_max = self.calcular_graus_min_max()

        return grau_min == grau_max, grau_min
    
    def completude(self):
        num_arestas_possiveis = (self.num_vertices * (self.num_vertices - 1)) // 2
        num_arestas = sum(sum(linha) for linha in self.matriz_adj) // 2
        
        return num_arestas == num_arestas_possiveis
    
    def vertices_universais(self):
        vertices_univ = []
        for i in range(self.num_vertices):
            if sum(self.matriz_adj[i]) == self.num_vertices - 1:
                vertices_univ.append(i + 1)
        return vertices_univ
    
    def vertices_isolados(self):
        vertices_isolados = []
        for i in range(self.num_vertices):
            if sum(self.matriz_adj[i]) == 0:
                vertices_isolados.append(i + 1)
        return vertices_isolados
    
    def subgrafo(self, vertices, arestas):
        # Verifica se todos os vértices de H estão em G
        for vertice in vertices:
            if vertice not in range(1, self.num_vertices + 1):
                return False

        # Verifica se todos os extremos das arestas de H estão em G
        for aresta in arestas:
            u, v = aresta
            if u not in vertices or v not in vertices:
                return False

        return True
    
    def passeio(self, sequencia_vertices):
        for i in range(len(sequencia_vertices) - 1):
            u = sequencia_vertices[i]
            v = sequencia_vertices[i + 1]
            if not self.adjacencia(u, v):
                return False
        return True
    
    def caminho(self, sequencia_vertices):
        if len(set(sequencia_vertices)) != len(sequencia_vertices):
            return False  # Verifica se há vértices repetidos
        return self.passeio(sequencia_vertices)
    
    def ciclo(self, sequencia_vertices):
        if len(sequencia_vertices) < 3:
            return False  # Um ciclo deve ter pelo menos 3 vértices
        if sequencia_vertices[0] != sequencia_vertices[-1]:
            return False  # O primeiro e o último vértices devem ser iguais
        return self.caminho(sequencia_vertices[:-1])
    
    def trilha(self, sequencia_vertices):
        arestas_visitadas = set()

        for i in range(len(sequencia_vertices) - 1):
            u = sequencia_vertices[i]
            v = sequencia_vertices[i + 1]
            if not self.adjacencia(u, v):
                return False  # Verifica se há uma aresta entre os vértices
            aresta = tuple(sorted((u, v)))
            if aresta in arestas_visitadas:
                return False  # Verifica se a aresta já foi visitada
            arestas_visitadas.add(aresta)

        return True
    
    def clique(self, conjunto_vertices):
        for u in conjunto_vertices:
            for v in conjunto_vertices:
                if u != v and not self.adjacencia(u, v):
                    return False  # Verifica se há uma aresta entre todos os pares de vértices
        return True
    
    def clique_maximal(self, conjunto_vertices):
        for vertice in range(1, self.num_vertices + 1):
            if vertice not in conjunto_vertices:
                if self.clique(conjunto_vertices.union({vertice})):
                    return False  # Verifica se o conjunto pode ser expandido
        return True
    
    def complemento(self):
        grafo_complementar = Grafo()
        grafo_complementar.num_vertices = self.num_vertices
        grafo_complementar.matriz_adj = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]

        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if not self.adjacencia(i + 1, j + 1):  # Se não há aresta entre os vértices
                    grafo_complementar.matriz_adj[i][j] = 1
                    grafo_complementar.matriz_adj[j][i] = 1  # Grafo não direcionado

        grafo_complementar.construir_lista_adj()
        return grafo_complementar
    
    def conjunto_independente(self, conjunto_vertices):
        for u in conjunto_vertices:
            for v in conjunto_vertices:
                if u != v and self.adjacencia(u, v):
                    return False  # Verifica se não há aresta entre todos os pares de vértices
        return True
    
    


