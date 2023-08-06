class InvalidAttribute(Exception):
    def __init__(self, tag, attr, allowed=None):
        self.tag = tag
        self.attr = attr
        self.allowed = allowed

    def __str__(self):
        r = f"The following attribute: {self.attr} isn't valid for {self.tag}."
        if not self.allowed:
            return r
        else:
            r += f"Please use one of the following: {self.allowed}"


class MissingAttribute(Exception):
    def __init__(self, tag, attr):
        self.t = tag
        self.a = attr

    def __str__(self):
        return f"{tag} is missing the {attr} attribute"
