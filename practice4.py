import json


def mac(pattern, filt):
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def normalize_label(raw):
    text = str(raw).strip().lower()
    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"
    return None


def judge(score_cross, score_x):
    if abs(score_cross - score_x) < 1e-9:
        return "UNDECIDED"
    if score_cross > score_x:
        return "Cross"
    return "X"


def get_size(key):
    """'size_13_1' 에서 13 을 꺼낸다. 실패하면 None."""
    parts = key.split("_")
    if len(parts) >= 2 and parts[1].isdigit():
        return int(parts[1])
    return None


def load_filters(data, size):
    """size 에 맞는 필터를 표준 라벨(Cross, X)로 바꿔서 돌려준다."""
    raw = data["filters"]["size_" + str(size)]
    result = {}
    for name, matrix in raw.items():
        label = normalize_label(name)
        if label is not None:
            result[label] = matrix
    return result


with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = 0
passed = 0
failed = []

for key, item in data["patterns"].items():
    total += 1
    print("---", key, "---")

    size = get_size(key)
    pattern = item["input"]
    expected = normalize_label(item["expected"])

    # 검증 1: 크기를 키에서 못 꺼냈거나 필터가 없는 경우
    if size is None or ("size_" + str(size)) not in data["filters"]:
        print("FAIL: 해당 크기의 필터를 찾을 수 없음")
        failed.append((key, "필터 없음"))
        continue

    filters = load_filters(data, size)

    # 검증 2: 패턴이 size x size 가 맞는지
    if len(pattern) != size or any(len(row) != size for row in pattern):
        print("FAIL: 패턴 크기 불일치")
        failed.append((key, "크기 불일치"))
        continue

    score_cross = mac(pattern, filters["Cross"])
    score_x = mac(pattern, filters["X"])
    result = judge(score_cross, score_x)

    print("Cross 점수:", score_cross)
    print("X 점수:", score_x)

    if result == expected:
        print("판정:", result, "| expected:", expected, "| PASS")
        passed += 1
    else:
        print("판정:", result, "| expected:", expected, "| FAIL")
        failed.append((key, "판정 " + result + " != expected " + str(expected)))

print()
print("총 테스트:", total)
print("통과:", passed)
print("실패:", len(failed))
for key, reason in failed:
    print("-", key, ":", reason)
    