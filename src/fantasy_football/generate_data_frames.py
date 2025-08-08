import nfl_data_py as nfl
from fantasy_football.data.named_tuple.all_data_frames import AllDataFrames
from fantasy_football.data.named_tuple.qb_data_frames import QbDataFrames


def create_all_dfs() -> AllDataFrames:
    """This function creates an instance of the
       AllDataFrames class, which stores all the
       data frames from all the sources.
    :return: AllDataFrames
    """

    # Todo: Add code that uses different sources and
    # Todo: creates the data frames.
    # Todo: Note: The number of dataframes should match the
    # Todo: AllDataFrames class, if not update the class.

    return AllDataFrames(
        # Todo: Fill this in
    )


def filter_dfs_for_qbs(
    all_data_frames: AllDataFrames,
) -> QbDataFrames:
    """This function filters down all the data in all
       the data frames to just be data about Qbs.

    :param all_data_frames: AllDataFrames
    :return: QbDataFrames
    """

    # Todo: Add code here to do the filtering.
    # Todo: Note: The "all_data_frames", the AllDataFrames instance is also a
    # Todo:       tuple. Therefore, you can use a for loop on it, if that makes
    # Todo:       it easier.

    return QbDataFrames(
        # Todo: Fill this in
    )