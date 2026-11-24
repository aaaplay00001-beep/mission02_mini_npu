line = input("한 줄 입력: ")
print("입력한 글자:", line)

parts = line.split()
print("공백으로 쪼갠 결과:", parts)

numbers = []
for p in parts:
    numbers.append(float(p))
print("숫자로 바꾼 결과:", numbers)