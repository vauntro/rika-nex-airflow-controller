"""Minimaler S-Ausdruck-Parser/-Schreiber für KiCad-Dateien."""


class Str(str):
    """Zeichenkette, die mit Anführungszeichen geschrieben wird."""


def parse(text):
    pos = 0
    n = len(text)
    stack = [[]]
    while pos < n:
        c = text[pos]
        if c in " \t\r\n":
            pos += 1
        elif c == "(":
            stack.append([])
            pos += 1
        elif c == ")":
            top = stack.pop()
            stack[-1].append(top)
            pos += 1
        elif c == '"':
            pos += 1
            buf = []
            while text[pos] != '"':
                if text[pos] == "\\":
                    pos += 1
                    buf.append({"n": "\n", "t": "\t"}.get(text[pos], text[pos]))
                else:
                    buf.append(text[pos])
                pos += 1
            pos += 1
            stack[-1].append(Str("".join(buf)))
        else:
            start = pos
            while pos < n and text[pos] not in ' \t\r\n()"':
                pos += 1
            stack[-1].append(text[start:pos])
    return stack[0]


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def dump(node, indent=0):
    if isinstance(node, Str):
        return q(node)
    if not isinstance(node, list):
        return str(node)
    flat = all(not isinstance(x, list) or all(not isinstance(y, list) for y in x) for x in node)
    if flat and len(node) <= 6:
        return "(" + " ".join(dump(x, indent) for x in node) + ")"
    out = "("
    first = True
    for x in node:
        if isinstance(x, list):
            out += "\n" + "  " * (indent + 1) + dump(x, indent + 1)
        else:
            out += ("" if first else " ") + dump(x, indent)
        first = False
    return out + ")"


def find(node, key):
    return [x for x in node if isinstance(x, list) and x and x[0] == key]
