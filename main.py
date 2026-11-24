import json
import time

EPSILON = 1e-9


# ---------- 핵심 연산 ----------
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
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    if score_cross > score_x:
        return "Cross"
    return "X"


# ---------- 성능 측정 ----------
def make_matrix(n):
    return [[1.0] * n for _ in range(n)]


def measure(n, repeat=10):
    pattern = make_matrix(n)
    filt = make_matrix(n)
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def print_performance(sizes):
    print("크기        평균 시간(ms)    연산 횟수")
    print("-" * 40)
    for n in sizes:
        avg = measure(n)
        print(f"{n}x{n}".ljust(10), f"{avg:.4f}".rjust(12), str(n * n).rjust(12))


# ---------- 모드 1: 사용자 입력 (3x3) ----------
def read_matrix(name):
    while True:
        print(name + " (3줄 입력, 공백 구분)")
        matrix = []
        try:
            for _ in range(3):
                parts = input().split()
                if len(parts) != 3:
                    raise ValueError
                matrix.append([float(p) for p in parts])
            return matrix
        except ValueError:
            print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")


def run_mode1():
    print()
    print("# [1] 필터 입력")
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")
    print()
    print("# [2] 패턴 입력")
    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    print()
    print("# [3] MAC 결과")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    if abs(score_a - score_b) < EPSILON:
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    elif score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")

    print()
    print("# [4] 성능 분석 (평균/10회)")
    print_performance([3])


# ---------- 모드 2: data.json 분석 ----------
def get_size(key):
    parts = key.split("_")
    if len(parts) >= 2 and parts[1].isdigit():
        return int(parts[1])
    return None


def load_filters(data, size):
    raw = data["filters"]["size_" + str(size)]
    result = {}
    for name, matrix in raw.items():
        label = normalize_label(name)
        if label is not None:
            result[label] = matrix
    return result


def run_mode2():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("data.json 을 읽을 수 없습니다:", e)
        return

    print()
    print("# [1] 필터 로드")
    for size_key in data["filters"]:
        print("✓", size_key, "필터 로드 완료")

    print()
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    total = 0
    passed = 0
    failed = []

    for key, item in data["patterns"].items():
        total += 1
        print("---", key, "---")

        size = get_size(key)
        pattern = item["input"]
        expected = normalize_label(item["expected"])

        if size is None or ("size_" + str(size)) not in data["filters"]:
            print("FAIL: 해당 크기의 필터를 찾을 수 없음")
            failed.append((key, "필터 없음"))
            continue

        filters = load_filters(data, size)

        if "Cross" not in filters or "X" not in filters:
            print("FAIL: Cross/X 필터가 모두 있어야 함")
            failed.append((key, "필터 라벨 오류"))
            continue

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
    print("# [3] 성능 분석 (평균/10회)")
    print_performance([3, 5, 13, 25])

    print()
    print("# [4] 결과 요약")
    print("총 테스트:", total)
    print("통과:", passed)
    print("실패:", len(failed))
    if failed:
        print("실패 케이스:")
        for key, reason in failed:
            print("-", key, ":", reason)


# ---------- 메뉴 ----------
def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ").strip()

    if choice == "1":
        run_mode1()
    elif choice == "2":
        run_mode2()
    else:
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()