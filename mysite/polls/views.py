from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .models import Choice, Question
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
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

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     #get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 
#     # 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘깁니다. 
#     # 만약 객체가 존재하지 않을 경우, Http404 예외가 발생합니다.
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))