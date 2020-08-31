"""`Factory` providers - building a complex object graph with deep init injections example."""

from dependency_injector import providers


class Regularizer:
    def __init__(self, alpha: float):
        self.alpha = alpha


class Loss:
    def __init__(self, regularizer: Regularizer):
        self.regularizer = regularizer


class ClassificationTask:
    def __init__(self, loss: Loss):
        self.loss = loss


class Algorithm:
    def __init__(self, task: ClassificationTask):
        self.task = task


algorithm_factory = providers.Factory(
    Algorithm,
    task=providers.Factory(
        ClassificationTask,
        loss=providers.Factory(
            Loss,
            regularizer=providers.Factory(
                Regularizer,
            ),
        ),
    ),
)


if __name__ == '__main__':
    algorithm_1 = algorithm_factory(task__loss__regularizer__alpha=0.5)
    assert algorithm_1.task.loss.regularizer.alpha == 0.5

    algorithm_2 = algorithm_factory(task__loss__regularizer__alpha=0.7)
    assert algorithm_2.task.loss.regularizer.alpha == 0.7

    algorithm_3 = algorithm_factory(task__loss__regularizer=Regularizer(alpha=0.8))
    assert algorithm_3.task.loss.regularizer.alpha == 0.8
