FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
# ローカルのdefault.confをコンテナにコピー
COPY ./docker_nginx/nginx/nginx.conf /etc/nginx/conf.d/kuni-example.com.conf
# EC2環境でbuild時vimがない
RUN apt-get update && apt-get -y install vim
