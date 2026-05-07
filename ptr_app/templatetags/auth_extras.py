from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Returns True if the user belongs to the given group or is superuser.
    Usage in template: {% if request.user|has_group:"tooling_manager" %}
    """
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()
