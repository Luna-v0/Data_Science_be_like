import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set
import random
import time

@dataclass
class Triangulo:
    """Representa um triângulo na triangulação"""
    indices: Tuple[int, int, int]  # índices dos vértices
    vertices: np.ndarray  # array 3x2 com as coordenadas dos vértices
    vizinhos: List[Optional['Triangulo']] = field(default_factory=lambda: [None, None, None])
    
    def __post_init__(self):
        """Garante que vertices seja um numpy array"""
        self.vertices = np.array(self.vertices)
    
    def orientacao(self) -> float:
        """Calcula a orientação do triângulo usando determinante"""
        # Matriz aumentada para calcular orientação
        matriz = np.ones((3, 3))
        matriz[:, :2] = self.vertices
        return np.linalg.det(matriz)
    
    def ponto_no_triangulo(self, ponto: np.ndarray) -> bool:
        """Verifica se um ponto está dentro do triângulo usando determinantes"""
        ponto = np.array(ponto)
        
        # Calcula as orientações para cada aresta
        def orientacao_2d(p1, p2, p3):
            """Calcula orientação de 3 pontos usando determinante"""
            matriz = np.array([
                [p1[0], p1[1], 1],
                [p2[0], p2[1], 1],
                [p3[0], p3[1], 1]
            ])
            return np.linalg.det(matriz)
        
        v0, v1, v2 = self.vertices[0], self.vertices[1], self.vertices[2]
        
        # Verifica se o ponto tem a mesma orientação em relação a todas as arestas
        d0 = orientacao_2d(ponto, v0, v1)
        d1 = orientacao_2d(ponto, v1, v2)
        d2 = orientacao_2d(ponto, v2, v0)
        
        tem_neg = (d0 < 0) or (d1 < 0) or (d2 < 0)
        tem_pos = (d0 > 0) or (d1 > 0) or (d2 > 0)
        
        return not (tem_neg and tem_pos)
    
    def ponto_no_circuncirculo(self, ponto: np.ndarray, epsilon: float = 1e-10) -> bool:
        """Teste InCircle usando determinante (mais estável numericamente)"""
        ponto = np.array(ponto)

        # Constrói a matriz para o teste InCircle
        ax, ay = self.vertices[0, 0] - ponto[0], self.vertices[0, 1] - ponto[1]
        bx, by = self.vertices[1, 0] - ponto[0], self.vertices[1, 1] - ponto[1]
        cx, cy = self.vertices[2, 0] - ponto[0], self.vertices[2, 1] - ponto[1]

        matriz = np.array([
            [ax, ay, ax*ax + ay*ay],
            [bx, by, bx*bx + by*by],
            [cx, cy, cx*cx + cy*cy]
        ])

        det = np.linalg.det(matriz)

        # O sinal do determinante depende da orientação do triângulo
        # Se o triângulo tem orientação positiva (CCW), det > 0 significa dentro
        # Se o triângulo tem orientação negativa (CW), det < 0 significa dentro
        # Usamos epsilon para tratar casos de pontos na circunferência
        orientacao = self.orientacao()

        if orientacao > 0:
            return det > epsilon
        else:
            return det < -epsilon
    
    def circuncirculo(self) -> Tuple[np.ndarray, float]:
        """Calcula o centro e raio do círculo circunscrito"""
        p0, p1, p2 = self.vertices[0], self.vertices[1], self.vertices[2]
        
        # Usa determinantes para calcular o centro
        ax, ay = p0
        bx, by = p1
        cx, cy = p2
        
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        
        if abs(d) < 1e-10:
            return np.array([0, 0]), 0
        
        ux = ((ax*ax + ay*ay) * (by - cy) + 
              (bx*bx + by*by) * (cy - ay) + 
              (cx*cx + cy*cy) * (ay - by)) / d
        
        uy = ((ax*ax + ay*ay) * (cx - bx) + 
              (bx*bx + by*by) * (ax - cx) + 
              (cx*cx + cy*cy) * (bx - ax)) / d
        
        centro = np.array([ux, uy])
        raio = np.linalg.norm(p0 - centro)
        
        return centro, raio
    
    def compartilha_aresta(self, outro: 'Triangulo') -> bool:
        """Verifica se compartilha uma aresta com outro triângulo"""
        vertices_comuns = set(self.indices) & set(outro.indices)
        return len(vertices_comuns) == 2
    
    def get_aresta_compartilhada(self, outro: 'Triangulo') -> Optional[Tuple[int, int]]:
        """Retorna a aresta compartilhada com outro triângulo"""
        vertices_comuns = set(self.indices) & set(outro.indices)
        if len(vertices_comuns) == 2:
            return tuple(vertices_comuns)
        return None
    
    def contem_vertice(self, indice: int) -> bool:
        """Verifica se o triângulo contém um vértice específico"""
        return indice in self.indices
    
    def __hash__(self):
        return hash(self.indices)
    
    def __eq__(self, other):
        if not isinstance(other, Triangulo):
            return False
        return self.indices == other.indices


