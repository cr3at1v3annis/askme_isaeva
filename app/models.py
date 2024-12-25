from audioop import reverse

from django.db import models
import operator
from django.contrib.auth.models import User
from django.db.models import DateField, DateTimeField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    def __str__(self):
        return self.user.name

class TagManager(models.Manager):
    def order_by_popular(self):
        return self.order_by('-count')

class Tag(models.Model):
    tag_name = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=13, default="33, 10, 230")
    count = models.IntegerField(default=0)
    objects = TagManager()
    def __str__(self):
        return self.tag_name

class QuestionManager(models.Manager):
    def order_by_date(self):
        return self.order_by('-creation_date')
    def order_by_rating(self):
        return self.order_by('-rating', '-answer_count')

    def get_by_tag(self, tag):
        return self.filter(tags__name__icontains=tag)

    def get_by_id(self, id):
        return self.get(pk=id)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, db_column="user_id", null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=70)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    creation_date = DateTimeField()
    objects = QuestionManager()
    def __str__(self):
        return f"{self.question_id} {self.title}"

class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('-rating')

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="user_id", null=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=70)
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    on_question_id = models.ForeignKey(Question, db_column="question_id", null=False, on_delete=models.CASCADE)
    objects = AnswerManager()
    def __str__(self):
        return f"{self.answer_id}"


class QuestionLike(models.Model):
    like_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, db_column="user_id", null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, db_column="question_id", null=False, on_delete=models.CASCADE)
    type_of_like = models.BooleanField()
    def __str__(self):
        return f"{self.like_id}"

    class Meta:
        unique_together = [["author", "question"]]

class AnswerLike(models.Model):
    like_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, db_column="user_id", null=False, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, db_column="answer_id", null=False, on_delete=models.CASCADE)
    type_of_like = models.BooleanField()
    class Meta:
        unique_together = [["author", "answer"]]
    def __str__(self):
        return f"{self.like_id}"



