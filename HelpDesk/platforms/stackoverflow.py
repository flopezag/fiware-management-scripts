import stackexchange
from platforms.questions import SOF
from Basics.settings import API_KEY_STACKOVERFLOW

__author__ = 'Manuel Escriche'


server = stackexchange.Site(stackexchange.StackOverflow,
                            app_key=API_KEY_STACKOVERFLOW,
                            impose_throttling=True)

server.be_inclusive()

questions = server.search(filter='withbody', tagged='fiware')

for question in questions:
    q = SOF(**question.json)
    print(q, q.tags, q.is_answered)

print(len(questions))


