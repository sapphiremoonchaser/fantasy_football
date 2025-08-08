from typing import NamedTuple

from pandas import DataFrame


class AllDataFrames(NamedTuple):
    """This is a named tuple class that
       stores all the data frames from all
       sources.

       Note: This is used as a return type for
             some functions.
    """

    name_of_source_1: DataFrame
    name_of_source_2: DataFrame
    name_of_source_n: DataFrame