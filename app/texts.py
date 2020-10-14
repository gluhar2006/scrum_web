from random import choice
from classes import Mark, User


def _get_text_unanimously(mark: Mark) -> str:
    """Get random text for unanimous voting"""
    return choice({
                      Mark.one.value: [
                          '...easy...',
                          'there will not be a day how this task will be done',
                          'it may be easier not to start such a task',
                          'I will do it in 5 ... 3 minutes!',
                          'I will do all day, I will say that the os crashed',
                      ],
                      Mark.two.value: [
                          'not bad',
                          'there will not be a month how this task will be done',
                          'start and ...finish',
                          'I will do it in 60 ... 30 minutes!',
                          'I will do all week, I will say that the pycharm has been updated',
                      ],
                      Mark.three.value: [
                          'ok, let\'s go...',
                          'there will not be a year how this task will be done',
                          'start, think and ...finish',
                          'I will do it in 300 ... 60 minutes!',
                          'I will do all month, I will say that I was bitten by python...',
                      ],
                      Mark.five.value: [
                          'looks interesting',
                          'day...may be couple of days',
                          'not bat, not bad',
                          'I will do it in a week ... no, I can handle in a day!',
                          'I will do all year, I will say that I was bitten by python in the head...',
                      ],
                      Mark.eight.value: [
                          'oh...',
                          'day...week...month',
                          'oh my god, 8!',
                          'I will do it in two weeks ... no, I can handle in a couple of days!',
                          'I will do all year, I will say that I was bitten by python in the ass...',
                      ],
                      Mark.xz.value: [
                          'Unanimously xz!? Are you kidding me?!?!?!',
                      ],
                      Mark.decompose.value: [
                          'Ok ... let\'s decompose that shit',
                      ]
                  }
                  [mark.value])


def _get_text_one_against_all() -> str:
    """Get text for: one against all"""
    return choice([
        'what\'s wrong with you?',
        'everythings all right?',
        'may be you need to change your mind...',
        'sad not to have like-minded people',
        'it seems you\'re outnumbered',
        'your colleagues disagree with you',
    ])


def get_text(users: list[User]) -> str:
    """Get text for voting results"""
    marks = [user.mark for user in users]
    marks_count = len(set(marks))

    if marks_count == 1:
        return _get_text_unanimously(marks[0])

    mark_values = [mark.value for mark in marks]
    sorted_marks_with_counts = sorted(
        [(mark_value, mark_values.count(mark_value)) for mark_value in mark_values], key=lambda x: x[1])
    non_popular_mark_value, non_popular_count = sorted_marks_with_counts[0]
    is_one_against_all = marks_count == 2 and non_popular_count == 1

    if is_one_against_all:
        non_popular_user = [user for user in users if user.mark.value == non_popular_mark_value][0]
        popular_mark_value, _ = sorted_marks_with_counts[1]
        return f'All voted {popular_mark_value}, except for {non_popular_user.name} - ' \
               f'voted {non_popular_mark_value}. {non_popular_user.name}, {_get_text_one_against_all()}'

    are_all_marks_good = [mark.is_mark() for mark in marks]

    if are_all_marks_good:
        mark_values = [mark.value for mark in marks]
        average_mark = sum(mark_values) / len(mark_values)
        return f'Voting is over. Average mark is {average_mark}'

    return 'Voting is over. Everything is difficult, sort it out yourself'
