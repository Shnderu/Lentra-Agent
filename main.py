import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

print(">>> MAIN START")

try:
    from core.runtime.unified import unified_entry
    print(">>> IMPORT OK")

    from aiogram import Bot, Dispatcher
    print(">>> AIROGRAM OK")

except Exception as e:
    print(">>> BOOT ERROR:")
    traceback.print_exc()
    raise

print(">>> MAIN READY")
