import time
from evolution import evolve

def loop():
    print("LEVEL 20 CIVILIZATION ACTIVE")

    while True:
        evolve()
        time.sleep(10)


if __name__ == "__main__":
    loop()
