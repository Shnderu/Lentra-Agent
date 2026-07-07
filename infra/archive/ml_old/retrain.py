import os
from lentra.ml.dataset_builder import build_dataset
from lentra.ml.train_model import train


def run():
    print("[ML] rebuilding dataset...")
    df = build_dataset()
    df.to_csv("/opt/lentra/infra/lentra/ml/dataset.csv", index=False)

    print("[ML] training model...")
    train()

    print("[ML] retrain complete")


if __name__ == "__main__":
    run()
