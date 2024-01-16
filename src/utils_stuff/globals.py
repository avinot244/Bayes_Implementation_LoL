from utils_stuff.Position import Position 

DATA_PATH = "../data/"
MINIMAP_WIDTH = 14750
MINIMAP_HEIGHT = 14750
YAML_PATH = ""

TYPES = ["INFO", "SNAPSHOT", "GAME_EVENT"]
GAME_TYPES = ["ESPORTS", "SCRIM", "COMPETITIVE"]
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

topLaneBoundary = [Position(1716,10133), Position(3728, 11764), Position(4080, 11626), Position(4061, 12182), Position(4656, 12653),
                   Position(4632, 14035), Position(3398, 14006), Position(1081, 13534), Position(866, 13223), Position(671, 10171)]

botLaneBoundary = [Position(10109, 728), Position(12309, 745), Position(13438, 1161), Position(13660, 1319), 
                   Position(13824, 1646), Position(14005, 4759), Position(13011, 4800), Position(12198, 4414),
                   Position(11905, 4261), Position(11080, 3296), Position(10788, 3226), Position(10577, 2957),
                   Position(10056, 2138), Position(10109, 1740)]

jungleEntry1Blue = [Position(3403, 9768), Position(2871, 9584), Position(2941, 9235), Position(3551, 9538)]

jungleEntry2Blue = [Position(4824, 8707), Position(4338, 8319), Position(4505, 7564), Position(4913, 7380), Position(5342, 7303),
                    Position(5290, 7554), Position(5280, 8275)]

jungleEntry3Blue = [Position(9068, 5398), Position(8888, 5393), Position(8675, 5132), Position(8420, 4728), Position(7783, 5213),
                    Position(7774, 5544), Position(8192, 5743), Position(8509, 5701)]

jungleEntry4Blue = [Position(11060, 3316), Position(10781, 3246), Position(10555, 2989), Position(10250, 2785),
                    Position(9932, 2902), Position(10010, 3268), Position(11029, 3669)]

jungleEntry1Red = [Position(3794, 11097), Position(4212, 11190), Position(4437, 11604), Position(4646, 11592),
                   Position(4638, 11921), Position(4429, 12157), Position(4061, 12192), Position(4085, 11639),
                   Position(3732, 11759)]

jungleEntry2Red = [Position(6278, 9026), Position(6978, 9194), Position(6957, 9553), Position(6452, 10023),
                   Position(6140, 9643), Position(5889, 9341)]

jungleEntry3Red = [Position(9470, 6355), Position(10045, 6023), Position(10319, 6545), Position(10310, 7134),
                   Position(9824, 7452), Position(9421, 7324)]

jungleEntry4Red = [Position(11860, 4244), Position(12181, 4410), Position(12509, 4610), Position(12164, 4928),
                   Position(12046, 5021), Position(11722, 4969), Position(11732, 4748), Position(11621, 4614)]

riverBot = [Position(7885, 6122), Position(9139, 5386), Position(10051, 5035), Position(10519, 4676), Position(11121, 3831),
            Position(11046, 3656), Position(11014, 3396), Position(11823, 4207), Position(11606, 4559), Position(11447, 4600),
            Position(11397, 4676), Position(11263, 5077), Position(10084, 5897), Position(9340, 6373), Position(8855, 6791)]

riverTop = [Position(6718, 8465), Position(6217, 8912), Position(6235, 9012), Position(5742, 9341), Position(4748, 9724),
            Position(4328, 10034), Position(3690, 10864), Position(3735, 11065), Position(3699, 11712), Position(2732, 10910),
            Position(2869, 10782), Position(3398, 9788), Position(3589, 9523), Position(3973, 9186), Position(4812, 8766),
            Position(5332, 8328), Position(5943, 7881)]

jungleBlueTop = [Position(4671, 8617), Position(4257, 8643), Position(3856, 8768), Position(3534, 9044), Position(3429, 9228),
                 Position(3442, 9431), Position(2936, 9215), Position(2200, 9524), Position(1858, 8505), Position(1871, 8249),
                 Position(2969, 7000), Position(3061, 6494), Position(3225, 6224), Position(3560, 5929), Position(3882, 5791),
                 Position(4494, 5856), Position(4875, 6093), Position(4960, 6638), Position(4842, 7138), Position(4487, 7565),
                 Position(4316, 8295)]

jungleBlueBot = [Position(7780, 5200), Position(7294, 5850), Position(6098, 5423), Position(6545, 4799), Position(6538, 4503),
                 Position(7037, 2544), Position(7412, 2223), Position(7833, 2026), Position(8207, 1947), Position(8897, 2104),
                 Position(9252, 2229), Position(9620, 2374), Position(9811, 2341), Position(10047, 2164), Position(10218, 2630),
                 Position(10245, 2630), Position(9916, 2887), Position(9969, 3255), Position(9465, 3498), Position(9180, 3872),
                 Position(9088, 4312), Position(8956, 4760), Position(8694, 5068), Position(8418, 4707)]

jungleRedTop = [Position(6993, 9518), Position(7710, 9023), Position(8836, 9495), Position(9024, 10957), Position(8910, 11339),
                Position(8478, 12039), Position(7698, 12277), Position(7374, 12613), Position(6959, 12744), Position(6509, 12755),
                Position(6014, 12664), Position(5491, 12647), Position(4830, 12716), Position(4654, 12636), Position(4483, 12477),
                Position(4648, 11942), Position(4665, 11606), Position(5143, 11418), Position(5445, 11139), Position(5673, 10741),
                Position(5792, 10115), Position(6111, 9649), Position(6452, 10036)]

jungleRedBot = [Position(10049, 6069), Position(10826, 5910), Position(11225, 5695), Position(11617, 5281), Position(11736, 5000),
                Position(12047, 5029), Position(12483, 4652), Position(12676, 5673), Position(12912, 6265), Position(12905, 6480),
                Position(11617, 8641), Position(11270, 8988), Position(10833, 9093), Position(10189, 9018), Position(9871, 8744),
                Position(9716, 8197), Position(9804, 7486), Position(10315, 7138), Position(10337, 6546)]

mapCenter = Position(MINIMAP_WIDTH//2, MINIMAP_HEIGHT//2)

roleMap : dict = {0 : "Top",
                  1 : "Jungle",
                  2 : "Mid",
                  3 : "ADC",
                  4 : "Support"}




