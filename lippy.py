import re
import abc
from components import tokenizer, node

keywords = (
        "var",  # variable
        "const",  # constant
        "fn",  # function
        "return",  # return value
)
single_line_comment_chars = ("//",)


class LippyTokens(tokenizer.TokenType):
    __ignored_tokens__ = ("WHITESPACE", "COMMENT")
    COMMENT = rf"({'|'.join((re.escape(c) for c in single_line_comment_chars))}).*" if single_line_comment_chars else ''  # noqa
    KEYWORD = rf"({'|'.join((re.escape(k) for k in keywords))})(?=\s|$)" if keywords else ''  # noqa
    NUMBER = r"(\d+(\.\d+)?)"
    STRING = r"(\"[^\"]*\")"
    IDENTIFIER = r"[a-zA-Z0-9_][a-zA-Z0-9_]*"
    BRACKET = r"[\[\]\(\)\{\}]"
    PUNCTUATION = r"[,;]"
    OPERATOR = r"(\+|-|\*|/|%|&|\||\^|~|<<|>>|>>>|&&|\|\||!|==|!=|<=|>=|<|>)"
    WHITESPACE = r"\s+"


class ASTNode(node.Node, metaclass = abc.ABCMeta): ...


class Statement(ASTNode, metaclass = abc.ABCMeta): ...


class Expression(ASTNode, metaclass = abc.ABCMeta): ...


class Program(ASTNode):
    def __init__(self, *body):
        super().__init__(children = body)


if __name__ == "__main__":
    with open("test.lippy") as f:
        code = f.read()
    tokens = LippyTokens.lex_tokens(code)
    for token in tokens:
        print(token)

