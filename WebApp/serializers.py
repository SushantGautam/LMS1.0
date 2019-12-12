from rest_framework import serializers

from . import models


class CenterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CenterInfo
        fields = (
            'pk', 'Center_Name', 'Center_Address', 'Use_Flag', 'Register_DateTime', 'Register_Agent'
        )


class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemberInfo
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'password', 'Member_Permanent_Address',
            'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar',
            'Member_Gender', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
            'Member_Memo', 'Is_Teacher', 'Is_Student', 'Is_CenterAdmin', 'Is_Parent', 'Member_Avatar', 'Center_Code', 'get_student_courses'
        )


class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseInfo
        fields = (
            'pk', 'Course_Name', 'Course_Description', 'Course_Cover_File', 'Course_Level',
            'Course_Info', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
            'Course_Provider', 'Center_Code'
        )


class ChapterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChapterInfo
        fields = (
            'pk', 'Chapter_No', 'Chapter_Name', 'Summary', 'Page_Num', 'Use_Flag',
            'Register_DateTime', 'Updated_DateTime', 'Register_Agent', 'Course_Code'
        )


class InningInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InningInfo
        fields = (
            'pk', 'Inning_Name', 'Start_Date', 'End_Date', 'Use_Flag', 'Register_DateTime',
            'Updated_DateTime', 'Groups', 'Course_Group',
            'Register_Agent', 'Center_Code'
        )


class SessionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionInfo
        fields = (
            'pk', 'Session_Name', 'Description', 'Use_Flag', 'Center_Code'
        )


class InningGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InningGroup
        fields = (
            'pk', 'Teacher_Code', 'Course_Code', 'Use_Flag', 'Register_DateTime',
            'Updated_DateTime', 'Register_Agent', 'Center_Code'
        )


class GroupMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GroupMapping
        fields = (
            'pk', 'Center_Code', 'Students', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
            'Register_Agent', 'GroupMapping_Name'
        )


# AssignmentInfoSerializer
class AssignmentInfoSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='Course_Code.Course_Name')
    Register_Agent_Name = serializers.ReadOnlyField(source='Register_Agent.__str__')

    class Meta:
        model = models.AssignmentInfo
        fields = (
            'pk', 'Assignment_Topic', 'Assignment_Deadline', 'Use_Flag', 'Register_DateTime',
            'Updated_DateTime', 'Register_Agent', 'Course_Code', 'course_name', 'Chapter_Code', 'Register_Agent_Name'
        )


class QuestionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignmentQuestionInfo
        fields = (
            'pk',
            'Question_Title', 'Question_Score', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
            'Register_Agent', 'Question_Media_File', 'Question_Description', 'Course_Code', 'Chapter_Code',
            'Answer_Choices', 'Answer_Type'
        )


class AssignAssignmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignAssignmentInfo
        fields = (
            'pk', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Inning_Code', 'Assignment_Code',
            'Assigned_By'
        )


class AssignAnswerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignAnswerInfo
        fields = (
            'pk', 'Assignment_Score', 'Question_Code',
            'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Assignment_Answer', 'Student_Code'
        )


class MessageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageInfo
        fields = (
            'pk',
            'teacher_code', 'message', 'message_read', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
            'Register_Agent'
        )
