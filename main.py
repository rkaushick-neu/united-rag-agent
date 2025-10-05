from src.parser.parser import Parser

def main():
    print("UNITED RAG AGENT!")
    print()
    print("1. Connect to Source (coming soon)")
    print("2. Parse a document from the local system")
    
    choice = input("What would you like to do today? ")
    print()

    match choice:
        case '1':
            print("Still work in progress...")
        case '2':
            print("Would you like to:")
            print("1. Parse a single document.")
            print("2. Parse multiple documents.")
            choice2 = input()
            match choice2:
                case '1':
                    file_loc = input("Enter the location of the file: ")
                    parser = Parser()
                    parser.parse_file(file_path=file_loc)
                case '2':
                    print("Work in progress")
                case _:
                    print("Oops looks like you selected an incorrect option.")
        case _:
            print("Oops looks like you selected an incorrect option.")

if __name__ == "__main__":

    # when the file is executed
    main()
else:
    # when it is run as a module
    pass
