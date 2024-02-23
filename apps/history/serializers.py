from rest_framework.serializers import ModelSerializer
from .models import *


class LanguageMixinForSerializers:
    def __init__(self, *args, **kwargs):
        self.accept_language = kwargs.pop('accept_language', 'en')
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # default = ['gas', 'drive', 'wheel', 'car_type', 'description', 'naming',]
        if self.accept_language == 'ru':
            data = {key: value for key, value in data.items() if not key.endswith((
                '_en', '_ky', #*default
            ))}
        elif self.accept_language == 'ky':
            data = {key: value for key, value in data.items() if not key.endswith((
                '_en', '_ru', #*default
            ))}
        else:
            data = {key: value for key, value in data.items() if not key.endswith((
                '_ru', '_ky', #*default
            ))}
        return data


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class YearsSerializer(ModelSerializer):
    class Meta:
        model = Years
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
