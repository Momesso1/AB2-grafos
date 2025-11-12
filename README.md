# Prática 2 — Grafos para Navegação de Robôs

Este projeto implementa o conceito de *Grafos de Visibilidade* aplicado ao *planejamento de caminho para veículos autônomos*.  
O objetivo é transformar um mapa (ocupancy grid) em uma representação topológica do ambiente, gerar um *grafo de visibilidade, construir uma **árvore mínima* (usando Kruskal ou Prim), e finalmente planejar um *caminho do robô* entre dois pontos.

---

## Descrição da Prática

A prática consiste em representar um ambiente 2D como um *grafo de visibilidade*, onde cada vértice representa:
- *quinas dos obstáculos*,  
- *posição inicial do robô*, e  
- *posição final desejada*.

Há uma aresta entre dois vértices se houver *visada direta* entre eles, isto é, uma linha reta entre os dois pontos *sem cruzar obstáculos*.

O grafo resultante é utilizado para gerar uma *árvore de custo mínimo* (usando Kruskal ou Prim), e a partir dela, encontrar o *melhor caminho* entre dois vértices (por exemplo, q_start → q_goal).

---

## ✅ Requisitos do Projeto

- [x] 1️⃣ Leitura do mapa (`.txt`) e imagem (`.png`)  
- [x] 2️⃣ Geração do grafo de visibilidade  
- [x] 3️⃣ Implementação do algoritmo de **Prim**  
- [x] 4️⃣ Função `verticeMaisProximo()`  
- [x] 5️⃣ Algoritmo de busca em árvore (BFS ou DFS)  
- [x] 6️⃣ Plotagem do caminho no mapa (`matplotlib`)  
- [x] 7️⃣ README completo com instruções e prints  

---

## ⚙️ Instalação

Clone este repositório e instale as dependências:

```bash
git clone https://github.com/LucasMomesso/AB2-grafos.git
cd AB2-grafos
python pratica2_grafos.py mapa_exemplo.txt
