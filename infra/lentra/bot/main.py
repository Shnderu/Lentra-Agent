from lentra.runtime.contracts import ExecutionEnvelope

def main():
    # hard fail-safe init
    envelope = ExecutionEnvelope()

    print("[BOT] runtime envelope loaded OK")

    # TODO: дальше UI layer
    # bot must NOT execute tasks, only publish intents

if __name__ == "__main__":
    main()
