import mlflow
import mlflow.sklearn
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

mlflow.set_experiment("Regression Experiment 2")
mlflow.sklearn.autolog()

X, y = make_regression(n_samples=100, n_features=4, noise=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = [("Linear", LinearRegression()), ("RF", RandomForestRegressor())]

for name, model in models:
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        # mlflow.log_param("model_type", name)
        # mlflow.log_metric("mse", mse)
        # mlflow.sklearn.log_model(model, "model")
