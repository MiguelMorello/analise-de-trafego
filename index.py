import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Descrição do Dataset
# O dataset analisado contém informações sobre requisições HTTP e suas características.
# Ele inclui colunas como:
# - 'method': método HTTP utilizado (e.g., GET, POST).
# - 'path': caminho requisitado.
# - 'class': classificação da requisição (e.g., legítima ou maliciosa).
# - 'path_length', 'body_length', 'badwords_count', etc.: métricas numéricas relacionadas ao conteúdo das requisições.

# Carregar o arquivo
file_path = '/mnt/data/2bad_reqff.csv'
data = pd.read_csv(file_path)

# Configurar visualizações
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 1. Lidar com valores ausentes
data['body'].fillna('N/A', inplace=True)  # Substituir valores ausentes por 'N/A'

# 2. Análise descritiva
def summarize_data(df):
    print("Resumo Estatístico:\n", df.describe(include='all'))
    print("\nValores Nulos por Coluna:\n", df.isnull().sum())

summarize_data(data)

# 3. Distribuição de métricas numéricas
num_cols = ['single_q', 'double_q', 'dashes', 'braces', 'spaces',
            'path_length', 'body_length', 'badwords_count']

for col in num_cols:
    plt.figure()
    sns.histplot(data[col], kde=True, bins=30, color='blue')
    plt.title(f'Distribuição de {col}')
    plt.xlabel(col)
    plt.ylabel('Frequência')
    plt.show()

# 4. Relações entre variáveis
plt.figure()
sns.heatmap(data[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title('Correlação entre Variáveis Numéricas')
plt.show()

# 5. Gráficos por classe
data['class'] = data['class'].astype('category')  # Converter para categórico

for col in num_cols:
    plt.figure()
    sns.boxplot(x='class', y=col, data=data)
    plt.title(f'Distribuição de {col} por Classe')
    plt.xlabel('Classe')
    plt.ylabel(col)
    plt.show()

# 6. Análise de padrões de path e body
data['path_length_bin'] = pd.qcut(data['path_length'], q=4, labels=['Curto', 'Médio', 'Longo', 'Muito Longo'])

plt.figure()
sns.countplot(x='path_length_bin', hue='class', data=data, palette='Set2')
plt.title('Distribuição do Comprimento do Path por Classe')
plt.xlabel('Comprimento do Path')
plt.ylabel('Frequência')
plt.show()

# 8. Salvar resumo em CSV
summary_path = '/mnt/data/log_analysis_summary.csv'
data.describe(include='all').to_csv(summary_path)
print(f"Resumo estatístico salvo em: {summary_path}")
