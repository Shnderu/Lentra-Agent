from lentra.core.market_intelligence.graph_v2.symbol_indexer import GraphSymbolIndexer


def build_symbol_index():
    indexer = GraphSymbolIndexer()
    return indexer.build()


if __name__ == "__main__":
    idx = build_symbol_index()
    print("nodes:", len(idx.nodes))
    print("symbols:", len(idx.symbol_index))
