import json
from django.shortcuts import render
from utils import global_context, decorators
from qb import models as qb_models


@decorators.login_required
@decorators.redirect_to_requested_page_after_login
def practice_home_page(request):
    context = global_context.Context.get_context()
    return render(request, 'practice/practice_home_page.html', context)


@decorators.login_required
@decorators.redirect_to_requested_page_after_login
def choose_practice_material(request, material: str):
    context = global_context.Context.get_context()
    if material == 'chapters':
        context['redirect_base_url'] = '/practise-chapter/'
        context['materials'] = qb_models.Chapter.objects.all()
    else: 
        context['is_adm'] = True
        context['redirect_base_url'] = '/practise-admission-test-questions/'
        context['materials'] = qb_models.AdmissionTest.objects.all()
    return render(request, 'practice/materials.html', context)


@decorators.login_required
@decorators.redirect_to_requested_page_after_login
def pracrise_chapter(request, chapter_id: int):
    context = global_context.Context.get_context()
    chapter = qb_models.Chapter.objects.get(id=int(chapter_id))
    bulk = qb_models.QuestionMetaData.objects.filter(chapter=chapter)
    answer_map = qb_models.QuestionMetaData.get_answer_map(bulk)
    context['bulk'] = bulk; context['answer_map_json'] = 'const v = '+ json.dumps(answer_map)
    context['page_title'] = 'Practise Chapter'; context['test_url'] = '/chapter-quick-test/' + str(chapter_id)
    return render(request, 'practice/practise.html', context)


@decorators.login_required
@decorators.redirect_to_requested_page_after_login
def pracrise_adm(request, adm_id: int):
    context = global_context.Context.get_context()
    adm_test = qb_models.AdmissionTest.objects.get(id=int(adm_id))
    university = qb_models.University.objects.filter(admission_test=adm_test)
    metadata_ids = [apr.metadata.id for apr in qb_models.Appearance.objects.filter(
        university__in=list(university))]
    bulk = qb_models.QuestionMetaData.objects.filter(id__in=metadata_ids)
    answer_map = qb_models.QuestionMetaData.get_answer_map(bulk)
    context['bulk'] = bulk; context['answer_map_json'] = 'const v = ' + json.dumps(answer_map) + ';'
    context['page_title'] = 'Practise Admission Test Questions'; context['test_url'] = '/admission-quick-test/' + str(adm_test.id)
    return render(request, 'practice/practise.html', context)
