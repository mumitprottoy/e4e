from django.shortcuts import render, redirect
from utils import decorators
from utils.global_context import Context
from qb import models as qb_models
from . import engine, models, operations as ops
from .operations import authtenticate_participant



@decorators.login_required
@decorators.phone_number_required
def quick_test(request):
    bulk = models.QuestionMetaData.objects.filter(
        chapter__in=ops.get_quick_syllabus_chapters())
    metadata_ids = '-'.join([str(metadata.id) for metadata in bulk])
    return redirect('/general-quick-test/'+metadata_ids)


@decorators.login_required
@decorators.phone_number_required
def chapter_quick_test(request, chapter_id: int):
    chapter = qb_models.Chapter.objects.get(id=int(chapter_id))
    bulk = models.QuestionMetaData.objects.filter(chapter=chapter)
    metadata_ids = '-'.join([str(metadata.id) for metadata in bulk])
    return redirect('/general-quick-test/'+metadata_ids)


@decorators.login_required
@decorators.phone_number_required
def adm_quick_test(request, adm_id):
    adm_test = qb_models.AdmissionTest.objects.get(id=int(adm_id))
    universities = qb_models.University.objects.filter(admission_test=adm_test)
    metadata_ids = '-'.join([str(apr.metadata.id) for apr in qb_models.Appearance.objects.filter(
        university__in=list(universities))])
    return redirect('/general-quick-test/'+metadata_ids)


@decorators.login_required
@decorators.phone_number_required
def general_quick_test(request, metadata_ids: str):
    metadata_ids = [int(_id) for _id in metadata_ids.split('-')]
    bulk = models.QuestionMetaData.objects.filter(id__in=metadata_ids)
    participant = engine.set_exam(bulk, 20, request.user)
    return redirect('/start-quick-test/'+participant.test.key)


@decorators.login_required
@decorators.phone_number_required
def start_quick_test(request, key: str):
    context = Context.get_context()
    test = models.Test.objects.get(key=key)
    if request.POST:
        engine.TestInitiator(test=test).initiate()
        return redirect('/test/'+test.key)
    context['test'] = test
    return render(request, 'tests/start_exam.html', context)


@decorators.login_required
@decorators.phone_number_required
def test_handler(request, key: str):
    user = request.user
    participant = authtenticate_participant(user, key)
    if participant is not None:
        test = participant.test
        context = Context.get_context()
        context['participant'] = participant
        if not participant.has_timer: 
            return redirect('/start-quick-test/'+participant.test.key)
        if not (participant.has_submitted or test.timer.has_ended()):
            timer: models.TestTimer = test.timer
            context['timer'] = timer 
            if timer.has_started:
                if request.POST:
                    participant.has_submitted = True
                    participant.save()
                else:
                    context['answer_paper'] = participant.get_answer_paper()
                    return render(request, 'tests/answer_paper.html', context)
            else: return render(request, 'tests/waiting_room.html', context)
        evaluator = engine.TestEvaluator(participant)
        context['short_report'] = evaluator.get_short_report_list()
        context['suggestions'] = evaluator.suggestions()
        return render(request, 'tests/result.html', context)
    return redirect('nope')      


@decorators.login_required
@decorators.phone_number_required
def all_tests(request):
    context = Context.get_context()
    timers = models.TestTimer.objects.filter(
        test__in=[part.test for part in models.TestParticipant.objects.filter(user=request.user) if part.has_ended]
        ).order_by('-start_datetime')
    context['timers'] = timers
    context['timers_count'] = timers.count()
    return render(request, 'tests/all_tests.html', context)


@decorators.login_required
@decorators.phone_number_required
def test_report(request, key: str):
    test = models.Test.objects.get(key=key)
    participant = models.TestParticipant.objects.get(test=test, user=request.user)
    evaluator = engine.TestEvaluator(participant)
    context = Context.get_context()
    context['short_report'] = evaluator.get_short_report_list()
    context['suggestions'] = evaluator.suggestions()
    return render(request, 'tests/result.html', context)