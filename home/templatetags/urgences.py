from django import template

from home.models import NumeroUrgence

register = template.Library()


@register.simple_tag
def numeros_urgence():
    return NumeroUrgence.objects.all()