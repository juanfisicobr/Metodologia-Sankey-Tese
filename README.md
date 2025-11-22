# Delineamento Metodológico em Pesquisa Qualitativa: Diagrama de Sankey

Este repositório contém o conjunto de dados e o código-fonte em Python utilizados para gerar o **Diagrama de Sankey** apresentado no artigo sobre bases epistemológicas do pensamento complexo em Educação.

O objetivo deste material é garantir a **transparência metodológica** e permitir a **replicação** dos fluxos de análise apresentados no estudo.

## 📂 Sobre os Dados

O arquivo `Tese tripla.xlsx` contém o levantamento das teses analisadas (2015-2024). Os dados foram estruturados em quatro dimensões metodológicas para a geração do fluxo:

1.  **ENFOQUE:** Abordagem da pesquisa (ex: Qualitativa).
2.  **ESTRATÉGIA:** O método ou design (ex: Estudo de Caso, Pesquisa-ação).
3.  **INSTRUMENTOS:** Técnicas de produção de dados (ex: Entrevistas, Observação).
4.  **ANÁLISE:** Técnicas de tratamento de dados (ex: Análise de Conteúdo, Bardin).

## 🛠️ Metodologia de Processamento

O script `sankey_diagram.py` realiza o tratamento dos dados brutos seguindo estas etapas:

1.  **Higienização:** Remoção de caracteres ocultos e padronização de formatação.
2.  **Desagregação (Explode):** Separação de termos múltiplos em uma mesma célula (ex: uma tese que usou "entrevista" e "observação" é contabilizada nos dois fluxos).
3.  **Padronização Semântica (Thesaurus):** Aplicação de um dicionário de sinônimos para unificar termos.
    * *Exemplo:* "questionários", "questões abertas" $\rightarrow$ unificados para **"questionário"**.
    * *Exemplo:* "bardin", "analise" $\rightarrow$ unificados para **"Análise de Conteúdo"** ou **"Bardin"**.
4.  **Filtragem:** Seleção dos **Top 30** termos mais frequentes para garantir a legibilidade visual do gráfico.
5.  **Visualização:** Geração do diagrama interativo utilizando a biblioteca `Plotly`.

## 🚀 Como Executar o Código

### Pré-requisitos
Você precisará de **Python 3.x** instalado. Recomenda-se o uso de ambientes virtuais ou do Google Colab.

### Instalação das Dependências
Execute o seguinte comando no terminal para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
