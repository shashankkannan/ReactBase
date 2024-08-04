import os


def main():
    print("Choose the application you want to set up:")
    print("1. ReactJS with Firebase")
    print("2. Python Flask with Firebase")

    choice = input("Enter the number corresponding to your choice (1 or 2): ").strip()

    if choice == '1':
        print("Setting up ReactJS with Firebase...")
        os.system('python main.py')
    elif choice == '2':
        print("Setting up Python Flask with Firebase...")
        os.system('python main2.py')
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
