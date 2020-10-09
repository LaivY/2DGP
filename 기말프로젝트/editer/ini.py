import math

# This variables should be modified my yourself
# Map
MAPID = 100
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
            DATA.append((BGR, i * 32, j * 32))
    print('Create new map. Map code : %d' % MAPID)
else:
    f.readline()
    TEMP = f.readlines()
    for i in TEMP:
        line = i.split()
        # Portal
        if (int(line[0]), int(line[1])) in [(11, 0), (10, 0), (9, 0), (10, 1)]:
            DATA.append(((int(line[0]), int(line[1])), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])))
        # Normal
        else:
            DATA.append(((int(line[0]), int(line[1])), int(line[2]), int(line[3])))
    f.close()
    print('Load data. Map code : %d' % MAPID)