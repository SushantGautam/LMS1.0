from . import models

from rest_framework import serializers


class CategoryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoryInfo
        fields = (
            'pk', 
            'Category_Name', 
        )


class SurveyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SurveyInfo
        fields = (
            'pk', 
            'Survey_Title', 'Start_Date', 'End_Date', 'Survey_Cover', 'Use_Flag','Added_By','Category_Code','Session_Code','Course_Code', 'Center_Code'
        )


class QuestionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QuestionInfo
        fields = (
            'pk', 
            'Question_Name','Survey_Code','Question_Type'
        )


class OptionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OptionInfo
        fields = (
            'pk', 
            'Option_Name','Question_Code'
        )


class SubmitSurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubmitSurvey
        fields = (
            'pk',
            'Survey_Code', 'Student_Code'
        )


class AnswerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnswerInfo
        fields = (
            'pk',
            'Answer_Value','Question_Code','Submit_Code'
        )


