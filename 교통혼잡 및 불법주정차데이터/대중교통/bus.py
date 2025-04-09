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
file_path_bus = os.getenv('FiLE_PATH_bus')

# 연도별 파일 리스트 딕셔너리 초기화
file_lists = {year: [] for year in ['2022', '2023', '2024', '2025']}
file_path_2021 = None  # 그 외 파일 (2021)

# 폴더 내 모든 파일 확인
for root, dirs, files in os.walk(file_path_bus):
    for file in files:
        full_path = os.path.join(root, file)
        added = False
        for year in file_lists:
            if year in full_path:
                file_lists[year].append(full_path)
                added = True
                break
        if not added:
            file_path_2021 = full_path

# 연도별 파일 데이터 저장용 딕셔너리
file_data = {year: {} for year in ['2022', '2023', '2024', '2025']}

# 파일 읽기
for year in ['2022', '2023', '2024']:
    for idx, path in enumerate(file_lists[year]):
        file_data[year][idx] = pd.read_csv(path, encoding='euc-kr', low_memory=False)

# 2025는 따로 처리
for idx, path in enumerate(file_lists['2025']):
    file_data['2025'][idx] = pd.read_csv(path, encoding='euc-kr', low_memory=False)

# 병합된 데이터프레임 생성
df_combined = {}
df_combined['2021'] = pd.read_csv(file_path_2021, encoding='euc-kr', low_memory=False)
df_combined['2022'] = pd.concat(file_data['2022'].values(), ignore_index=True)
df_combined['2023'] = pd.concat(file_data['2023'].values(), ignore_index=True)
df_combined['2024'] = pd.concat(file_data['2024'].values(), ignore_index=True)
df_combined['2025'] = pd.concat(file_data['2025'].values(), ignore_index=True)

df_all_years = pd.concat(df_combined.values(), ignore_index=True)

# 데이터프레임 시간별 목록
time_list2 = df_all_years.columns[6:54]

# 시간대별 열 그룹화
one = [col for col in time_list2 if "1시" in col or "2시" in col or "3시" in col]
two = [col for col in time_list2 if "4시" in col or "5시" in col or "6시" in col]
three = [col for col in time_list2 if "7시" in col or "8시" in col or "9시" in col]
four = [col for col in time_list2 if "10시" in col or "11시" in col or "12시" in col]
five = [col for col in time_list2 if "13시" in col or "14시" in col or "15시" in col]
six = [col for col in time_list2 if "16시" in col or "17시" in col or "18시" in col]
seven = [col for col in time_list2 if "19시" in col or "20시" in col or "21시" in col]
eight = [col for col in time_list2 if "22시" in col or "23시" in col or "00시" in col]
# 시간대별 합계 계산
time_sums2 = [
    sum(df_all_years[one].sum(axis=1)),    # 00-03시
    sum(df_all_years[two].sum(axis=1)),    # 03-06시
    sum(df_all_years[three].sum(axis=1)),  # 06-09시
    sum(df_all_years[four].sum(axis=1)),   # 09-12시
    sum(df_all_years[five].sum(axis=1)),   # 12-15시
    sum(df_all_years[six].sum(axis=1)),    # 15-18시
    sum(df_all_years[seven].sum(axis=1)),  # 18-21시
    sum(df_all_years[eight].sum(axis=1)),  # 21-24시
]

# 시간대 라벨
time_labels = [
    "00-03시", "03-06시", "06-09시", "09-12시",
    "12-15시", "15-18시", "18-21시", "21-24시"
]

x_raw = np.linspace(0, 24, 8)
y_raw = time_sums2

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
plt.title("시간대별 승차/하차 합계 (곡선형)", fontsize=15)
plt.xlabel("시간대", fontsize=12)
plt.ylabel("총 인원 수", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

plt.show()