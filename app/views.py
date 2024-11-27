import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import models

from app.models import QuestionManager

# Create your views here.

QUESTIONS = [
    {
        'title': f'Title {i + 1}',
        'id': i,
        'text': f'This is text for question # {i + 1}'
    } for i in range(30)
]


def index(request):
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    page = paginate(models.Question.objects.order_by_date(), request)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page,
                                                  'tags': popular_tags, 'members': best_members})


def ask(request):
    return render(request, 'ask.html')


def question(request, question_id):
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    if (not models.Question.objects.get_by_id(id=question_id).exists()) or question_id < 0:
        return render(request, 'page404.html', status=404)
    question = models.Question.objects.get_by_id(id=question_id)
    return render(request, 'question.html', context={'question': question,
                                                     'answers': models.Answer.objects.get_answers(question),
                                                     'tags': popular_tags, 'members': best_members})


def login(request):
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    return render(request, 'login.html', context={'tags': popular_tags, 'members': best_members})


def signup(request):
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    return render(request, 'signup.html', context={'tags': popular_tags, 'members': best_members})

def tag_page(request, tag_name):
    if not models.Tag.objects.filter(name=tag_name).exists():
        return render(request, "page404.html", status=404)
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    return render(request, 'tag_page.html', context={'tag': tag_name, 'questions': models.Question.objects.get_by_tag(tag_name),
                                                'tags': popular_tags, 'members': best_members})

def hot(request):
    popular_tags = models.Tag.objects.order_by_popular()[:10]
    best_members = models.Profile.objects.all()[:5]
    page = paginate(models.Question.objects.order_by_rating(), request)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page,
                                                  'tags': popular_tags, 'members': best_members})


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


