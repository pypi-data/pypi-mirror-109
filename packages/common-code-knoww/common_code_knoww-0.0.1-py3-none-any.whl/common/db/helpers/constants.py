import enum


# noinspection PyTypeChecker
class BaseChoices(enum.Enum):
    @staticmethod
    def values(elements):
        return [e.value for e in elements]

    def __str__(self):
        return self.value

    @classmethod
    def values_list(cls):
        return cls.values(list(cls))

    @classmethod
    def name_list(cls):
        return [e.name for e in list(cls)]

    @classmethod
    def item_dict(cls):
        return {e.name: e.value for e in list(cls)}


class Connections(BaseChoices):
    THIRD_DEGREE = '3rdDegree'
    SECOND_DEGREE = '2ndDegree'
    NONE = 'none'
