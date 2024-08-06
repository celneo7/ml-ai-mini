import pandas as pd
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

test = pd.read_csv("test.csv")
train = pd.read_csv("train.csv")

test.drop(columns=["Name", "Ticket","Cabin"], inplace=True)
train.drop(columns=["Name", "Ticket","Cabin"], inplace=True)

y = train["Survived"]
X = train.drop(columns=["Survived"])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

cat = X.select_dtypes(include=['object']).columns.tolist()
num = X.select_dtypes(exclude=['object']).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(), cat),
     ("num", StandardScaler(), num)]
)

param_grid = {
    'classifier__learning_rate': [0.01, 0.05, 0.1],
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [3, 4, 5],
    'classifier__subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'classifier__colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0]
}

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", xgb.XGBClassifier())
])

grid_search = GridSearchCV(model, param_grid=param_grid, cv=5, verbose=2)

grid_search.fit(X_train, y_train)


best_model = grid_search.best_estimator_

print(grid_search.best_params_)
test_score = best_model.score(X_test, y_test)
print("Test set accuracy:", test_score)

predictions = best_model.predict(test)

results = pd.DataFrame({
    "PassengerId": test["PassengerId"],
    "Survived": predictions 
})


results.to_csv("predictions.csv")