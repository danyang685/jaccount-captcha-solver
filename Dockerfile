FROM python:3.8-slim
WORKDIR /root

COPY ./requirements.txt ./
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
COPY ./ app/

EXPOSE 8080

CMD cd app && gunicorn -w 4 -b :8080 online:app