try:
    from tiramisu.i18n import _
except ModuleNotFoundError:
    # FIXME
    def _(val):
        return val
