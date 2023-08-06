#    ___  _ _                         ____________  _____
#   / _ \| | |                        | ___ \ ___ \/  __ \
#  / /_\ \ | |_ ___  __ _ _ __ _ __   | |_/ / |_/ /| /  \/
#  |  _  | | __/ _ \/ _` | '__| '_ \  |    /|  __/ | |
#  | | | | | ||  __/ (_| | |  | | | | | |\ \| |    | \__/\
#  \_| |_/_|\__\___|\__,_|_|  |_| |_| \_| \_\_|     \____/
#
#

# Durée entre chaque changement de statut (en secondes)
# /!\ Discord impose 15s minimum entre chaque changement
change_time = 60

# Durée entre chaque tentative de connection aprés une erreur
# Mettre ce temps trés bas n'est pas recommandé, surtout si retry_number est sur 0
retry_time = 60

# Nombre de tentatives de connexion échouées à la suite avant de quitter le programme
# Définir à 0 pour désactiver
retry_number = 5

# Noms des différents éléments à afficher
names = ["Altearn", "Gunivers", "Curiosity"]

# IDs de clients des éléments
ids = {"Altearn": "844964834880782357",
       "Gunivers": "845325102551924756",
       "Curiosity": "845325302435414046"}

# Slogans des éléments
states = {"Gunivers": "Creativity begins here !",
          "Altearn": "Apprendre, autrement !",
          "Curiosity": "Apprennez sans cesse !"}

# Images de jour pour chaque élément
large_image = {"Altearn": "altearn_white",
               "Gunivers": "gunivers",
               "Curiosity": "curiosity"}

# Images de nuit pour chaque élément
large_image_night = {"Altearn": "altearn_black",
                     "Gunivers": "gunivers",
                     "Curiosity": "curiosity"}

# Boutons pour chaque éléments
buttons = {"Altearn": [{"label": "En savoir plus", "url": "https://altearn.xyz/"},
                       {"label": "Wiki", "url": "https://wiki.altearn.xyz"}],
           "Gunivers": [{"label": "En savoir plus", "url": "https://gunivers.net/"},
                        {"label": "Discord", "url": "https://discord.gg/E8qq6tN"}],
           "Curiosity": [{"label": "Discord", "url": "https://discord.gg/8Dub7zVvV9"}]}

# Citations aléatoires
quotes = [
    "Luxembourg -- Nemesis, 2021",
    "C'est le top ça -- Leirof, 2021",
    "Je s'appelle groot -- Fleaudesme, 2021",
    "Pain au chocolat ou chocolatine ? -- 301, 2017",
    "Fromage -- Fantomitechno, 2021",
    "On peut être efficace (sérieux c'est moins sur) -- Leirof, 2021",
    "Never gonna give you up -- Rick Asley"
]
