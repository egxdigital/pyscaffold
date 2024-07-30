"""
Entry point for the Pyscaffold application.

This script serves as the main entry point for the Pyscaffold application. 
It initializes the application, processes command-line arguments, and 
invokes the appropriate functionality based on the subcommands provided.

Usage:
    pyscaffold start projectA --python 3.10
    pyscaffold resume projectA

Arguments:
    -h, --help      Show this help message and exit.
    -v, --version   Show the version of the application and exit.
    --config FILE   Specify a configuration file.

Functions:
    execute(command: str, args: argparse.Namespace) -> None
        Invokes the function associated with the specified command, passing the provided arguments.
        
    main() -> None
        Initializes the argument parser, preprocesses the arguments, and executes the specified command.
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
    """
    Invoke the function associated with the specified command.

    Args:
        command (str): The command to be executed.
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    func = SUBCOMMANDS[command]
    try:
        result = func(**vars(args))
    except Exception as e:
        print(f"Error: {e}")
    else:
        return result

def main():
    """
    Initialize the argument parser, preprocess arguments, and execute the specified command.

    Returns:
        None
    """
    parser = create_parser()
    args = parser.parse_args()
    preprocess_arguments(args)
    execute(args.command, args)
