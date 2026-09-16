"""
    Numpy 연습 - 학생 점수 분석
"""
import numpy as np

# 학생 5명  x 3과목 (국어,영어,수학)
scores = np.array([[90, 80, 70],
                   [60, 100, 80],
                   [50, 40, 30],
                   [100, 95, 90],
                   [70, 65, 60],
])

print(scores)
print(f"shape :{scores.shape}")

student_avg = scores.mean(axis=1)
print(f"학생별 평균 : {student_avg}")

subject_avg = scores.mean(axis=0)
print(f"과목별 평균 : {subject_avg}")

passed = student_avg >= 60
print(f"통과 여부 : {passed}")
print(f"통과 인원 : {passed.sum()}명")

print("="*60)

# 2번 학생의 영어 점수가 없는 경우
scores2 = scores.astype(float)    # nan 을 담으려면 실수 배열이어야 함
scores2[1,1] = np.nan

print(scores2)
print(f"학생별 평균 : {scores2.mean(axis=1)}")

avg2 =scores2.mean(axis=1)
print(f"통과인원 :{(avg2 >= 60).sum()}명")
print(f"전체 평균 : {avg2.mean()}")

print("="*60)

avg3 = np.nanmean(scores2, axis=1)
print(f"학생별 평균(nan 무시) : {avg3}")

print(f"통과 인원: {(avg3 >= 60).sum()}명")
print(f"전체 평균 : {avg3.mean()}")

