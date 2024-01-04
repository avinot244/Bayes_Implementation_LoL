from utils_stuff.Position import Position 

DATA_PATH = "../data/"
MINIMAP_WIDTH = 14750
MINIMAP_HEIGHT = 14750
YAML_PATH = ""

TYPES = ["INFO", "SNAPSHOT", "GAME_EVENT"]
GAME_TYPES = ["ESPORTS", "SCRIM", "CHAMPIONS_QUEUE", "GENERIC"]
DOWNLOAD_OPTIONS = ["GAMH_DETAILS", "GAMH_SUMMARY", "ROFL_REPLAY", "HISTORIC_BAYES_SEPARATED", "HISTORIC_BAYES_DUMP"]

towerPositionRedSide = [Position(4318, 13875), Position(7943, 13411), Position(10481, 13650), Position(12611, 13084), 
                        Position(8955, 8510),Position(9767, 10113), Position(11134, 11207), Position(13866, 4505), 
                        Position(13327, 8226), Position(13624, 10572),Position(13052, 12612)]

towerPositionBlueSide = [Position(5846, 6396), Position(5048, 4812), Position(3651, 3696), Position(10504, 1029), 
                         Position(6919, 1483), Position(4281, 1253), Position(2177, 1807), Position(981, 10441), 
                         Position(1512, 6699), Position(1169, 4287), Position(1748, 2270)]

inhibitorPositionRedSide = [Position(11261, 13659), Position(11603, 11667), Position(13598, 11316)]
inhibitorPositionBlueSide = [Position(1169, 3573), Position(3203, 3208), Position(3454, 1241)]

midLaneBoundary = [Position(6074,5430), Position(7757, 6047), Position(8633, 6692), Position(9738, 8815), Position(8836, 9479),
                   Position(7085, 8736), Position(6262, 8046), Position(5183, 6038)]

topLaneBoundary = [Position(1716,10133), Position(3939, 11566), Position(4167, 11760), Position(4656, 12653),
                   Position(4632, 14035), Position(3398, 14006), Position(1081, 13534), Position(866, 13223), Position(671, 10171)]

botLaneBoundary = [Position(10119, 745), Position(11263, 736), Position(13353, 1109), Position(13763, 1370), Position(13885, 1650),
                   Position(14096, 4760), Position(14076, 5060), Position(12983, 5089), Position(11822, 4702), Position(10951, 4199),
                   Position(10177, 2167)]

jungleEntry1Blue = [Position(8464, 4705), Position(9030, 5411), Position(8221, 5919), Position(7652, 5192)]

jungleEntry2Blue = [Position(10155, 2598), Position(11240, 3162), Position(11094, 3799), Position(10042, 3547)]

jungleEntry3Blue = [Position(4881, 7805), Position(5566, 8569), Position(5008, 8841), Position(4459, 8417), Position(4329, 7828)]

jungleEntry4Blue = [Position(3570, 9789), Position(3249, 9226), Position(3624, 8875), Position(3900, 9343)]

mapCenter = Position(MINIMAP_WIDTH//2, MINIMAP_HEIGHT//2)

roleMap : dict = {0 : "Top",
                  1 : "Jungle",
                  2 : "Mid",
                  3 : "ADC",
                  4 : "Support"}




