from django import template

register = template.Library()

@register.filter(name='setValidationClass')
def setValidationClass(input):
    bootstrap_class = ''
    if input.help_text == 'filter_option' and input.data != None:
        if input.errors:
            #CSS Class for only filters forms
            bootstrap_class = 'is-invalid' 
    return input.as_widget(attrs={'class':'form-control '+ bootstrap_class})