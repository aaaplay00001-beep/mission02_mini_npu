def normalize_label(raw):
    """여러 표기를 표준 라벨(Cross, X)로 통일한다. 모르는 값이면 None."""
    text = str(raw).strip().lower()
    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"
    return None


print(normalize_label("+"))
print(normalize_label("cross"))
print(normalize_label("x"))
print(normalize_label("X"))
print(normalize_label(" Cross "))
print(normalize_label("abc"))