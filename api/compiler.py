from fastapi import APIRouter

router = APIRouter()

@router.post("/compile")
def compile_dsl(body: dict):
    dsl = body["dsl"]

    # simplified compiler
    graph = {
        "nodes": [],
        "edges": []
    }

    for step in dsl.get("steps", []):
        graph["nodes"].append(step["name"])

        for dep in step.get("depends_on", []):
            graph["edges"].append((dep, step["name"]))

    return {
        "compiled": True,
        "graph": graph
    }
