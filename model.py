import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
import joblib

# Carregar o dataset
dataframe = pd.read_csv('dataset_complete_bandpass_only.csv')

y = dataframe.iloc[:, 1].to_numpy()   # target (coluna 'singer')
X = dataframe.iloc[:, 3:].to_numpy()  # features

# Dividir o dataset em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo SVM com kernel RBF e C=1
svm_model = SVC(kernel='linear', C=1, gamma='scale')  # Modificado para kernel 'rbf' e C=1
svm_model.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = svm_model.predict(X_test)

# Avaliar o modelo
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))
print("F1-Score:", f1_score(y_true=y_test, y_pred=y_pred, average='macro'))
print("Precision-Score:", precision_score(y_true=y_test, y_pred=y_pred, average='macro'))
print("Recall-Score:", recall_score(y_true=y_test, y_pred=y_pred, average='macro'))
print("Accuracy-Score:", accuracy_score(y_true=y_test, y_pred=y_pred))

# Salva o modelo treinado para uso futuro
joblib.dump(svm_model, 'singer_identifier_svm_linear_model.pkl')

# Para carregar o modelo e fazer novas previsões
# svm_model = joblib.load('singer_identifier_svm_linear_model.pkl')
# y_new_pred = svm_model.predict(X_new_scaled)  # Onde X_new_scaled são os novos dados padronizados
