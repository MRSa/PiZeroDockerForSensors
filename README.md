# PiZeroDockerForSensors : Raspberry Pi Zero で Docker & センサデータの収集
Raspberry Pi Zero に Dockerを載せて、コンテナを３つ（Redis, Grafana, Python)立ち上げ、I2Cで接続した(BME688の)センサーからのデータをセンサーデータは、5分起きに収取してRedisに時系列データとして蓄積し、Grafanaを使ってグラフ表示できるようにする。

## リポジトリ
https://github.com/MRSa/PiZeroDockerForSensors

### docker-compose.yml
https://github.com/MRSa/PiZeroDockerForSensors/blob/main/monitor_sensor/docker-compose.yml

## システム構成
![System Image](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/pizero.jpg?raw=true)

## 収集結果表示イメージ(Grafana)
![Grafana Image](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/grafana.jpg?raw=true)

---------------------------------------

## Raspberry Pi Zeroの設定 (概要)
1. Raspberry Pi OS Lite (32bit) : 2022-09-22
2. パッケージを最新にする(sudo apt update; sudo apt full-upgrade を実行する)
3. スワップを設定 (/etc/dphys-swapfile を更新)
4. raspi-config で I2Cを有効にしておく
5. Dockerをインストール
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker (普段使いユーザ名)
```
6. docker-composeのインストール(普通にインストールすると bcrypt と cryptography がエラーになるので回避する)
```
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install bcrypt==3.2.2
pip3 install cryptography==3.4.8
pip3 install docker-compose
```
7. このへんでOSの再起動を行う (sudo /sbin/shutdown -r now)
8. データフォルダを作成し、書き込み可にしておく
```
/data/opt/mysensor
/data/opt/redis/lib
/data/opt/redis/var
/data/opt/redis/log
/data/opt/redis/run
/data/opt/grafana/logs
/data/opt/grafana/data
```
9. docker-compose build する
10. docker-compose up -d してサービスを起動する (起動時間がかかりすぎてタイムアウトするようならば、タイムアウト時間を延長しておく)
```
COMPOSE_HTTP_TIMEOUT=240 docker-compose up　-d
```
11. しばらく待つ
12. Webブラウザからポート3000にアクセスすると、Grafanaが表示される

初期ユーザ名 admin パスワード admin、ログイン時にパスワード変更を促されるのでパスワードを変更する

---------------------------------------

## Grafanaの設定
グラフ表示をするため、GrafanaからRedisに接続し、グラフ表示を行う。

### データソースの設定
#### Data Sourceに「Redis」を追加する
![Data Source](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/datasource0.jpg?raw=true)

#### Redis の Address に「redis:6379」を設定する
![Redis](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/datasource.jpg?raw=true)

## Dashboard に Panel を追加する

Queryの値は、RedisTimeSeries のタイプで設定する
- Data source : Redis
- Type : RedisTimeSeries
- Command : TS.RANGE
- Key : 以下を設定する
  - ts:bme680humidity : 湿度
  - ts:bme680pressure : 圧力
  - ts:bme680temperature : 温度
  - ts:bme680gasresistance : ガス抵抗値

![Dashboard Settings](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/timeseries.jpg?raw=true)

### グラフの軸などをカスタマイズする

---------------------------------------
## 参考リンク
- Grafana : https://grafana.com/grafana/
- Redis : https://redis.io/
- RedisTimeSeries : https://redis.io/docs/stack/timeseries/
- pimoroni/BME68x : https://github.com/pimoroni/bme680-python
- Docker Container(Alpine) : https://hub.docker.com/_/alpine
- Alpine Linux Packages : https://pkgs.alpinelinux.org/packages
