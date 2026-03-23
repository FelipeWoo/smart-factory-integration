from app.utils.boot import boot


def main() -> None:
    config = boot("main")
    print(f"Application: {config.name}")


if __name__ == "__main__":
    main()
