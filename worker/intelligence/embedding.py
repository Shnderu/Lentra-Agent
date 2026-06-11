from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    if not text:
        return _model.encode("")
    return _model.encode(text)


def embed_item(item: dict):
    text = f"{item.get('title','')} {item.get('location','')} {item.get('price','')}"
    return embed_text(text)
