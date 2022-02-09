import argparse
import os
from typing import Optional
import matplotlib.pyplot as plt
from model.gaussian_kernel import GaussianKernel

def process_inputs() -> dict:
    """Processes inputs from command line for further processing.

    Returns:
        Dictionary that maps parser command line arguments (key) to
        the parameters (values) inputted by the user.
    """

    parser = argparse.ArgumentParser(
        prog = "local_linear",
        description= "Parse x, y inputs, k-folds and graph flag."
    )
    # Adding Relevant Command Line Arguments
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
    parser.add_argument("--xout",
        required = False,
        help = "Optional file param that contains x values for evaluation")

    return vars(parser.parse_args())

def parse_file(filename: str) -> Optional[list[float]]:
    """Parses dms file at target filepath

    If dms file manages to be parsed, returns a 1D float array of data.
    If filename is None, returns None. This is helpful in helping the
    kernel identify whether to predict xin or xout.

    Args:
        filename (str): Path of the file

    Returns:
        List[float] / None: None if filename is None, else float array of data

    Raises:
        OSError: If target file is not found
        ValueError: If file contains non-numeric characters
    """

    # Caters for the case when no xout argument is fed
    if filename is None:
        return None
    # xin and yin are always in data, but for xout,
    # source directory could differ
    if filename in ("xin", "yin"):
        fullpath = f'./data/{filename}.dms'
    else:
        fullpath = f'{filename}.dms'

    # we know these 2 pathfiles will exist, but not the predicted x
    try:
        with open(fullpath, encoding = "utf-8-sig") as f:
            file_str = f.readlines()
            parsed_data = list(map(lambda x: float(x.strip()), file_str))
        return parsed_data

    except (OSError, ValueError) as e:
        raise e

def plot_graph(x_raw: list[float],
    y_raw: list[float],
    x_pred: list[float],
    y_pred: list[float],
    is_plot: bool):
    """Creates the scatterplot of y against x using matplotlib.pyplot.

    Args:
        x_raw: list of x input data used to determine optimal h
        y_raw: list of y input data used to determine optimal h
        x_pred: list of x data predicted using linear kernel regression
        y_pred: list of y data predicted using linear kernel regression
        is_plot: Flag of Whether graph should be plotted or not

    Returns:
        A graph of the corresponding scatter plot, stored in
        ./output directory
    """
    # Plot Scatter Plot of Predicted Graph
    if is_plot:
        plt.scatter(x = x_raw, y = y_raw,
            color = 'skyblue', s = 30, alpha = 0.5,
            marker = 'x', label = "data")
        # Plot Scatter Plot of Predict Graph
        plt.scatter(x = x_pred, y = y_pred,
            color = 'red', s = 30, alpha = 0.3,
            marker = '.', label="prediction")
        plt.legend()
        plt.savefig('./output/graph.png')
        plt.show()

def post_process(filename: str, pred_y: list[float]):
    """Produces the output file of predicted y.

    Args:
        filename:  name of output file. placed in ./output directory
        pred_y: float array of predicted y values based on optimal h

    Returns:
        A text file output/{filename}.dms that contains the predicted
        y values, separated by newlines.
    """
    output_dir = './output'
    # make directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filepath = f'./output/{filename}.dms'
    with open(output_filepath, "w", encoding = "utf-8") as fn:
        for line in pred_y:
            fn.write(f'{line}\n')

def execute():
    """Overall function that runs kernel linear regression"""
    args = process_inputs()
    # Get Raw X, Y data and predict
    x_raw = parse_file(args["x"])
    y_raw = parse_file(args["y"])
    x_to_predict = parse_file(args["xout"])

    # Instantiate Kernel, train it and predict if applicable
    kernel = GaussianKernel(x_raw, y_raw, args["num_folds"])
    final_y_pred = kernel.train_and_predict(x_to_predict)
    # Produce Output Directory and Graph
    post_process(args["output"], final_y_pred)
    # Plot the graph, if boolean parameter is given
    is_plot = args["plot"]
    plot_graph(x_raw,
        y_raw,
        x_raw if not x_to_predict else x_to_predict,
        final_y_pred,
        is_plot)

if __name__ == '__main__':
    # Process Command Line Inputs
    execute()
