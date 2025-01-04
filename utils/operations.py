from django.shortcuts import render
from django.contrib.auth.models import User
from qb.models import *
from .stuff import stuff
from .chapters import chapters
from .atnu import atnu
from qb import models
from . import constants as const, global_context


def create_super_user():
    if User.objects.count() != 0:
        user = User(
            username='pro',
            email='mumitprottoy@gmail.com',
            first_name='Mumit',
            last_name='Prottoy'
        )
        user.save()
        user.is_superuser = True
        user.is_staff = True
        user.save()
        user.set_password('prottoy21')
        user.save()

def import_universities():
    University.objects.all().delete()
    _map = {'MEDICAL': 'MAT', 'DENTAL': 'DAT'}
    for at in atnu:
        for u in atnu[at]:
            _at = at if at not in _map else _map[at]
            admission_test = AdmissionTest.objects.get(acronym=_at)
            try:
                University(
                    admission_test=admission_test,
                    acronym=u,
                ).save()
            except: print('Error:', at, u)
    

def import_chapters():
    for chapter in chapters:
        Chapter(name=chapter).save()


def get_chaps():
    file = open('utils/chaps.txt', 'r')
    return file.read().split('\n')

def compare():
    return [chap.name for chap in Chapter.objects.all() if chap.name not in get_chaps()]


def import_qb():
    QuestionMetaData.objects.all().delete()
    import json
    file = open('utils/cool_qb.txt', 'r', encoding='utf-8')
    qb = json.loads(file.read())
    _len = len(qb)
    print('len:', _len)
    count = 0
    for _ in qb:
        university = University.objects.get(acronym=_['university'])
        metadata = QuestionMetaData(
            has_passage = _['has_passage'],
            has_appeared = True,
            chapter=Chapter.objects.get(name=_['chapter'])          
        )
        metadata.save()
        Appearance(
            metadata=metadata,
            university=university,
            unit=_['unit'],
            year=str(_['year'])
        ).save()
        if metadata.has_passage:
            Passage(metadata=metadata, text=_['passage']).save()
        for __ in _['block']:
            question = Question(metadata=metadata, text=__['text'])
            question.save()
            for opt in __['options']:
                option = Option(
                    question=question, 
                    text=opt['text'], 
                    is_correct=opt['is_correct']
                ) 
                option.save()
            Explanation(question=question, text=__['explanation']).save()
        count += 1
        print(f'{count}/{_len}')


def trim():
    chapter = models.Chapter.objects.filter(name='Comprehension').first()
    metadata_list = list(models.QuestionMetaData.objects.filter(chapter=chapter))
    for metadata in metadata_list:
        questions = list(metadata.questions.all())
        if (not metadata.has_passage) or (len(questions) < const.COMP_QUES_QTY):
            metadata.delete()
        else:
            i = const.COMP_QUES_QTY
            while i < len(questions):
                questions[i].delete()
                i += 1

def mcqc():
    chapter = models.Chapter.objects.filter(name='Comprehension').first()
    metadata_list = list(models.QuestionMetaData.objects.filter(chapter=chapter))
    for metadata in metadata_list:
        print(models.Question.objects.filter(metadata=metadata).count())
        

def chapter_wise_count():
    return {
        chapter.name:models.QuestionMetaData.objects.filter(
            chapter=chapter).count() for chapter in models.Chapter.objects.all()
    }


def chapter_count_map(bulk=models.QuestionMetaData.objects.all()):
    _map = dict()
    for m in bulk.all():
        if m.chapter.name in _map:
            _map[m.chapter.name] += 1
        else: _map[m.chapter.name] = 1
    return _map


def create_form_data(header, input_type, name, placeholder, submit_btn_text):
    return {
            'form_data' : {
            'form_header': header,
            'input_type': input_type,
            'input_name': name,
            'input_placeholder': placeholder,
            'submit_btn_text': submit_btn_text,
        }
    }


def redirect_to_success_page(
    request, success_msg='Task successfully completed.', sl=5, redirect_url='/', context=global_context.Context.get_context()):
    context['success_msg'] = success_msg
    context['sl'] = sl; context['redirect_url'] = redirect_url
    return render(request, 'success_page.html', context)


def set_form_data(header, _type, name, placeholder, btn_txt):
    return {
        'form_header': header,
        'input_type': _type,
        'input_name': name,
        'input_placeholder': placeholder,
        'submit_btn_text': btn_txt
    }