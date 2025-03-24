from django.forms.widgets import Select
from django.forms.models import ModelChoiceIterator
"""
Working on a select widget which only renders selected option, as all other options will be loaded via REST API
"""
class Select2Widget(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Access the queryset from the field to get the model dynamically
        queryset = self.choices
        if isinstance(queryset, ModelChoiceIterator):
            model = queryset.queryset.model  # Access model from queryset
        else:
            model = None
        
        if model:
            # Get the instance of the model from the value (pk)
            instance = model.objects.get(pk=value) if value else None
            choices = [(value, str(instance))] if instance else []
        else:
            choices = []

        # Render the select widget with only the selected option
        self.choices = choices
        return super().render(name, value, attrs, renderer)