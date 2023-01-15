import enum
import re
import collections
import functools
import tqdm


Token = collections.namedtuple("Token", ["type", "value", "pos"])


class TokenType(enum.Enum):
    _ignore_ = ("__ignored_tokens__",)

    @classmethod
    @property
    @functools.cache
    def regex(cls) -> re.Pattern:  # noqa
        return re.compile(
                r"|".join(f"(?P<{rule.name}>{rule.value})" for rule in cls if rule.value),
        )

    @classmethod
    @functools.cache
    def lex_tokens(cls, code: str) -> list[Token]:
        tokens = []
        ignores = getattr(cls, "__ignored_tokens__", ())
        for match in tqdm.tqdm(
                re.finditer(  # noqa
                    cls.regex,
                    code.strip(),
                ),
                desc = "Lexing",
                total = len(code),

        ):
            if match.lastgroup not in ignores:
                tokens.append(
                        Token(
                                type = match.lastgroup,
                                value = match.group(),
                                pos = match.span(),
                        )
                )
        return tokens

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}(r{self.value})"

    def __hash__(self):
        return hash(self.value if self.value else self.name)

