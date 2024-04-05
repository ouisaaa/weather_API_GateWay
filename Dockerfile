FROM python: 3.9
LABEL authors="uhweng_"

#앱 디렉터리 생성
WORKDIR ./api_app

#앱 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

#앱소스 코드를 복사
COPY ./ ./

#명령문 삽입
CMD ["python ./py/app.py"]