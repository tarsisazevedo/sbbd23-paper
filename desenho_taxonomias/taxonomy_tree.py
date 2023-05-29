import argparse
import os
import random

import pandas as pd
import pygraphviz as pgv

sampled_nodes = {
    "Taxonomia em topicos da biblio": ["Arquitetura de bancos de dados", "Data Warehouse", "Controle de concorrencia"],
    "Taxonomia em topicos das ementas": ["Big Data", "Data Warehouse", "Modelagem Conceitual"],
    "Taxonomia em topicos da industria": ["Modelagem Conceitual", "Bancos de dados não relacionais", "Data Warehouse"],
}

def desenha_arvore(data, nome_arquivo, full=False, orientation="LR", sample=False):
    # Cria o grafo
    graph = pgv.AGraph(directed=True)
    graph.add_node("0", label=nome_arquivo[:-4])

    nodes_added = []
    # Adiciona os nós ao grafo
    for index, row in data.iterrows():
        node_id = row["1º"]
        if sample:
            if node_id not in sampled_nodes[nome_arquivo]:
                continue
        if str(node_id) == "nan":
            continue
        node_label = row["1º"]
        graph.add_node(node_id, label=node_label)
        graph.add_edge("0", node_id)
        nodes_added.append(node_id)

    node_name = data.loc[0, "1º"]
    # Adiciona as arestas ao grafo
    child_counts = {}
    for index, row in data.iterrows():
        node_id = row["1º"]
        if str(node_id) != "nan":
            node_name = node_id
        if node_name not in nodes_added:
            continue
        parent_id = row["2º"]
        if str(parent_id) == "nan":
            continue
        if parent_id in child_counts:
            child_counts[parent_id] += 1
            parent_id = f"{parent_id}_{child_counts[parent_id]}"
        else:
            child_counts[parent_id] = 0
        graph.add_edge(node_name, parent_id)

    if full:
        child_counts = {}
        for index, row in data.iterrows():
            node_id = row["2º"]
            if str(node_id) != "nan":
                node_name = node_id
            parent_id = row["3º"]
            if str(parent_id) == "nan":
                continue
            if parent_id in child_counts:
                child_counts[parent_id] += 1
                parent_id = f"{parent_id}_{child_counts[parent_id]}"
            else:
                child_counts[parent_id] = 0
            graph.add_edge(node_name, parent_id) 
    # Define a posição dos nós no layout
    graph.graph_attr["rankdir"] = orientation
    graph.layout(prog="dot")

    # Salva o grafo em um arquivo de imagem
    if sample:
        nome_arquivo = f"{nome_arquivo}_sample"
    graph.draw(f"{nome_arquivo}.png")


def run_all(full=False, orientation="LR", sample=False):
    diretorio = "desenho_taxonomias"

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            data = pd.read_csv(caminho_arquivo)
            desenha_arvore(data, arquivo[:-4], full=full, orientation=orientation, sample=sample)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--orientation", default="LR")
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    run_all(full=args.full, orientation=args.orientation, sample=args.sample)