import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("최상위 이름표:", list(data.keys()))
print("필터 크기들:", list(data["filters"].keys()))
print("패턴 이름들:", list(data["patterns"].keys()))

p = data["patterns"]["size_5_1"]
print("size_5_1 의 expected:", p["expected"])
print("size_5_1 의 크기:", len(p["input"]), "x", len(p["input"][0]))

cross5 = data["filters"]["size_5"]["cross"]
print("5x5 십자가 필터:", cross5)