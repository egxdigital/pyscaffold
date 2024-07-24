"""
Entry point for the Pyscaffold application.

This script serves as the main entry point for the Pyscaffold application. 
It initializes the application, processes command-line arguments, and 
starts the main functionality of the project.

Usage:
    pyscaffold start projectA --python 3.10
    pyscaffold resume projectA

Arguments:
    -h, --help      Show this help message and exit.
    -v, --version   Show the version of the application and exit.
    --config FILE   Specify a configuration file.

Functions:
    main()      The main function that initializes and runs the application.
    execute()   The function that invokes the subcommand passed to the application.

"""
from pyscaffold.pyscaffold import Pyscaffold
from pyscaffold.arg_parser import create_parser
from pyscaffold.utils import preprocess_arguments

SUBCOMMANDS = {
    'list': None,
    'start': Pyscaffold.start,
    'resume': Pyscaffold.resume
}

def execute(command, args):
    func = SUBCOMMANDS[command]
    try:
        result = func(**vars(args))
    except Exception as e:
        print(f"Error: {e}")
    else:
        return result

def main():
    parser = create_parser()
    args = parser.parse_args()
    preprocess_arguments(args)
    execute(args.command, args)
