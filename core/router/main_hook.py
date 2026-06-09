# DISABLED GHOST PIPELINE
# раньше здесь был UI handler, он конфликтовал с main.py

async def main_hook(*args, **kwargs):
    print("🛑 main_hook DISABLED")
    return None
