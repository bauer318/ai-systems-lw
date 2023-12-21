from enum import Enum


class RecommendationStrategy(Enum):
    # Do recommendation before filtration
    RecommendFilter = 1
    # Filter before recommendation
    FilterRecommend = 2