def criar_super_triangulo(pontos: np.ndarray) -> Tuple[np.ndarray, Triangulo]:
    """Cria um super triângulo que engloba todos os pontos"""
    # Encontra os limites
    min_x, min_y = np.min(pontos, axis=0)
    max_x, max_y = np.max(pontos, axis=0)
    
    # Centro e margem
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    M = max(max_x - min_x, max_y - min_y) * 10
    
    # Vértices do super triângulo (como nos slides)
    super_vertices = np.array([
        [cx - 3*M, cy - 3*M],  # p_{-3}
        [cx + 3*M, cy - 3*M],  # p_{-2}
        [cx, cy + 3*M]         # p_{-1}
    ])
    
    # Adiciona o super triângulo no início da lista de pontos
    pontos_aumentados = np.vstack([super_vertices, pontos])
    
    # Cria o triângulo inicial
    super_triangulo = Triangulo(
        indices=(0, 1, 2),
        vertices=super_vertices
    )
    
    return pontos_aumentados, super_triangulo


def encontrar_triangulos_ruins(ponto: np.ndarray, triangulos: List[Triangulo]) -> List[Triangulo]:
    """Encontra todos os triângulos cujo círculo circunscrito contém o ponto"""
    triangulos_ruins = []
    for tri in triangulos:
        if tri.ponto_no_circuncirculo(ponto):
            triangulos_ruins.append(tri)
    return triangulos_ruins


def encontrar_cavidade(triangulos_ruins: List[Triangulo]) -> List[Tuple[int, int]]:
    """Encontra o polígono de borda (cavity) dos triângulos ruins"""
    arestas_contagem = {}
    
    # Conta quantas vezes cada aresta aparece
    for tri in triangulos_ruins:
        arestas = [
            tuple(sorted([tri.indices[0], tri.indices[1]])),
            tuple(sorted([tri.indices[1], tri.indices[2]])),
            tuple(sorted([tri.indices[2], tri.indices[0]]))
        ]
        
        for aresta in arestas:
            if aresta in arestas_contagem:
                arestas_contagem[aresta] += 1
            else:
                arestas_contagem[aresta] = 1
    
    # Arestas que aparecem apenas uma vez formam a cavidade
    cavidade = []
    for aresta, count in arestas_contagem.items():
        if count == 1:
            cavidade.append(aresta)
    
    return cavidade


