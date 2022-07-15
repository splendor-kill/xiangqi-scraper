#! python3
# chineseChessGameDataScraper.py -
# Downloads chinese chess (xiangqi) data from playok.com into .txt files
# example: http://www.playok.com/zh/game.phtml/57390680.txt?xq

import argparse
import os
import requests

# set working directory to where script is
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(dataPath, exist_ok=True)
os.chdir(dataPath)

# start, end = 57385152, 57390690
start, end = 186000000, 187000000

for gameID in range(start, end):
    # open corresponding page
    # targetURL = f'http://www.playok.com/zh/game.phtml/{gameID}.txt?g=xq'
    targetURL = f'https://www.playok.com/p/?g=xq{gameID}.txt'
    try:
        res = requests.get(targetURL)
        res.raise_for_status()
    except Exception:
        continue
    # Save content of page into corresponding text file
    gameFileName = f'{gameID}.txt'
    with open(gameFileName, 'wb') as fp:
        for chunk in res.iter_content(100000):
            fp.write(chunk)

    print(f'Parsed gameid {gameID}')
