class UnionOptionsOptions:
    def __init__(self, primary: bool, deprecated: bool, implicit: bool):
        self.primary = primary
        self.deprecated = deprecated
        self.implicit = implicit


class UnionOptions:

    def __init__(self, options: UnionOptionsOptions):
        self.options = options

    def is_primary(self):
        return self.options.primary

    def is_deprecated(self):
        return self.options.deprecated

    def is_implicit(self):
        return self.options.implicit
