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
    NUMBER = r"(\d+(\.\d+)?([eE][+-]?\d+)?([jJ])?)"
    STRING = r"(\"[^\"]*\")"
    IDENTIFIER = r"[a-zA-Z0-9_][a-zA-Z0-9_]*"
    BRACKET = r"[\[\]\(\)\{\}]"
    PUNCTUATION = r"[,;]"
    OPERATOR = r"(\+|-|\*|/|%|&|\||\^|~|<<|>>|>>>|&&|\|\||!|==|!=|<=|>=|<|>)"
    WHITESPACE = r"\s+"


def program(file_path = "<stdin>", **kwargs):
    kwargs.update({'file_path': file_path})
    return type("Program", (node.Node,), kwargs)
