import pytiled_parser as pp
from pathlib import Path

levels = []
amount_of_levels = 1
for i in range(1, amount_of_levels+1):
    level = pp.parse_map(Path(f"maps/map{i}.tmx"))
    levels.append(level)
