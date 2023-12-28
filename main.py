from cli import main_loop
from contentBasedRecomendationSystem.closeness_strategy import ClosenessStrategy
from contentBasedRecomendationSystem.recomendattion_system import RecommendationSystem
from measure_worker import calculate_measure_using_cosine_distance


def main():
    likes = []
    dislikes = []

    recommendation_system = RecommendationSystem()
    recommendation_system.set_closeness_strategy(ClosenessStrategy.NearDistinctSeeds)
    recommendation_system.calculate_measure_func(calculate_measure_using_cosine_distance)

    while True:
        rc = main_loop(recommendation_system, likes, dislikes)
        if rc == 1:
            return 0


if __name__ == '__main__':
    main()
