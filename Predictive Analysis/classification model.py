import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

# Load data
dta_file = "ted_2006_2015_panel_collapsed_for_publ_180205.dta"
df = pd.read_stata(dta_file)

# Convert singleb to 0–1 range
df["singleb"] = df["singleb"] / 100

# Create binary target: high corruption risk if singleb > 0.75
df["high_risk"] = (df["singleb"] > 0.75).astype(int)
y = df["high_risk"]

# Select predictor variables
X = df[[
    "exante_transp100",
    "expost_transp100",
    "nocft",
    "ca_contract_type31",
    "ca_contract_type32",
    "ca_contract_type33",
    "econ_2gdp_mio_eur",
    "demo_d3dens"
]]

# Drop missing values
df_model = pd.concat([X, y], axis=1).dropna()
X = df_model.drop(columns=["high_risk"])
y = df_model["high_risk"]

# Scale predictors
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Logistic Regression
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
y_pred_log = log_model.predict(X_test)

print("📊 Logistic Regression Results:")
print("Accuracy:", accuracy_score(y_test, y_pred_log))
print("F1 Score:", f1_score(y_test, y_pred_log))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_log))

# Decision Tree Classifier
tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)

print("\n🌳 Decision Tree Results:")
print("Accuracy:", accuracy_score(y_test, y_pred_tree))
print("F1 Score:", f1_score(y_test, y_pred_tree))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_tree))

# Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

print("\n🌲 Random Forest Results:")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print("F1 Score:", f1_score(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
print("\nClassification Report:\n", classification_report(y_test, y_pred_rf))
