import os

print("===================================")
print("  LENTRA STABILITY SUITE V11.5")
print("===================================")

os.system("python /app/core/diagnostics/stability_test_01_dedupe.py")
os.system("python /app/core/diagnostics/stability_test_02_locking.py")
os.system("python /app/core/diagnostics/stability_test_05_metrics.py")

print("\n>>> RUN SENDER TEST MANUALLY IF NEEDED")
