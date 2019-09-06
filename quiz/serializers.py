from . import models

from rest_framework import serializers


# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.Profile
#         fields = (
#             'pk',
#         )


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Quiz
        fields = (
            'pk', 'title', 'description', 'mcquestion', 'tfquestion', 'saquestion', 'url', 'cent_code', 'course_code', 'chapter_code', 'duration', 'random_order', 'answers_at_end', 'exam_paper', 'single_attempt', 'pre_test', 'post_test', 'pass_mark', 'success_text', 'fail_text'
        )

class MCQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MCQuestion
        fields = (
            'pk','figure', 'content', 'course_code', 'explanation', 'cent_code', 'answer_order'
        )

class TF_QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TF_Question
        fields = (
            'pk','figure', 'content', 'course_code', 'explanation', 'cent_code', 'correct'
        )

class SA_QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.SA_Question
        fields = (
            'pk','figure', 'content', 'course_code', 'explanation', 'cent_code'
        )

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = (
            'pk','question', 'content', 'correct'
        )

class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Progress
        fields = (
            'pk','user', 'score'
        )

class SittingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sitting
        fields = (
            'pk','user', 'quiz', 'question_order', 'question_list', 'incorrect_questions', 'current_score', 'complete', 'user_answers', 'start', 'end', 'objects'
        )        