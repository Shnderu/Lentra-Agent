import joblib
import numpy as np

MODEL_PATH = "/opt/lentra/infra/lentra/ml/model.pkl"

model = None


def load():
    global model
    model = joblib.load(MODEL_PATH)


def predict(property_obj):
    global model

    if model is None:
        load()

    x = np.array([[
        property_obj.price_vnd_mln or 0,
        property_obj.area_m2 or 0,
        property_obj.bedrooms or 0,
        property_obj.bathrooms or 0,
        1 if property_obj.pool else 0,
        1 if property_obj.sea_view else 0
    ]])

    return float(model.predict(x)[0])
EOFcat << 'EOF' > /opt/lentra/infra/lentra/ml/predictor.py
import joblib
import numpy as np

MODEL_PATH = "/opt/lentra/infra/lentra/ml/model.pkl"

model = None


def load():
    global model
    model = joblib.load(MODEL_PATH)


def predict(property_obj):
    global model

    if model is None:
        load()

    x = np.array([[
        property_obj.price_vnd_mln or 0,
        property_obj.area_m2 or 0,
        property_obj.bedrooms or 0,
        property_obj.bathrooms or 0,
        1 if property_obj.pool else 0,
        1 if property_obj.sea_view else 0
    ]])

    return float(model.predict(x)[0])
