"""pyscaffold

A CLI application for scaffolding Python applications

Examples
    pyscaffold list
    pyscaffold start projectA --python 3.10
    pyscaffold resume projectA

"""
#from pyscaffold.pyscaffold import Pyscaffold
from pyscaffold.pyscaffold import Pyscaffold
from pyscaffold.arg_parser import create_parser
from pyscaffold.utils import preprocess_arguments

SUBCOMMANDS = {
    'list': Pyscaffold.list_projects,
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
