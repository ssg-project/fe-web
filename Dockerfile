# python 버전 선택
FROM --platform=linux/amd64 python:3.9.19

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY . /app/

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 컨테이너 포트 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
