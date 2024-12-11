from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Category)
class CategoryTranslateOptions(TranslationOptions):
    fields = ('name',)


@register(Post)
class CatalogueTranslateOptions(TranslationOptions):
    fields = ('title', 'article',)


@register(Collection)
class ProductTranslateOptions(TranslationOptions):
    fields = ('title',)


@register(Question)
class QuestionTranslateOptions(TranslationOptions):
    fields = ('text',)


@register(Answer)
class AnswerTranslateOptions(TranslationOptions):
    fields = ('text',)
