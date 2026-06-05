from core.engine.queue import push_task


def main():
    print("TASK PUSHED V3")
    push_task('{"type":"alert","payload":{"message":"Hello V3 PRODUCTION"}}')


if __name__ == "__main__":
    main()
