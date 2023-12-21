from enum import Enum


class ClosenessStrategy(Enum):
    # search in the vicinity of the records received from the user.
    NearDistinctSeeds = 1
    # search in the vicinity of the center of the records received from the user.
    NearGeneralCenter = 2