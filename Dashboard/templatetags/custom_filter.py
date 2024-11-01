from django import template

register = template.Library()


@register.filter
def slice_from_last_underscore(value, length=15):
    # Find the last underscore and slice from there
    if "_" in value:
        value = value.rsplit("_", 1)[0]  # Slice after the last underscore
    
    return value[:length].upper()  # Return the first `length` characters in uppercase


