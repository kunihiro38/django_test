# Python3のイメージを基にする
FROM python:3.8
ENV PYTHONUNBUFFERED 1

# 存在していなければ作成される
WORKDIR /usr/src/app

# 左がローカルからコピーするファイルで、右がWORKDIRにコピーされるファイル
COPY ./requirements.txt /usr/src/app/requirements.txt

# requirements.txt のインストールコマンド
RUN pip3 install -r requirements.txt
