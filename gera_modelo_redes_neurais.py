import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import joblib

# Carregar o dataset
dataset = pd.read_csv('dataset_complete_with_recordings.csv')

X = dataset.iloc[:, 3:]  # Características
y = dataset.iloc[:, 1]   # Variável alvo

# Codificar as classes como inteiros
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Converter y para categórico
y = to_categorical(y)

# Dividir o dataset em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pré-processamento: padronizar as características (normalização z-score)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Definir o modelo de rede neural
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(y_train.shape[1], activation='softmax'))  # Softmax para classificação multiclasse

# Compilar o modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinar o modelo
model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=1)

# Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)
y_pred_classes = y_pred.argmax(axis=-1)
y_test_classes = y_test.argmax(axis=-1)

# Avaliar o modelo
print("Relatório de Classificação:")
print(classification_report(y_test_classes, y_pred_classes))
print("Acurácia:", accuracy_score(y_test_classes, y_pred_classes))

# Salva o modelo treinado para uso futuro
# model.save('modelo_redes_neurais_bandpass.h5')
# joblib.dump(scaler, 'scaler.pkl')  # Salvar o scaler também
# joblib.dump(label_encoder, 'label_encoder.pkl')  # Salvar o codificador de rótulos também
# Salva o modelo treinado para uso futuro
joblib.dump(model, 'nn_model.pkl')