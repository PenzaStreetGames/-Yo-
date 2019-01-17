key_words = ["while", "if", "else", "break", "continue", "none", "true",
             "false", "not", "and", "or", "xor"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", "|", ">", "<", "?"]
sign_combos = ["=?"]
quotes = ["'", '"']
comment = "#"
space, empty = " ", ""

groups = {
    "punctuation": [",", ";", "\n", "{", "}", ":", ")", "]"],
    "math": ["+", "-", "*", "/", "%"],
    "comparison": [">", "=?", "<"],
    "logic": ["not", "and", "or", "xor"],
    "equating": ["="],
    "structure_words": ["if", "else", "while", "break", "continue"],
    "logic_values": ["true", "false"]
}

group_priority = {
    "object": 1,
    "expression": 2,
    "sub_object": 3,
    "call": 4,
    "math": 5,
    "comparison": 6,
    "logic": 7,
    "equating": 8,
    "punctuation": 9,
    "key_word": 10,
    "indent": 99,
    "program": 100
}

priority = {
    "object":
    {
        "name": 1,
        "none": 1,
        "logic": 1,
        "number": 1,
        "string": 1,
        "list": 1
    },
    "expression":
    {
        "(": 1
    },
    "sub_object":
    {
        "[": 1
    },
    "call":
    {
        "(": 1
    },
    "math":
    {
        "+": 3,
        "-": 3,
        "*": 2,
        "/": 2,
        "%": 2,
        "~": 1
    },
    "comparison":
    {
        "=?": 1,
        ">": 1,
        "<": 1,
    },
    "logic":
    {
        "not": 1,
        "and": 2,
        "or": 3,
        "xor": 3
    },
    "equating":
    {
        "=": 1
    },
    "punctuation":
    {
        ",": 1,
        ";": 1,
        ":": 1,
        ")": 1,
        "]": 1,
        "{": 1,
        "}": 1,
        "\n": 1
    },
    "key_word":
    {
        "while": 1,
        "if": 1
    },
    "indent":
    {
        "indent": 1
    },
    "program":
    {
        "program": 1
    }
}

args_number = {
    "object":
    {
        "name": "no",
        "none": "no",
        "logic": "no",
        "number": "no",
        "string": "no",
        "list": "many"
    },
    "expression":
    {
        "(": "many"
    },
    "sub_object":
    {
        "[": "binary"
    },
    "call":
    {
        "(": "binary"
    },
    "math":
    {
        "+": "binary",
        "-": "binary",
        "*": "binary",
        "/": "binary",
        "%": "binary"
    },
    "comparison":
    {
        "=?": "binary",
        ">": "binary",
        "<": "binary"
    },
    "logic":
    {
        "not": "unary",
        "and": "binary",
        "or": "binary",
        "xor": "binary"
    },
    "equating":
    {
        "=": "binary"
    },
    "punctuation":
    {
        ",": 1,
        ";": 1,
        ":": 1,
        ")": 1,
        "]": 1,
        "{": 1,
        "}": 1,
        "\n": 1
    },
    "key_word":
    {
        "while": 1,
        "if": 1
    },
    "indent":
    {
        "indent": "no"
    },
    "program":
    {
        "program": "many"
    }
}


class TokenError(Exception):
    pass


class YoSyntaxError(Exception):
    pass


class YoObject:

    def __init__(self, parent, func):
        self.parent = parent
        self.func = func
        self.args = []
        self.priority = [group_priority[func["group"]],
                         priority[func["group"]][func["sub_group"]]]
        self.name = func["name"]
        self.sub_group = func["sub_group"]
        self.group = func["group"]
        self.args_number = args_number[self.group][self.sub_group]
        self.commas, self.points = get_punctuation(self)
        self.close = False
        self.indent = 0
        self.indent_depend = True

    def check_close(self):
        if self.args_number == "no":
            self.close = True
        elif self.args_number == "unary":
            if len(self.args) == 1:
                self.close = True
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "binary" or self.args_number == "binary_right":
            if len(self.args) == 2:
                self.close = True
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "many":
            self.close = True

    def __str__(self):
        if self.sub_group == self.name:
            return f"{self.group} \"{self.name}\" {self.priority}"
        else:
            return f"{self.sub_group} \"{self.name}\" {self.priority}"

    def __repr__(self):
        return self.__str__()


def translate(program):
    # token_split
    pre_symbol, word, pre_group, quote = "", "", "", ""
    result = []
    result += [YoObject(None, {"group": "program", "sub_group": "program",
                               "name": "program"})]

    def add_word(word, result):
        if word != empty:
            obj = token_analise(word, result)
            result += [obj]
        return "", result

    for symbol in program:
        if symbol == comment:
            if pre_group != "comment":
                if quote == empty:
                    word, result = add_word(word, result)
                    pre_group = "comment"
                else:
                    word += symbol
        elif symbol in ["\n", "\r"]:
            if pre_group != "line feed" and word:
                word, result = add_word(word, result)
                word += symbol
                pre_group = "line feed"
        elif pre_group == "comment":
            pass
        elif symbol in quotes:
            if quote == empty:
                word, result = add_word(word, result)
                quote = symbol
                pre_group = "quote"
            elif symbol == quote:
                if pre_symbol != "\\":
                    quote = ""
            word += symbol
        elif quote != empty:
            word += symbol
        elif symbol == space:
            if pre_group == "line feed":
                if pre_symbol in ["\n", "\r"]:
                    word, result = add_word(word, result)
                word += symbol
            elif pre_group != "space":
                word, result = add_word(word, result)
                pre_group = "space"
            else:
                pass
        elif symbol in signs:
            if not(pre_group == "sign" and word + symbol in sign_combos):
                word, result = add_word(word, result)
            pre_group = "sign"
            word += symbol
        elif symbol.isalpha():
            if pre_group in ["sign", "line feed"]:
                word, result = add_word(word, result)
            pre_group = "alpha"
            word += symbol
        elif symbol.isdigit():
            if pre_group in ["sign", "line feed"]:
                word, result = add_word(word, result)
            pre_group = "digit"
            word += symbol
        else:
            raise TokenError(f"Неизвестный символ \"{symbol}\"")
        pre_symbol = symbol
    add_word(word, result)

    return result


def token_analise(token, tokens):
    group, sub_group = "", ""

    def is_close(pre_token):
        return pre_token.close and pre_token.group in ["sub_object", "call",
                                                       "object", "expression"]

    pre_token = tokens[-1]
    if token.startswith(space):
        group = "indent"
        sub_group = "indent"
    elif token in groups["math"]:
        group = "math"
        if token == "-":
            if is_close(pre_token):
                sub_group = "-"
            else:
                sub_group = "~"
    elif token in groups["comparison"]:
        group = "comparison"
    elif token in groups["logic"]:
        group = "logic"
    elif token in groups["structure_words"]:
        group = "key_word"
    elif token in groups["punctuation"]:
        group = "punctuation"
    elif token == "=":
        group = "equating"
    elif token == "[":
        if is_close(pre_token):
            group = "sub_object"
        else:
            group = "object"
            sub_group = "list"
    elif token == "(":
        if is_close(pre_token):
            group = "call"
        else:
            group = "expression"
    elif token[0] in quotes:
        group = "object"
        sub_group = "string"
    elif token.isdigit():
        group = "object"
        sub_group = "number"
    elif token in groups["logic_values"]:
        group = "object"
        sub_group = "logic"
    elif token == "none":
        group = "object"
        sub_group = "none"
    elif token[0].isalpha():
        group = "object"
        sub_group = "name"
    else:
        raise TokenError(f"Неизвестный токен {token}")
    if sub_group == empty:
        sub_group = token
    func = {"group": group, "sub_group": sub_group, "name": token}
    obj = YoObject(pre_token, func)

    return obj


def get_punctuation(yo_object):
    if yo_object.group == "program":
        return [";", "\n"], ["}"]
    elif yo_object.group == "key_word":
        return [":", "{"], ["}"]
    elif yo_object.group == "list":
        return [","], ["]"]
    elif yo_object.group == "call":
        return [","], [")"]
    elif yo_object.group == "expression":
        return [], [")"]
    elif yo_object.group == "sub_object":
        return [], ["]"]
    else:
        return [], []


def syntax_analise(yo_object, result):
    pass


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        objects = []
        result = translate(infile.read())
    print(result)