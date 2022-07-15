# coding: utf-8

# Downloads chinese chess (xiangqi) data from playok.com into .txt files
# example: http://www.playok.com/zh/game.phtml/57390680.txt?xq
# example: https://www.playok.com/p/?g=xq186002968.txt

import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from time import time

import requests

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, default=58000000, help='where to start downloading')
parser.add_argument('--num', type=int, default=10000, help='how many to download')
parser.add_argument('--data_dir', type=str, help='where to save')
parser.add_argument('--n_concur', type=int, default=1, help='how many processes/threads')

args = parser.parse_args()
script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = args.data_dir if args.data_dir else os.path.join(script_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

start = args.start
n_replays = args.num
end = start + n_replays


def download(game_id):
    # targetURL = f'http://www.playok.com/zh/game.phtml/{game_id}.txt?g=xq'
    targetURL = f'https://www.playok.com/p/?g=xq{game_id}.txt'
    try:
        res = requests.get(targetURL)
        res.raise_for_status()
    except Exception:
        return
    file_path = os.path.join(data_dir, f'{game_id}.txt')
    with open(file_path, 'wb') as fp:
        for chunk in res.iter_content(100000):
            fp.write(chunk)
    print(f'got game replay {game_id}')


start_time = time()
with ThreadPoolExecutor(max_workers=args.n_concur) as executor:
    executor.map(download, range(start, end))
print(f'download {n_replays} spend {time() - start_time} sec.')
