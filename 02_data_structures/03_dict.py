"""
    딕셔너리 (dict)
"""

# JSON 형식과 유사한 구조
# key-value 형태로 데이터를 관리

user = {
    "name": "이우진",
    "age" : "20",
    "skills" : ["Java","sql","html/css","js","python"]
}

print(f"user : {user}")
# 딕셔너리 내의 데이터 접근 -> 키값 사용
print(f"이름 : {user['name']}")
print(f"스킬 : {user['skills']}")

# print(f"연락처 : {user['phone']}")
# 직접 접근 시 존재하지 않는 키값은 오류가 발생!
print()
# get() 사용하여 접근
print(f"이름 : {user.get('name')} ")
print(f"스킬 : {user.get('skills')}")

print(f"연락처 : {user.get('phone')}")  
# 존재하지 않는 키값인 경우 None 반환
# get 메소드 사용시 간접 접근으로 오류가 나지 않음 None 반환
print(f"연락처 : {user.get('phone', '없음')}")  # 기본값 지정 가능
print()

# 변경 (추가/수정/삭제)
user['email'] = 'email@test.com'    # 새로운 키값을 지정하면 추가
print(f"user - {user}")

user['age'] = 40                    # 기존의 키값을 지정하면 변경
print(f"user - {user}")

del user['age']                     
print(f"user - {user}")             
"""
del user['phone']                   # 없는 키값을 삭제 지정하면 오류!
print(f"user - {user}")
"""
print()
print("="*60)

# ------------------------------------------------------------
# 탐색
# ------------------------------------------------------------
# 딕셔너리를 for 로 돌면 "키"가 나온다
for key in user:
    print(f"key: {key} / value: {user[key]}")

print()

# items() : 키와 값을 한 번에 꺼낸다
for k, v in user.items():
    print(f"key: {k} / value: {v}")

print()

# 키 목록 / 값 목록만 뽑기
print(f"키 목록 : {list(user.keys())}")
print(f"값 목록 : {list(user.values())}")
print(f"길이   : {len(user)}")

# 키 존재 여부 확인
print(f"name 키가 있나? {'name' in user}")
print(f"phone 키가 있나? {'phone' in user}")

print(f"키 목록 : {list(user.keys())}")
print(f"밸류 목록 : {list(user.values())}")
print(f"itmes() : {list(user.items())}")

