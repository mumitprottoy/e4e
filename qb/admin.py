from django.contrib import admin
from .models import (
    AdmissionTest,
    QuestionMetaData,
    Appearance,
    Passage,
    Question,
    Option,
    Explanation
) 


@admin.register(AdmissionTest)
class AdmissionTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym')


admin.site.register((
    QuestionMetaData,
    Appearance,
    Passage,
    Question,
    Option,
    Explanation
) )
