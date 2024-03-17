from django import template

register = template.Library()


def censor(value):
    bad_words = ['Редиска', 'Карнаухов']
    for word in bad_words:
        value = value.replace(word, word[0] + '*' * len(word))
    return value


register.filter('censor', censor)
