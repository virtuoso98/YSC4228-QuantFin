import argparse, os
import matplotlib.pyplot as plt
from model.gaussian_kernel import GaussianKernel

def process_inputs() -> dict:
    """Processes inputs from command line for further processing."""

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
    parser.add_argument("--xout", required = False, help = "File to Get predictions on")

    return vars(parser.parse_args())

def parse_file(filename: str):
    """Parses dms file at target filepath

    If dms file manages to be parsed, returns a 1D float array of data.
    If filename is None, returns None because this helps the kernel target
    where to predict

    Args:
        filename (str): Path of the file

    Returns:

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

    except (OSError, IOError) as e:
        raise e

def plot_graph(x_raw, y_raw, x_pred, y_pred, is_plot):
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
        plt.show()

    # TODO: Place this in output directory too


def post_process(filename, pred_y):
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filepath = f'./output/{filename}.dms'
    with open(output_filepath, "w", encoding = "utf-8") as fn:
        for line in pred_y:
            fn.write(f'{line}\n')

def execute() -> None:
    """Consolidated function that runs the linear regression model."""
    # Process Command Line Inputs
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
    execute()
