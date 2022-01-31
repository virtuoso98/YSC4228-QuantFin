import argparse

from model.gaussian_kernel import GaussianKernel

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

def parse_files(x_file, y_file):
    """Parse x and y inputs"""
    x_filepath = f'./data/{x_file}.dms'
    y_filepath = f'./data/{y_file}.dms'
    with open(x_filepath) as fx:
        x_str = fx.readlines()
        x_raw = list(map(lambda x: float(x.strip()), x_str))
    with open(y_filepath) as fy:
        y_str = fy.readlines()
        y_raw = list(map(lambda y: float(y.strip()), y_str))

    return x_raw, y_raw    

def execute() -> None:
    # Process Command Line Inputs
    args = process_inputs()
    # Get Raw X, Y data
    x_raw, y_raw = parse_files(args["x"], args["y"])
    kernel = GaussianKernel(x_raw, y_raw, args["num_folds"])
    kernel.train()
    
if __name__ == '__main__':
    execute()
    