import time


def mac(pattern, filt):
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def make_matrix(n):
    """측정용으로 n x n 크기의 숫자표를 만든다 (값은 전부 1.0)."""
    return [[1.0] * n for _ in range(n)]


def measure(n, repeat=10):
    """n x n MAC 연산을 repeat번 재서 평균 시간(ms)을 돌려준다."""
    pattern = make_matrix(n)
    filt = make_matrix(n)

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        end = time.perf_counter()
        times.append((end - start) * 1000)   # 초 -> 밀리초(ms)

    return sum(times) / len(times)


print("크기        평균 시간(ms)    연산 횟수")
print("-" * 40)
for n in (3, 5, 13, 25):
    avg = measure(n)
    print(f"{n}x{n}".ljust(10), f"{avg:.4f}".rjust(12), str(n * n).rjust(12))