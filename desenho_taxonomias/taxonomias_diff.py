import json
from collections import defaultdict

import networkx as nx
import pandas as pd


def pretty_print_dict(dictionary):
    # Serializa o dicionário como uma string JSON formatada
    json_str = json.dumps(dictionary, indent=4, sort_keys=True)

    # Imprime a string JSON formatada
    print(json_str)


# Função para criar uma árvore a partir de um arquivo CSV
def criar_arvore_csv(arquivo_csv):
    # Carrega os dados do arquivo CSV
    data = pd.read_csv(arquivo_csv)

    # Cria um grafo direcionado
    graph = nx.DiGraph()

    # Adiciona os nós ao grafo
    for index, row in data.iterrows():
        node_id = row["1º"]
        if str(node_id) == "nan":
            continue
        node_label = row["1º"]
        graph.add_node(node_id, label=node_label)
        graph.add_edge("0", node_id)

    node_name = data.loc[0, "1º"]
    # Adiciona as arestas ao grafo
    child_counts = {}
    for index, row in data.iterrows():
        node_id = row["1º"]
        if str(node_id) != "nan":
            node_name = node_id
        parent_id = row["2º"]
        if str(parent_id) == "nan":
            continue
        if parent_id in child_counts:
            child_counts[parent_id] += 1
            parent_id = f"{parent_id}_{child_counts[parent_id]}"
        else:
            child_counts[parent_id] = 0
        graph.add_edge(node_name, parent_id)

    return graph


diretorio = "artigo sbbd/desenho_taxonomias"
# Arquivos CSV das duas árvores
arquivo_csv_1 = f"{diretorio}/Taxonomia em topicos das ementas.csv"
arquivo_csv_2 = f"{diretorio}/Taxonomia em topicos da industria.csv"

# Cria as duas árvores a partir dos arquivos CSV
arvore1 = criar_arvore_csv(arquivo_csv_1)
arvore2 = criar_arvore_csv(arquivo_csv_2)

# Obtém os conjuntos de nós de cada árvore
nos_arvore1 = set(arvore1.nodes)
nos_arvore2 = set(arvore2.nodes)

# Identifica os nós que são diferentes entre as duas árvores
nos_diferentes = set(arvore2.nodes).difference(arvore1.nodes)

# Exibe os nós e seus pais
print("Nós diferentes:")
arvore = defaultdict(list)
for no in nos_diferentes:
    pais = list(arvore2.predecessors(no))
    if pais:
        for pai in pais:
            arvore[pai].append(no)

pretty_print_dict(arvore)
