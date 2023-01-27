from cmu_graphics import *
import json

def readJson():
    with open('PokemonData.json', 'r') as inFile:
        pokemon = json.load(inFile)
    inFile.close()

    return pokemon

app.background = 'powderblue'

search = Rect(200, 200, 150, 80, align='center', fill='seashell', border='black', borderWidth=4)

menu = Group(
    search,
    Label('SEARCH', 200, 200, size=30),
    Label('POKEMON DICTIONARY', 200, 50, size=30, bold=True),
    Label('By the MJ Incorporation', 200, 80, size=15),
)

def drawInfo(pokemonName, pokemon):
    global menu

    menu.clear()

    search.centerY = 300

    pokemonType = Label(pokemon[0], 300, 50, size=25, font='monospace')

    i = 0
    if (len(pokemon) == 9):
        i = 1
        pokemonType.value = pokemon[0] + ' ' + pokemon[1]

    menu = Group(
        Label('Pokemon:', 100, 25, size=25, font='monospace'),
        Label(pokemonName, 300, 25, size=25, font='monospace'),

        Label('Type:', 100, 50, size=25, font='monospace'),
        pokemonType,

        Label('BST:', 100, 75, size=25, font='monospace'),
        Label(pokemon[1 + i], 300, 75, size=25, font='monospace'),

        Label('HP:', 100, 100, size=25, font='monospace'),
        Label(pokemon[2 + i], 300, 100, size=25, font='monospace'),

        Label('Attack:', 100, 125, size=25, font='monospace'),
        Label(pokemon[3 + i], 300, 125, size=25, font='monospace'),

        Label('Defense:', 100, 150, size=25, font='monospace'),
        Label(pokemon[4 + i], 300, 150, size=25, font='monospace'),

        Label('Sp Attack:', 100, 175, size=25, font='monospace'),
        Label(pokemon[5 + i], 300, 175, size=25, font='monospace'),

        Label('Sp Defense:', 100, 200, size=25, font='monospace'),
        Label(pokemon[6 + i], 300, 200, size=25, font='monospace'),

        Label('Speed:', 100, 225, size=25, font='monospace'),
        Label(pokemon[7 + i], 300, 225, size=25, font='monospace'),

        search,
        Label('SEARCH', 200, 300, size=30),
    )

def onMouseMove(mouseX, mouseY):
    if (search.hits(mouseX, mouseY)):
        search.border = 'gold'
    else:
        search.border = 'black'

def onMousePress(mouseX, mouseY):
    global menu

    if (search.hits(mouseX, mouseY)):
        response = app.getTextInput('Which Pokemon Would You Like To Search?')

        response = response.lower()
        response = response.capitalize()

        try:
            pokemon = readJson()[response]
            drawInfo(response, pokemon)
        except:
            menu.add(Label('POKEMON NAME NOT VALID', 200, 360, size=25, font='monospace', fill='red'))

cmu_graphics.run()
