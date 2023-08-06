"""
@Author Jay Lee
Here, we will get funky with decorators
and learn to handle decorating class methods
and or functions
"""
import typing as t
from functools import wraps
from src.decko.decorators import _handle_decorator_kwargs, freeze


@freeze
class RandomClass:
    def __init__(self, a_tuple):
        self.a_tuple = a_tuple


@freeze
def random_func(item):
    print(f"Here is a random function: {item}")


if __name__ == "__main__":
    # cls_instance = RandomClass((1, 2, 3))
    # print(cls_instance)
    #
    # # Frozen class should not be able to mutate existing properties
    # cls_instance.a_tuple = 100
    random_func(10)
