import sys
sys.path.append("src")
from castle.castle_map_maker import CastleMapMaker as Maker
grid = Maker.make_dungeon_map(60, 30, 64, 80)
Maker.print_map(grid)