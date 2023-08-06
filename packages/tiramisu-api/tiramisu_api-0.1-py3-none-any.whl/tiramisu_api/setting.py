try:
    from tiramisu.setting import undefined
except ModuleNotFoundError:
    class Undefined(object):
        def __str__(self):
            return 'Undefined'

        __repr__ = __str__


    undefined = Undefined()
