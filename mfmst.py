# run from terminal as e.g. "python mfmst.py < test01.uwg"

import sys

vertices = int(sys.stdin.readline().replace("\n", ""))
print(vertices)

edges = int(sys.stdin.readline().replace("\n", ""))
print(edges)

for _ in range(edges):
    line = sys.stdin.readline().replace("\n", "")
    print(line)
