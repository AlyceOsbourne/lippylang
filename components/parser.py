from . import node, tokenizer


class Parser:
    def __init__(self, /, *, tokens: list[tokenizer.Token], root: node.Node):
        self.tokens = tokens
        self.token_index = 0
        self.root = root
        self.stack = []

    @property
    def current_token(self) -> tokenizer.Token:
        return self.tokens[self.token_index]

    @property
    def next_token(self) -> tokenizer.Token:
        return self.tokens[self.token_index + 1]

    def advance(self) -> tokenizer.Token:
        self.token_index += 1
        return self.current_token

    def expect(self, *types: str, value_predicate = None) -> bool:
        if self.current_token.type in types:
            if value_predicate is None or value_predicate(self.current_token.value):
                return True
        return False

    def parse(self) -> node.Node:
        raise NotImplementedError

    def add_to_stack(self, node: node.Node):
        self.stack.append(node)

    def pop_from_stack(self) -> node.Node:
        return self.stack.pop()

    def eof(self) -> bool:
        return self.token_index == len(self.tokens) - 1

    def has_failed(self) -> bool:
        return self.eof() and self.stack

    def __str__(self):
        return f"{self.__class__.__name__}({self.root})"

