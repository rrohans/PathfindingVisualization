import argparse, sys

from App import App
from Cli import Cli


def main() -> None:

    parser = argparse.ArgumentParser(
        "Pathfinding Algorithm Visualizer",
        description="Visualize pathfinding algorithms in action or test different algorithms against each other.",
        epilog="Made by: Rohan Simon",
    )

    parser.add_argument("-mode", help="Run the GUI or CLI version of the program.", choices=["gui", "cli"])
    parser.add_argument("-random", help="Generate a random NxN maze.")
    parser.add_argument("filename", help="The file to read the maze from.", nargs="?")

    args = parser.parse_args()

    if args.mode == "gui":
        app = App()
        app.run()

    elif args.mode == "cli" and args.filename:
        cli = Cli(args.filename)
        cli.run()

    elif args.random:
        cli = Cli.generate_random_maze(int(args.random))
        return
    else:
        if not args.filename and args.mode == "cli":
            print("No filename was provided when running in CLI mode.")
        else:
            parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()
