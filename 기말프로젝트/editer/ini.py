import math

# This variables should be modified myself
# Map
MAPID = 200
MAP_WIDTH = 800
MAP_HEIGHT = 600

# Resource path
path = '../res/Map/'

# 현재 선택한 타일셋
selection = None

# Background tile
BGR = (11, 10)

# Mouse position
mPos = (0, 0)

# Data will be saved here
DATA = []

# Load map if file is exist
try:
    f = open(str(MAPID) + '.txt', 'r')
except:
    for i in range(math.ceil(MAP_WIDTH / 32) + 1):
        for j in range(math.ceil(MAP_HEIGHT / 32) + 1):
            DATA.append(('t', BGR, i * 32, j * 32))
    print('Create new map. Map code : %d' % MAPID)
else:
    f.readline()
    TEMP = f.readlines()
    for i in TEMP:
        line = i.split()
        # Portal
        if line[0] == 't' and (int(line[1]), int(line[2])) in [(11, 0), (10, 0), (9, 0), (10, 1)]:
            DATA.append(('t', (int(line[1]), int(line[2])), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7])))
        # Normal tile
        elif line[0] == 't':
            DATA.append(('t', (int(line[1]), int(line[2])), int(line[3]), int(line[4])))
        elif line[0] == 'm':
            DATA.append(('m', (int(line[1]), int(line[2])), int(line[3]), int(line[4])))
    f.close()
    print('Load data. Map code : %d' % MAPID)