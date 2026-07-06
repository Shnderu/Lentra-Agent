from lentra.runtime.dag_builder import DependencyGraph
from lentra.runtime.dag_validator import DAGValidator
from lentra.runtime.dag_policy import check_policy


def main():
    print("[DAG] scanning project...")

    g = DependencyGraph()
    g.scan_dir("/opt/lentra/infra/lentra")

    graph = g.get_graph()

    print("[DAG] validating cycles...")
    DAGValidator(graph).validate()

    print("[DAG] checking policy...")
    check_policy(graph)

    print("[DAG] OK - architecture clean")


if __name__ == "__main__":
    main()
