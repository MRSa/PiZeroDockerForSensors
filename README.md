# PiZeroDockerForSensors : Raspberry Pi Zero で Docker & センサデータの収集
Raspberry Pi Zero に Dockerを載せて、コンテナ３つ（Redis, Grafana, Python)を立ち上げ、I2Cで接続した(BME688の)センサーからのデータをRedisに蓄積し、Grafanaを使ってグラフ表示できます。

## リポジトリ
https://github.com/MRSa/PiZeroDockerForSensors

## システム構成
![System Image](https://github.com/MRSa/PiZeroDockerForSensors/blob/main/pics/pizero.jpg?raw=true)


---------------------------------------

## Raspberry Pi Zeroの設定 (概略)
1. Raspberry Pi OS Lite (32bit) : 2022-09-22
2. パッケージを最新にする(sudo apt update; sudo apt full-upgrade を実行する)
3. スワップを設定 (/etc/dphys-swapfile を更新)
4. raspi-config で I2Cを有効にしておく
5. Dockerのインストール
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker (普段使いユーザ名)
```
6. docker-composeのインストール
```
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install bcrypt==3.2.2
pip3 install cryptography==3.4.8
pip3 install docker-compose
```
7. OSの再起動を行う




---------------------------------------
## 参考
- Grafana : https://grafana.com/grafana/
- Redis : https://redis.io/
- pimoroni/BME68x : https://github.com/pimoroni/bme680-python

