from os.path import join, exists
from os import makedirs
from pickle import load

STOREHOME = '/Users/fernandolopez/Documents/workspace/python/fiware-management-scripts/HelpDesk/store'


def load_1(filename):
    timestamp = 0.0
    questions = list()
    try:
        with open(join(STOREHOME, filename), 'rb') as f:
            timestamp, questions = load(f)
    except FileNotFoundError as e:
        if exists(STOREHOME) == False:
            makedirs(STOREHOME)
        print(e)
    except EOFError as e:
        print(e)

    print('loaded questions from file: {}'.format(filename))
    return timestamp, questions


filename = 'FIWARE.Helpdesk.Askbot.pkl'
timestamp, questions = load_1(filename=filename)

print(questions)
print(timestamp)
