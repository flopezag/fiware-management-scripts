from logging import debug
from datetime import datetime
from re import sub

__author__ = 'Manuel Escriche'


class Question(object):
    def __init__(self, **kwargs):
        # print(kwargs)
        self.tags = kwargs['tags']
        self.score = kwargs['score']
        self.answer_count = kwargs['answer_count']
        self.monitor = None

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class ASK(Question):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.id = 'ASK-{}'.format(kwargs['id'])
        self.summary = kwargs['title']
        self.description = sub(r'<[^<]+?>', '', kwargs['summary'])
        self.author = kwargs['author']
        self.url = kwargs['url']

        self.is_answered = True if kwargs['accepted_answer_id'] is not None else False

        self.added_at = datetime.fromtimestamp(int(kwargs['added_at']))
        self.last_activity_at = datetime.fromtimestamp(int(kwargs['last_activity_at']))


class SOF(Question):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self._id = str(kwargs['question_id'])
        self.id = 'SOF-{}'.format(kwargs['question_id'])
        debug('key = {}'.format(self.id))
        self.summary = kwargs['title']
        self.description = sub(r'<[^<]+?>', '', kwargs['body'])
        self.author = kwargs['owner']
        self.url = kwargs['link']
        self.is_answered = kwargs['is_answered']

        self.accepted_answer_id = str(kwargs['accepted_answer_id']) if 'accepted_answer_id' in kwargs else None

        self.answer_date = \
            datetime.fromtimestamp(int(kwargs['last_edit_date'])) if 'last_edit_date' in kwargs else None

        self.added_at = datetime.fromtimestamp(int(kwargs['creation_date']))
        self.last_activity_at = datetime.fromtimestamp(int(kwargs['last_activity_date']))

    @property
    def qid(self):
        return self._id


if __name__ == "__main__":
    pass
