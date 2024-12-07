from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, TextInput
from .models import Recipe, Tag

class RecipeForm(ModelForm):
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget = CheckboxSelectMultiple(),
        required = False,
        to_field_name='name'
    )

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'cooking_time', 'tags']
        

    # def save(self, commit=True):
    #     recipe = super().save(commit=False)
    #     recipe.author = self.request.user
    #     if commit:
    #         recipe.save()
    #         self.save_m2m()
    #     return recipe