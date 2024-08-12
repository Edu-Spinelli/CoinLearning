import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Carregar o arquivo CSV    
csv_file = 'sagausdt_data.csv'
df = pd.read_csv(csv_file)

# Exibir as primeiras linhas do dataset
print(df.head())
# Remover duplicatas (se houver)
df = df.drop_duplicates()

# Verificar se há valores ausentes
missing_data = df.isnull().sum()
print("Dados faltantes por coluna:\n", missing_data)

# Se houver valores ausentes, podemos descartá-los ou substituí-los, dependendo do contexto
df = df.dropna()  # Isso removerá quaisquer linhas com valores ausentes

# Exibir novamente as primeiras linhas do dataset
print(df.head())
# Converter a coluna de timestamp para datetime, se ainda não estiver
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Ordenar os dados por timestamp, se necessário
df = df.sort_values('timestamp')

# Criar uma média móvel de 5 períodos
df['moving_average_5'] = df['price'].rolling(window=5).mean()

# Calcular a volatilidade (desvio padrão) em um período de 5 períodos
df['volatility_5'] = df['price'].rolling(window=5).std()

# Calcular o retorno percentual entre os períodos
df['return_pct'] = df['price'].pct_change()

# Exibir as primeiras linhas com as novas features
print(df.head())

features_to_normalize = ['price', 'moving_average_5', 'volatility_5', 'return_pct']

# Inicializar o normalizador
scaler = MinMaxScaler()

# Aplicar a normalização
df[features_to_normalize] = scaler.fit_transform(df[features_to_normalize])

# Exibir as primeiras linhas com os dados normalizados
print(df.head())
# Salvar o dataset pré-processado em um novo arquivo CSV
df.to_csv('sagausdt_preprocessed.csv', index=False)
