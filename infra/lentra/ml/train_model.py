import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

DATA_PATH = "/opt/lentra/infra/lentra/ml/dataset.csv"
MODEL_PATH = "/opt/lentra/infra/lentra/ml/model.pkl"


def train():
    df = pd.read_csv(DATA_PATH)

    features = [
        "price_vnd_mln",
        "area_m2",
        "bedrooms",
        "bathrooms",
        "pool",
        "sea_view"
    ]

    X = df[features].fillna(0)
    y = df["label"]

    model = GradientBoostingRegressor()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("[ML] model trained")


if __name__ == "__main__":
    train()
