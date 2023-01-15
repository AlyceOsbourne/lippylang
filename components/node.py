import json


class Node:
    """This is the Node of the tree, it has a value and a list of children"""

    def __init__(self, *children: "Node", parent: "Node" = None, **data: object):
        self.children = set(children)
        self.parent = parent
        self.__dict__.update(data)
        self._added_data = list(data.keys())

    def __str__(self, *, depth=0, last=True, prefix="", root=True):
        return (
            prefix
            + (
                ("\x1b[1;32m└── \x1b[0m" if last else "\x1b[1;32m├── \x1b[0m")
                if not root
                else ""
            )
            + (
                "\x1b[1;31m"
                if not self.parent
                else "\x1b[1;33m"
                if self.children
                else "\x1b[1;34m"
            )
            + self.__repr__()
            + "\x1b[0m"
            + "\n"
            + "".join(
                child.__str__(
                    depth=depth + 1,
                    last=i == len(self.children) - 1,
                    prefix=prefix + ("    " if last else "│   "),
                    root=False,
                )
                for i, child in enumerate(self.children)
            )
        )

    def __repr__(self):
        return f"Node({self.data})"

    def __eq__(self, other):
        return self.data == other.data and self.children == other.children

    def __hash__(self):
        return hash((self.data, self.children))

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if hasattr(self, "_parent") and getattr(self, "_parent") is not None:
            self._parent.children.remove(self)
        self._parent = parent
        if self.parent:
            self.parent.children.add(self)

    @property
    def root(self):
        if self.parent:
            return self.parent.root
        return self

    @property
    def data(self):
        return {k: v for k, v in self.__dict__.items() if k in self._added_data}

    def extend(self, other):
        if isinstance(other, Node):
            other.parent = self
        elif isinstance(other, (list, tuple)):
            for child in other:
                self.extend(child)
        else:
            raise TypeError("Can only extend with Node, list or tuple")

    def delete(self):
        for child in self.children:
            child.delete()
        self.parent = None
        del self

    def to_dict(self):
        return {
            **self.data,
            "children": [child.to_dict() for child in self.children],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_json(cls, data):
        return cls.from_dict(json.loads(data))

    @classmethod
    def new_subtype(cls, name, **data):
        # is basically here for when you want subtypes for type checking,
        # but don't need to change any of the properties
        return type(name, (cls,), data)
