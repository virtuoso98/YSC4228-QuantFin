from tools.fetcher import Fetcher

class Processor(Fetcher):

    def __init__(self, args: dict):
        super().__init__(args)
        self._check_processor_validity(args)
        self._initial_aum = args["initial_aum"]
        self._is_plot = args["plot"]

    def _check_processor_validity(self, args: dict):

        pass
