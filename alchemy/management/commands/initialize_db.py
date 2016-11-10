from django.core.management.base import BaseCommand
from alchemy.core.models import Rule, Item
 

class Command(BaseCommand):

    def handle(self, *args, **options):
        for rule in RULES:
            populate_rule(rule)

        cards = list(generate_cards())
        for card in cards:
            card.populate()
        for card in cards:
            for rule in card.rules():
                populate_rule(rule)


def populate_rule(rule):
    i1 = Item.objects.get_or_create(name=rule[0])[0]
    i2 = Item.objects.get_or_create(name=rule[1])[0]
    res = Item.objects.get_or_create(name=rule[2])[0]
    Rule.objects.create(input1=i1, input2=i2, result=res)


def generate_cards():
    for color in [' '] + list(SYMBOLS['color'].keys()):
        for suit in [' '] + list(SYMBOLS['suit'].keys()):
            for number in [' '] + list(SYMBOLS['number'].keys()):
                yield Card(color=color, suit=suit, number=number)


class Card(object):

    def __init__(self, color=' ', suit=' ', number=' '):
        self.color = color
        self.suit = suit
        self.number = number

    def dict(self):
        return {
            'color': self.color,
            'suit': self.suit,
            'number': self.number,
        }

    def populate(self):
        Item.objects.get_or_create(name=str(self), defaults={'limit': self.limit()})

    def limit(self):
        if ' ' in str(self):
            return None
        return 1

    def __str__(self):
        return '[%s%s%s]' % (self.color, self.suit, self.number)

    def rules(self):
        d = self.dict()
        for key in d:
            if d[key] != ' ':
                yield (
                    SYMBOLS[key][d[key]],
                    str(Card(**{**d, key: ' '})),
                    str(self)
                )


SYMBOLS = {
    'color': {
        'R': 'Červená farba',
        'B': 'Modrá farba',
    },

    'suit': {
        '♥': 'Znak srdce',
        '♣': 'Znak tref',
        '♠': 'Znak pika',
        '♦': 'Znak káro',
    },

    'number': {
        '2': 'Číslo dva',
        '3': 'Číslo tri',
        '4': 'Číslo štyri',
        '5': 'Číslo päť',
        '6': 'Číslo šesť',
        '7': 'Číslo sedem',
        '8': 'Číslo osem',
        '9': 'Číslo deväť',
        '0': 'Číslo desať',
        'J': 'Číslo J',
        'Q': 'Číslo Q',
        'K': 'Číslo K',
        'A': 'Číslo A',
    },
}

RULES = (
    ('Voda', 'Oheň', 'Para'),
    ('Voda', 'Vzduch', 'Dážď'),
    ('Voda', 'Zem', 'Blato'),
    ('Voda', 'Voda', 'More'),

    ('Oheň', 'Oheň', 'Energia'),
    ('Oheň', 'Vzduch', 'Dym'),
    ('Oheň', 'Zem', 'Láva'),

    ('Zem', 'Vzduch', 'Piesok'),
    ('Zem', 'Zem', 'Kameň'),

    ('Vzduch', 'Vzduch', 'Vietor'),

    ('Vietor', 'Voda', 'Ľad'),

    ('Para', 'Vietor', 'Dážď'),

    ('Blato', 'Oheň', 'Tehla'),
    ('Blato', 'Energia', 'Život'),
    ('Blato', 'Voda', 'Bažina'),

    ('Život', 'Zem', 'Rastlina'),
    ('Život', 'Život', 'Láska'),
    ('Život', 'Voda', 'Láska'),
    ('Život', 'Kameň', 'Muž'),
    ('Život', 'Láska', 'Žena'),
    ('Život', 'Bažina', 'Pavúk'),
    ('Život', 'More', 'Poseidon'),
    ('Život', 'Sedmokráska', 'Králik'),

    ('Žena', 'Muž', 'Sympatia'),
    ('Žena', 'Energia', 'Deva'),
    ('Žena', 'Pavúk', 'Zdesenie'),
    ('Žena', 'Ľad', 'Elza'),

    ('Muž', 'Hrach', 'Janko Hraško'),

    ('Rastlina', 'Rastlina', 'Strom'),
    ('Rastlina', 'Bažina', 'Trstina'),
    ('Rastlina', 'Zem', 'Tulipán'),
    ('Rastlina', 'Voda', 'Sedmokráska'),
    ('Rastlina', 'Vzduch', 'Hrach'),

    ('Drevo', 'Oheň', 'Uhlík'),

    ('Uhlík', 'Voda', 'Atrament'),

    ('Kameň', 'Strom', 'Drevo'),
    ('Kameň', 'Drevo', 'Papier'),
    ('Kameň', 'Trstina', 'Papier'),
    ('Kameň', 'Tulipán', 'Červená farba'),
    ('Kameň', 'Voda', 'Modrá farba'),
    ('Kameň', 'Uhlík', 'Diamant'),
    ('Kameň', 'Zem', 'Koleso'),

    ('Strom', 'Vietor', 'List'),

    ('List', 'List', 'Dvojlístok'),
    ('List', 'Dvojlístok', 'Trojlístok'),
    ('List', 'Trojlístok', 'Štvorlístok'),

    ('Papier', 'Papier', str(Card())),
    ('Papier', 'List', 'Znak pika'),
    ('Papier', 'Diamant', 'Znak káro'),
    ('Papier', 'Trojlístok', 'Znak tref'),
    ('Papier', 'Láska', 'Znak srdce'),

    ('Atrament', 'Dvojlístok', 'Číslo dva'),
    ('Atrament', 'Trojlístok', 'Číslo tri'),
    ('Atrament', 'Štvorlístok', 'Číslo štyri'),
    ('Atrament', 'Sympatia', 'Číslo päť'),
    ('Atrament', 'Žena', 'Číslo šesť'),
    ('Atrament', 'Sedmokráska', 'Číslo sedem'),
    ('Atrament', 'Poseidon', 'Číslo osem'),
    ('Atrament', 'Deva', 'Číslo deväť'),
    ('Atrament', 'Zdesenie', 'Číslo desať'),
    ('Atrament', 'Janko Hraško', 'Číslo J'),
    ('Atrament', 'Elza', 'Číslo Q'),
    ('Atrament', 'Králik', 'Číslo K'),
    ('Atrament', 'Koleso', 'Číslo A'),

)
