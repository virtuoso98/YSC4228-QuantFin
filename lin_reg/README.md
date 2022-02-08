# Assignment 1

This repository houses our code for the first assignment of Data Science in Quantitative Finance. In order to run the code, run the following command:

```
python local_linear.py --x xin –-y yin –-output output –-num_folds 10
```

Additionally, 2 optional parameters, `--plot` and `--xout` are supported. the `--plot` flag is boolean which accepts the values True or False. If the flag is set to true, then a scatter plot of both the input data and predicted data will be created and saved at `./output/graph.png`. The `--xout` parameter accepts a path of the target file as a string. If defined properly, the Gaussian Kernel will predict the y values at the points provided instead of `xin`. As an example, `xout.dms` has been provided. You may run the command

```
python local_linear.py --x xin –-y yin –-output output –-num_folds 10 --plot True --xout ./data/xout
```

Lastly, if you'd like to run all the unit tests, you may run `py.test` at the root directory of this repository. A `requirements.txt` file is also provided in case you need to install the relevant dependencies
