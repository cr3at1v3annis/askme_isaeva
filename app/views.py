import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

QUESTIONS = [
    {
        'title': f'Title {i + 1}',
        'id': i,
        'text': f'This is text for question # {i + 1}'
    } for i in range(30)
]


def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def ask(request):
    return render(request, 'ask.html')


def question(request, question_id):
    question = QUESTIONS[question_id]
    return render(request, 'question.html', context={'question': question})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def hot(request):
    new_questions = copy.deepcopy(QUESTIONS)
    new_questions.reverse()
    page = paginate(new_questions, request)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

