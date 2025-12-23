# machine_learning.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# ----- Step 1: Cargar los datasets ----- #
legitimate_df = pd.read_csv('structured_data_legitimate.csv')
phishing_df = pd.read_csv('structured_data_phishing.csv')

# ----- Step 2: Combinar y limpiar datos ----- #
df = pd.concat([legitimate_df, phishing_df], axis=0)
df = df.sample(frac=1).reset_index(drop=True)
df = df.drop('URL', axis=1)
df = df.drop_duplicates()

X = df.drop('label', axis=1)
Y = df['label']

# ----- Step 3: Train/Test split (solo para ejemplo rápido) ----- #
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)

# ----- Step 4: Crear modelos ----- #
svm_model = svm.LinearSVC()
rf_model = RandomForestClassifier(n_estimators=60)
dt_model = tree.DecisionTreeClassifier()
ab_model = AdaBoostClassifier()
nb_model = GaussianNB()
nn_model = MLPClassifier(alpha=1, max_iter=500)
kn_model = KNeighborsClassifier()

# ----- Step 5: Entrenar todos los modelos con todo el dataset de ejemplo ----- #
svm_model.fit(x_train, y_train)
rf_model.fit(x_train, y_train)
dt_model.fit(x_train, y_train)
ab_model.fit(x_train, y_train)
nb_model.fit(x_train, y_train)
nn_model.fit(x_train, y_train)
kn_model.fit(x_train, y_train)

# ----- Step 6: K-Fold manual (K=5) ----- #
K = 5
total = X.shape[0]
index = total // K

X_train_list, X_test_list, Y_train_list, Y_test_list = [], [], [], []

for i in range(K):
    start = i * index
    end = (i + 1) * index if i < K - 1 else total
    X_test_list.append(X.iloc[start:end])
    X_train_list.append(pd.concat([X.iloc[:start], X.iloc[end:]], axis=0))
    Y_test_list.append(Y.iloc[start:end])
    Y_train_list.append(pd.concat([Y.iloc[:start], Y.iloc[end:]], axis=0))

# ----- Step 7: Función para calcular métricas ----- #
def calculate_measures(TN, TP, FN, FP):
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    return accuracy, precision, recall

# ----- Step 8: Inicializar listas de resultados ----- #
models = {
    'NB': nb_model,
    'SVM': svm_model,
    'DT': dt_model,
    'RF': rf_model,
    'AB': ab_model,
    'NN': nn_model,
    'KN': kn_model
}

results_acc = {name: [] for name in models}
results_prec = {name: [] for name in models}
results_rec = {name: [] for name in models}

# ----- Step 9: K-Fold cross validation ----- #
for i in range(K):
    for name, model in models.items():
        model.fit(X_train_list[i], Y_train_list[i])
        pred = model.predict(X_test_list[i])
        tn, fp, fn, tp = confusion_matrix(Y_test_list[i], pred).ravel()
        acc, prec, rec = calculate_measures(tn, tp, fn, fp)
        results_acc[name].append(acc)
        results_prec[name].append(prec)
        results_rec[name].append(rec)

# ----- Step 10: Promediar resultados ----- #
df_results = pd.DataFrame({
    'accuracy': [np.mean(results_acc[name]) for name in models],
    'precision': [np.mean(results_prec[name]) for name in models],
    'recall': [np.mean(results_rec[name]) for name in models]
}, index=list(models.keys()))

# ----- Step 11: Mostrar métricas en consola ----- #
for name in models:
    print(f"{name} - Accuracy: {np.mean(results_acc[name]):.3f}, "
          f"Precision: {np.mean(results_prec[name]):.3f}, "
          f"Recall: {np.mean(results_rec[name]):.3f}")
