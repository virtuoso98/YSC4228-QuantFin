import argparse
import os

def process_inputs() -> dict:
    """Processes inputs from command line for further processing."""

    parser = argparse.ArgumentParser(
        prog = "local_linear",
        description= "Parse x, y inputs, k-folds and graph flag."
    )
    # Adding Command Line Arguments
    parser.add_argument("--x", required = True, help = "Get x-coords filename")
    parser.add_argument("--y", required = True, help = "Get y-coords filename")
    parser.add_argument("--output", required = True, help = "Output Directory of Regression Model")
    parser.add_argument("--num_folds", required = True, type = int)   

    # TODO: ADD ARGUMENT FOR PLOT
    # Adding Relevant Arguments to parser

    return vars(parser.parse_args())


def parse_files(x_filepath, y_filepath):
    """Parse x and y inputs"""

def execute() -> None:
    args = process_inputs()

    # Get x and y filepath name and check if they exist
    x_filepath = f'./data/{args["x"]}.dms'
    y_filepath = f'./data/{args["y"]}.dms'
    x_raw, y_raw = parse_files(x_filepath, y_filepath)

if __name__ == '__main__':
    execute()

    