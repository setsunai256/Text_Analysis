import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def normalize_word(word: str) -> str:
    return morph.parse(word)[0].normal_form


def normalize_list(words: list[str]) -> list[str]:
    return list(set(normalize_word(w) for w in words))