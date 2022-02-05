import argparse
import os
import matplotlib.pyplot as plt
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
    parser.add_argument("--output",
        required = True,
        help = "Output Directory of Regression Model")
    parser.add_argument("--num_folds",
        required = True,
        type = int,
        help = "Number of Folds used for Cross Validation")
    parser.add_argument("--plot",
        required = False,
        type = bool,
        default = False,
        help = "Optional Param to display Scatterplot or not")
    parser.add_argument("--xout", required = False, help = "File to Get predictions on")

    return vars(parser.parse_args())

def parse_files(x_file, y_file):
    """Parse x and y inputs"""
    x_filepath = f'./data/{x_file}.dms'
    y_filepath = f'./data/{y_file}.dms'

    # we know these 2 pathfiles will exist, but not the predicted x
    with open(x_filepath) as fx:
        x_str = fx.readlines()
        x_raw = list(map(lambda x: float(x.strip()), x_str))
    with open(y_filepath) as fy:
        y_str = fy.readlines()
        y_raw = list(map(lambda y: float(y.strip()), y_str))
    
    # Check whether file to predict exists

    return x_raw, y_raw

def plot_graph(x_raw, y_raw, pred_y, is_plot):
    if is_plot:
        plt.scatter(x_raw, y_raw, color = 'skyblue', s = 30, alpha = 0.5, marker = 'x', label = "data")
        plt.scatter(x_raw, pred_y, color = 'red', s = 30, alpha = 0.3, marker = '.', label="prediction")
        plt.legend(); plt.show()


def post_process(filename, pred_y):
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filepath = f'./output/{filename}.dms'
    with open(output_filepath, "w") as fn:
        for line in pred_y:
            fn.write(f'{line}\n')

def execute() -> None:
    """Consolidated function that runs the linear regression model."""
    # Process Command Line Inputs
    args = process_inputs()
    # Get Raw X, Y data
    x_raw, y_raw = parse_files(args["x"], args["y"])
    kernel = GaussianKernel(x_raw, y_raw, args["num_folds"])
    pred_y = kernel.train()
    # TODO: PREDICTION
    # Produce Output Directory and Graph
    # post_process(args["output"], pred_y)
    # plot_graph(x_raw, y_raw, pred_y, args["plot"])

if __name__ == '__main__':
    execute()
