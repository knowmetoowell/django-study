from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Question
from django.http import Http404

from django.shortcuts import get_object_or_404, render
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    #render() 함수는 request 객체를 첫번째 인수로 받고, 
    # 템플릿 이름을 두번째 인수로 받으며, 
    # context 사전형 객체를 세전째 선택적(optional) 인수로 받습니다. 
    # 인수로 지정된 context로 표현된 템플릿의 HttpResponse 객체가 반환됩니다.
    # 모든 뷰에 적용한다면, 더 이상 loader와 HttpResponse를 임포트하지 않아도 됩니다. 
    # (만약 detail, results, vote에서 stub 메소드를 가지고 있다면, HttpResponse를 유지해야 할 것입니다.)


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 
    # 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘깁니다. 
    # 만약 객체가 존재하지 않을 경우, Http404 예외가 발생합니다.
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)