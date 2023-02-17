# myapp サンプルコード
# URL
http://kuni-example.com
https://kuni-example.com

## 概要
myapp のサンプルコードです。
dockerの開発環境をそのままEC2の上に乗せて、起動させて反映できるようにしています。

## サーバー環境
###  nginx


## 開発環境（local）での起動手順
Docker を開いておく
```
kuni@mbp myapp % pwd   
/Users/kuni/git/django_test/myapp
kuni@mbp myapp % docker-compose up
```
起動が確認できたら http://127.0.0.1:8000 にブラウザアクセスする。

docker-compose up -d にするとログが見れないので、オプションは up のみで起動させる。

http://127.0.0.1:8000/ にブラウザアクセスしたら nginx が、ポート80で受け取って、nginx.conf に記載したプロキシが中継して、myapp_web_1 という docker のサーバーの port8000番 に繋げる。


## 導入手順
### git clone
github からssh接続できる状態。
```
[dev@kuni-myapp-stage-web01 ~]$ pwd
/home/dev
[dev@kuni-myapp-stage-web01 ~]$ git clone git@github.com:kunihiro38/django_test
.
.
.
Resolving deltas: 100% (3/3), done.
```
### git pull
EC2 環境へ github 上のソースコードを pull する
```
[dev@kuni-myapp-stage-web01 django_test]$ pwd
/home/dev/django_test
[dev@kuni-myapp-stage-web01 django_test]$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
[dev@kuni-myapp-stage-web01 django_test]$ git pull origin main
```


### dockerのインストール
ルートユーザーで dev/django_test ディレクトリへ
```
[root@kuni-myapp-stage-web01 django_test]# pwd
/home/dev/django_test
```
インストール
```
[root@kuni-myapp-stage-web01 django_test]# yum install docker
```
起動
```
[root@kuni-myapp-stage-web01 django_test]# sudo systemctl start docker
```
dev を docker グループへ
```
[root@kuni-myapp-stage-web01 django_test]# sudo usermod -a -G docker dev
```
グループ変更後は一旦ログアウトして、再ログインすること

自動起動の設定
```
[root@kuni-myapp-stage-web01 dev]# sudo systemctl enable docker
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.
```
### docker-composeのインストール
```
[root@kuni-myapp-stage-web01 dev]# sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 12.1M  100 12.1M    0     0  27.7M      0 --:--:-- --:--:-- --:--:-- 27.7M
[root@kuni-myapp-stage-web01 dev]# sudo chmod +x /usr/local/bin/docker-compose
```
起動
```
[dev@kuni-myapp-stage-web01 django_test]$ docker-compose up -d
```
docker-compose.yml -> servicec -> web にgunicorn による自動起動のコマンドを書いている。
```
command: gunicorn config.wsgi --bind=0.0.0.0:8000
```
なので docker を起動させた時点でサーバーに反映される。


## docker-compose.yml の設定
### portsについて
nginx の ports は80を指定する。
これは、AWS -> EC2 -> セキュリティグループのインバウンドルールで、指定しているポート番号を受け入れる。
例えば、仮に8000番ポートでも、受け入れをしたい場合は、docker-compose.yml の nginx のホスト側のportsに 8000 を指定し、且つセキュリティグループのインバウンドルールに、カスタムTCPの 8000 を加える。



###　その他:エイリアスレコードのメモ
トラフィックの確認として、Route53 の エイリアスに直接IPアドレスを書き込む方法がある。
Route53 -> ホストゾーン -> kuni-example.com のレコードの編集で、エイリアスを OFF にし、EC2 の web のパブリックIPを指定する。
※Route53 は、エイリアスレコードの名前 (acme.example.com など) とエイリアスレコードのタイプ (A や AAAA など) が DNSクエリ の名前およびタイプと一致した場合にだけ DNS クエリに応答する。
