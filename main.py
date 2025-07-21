import os
import json
import sys
sys.set_int_max_str_digits(100000)

class ProgressRecorder:
    """データ保存・再開が簡単になるクラス"""
    def __init__(self, filename:str='progress.json'):
        self.filename = filename
        self.state = {"current_index": 0}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.state = json.load(f)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.state, f, indent=2)

    def set_index(self, index):
        self.state['current_index'] = index

    def get_index(self):
        return self.state['current_index']

class SequenceRecorder:
    """データ保存用クラス"""
    def __init__(self, filename):
        self.filename = filename
        self.values = []
        self.load_existing()

    def load_existing(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.values = [line.strip() for line in f if line.strip()]
        else:
            self.values = []

    def append(self, value):
        with open(self.filename, 'a') as f:
            f.write(f"{str(value)}\n")
        self.values.append(str(value))

    def get_last(self):
        for val in reversed(self.values):
            if val.isdigit():
                return int(val)
        return None


def calc_primes(N):
    result = [True] * (N + 1)
    primes = [2]
    for i in range(3, N + 1, 2):
        if not result[i]:
            continue
        primes.append(i)
        idx = 3
        while idx * i <= N:
            result[idx * i] = False
            idx += 2
    return primes

def is_mersenne_prime(p:int):
    m = 2**p-1
    S = 4
    for _ in range(p-2):
        S = (S*S-2)%m
    return S == 0


N = 10**6
primes = calc_primes(N)
sr = SequenceRecorder("result.txt")
pr = ProgressRecorder()
start = pr.get_index()

for idx in range(start, len(primes)):
    p = primes[idx]
    if is_mersenne_prime(p):
        num = (2**(p-1)) * (2**p - 1)
        sr.append(f"{p} ({idx+1}th prime)\n---\n{num}\n======")
    pr.set_index(idx+1)
    pr.save()
pr.save()
