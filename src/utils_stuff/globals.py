from utils_stuff.Position import Position 

DATA_PATH = "../data/"
MINIMAP_WIDTH = 14750
MINIMAP_HEIGHT = 14750

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








