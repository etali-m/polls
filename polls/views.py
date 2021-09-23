from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] 
    context = {'latest_question_list': latest_question_list, }
    return  render(request, 'polls/index.html', context) #goes diretly to the templates folder

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #we get the question if there is not errors
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) #get the ID of the selected choice
    except(KeyError, Choice.DoesNotExist):
        #redisplay the question voting form if
        return render(request, 'polls/detail.html', {'question': question,
        'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes +=1
        selected_choice.save()

    #always return an HttpResponseRedirect after successfully dealing with POST data
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))