def triangulacao_delaunay(pontos: np.ndarray) -> List[Triangulo]:
    """
    Implementa o algoritmo incremental de triangulação de Delaunay
    
    Parâmetros:
        pontos: array numpy de shape (n, 2) com as coordenadas dos pontos
    
    Retorna:
        Lista de triângulos formando a triangulação de Delaunay
    """
    pontos = np.array(pontos)
    
    if len(pontos) < 3:
        return []
    
    # Cria o super triângulo
    pontos_aumentados, super_triangulo = criar_super_triangulo(pontos)
    triangulos = [super_triangulo]
    
    # Adiciona pontos um por um (ordem aleatória para melhor performance)
    indices_pontos = list(range(3, len(pontos_aumentados)))
    random.shuffle(indices_pontos)
    
    for idx_ponto in indices_pontos:
        ponto = pontos_aumentados[idx_ponto]
        
        # Encontra triângulos ruins (que violam a condição de Delaunay)
        triangulos_ruins = encontrar_triangulos_ruins(ponto, triangulos)
        
        if not triangulos_ruins:
            continue
        
        # Encontra a cavidade (polígono de borda)
        cavidade = encontrar_cavidade(triangulos_ruins)
        
        # Remove os triângulos ruins
        for tri in triangulos_ruins:
            triangulos.remove(tri)
        
        # Cria novos triângulos conectando o ponto à cavidade
        for aresta in cavidade:
            novo_tri = Triangulo(
                indices=(aresta[0], aresta[1], idx_ponto),
                vertices=pontos_aumentados[[aresta[0], aresta[1], idx_ponto]]
            )
            triangulos.append(novo_tri)
    
    # Remove triângulos que contêm vértices do super triângulo
    triangulos_finais = []
    for tri in triangulos:
        if not any(v < 3 for v in tri.indices):
            # Ajusta os índices (remove offset do super triângulo)
            indices_ajustados = tuple(i - 3 for i in tri.indices)
            triangulo_final = Triangulo(
                indices=indices_ajustados,
                vertices=pontos[list(indices_ajustados)]
            )
            triangulos_finais.append(triangulo_final)
    
    return triangulos_finais


