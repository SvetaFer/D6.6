from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post, Category, Author
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(field_name="time_in", widget=forms.DateInput(attrs={'type': "date"}),
                      label='Дата', lookup_expr='date__gte')

    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        label='Категория',
    )

    class Meta:
        model = Post
        fields = {

            'header': ['icontains'],
            'author': ['in'],

        }
