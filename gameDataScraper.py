# coding: utf-8

# Downloads chinese chess (xiangqi) data from playok.com into .txt files
# example: http://www.playok.com/zh/game.phtml/57390680.txt?xq
# example: https://www.playok.com/p/?g=xq186002968.txt

import argparse
import os

import requests

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, default=58000000, help='where to start downloading')
parser.add_argument('--num', type=int, default=10000, help='how many to download')
parser.add_argument('--data_dir', type=str, help='where to save')

args = parser.parse_args()
script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = args.data_dir if args.data_dir else os.path.join(script_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

start = args.start
end = start + args.num

for gameID in range(start, end):
    # targetURL = f'http://www.playok.com/zh/game.phtml/{gameID}.txt?g=xq'
    targetURL = f'https://www.playok.com/p/?g=xq{gameID}.txt'
    try:
        res = requests.get(targetURL)
        res.raise_for_status()
    except Exception:
        continue
    file_path = os.path.join(data_dir, f'{gameID}.txt')
    with open(file_path, 'wb') as fp:
        for chunk in res.iter_content(100000):
            fp.write(chunk)

    print(f'got game replay {gameID}')