def plotar_triangulacao(pontos: np.ndarray, triangulos: List[Triangulo], 
                        mostrar_circulos: bool = False):
    """Visualiza a triangulação"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plota os pontos
    ax.scatter(pontos[:, 0], pontos[:, 1], c='red', s=50, zorder=5)
    
    # Numera os pontos
    for i, p in enumerate(pontos):
        ax.annotate(str(i), (p[0], p[1]), xytext=(3, 3), 
                   textcoords='offset points', fontsize=8)
    
    # Plota os triângulos
    for tri in triangulos:
        poligono = patches.Polygon(tri.vertices, fill=False, 
                                  edgecolor='blue', linewidth=1)
        ax.add_patch(poligono)
        
        if mostrar_circulos:
            # Desenha o círculo circunscrito
            centro, raio = tri.circuncirculo()
            circulo = plt.Circle(centro, raio, fill=False, 
                                edgecolor='green', linewidth=0.5, alpha=0.3)
            ax.add_patch(circulo)
    
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Triangulação de Delaunay - Algoritmo Incremental')
    plt.grid(True, alpha=0.3)
    plt.show()


def salvar_triangulacao(pontos: np.ndarray, triangulos: List[Triangulo], 
                        nome_arquivo: str):
    """Salva a triangulação em arquivo texto"""
    with open(nome_arquivo, 'w') as f:
        f.write(f"# Triangulação de Delaunay\n")
        f.write(f"# Número de pontos: {len(pontos)}\n")
        f.write(f"# Número de triângulos: {len(triangulos)}\n\n")
        
        f.write("# Pontos (índice x y)\n")
        for i, p in enumerate(pontos):
            f.write(f"{i} {p[0]:.6f} {p[1]:.6f}\n")
        
        f.write("\n# Triângulos (v0 v1 v2)\n")
        for tri in triangulos:
            f.write(f"{tri.indices[0]} {tri.indices[1]} {tri.indices[2]}\n")


def testar_performance():
    """Testa a performance do algoritmo com diferentes números de pontos"""
    tamanhos = [10, 50, 100, 500, 1000, 5000]
    tempos = []
    
    print("Testando performance do algoritmo:")
    print("-" * 40)
    
    for n in tamanhos:
        # Gera pontos aleatórios
        pontos = np.random.rand(n, 2) * 100
        
        # Mede o tempo de execução
        inicio = time.time()
        triangulos = triangulacao_delaunay(pontos)
        tempo_decorrido = time.time() - inicio
        
        tempos.append(tempo_decorrido)
        print(f"n = {n:5d}: {tempo_decorrido:.4f} segundos "
              f"({len(triangulos)} triângulos)")
    
    # Plota o gráfico de performance
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(tamanhos, tempos, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Número de pontos')
    plt.ylabel('Tempo (segundos)')
    plt.title('Tempo de execução')
    plt.grid(True, alpha=0.3)
    
    # Plota em escala log-log para verificar complexidade
    plt.subplot(1, 2, 2)
    plt.loglog(tamanhos, tempos, 'ro-', label='Tempo medido', 
               linewidth=2, markersize=8)
    
    # Adiciona linha de referência O(n log n)
    tempos_np = np.array(tempos)
    tamanhos_np = np.array(tamanhos)
    
    # Ajusta uma linha de referência O(n log n)
    c = tempos_np[0] / (tamanhos_np[0] * np.log(tamanhos_np[0]))
    nlogn_ref = c * tamanhos_np * np.log(tamanhos_np)
    
    plt.loglog(tamanhos, nlogn_ref, 'g--', label='O(n log n) esperado', 
               linewidth=2, alpha=0.7)
    
    # Adiciona também O(n²) para comparação
    c2 = tempos_np[0] / (tamanhos_np[0]**2)
    n2_ref = c2 * tamanhos_np**2
    plt.loglog(tamanhos, n2_ref, 'b--', label='O(n²) referência', 
               linewidth=1, alpha=0.5)
    
    plt.xlabel('Número de pontos (log)')
    plt.ylabel('Tempo (log)')
    plt.title('Análise de complexidade')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def exemplo_pontos_em_circulo(n: int = 20):
    """Cria pontos distribuídos em um círculo"""
    angulos = np.linspace(0, 2*np.pi, n, endpoint=False)
    raio = 5
    pontos = np.column_stack([
        raio * np.cos(angulos),
        raio * np.sin(angulos)
    ])
    
    # Adiciona alguns pontos no interior
    pontos_internos = np.random.rand(5, 2) * 4 - 2
    pontos = np.vstack([pontos, pontos_internos])
    
    return pontos


def exemplo_grade_regular(nx: int = 5, ny: int = 5):
    """Cria pontos em uma grade regular com pequena perturbação"""
    x = np.linspace(0, 10, nx)
    y = np.linspace(0, 10, ny)
    xx, yy = np.meshgrid(x, y)
    
    pontos = np.column_stack([xx.ravel(), yy.ravel()])
    
    # Adiciona pequena perturbação para evitar degenerações
    ruido = np.random.randn(*pontos.shape) * 0.1
    pontos += ruido
    
    return pontos


# Exemplos de uso
if __name__ == "__main__":
    # Exemplo 1: Conjunto pequeno de pontos
    print("Exemplo 1: Triangulação com poucos pontos")
    pontos_simples = np.array([
        [0, 0], [4, 0], [2, 3], [2, 1],
        [5, 2], [1, 1], [3, 2]
    ])
    
    triangulos = triangulacao_delaunay(pontos_simples)
    plotar_triangulacao(pontos_simples, triangulos, mostrar_circulos=True)
    salvar_triangulacao(pontos_simples, triangulos, "triangulacao_simples.txt")
    
    # Exemplo 2: Pontos em círculo
    print("\nExemplo 2: Pontos distribuídos em círculo")
    pontos_circulo = exemplo_pontos_em_circulo(15)
    triangulos_circulo = triangulacao_delaunay(pontos_circulo)
    plotar_triangulacao(pontos_circulo, triangulos_circulo)
    
    # Exemplo 3: Grade regular
    print("\nExemplo 3: Grade regular com perturbação")
    pontos_grade = exemplo_grade_regular(6, 6)
    triangulos_grade = triangulacao_delaunay(pontos_grade)
    plotar_triangulacao(pontos_grade, triangulos_grade)
    
    # Exemplo 4: Pontos aleatórios
    print("\nExemplo 4: Pontos aleatórios")
    np.random.seed(42)
    pontos_aleatorios = np.random.rand(30, 2) * 10
    triangulos_aleatorios = triangulacao_delaunay(pontos_aleatorios)
    plotar_triangulacao(pontos_aleatorios, triangulos_aleatorios, mostrar_circulos=True)
    salvar_triangulacao(pontos_aleatorios, triangulos_aleatorios, "triangulacao_aleatoria.txt")
    
    # Teste de performance
    print("\n" + "="*50)
    print("TESTE DE PERFORMANCE")
    print("="*50)
    testar_performance()