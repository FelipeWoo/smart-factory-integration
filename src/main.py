from utils.boot import boot

def main():
    config = boot("main")
    
    # TODO: Add your core logic here
    print(f"Application: {config.name}")

if __name__ == "__main__":
    main()
