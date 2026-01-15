# import typing
#  = typing.NamedTuple("DeviationUnit", [('argument', float), ('abs_deviation', float), ('percent', float)])

class Deviations:
    def __init__(self):
        self.values = dict[int, list[float]]()
