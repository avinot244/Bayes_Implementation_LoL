from utils_stuff.Position import Position 

DATA_PATH = "../data/"
MINIMAP_WIDTH = 14750
MINIMAP_HEIGHT = 14750
YAML_PATH = ""

TYPES = ["INFO", "SNAPSHOT", "GAME_EVENT"]

champions_list = ["Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Ashe", "Azir",
                  "Blitzcrank", "Brand", "Braum",
                  "Caitlyn", "Cassiopeia", "Cho'Gath", "Corki",
                  "Darius", "Diana", "Dr. Mundo", "Draven",
                  "Elise", "Evelynn", "Ezreal",
                  "Fiddlesticks", "Fiora", "Fizz",
                  "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves",
                  "Hecarim", "Heimerdinger", 
                  "Irelia", 
                  "Janna", "Jarvan IV", "Jax", "Jayce", "Jinx",
                  "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kennen", "Kha'Zix", "Kog'Maw",
                  "LeBlanc", "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux",
                  "Malphite", "Malzahar", "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana"
                  "Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne", "Nunu", 
                  "Olaf", "Orianna",
                  "Pantheon", "Poppy",
                  "Quinn",
                  "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven", "Rumble", "Ryze",
                  "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Syndra",
                  "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch",
                  "Udyr", "Urgot",
                  "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor", "Vladimir", "Volibear",
                  "Warwick", "Wukong",
                  "Xerath", "Xin Zhao", 
                  "Yasuo", "Yorick", 
                  "Zac", "Zed", "Ziggs", "Zilean", "Zyra",
                  "Bard", "Ekko", "Tahm kench", "Kindred", "Illaoi", "Jhin", "Aurelion sol", "Taliyah", "Kled", "Ivern", "Camille",
                  "Rakan", "Xayah", "Kayn", "Ornn", "Zoe", "Kai'sa", "Pyke", "Neeko", "Sylas", "Yuumi", "Qiyana", "Senna", "Aphelios",
                  "Sett", "Lillia", "Yone", "Samira", "Seraphine", "Rell", "Viego", "Gwen", "Akshan", "Vex", "Zeri", "Renata Glasc",
                  "Bel'Veth", "Nilah", "K'Sante", "Milio", "Naafiri", "Briar"]

towerPositionRedSide = [Position(4318, 13875), Position(7943, 13411), Position(10481, 13650), Position(12611, 13084), 
                        Position(8955, 8510),Position(9767, 10113), Position(11134, 11207), Position(13866, 4505), 
                        Position(13327, 8226), Position(13624, 10572),Position(13052, 12612)]

towerPositionBlueSide = [Position(5846, 6396), Position(5048, 4812), Position(3651, 3696), Position(10504, 1029), 
                         Position(6919, 1483), Position(4281, 1253), Position(2177, 1807), Position(981, 10441), 
                         Position(1512, 6699), Position(1169, 4287), Position(1748, 2270)]

inhibitorPositionRedSide = [Position(11261, 13659), Position(11603, 11667), Position(13598, 11316)]
inhibitorPositionBlueSide = [Position(1169, 3573), Position(3203, 3208), Position(3454, 1241)]

midLaneBoundary = [Position(5200,6030), Position(6055,5388), Position(9740,8810), Position(8840,9480)]

topLaneBoundary = [Position(1724,10202), Position(1733,10523), Position(1778,10889), Position(1947,11397),
                   Position(2241,11816), Position(2812,11281), Position(3667,11459), Position(3427,11878),
                   Position(3427,11878), Position(2972, 12199), Position(2954,12467), Position(3614, 12841),
                   Position(4095,13019), Position(4666,13108), Position(4639, 14036), Position(3703, 14027),
                   Position(2758, 13795), Position(2179, 13482), Position(1893,13492), Position(1430, 13634),
                   Position(1109, 13501), Position(886, 13242), Position(904, 12752), Position(1038, 12574),
                   Position(1038, 12217), Position(717, 11433), Position(681, 10434)]

mapCenter = Position(MINIMAP_WIDTH//2, MINIMAP_HEIGHT//2)




