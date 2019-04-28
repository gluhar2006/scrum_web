from random import choice

oneAgaintsAll = [
    'what\'s wrong with you?',
    'everythings all right?',
    'may be you need to change your mind...',
    'sad not to have like-minded people',
    'it seems you\'re outnumbered',
    'your colleagues disagree with you',
]

allOne = [
    '...easy...',
    'there will not be a day how this task will be done',
    'it may be easier not to start such a task',
    'I will do it in 5 ... 3 minutes!',
    'I will do all day, I will say that the os crashed',
]

allTwo = [
    'not bad',
    'there will not be a month how this task will be done',
    'start and ...finish',
    'I will do it in 60 ... 30 minutes!',
    'I will do all week, I will say that the pycharm has been updated',
]

allThree = [
    'ok, let\'s go...',
    'there will not be a year how this task will be done',
    'start, think and ...finish',
    'I will do it in 300 ... 60 minutes!',
    'I will do all month, I will say that I was bitten by python...',
]

allFive = [
    'looks interesting',
    'day...may be couple of days',
    'not bat, not bad',
    'I will do it in a week ... no, I can handle in a day!',
    'I will do all year, I will say that I was bitten by python in the head...',
]

allEight = [
    'oh...',
    'day...week...month',
    'oh my god, 8!',
    'I will do it in two weeks ... no, I can handle in a couple of days!',
    'I will do all year, I will say that I was bitten by python in the ass...',
]

def getText(var) -> str:
    """
    Get random text for situation.
    Possible situations are: 
        one - oneAgainstAll
        1,2,3,5,8 - ...
    """
    print(var)
    if var == 'one':
        return choice(oneAgaintsAll)
    if var == 1:
        return choice(allOne)
    if var == 2:
        return choice(allTwo)
    if var == 3:
        return choice(allThree)
    if var == 5:
        return choice(allFive)
    if var == 8:
        return choice(allEight)
