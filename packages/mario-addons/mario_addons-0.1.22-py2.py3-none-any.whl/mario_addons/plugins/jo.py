"""Functions for the jo command.

Inspired by https://github.com/jpmens/jo
"""

import functools

import lark

GRAMMAR = """
?start: sequence

?value: object
  | array
  | string
  | SIGNED_NUMBER      -> number
  | "true"             -> true
  | "false"            -> false
  | "null"             -> null
array  : "[" [value ("," value)*] "]"
object : "{" [pair ("," pair)*] "}"
pair   : string ":" value
string : ESCAPED_STRING

?thing : value
       | eqpair
       | eqnull
       | name_at_val
       | array_index_pair
       | object_index_pair

name : NAME
eqpair : (value|name) "=" value

eqnull : (thing | name ) "="

sequence : thing+

name_at_val : name "@" value

array_index_pair : name "[]=" thing

object_index_pair : name "[" name "]=" thing

%import common.ESCAPED_STRING
%import common.CNAME -> NAME
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

"""


@functools.lru_cache(None)
def get_parser():
    return lark.Lark(GRAMMAR, parser="lalr")


def parse(text):
    parser = get_parser()
    return parser.parse(text)


class JOTransformer(lark.Transformer):
    def name(self, arg):
        return "".join(arg)

    def number(self, arg):
        try:
            return int(arg[0])
        except ValueError:
            return float(arg[0])

    @lark.v_args(inline=True)
    def eqpair(self, k, v):

        return {k: v}

    @lark.v_args(inline=True)
    def eqnull(self, arg):
        return {arg: None}

    def array(self, arg):
        return list(arg)

    @lark.v_args(inline=True)
    def name_at_val(self, name, value):
        return {name: bool(value)}

    def sequence(self, items):
        out = {}

        for d in items:
            for k, v in d.items():
                if isinstance(v, list):
                    out.setdefault(k, []).extend(v)
                elif isinstance(v, dict):
                    out.setdefault(k, {})
                    for subk, subv in v.items():
                        out[k].setdefault(subk, {})
                        out[k][subk] = subv
                else:
                    out[k] = v

        return out

    def true(self, _arg):
        return True

    def false(self, _arg):
        return False

    @lark.v_args(inline=True)
    def array_index_pair(self, left, right):
        return {left: [right]}

    @lark.v_args(inline=True)
    def object_index_pair(self, left, middle, right):
        return {left: {middle: right}}


def main(text):
    tree = parse(text)
    return JOTransformer().transform(tree)
