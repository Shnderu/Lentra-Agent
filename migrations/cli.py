import sys
from migrations.runner import rollback

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: rollback <migration_name>")
        exit(1)

    rollback(sys.argv[1])
