from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .forms import UserResponseForm
from .models import Question, Answer, UserAnswer

# Create your views here.
def single(request, id):
    print id
    if request.user.is_authenticated():
        form = UserResponseForm(request.POST or None)
        if form.is_valid():
            print form.cleaned_data
            #form.cleaned_data['question_id']
            question_id = form.cleaned_data.get('question_id')

            user_answer_id = form.cleaned_data.get('user_answer_id')
            importance_level = form.cleaned_data.get('importance_level')

            match_answer_id = form.cleaned_data.get('match_answer_id')
            match_importance_level = form.cleaned_data.get(
                'match_importance_level'
                )

            question_instance = Question.objects.get(id=question_id)
            answer_instance = Answer.objects.get(id=user_answer_id)

            new_user_answer = UserAnswer()
            new_user_answer.user = request.user
            new_user_answer.question = question_instance
            new_user_answer.user_answer = answer_instance
            new_user_answer.user_answer_importance = importance_level
            if match_answer_id != -1:
                match_answer_instance = Answer.objects.get(id=match_answer_id)
                new_user_answer.match_answer = match_answer_instance
                new_user_answer.match_answer_importance = match_importance_level
            else:
                new_user_answer.match_answer_importance = "Not Important"
            new_user_answer.save()

            next_q = Question.objects.all().order_by("?").first()



            return redirect("question_single", id=next_q.id)
        queryset = Question.objects.all().order_by('-timestamp')
        instance = get_object_or_404(Question, id=id)
        context = {
            "form": form,
            "instance": instance,
            #"queryset": queryset
        }
        return render(request, "questions/single.html", context)
    else:
        raise Http404

def home(request):
    if request.user.is_authenticated():
        form = UserResponseForm(request.POST or None)
        if form.is_valid():
            print form.cleaned_data
            question_id = form.cleaned_data.get('question_id') #form.cleaned_data['question_id']
            user_answer_id = form.cleaned_data.get('user_answer_id')
            question_instance = Question.objects.get(id=question_id)
            answer_instance = Answer.objects.get(id=user_answer_id)
            print question_instance.text, answer_instance.text
        queryset = Question.objects.all().order_by('-timestamp')
        instance = queryset[1]
        context = {
            "form": form,
            "instance": instance,
            #"queryset": queryset
        }
        return render(request, "questions/home.html", context)
    else:
        raise Http404
