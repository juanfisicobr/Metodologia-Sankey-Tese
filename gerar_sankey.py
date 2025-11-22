import pandas as pd
import plotly.graph_objects as go
import io
import os

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
# Tenta localizar o arquivo automaticamente na pasta data ou na raiz
possible_files = [
    "data/Tese tripla.xlsx", 
    "Tese tripla.xlsx", 
    "Tese tripla.xlsx - Sheet 1.csv"
]

filename = None
for f in possible_files:
    if os.path.exists(f):
        filename = f
        break

# Se não achar, tenta upload (caso esteja no Colab)
if filename is None:
    try:
        from google.colab import files
        print("Arquivo de dados não encontrado automaticamente.")
        print("Por favor, faça o upload do arquivo 'Tese tripla.xlsx':")
        uploaded = files.upload()
        filename = next(iter(uploaded))
    except:
        print("ERRO: Arquivo de dados não encontrado. Coloque-o na pasta 'data/'.")
        exit()

# ==============================================================================
# 1. CARREGAMENTO
# ==============================================================================
try:
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = pd.read_excel(filename)
    else:
        df = pd.read_csv(filename)
    print(f"Dados carregados de: {filename}")
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")
    exit()

# ==============================================================================
# 2. LIMPEZA E PREPARAÇÃO
# ==============================================================================
cols_interesse = df.columns[:4].tolist()
print(f"Colunas detectadas: {cols_interesse}")

def limpar_e_separar(texto):
    if pd.isna(texto): return []
    texto = str(texto).replace('\n', ';').replace(',', ';')
    return [p.strip() for p in texto.split(';') if p.strip() != '']

df_clean = df.copy()
for col in cols_interesse:
    df_clean[col] = df_clean[col].apply(limpar_e_separar)

df_long = df_clean
for col in cols_interesse:
    df_long = df_long.explode(col)

df_long.reset_index(drop=True, inplace=True)

# Thesaurus
thesaurus = {
    'pesquisa-ação': 'Pesquisa-ação',
    'bibliográfico': 'bibliografias',
    'bibliográfica': 'bibliografias',
    'interpretativo': 'interpretativa',
    'intepretativo': 'interpretativa',
    'análise textual discursiva': 'Análise Textual Discursiva',
    'questionários': 'questionário',
    'entrevistas semiestruturadas': 'entrevista semiestruturada',
    'entrevista semiestruturada': 'entrevistas',
    'entrevista': 'entrevistas',
    'analise': 'análise de conteúdo',
    'análise de conteúdo': 'Análise de Conteúdo',
    'bardin': 'Bardin',
    'estudo de casos múltiplos.': 'estudo de casos múltiplos',
    'não informado': 'Não Informado',
    'NÃO INFORMADO': 'Não Informado'
}
df_long.replace(thesaurus, inplace=True)
df_long.dropna(subset=cols_interesse, inplace=True)

# ==============================================================================
# 3. FILTRO E LINKS
# ==============================================================================
NUMERO_MAXIMO = 30
mask = pd.Series([True] * len(df_long))

for col in cols_interesse:
    top_terms = df_long[col].value_counts().head(NUMERO_MAXIMO).index
    mask = mask & df_long[col].isin(top_terms).values

df_final = df_long[mask]

links = []
def add_links(df, col_origem, col_destino, index_origem, index_destino):
    suf_origem = f"_{index_origem}"
    suf_destino = f"_{index_destino}"
    g = df.groupby([col_origem, col_destino]).size().reset_index(name='val')
    return [{'source': row[col_origem] + suf_origem, 'target': row[col_destino] + suf_destino, 'value': row['val']} for _, row in g.iterrows()]

for i in range(len(cols_interesse) - 1):
    links += add_links(df_final, cols_interesse[i], cols_interesse[i+1], i, i+1)

# ==============================================================================
# 4. VISUALIZAÇÃO
# ==============================================================================
all_nodes = list(set([l['source'] for l in links] + [l['target'] for l in links]))
node_map = {name: i for i, name in enumerate(all_nodes)}
sources = [node_map[l['source']] for l in links]
targets = [node_map[l['target']] for l in links]
values  = [l['value'] for l in links]
labels_display = [name.rsplit('_', 1)[0] for name in all_nodes]

colors_palette = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A2BE2"]
node_colors = []
for node in all_nodes:
    idx = int(node.rsplit('_', 1)[1])
    node_colors.append(colors_palette[idx % len(colors_palette)])

titulos_annotations = []
num_cols = len(cols_interesse)
for i, col_name in enumerate(cols_interesse):
    pos_x = i / (num_cols - 1) if num_cols > 1 else 0.5
    titulos_annotations.append(dict(
        x=pos_x, y=1.1, xref="paper", yref="paper",
        text=f"<b>{col_name}</b>", showarrow=False,
        font=dict(size=13, color="black"), xanchor="center"
    ))

fig = go.Figure(data=[go.Sankey(
    node = dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels_display, color=node_colors),
    link = dict(source=sources, target=targets, value=values, color="rgba(200, 200, 200, 0.3)")
)])

fig.update_layout(title_text="Delineamento Metodológico: Estratégia, Instrumentos e Análise", font_size=12, height=600, margin=dict(t=100), annotations=titulos_annotations)

# Salvar HTML interativo
fig.write_html("output/sankey_diagram.html")
print("Gráfico salvo em 'output/sankey_diagram.html'")

# Tentar salvar PNG estático (requer kaleido)
try:
    fig.write_image("output/sankey_diagram.png", scale=3)
    print("Imagem PNG salva em 'output/sankey_diagram.png'")
except:
    print("Aviso: Kaleido não instalado, PNG não gerado. Apenas HTML disponível.")

fig.show()
