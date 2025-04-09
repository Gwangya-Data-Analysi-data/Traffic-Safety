import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
from scipy.interpolate import make_interp_spline
from dotenv import load_dotenv

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")

# 환경 변수 로드
load_dotenv()
file_path_timeday = os.getenv('FiLE_PATH_timeday')
file_path_timeweek = os.getenv("FiLE_PATH_timeweek")

# CSV 파일 읽기
df_timeday = pd.read_csv(file_path_timeday, encoding='euc-kr')
df_timeweek = pd.read_csv(file_path_timeweek, encoding='euc-kr')

# 연도 리스트
years = [2020, 2021, 2022, 2023]

# 연도별 결과 저장용 딕셔너리
timeday_chunked_dict = {}
timeweek_chunked_dict = {}

for year in years:
    # === timeday 처리 ===
    df_day = df_timeday[df_timeday["year"] == year].drop('year', axis=1)
    df_day = df_day.apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sums_day = df_day.sum(axis=1)
    sliced_day = row_sums_day[1:25]
    chunked_day = [sliced_day[i:i + 3] for i in range(0, len(sliced_day), 3)]
    timeday_chunked_dict[year] = chunked_day

    # === timeweek 처리 ===
    df_week = df_timeweek[df_timeweek["year"] == year].drop('year', axis=1)
    df_week = df_week.apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sums_week = df_week.sum(axis=1)
    sliced_week = row_sums_week[1:25]
    chunked_week = [sliced_week[i:i + 3] for i in range(0, len(sliced_week), 3)]
    timeweek_chunked_dict[year] = chunked_week


sum_list = []

for chunk_idx in range(8):  # 0, 1, 2번 chunk
    total = 0
    for year in years:
        total += sum(timeweek_chunked_dict[year][chunk_idx])
        total += sum(timeday_chunked_dict[year][chunk_idx])
    sum_list.append(total)

print(sum_list)


# 시간대 라벨
time_labels = [
    "00-03시", "03-06시", "06-09시", "09-12시",
    "12-15시", "15-18시", "18-21시", "21-24시"
]

x_raw = np.linspace(0, 24, 8)
y_raw = sum_list

# 보간(스플라인) 설정
# 스플라인 범위를 구간 중앙값 최소~최대 사이로 설정
x_smooth = np.linspace(min(x_raw), max(x_raw), 300)
y_smooth = make_interp_spline(x_raw, y_raw)(x_smooth)

# 그래프 생성
plt.figure(figsize=(10, 6))

# 곡선형 라인 차트
plt.plot(x_smooth, y_smooth, color='b', label='총 승차/하차 인원', linewidth=2)

# X축 눈금: 구간 중앙값에 라벨 달기
plt.xticks(x_raw, time_labels)

# X축 범위를 0~24로 지정하면 처음/끝 구간이 더 자연스러워 보임
plt.xlim(0, 24)

# 차트 꾸미기
plt.title("시간대별 버스 승차/하차 합계 (곡선형)", fontsize=15)
plt.xlabel("시간대", fontsize=12)
plt.ylabel("총 인원 수", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

plt.show()
