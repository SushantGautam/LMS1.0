import unittest
from django.urls import reverse
from django.test import Client
from .models import Profile, CenterInfo, MemberInfo, CourseInfo, ChapterInfo, ChapterContentsInfo, ChapterMissonCheckCard, ChapterMissonCheckItem, InningInfo, OmrQuestionInfo, QuizInfo, AssignHomeworkInfo, AssignQuestionInfo, BoardInfo, BoardContentInfo, InningGroup, ChapterContentMedia, ChapterImgInfo, ChapterMissonCheck, ChapterWrite, GroupMapping, HomeworkInfo, LearningNote, CourseUbtInfo, LessonInfo, LessonLog, MemberGroup, MessageInfo, OmrAnswerInfo, OmrAssignInfo, OmrExampleInfo, QAnswerInfo, QAnswerLog, QExampleInfo, QuestionInfo, QuizAnswerInfo, QuizExampleInfo, ScheduleInfo, TalkMember, TalkRoom, TalkMessage, TalkMessageRead, TodoInfo, TodoTInfo
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_profile(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Profile.objects.create(**defaults)


def create_centerinfo(**kwargs):
    defaults = {}
    defaults["Center_Name"] = "Center_Name"
    defaults["Center_Address"] = "Center_Address"
    defaults["Use_Flag"] = "Use_Flag"
    defaults["Register_DateTime"] = "Register_DateTime"
    defaults["Register_Agent"] = "Register_Agent"
    defaults.update(**kwargs)
    return CenterInfo.objects.create(**defaults)


def create_memberinfo(**kwargs):
    defaults = {}
    defaults["Member_ID"] = "Member_ID"
    defaults["Member_Password"] = "Member_Password"
    defaults["Member_Type"] = "Member_Type"
    defaults["Member_Name"] = "Member_Name"
    defaults["Member_Permanent_Address"] = "Member_Permanent_Address"
    defaults["Member_Temporary_Address"] = "Member_Temporary_Address"
    defaults["Member_BirthDate"] = "Member_BirthDate"
    defaults["Member_Email"] = "Member_Email"
    defaults["Member_Phone"] = "Member_Phone"
    defaults["forum_avatar"] = "forum_avatar"
    defaults["member_Gender"] = "member_Gender"
    defaults["Use_Flag"] = "Use_Flag"
    defaults["Register_DateTime"] = "Register_DateTime"
    defaults["Register_Agent"] = "Register_Agent"
    defaults["Member_Memo"] = "Member_Memo"
    defaults.update(**kwargs)
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    return MemberInfo.objects.create(**defaults)


def create_courseinfo(**kwargs):
    defaults = {}
    defaults["course_name"] = "course_name"
    defaults["course_teacher"] = "course_teacher"
    defaults["course_cover"] = "course_cover"
    defaults["course_cover_file"] = "course_cover_file"
    defaults["course_level"] = "course_level"
    defaults["course_info"] = "course_info"
    defaults["teacher"] = "teacher"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["course_certification"] = "course_certification"
    defaults["course_provider"] = "course_provider"
    defaults["cert_crit_prog"] = "cert_crit_prog"
    defaults["cert_crit_post"] = "cert_crit_post"
    defaults["cert_crit_ubt"] = "cert_crit_ubt"
    defaults["cert_crit_issue"] = "cert_crit_issue"
    defaults.update(**kwargs)
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    return CourseInfo.objects.create(**defaults)


def create_chapterinfo(**kwargs):
    defaults = {}
    defaults["chapter_no"] = "chapter_no"
    defaults["chapter_name"] = "chapter_name"
    defaults["topic"] = "topic"
    defaults["summary"] = "summary"
    defaults["page_num"] = "page_num"
    defaults["vod_size"] = "vod_size"
    defaults["intro"] = "intro"
    defaults["target"] = "target"
    defaults["top_img"] = "top_img"
    defaults["bottom_img1"] = "bottom_img1"
    defaults["bottom_img2"] = "bottom_img2"
    defaults["bottom_img3"] = "bottom_img3"
    defaults["thum_file"] = "thum_file"
    defaults["vod_file"] = "vod_file"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["today"] = "today"
    defaults["chapter_type"] = "chapter_type"
    defaults["prologue_type"] = "prologue_type"
    defaults["tabset"] = "tabset"
    defaults["chapter_image"] = "chapter_image"
    defaults["chapter_use"] = "chapter_use"
    defaults["offline_file"] = "offline_file"
    defaults["pre_test_type"] = "pre_test_type"
    defaults["post_test_type"] = "post_test_type"
    defaults["level1_avg"] = "level1_avg"
    defaults["level2_avg"] = "level2_avg"
    defaults["level3_avg"] = "level3_avg"
    defaults["level1_hard_avg"] = "level1_hard_avg"
    defaults["level1_medium_avg"] = "level1_medium_avg"
    defaults["level1_easy_avg"] = "level1_easy_avg"
    defaults["level2_hard_avg"] = "level2_hard_avg"
    defaults["level2_medium_avg"] = "level2_medium_avg"
    defaults["level2_easy_avg"] = "level2_easy_avg"
    defaults["level3_hard_avg"] = "level3_hard_avg"
    defaults["level3_medium_avg"] = "level3_medium_avg"
    defaults["level3_easy_avg"] = "level3_easy_avg"
    defaults["homework_count"] = "homework_count"
    defaults["epilogue_type"] = "epilogue_type"
    defaults["epilogue_img"] = "epilogue_img"
    defaults["pbl_flag"] = "pbl_flag"
    defaults["chapter_use_time"] = "chapter_use_time"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    return ChapterInfo.objects.create(**defaults)


def create_chaptercontentsinfo(**kwargs):
    defaults = {}
    defaults["chapter_contents"] = "chapter_contents"
    defaults["chapter_audio"] = "chapter_audio"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["contents_index"] = "contents_index"
    defaults["chapter_type"] = "chapter_type"
    defaults["thum_file"] = "thum_file"
    defaults["vod_file"] = "vod_file"
    defaults["today"] = "today"
    defaults["front1_img"] = "front1_img"
    defaults["front1_text"] = "front1_text"
    defaults["back1_img"] = "back1_img"
    defaults["back1_text"] = "back1_text"
    defaults["pdf_file"] = "pdf_file"
    defaults["front2_img"] = "front2_img"
    defaults["front3_img"] = "front3_img"
    defaults["front4_img"] = "front4_img"
    defaults["front2_text"] = "front2_text"
    defaults["front3_text"] = "front3_text"
    defaults["front4_text"] = "front4_text"
    defaults["back2_img"] = "back2_img"
    defaults["back3_img"] = "back3_img"
    defaults["back4_img"] = "back4_img"
    defaults["back2_text"] = "back2_text"
    defaults["back3_text"] = "back3_text"
    defaults["back4_text"] = "back4_text"
    defaults["c1_audio"] = "c1_audio"
    defaults["c2_audio"] = "c2_audio"
    defaults["c3_audio"] = "c3_audio"
    defaults["c4_audio"] = "c4_audio"
    defaults["vod_size"] = "vod_size"
    defaults["offline_file"] = "offline_file"
    defaults["teacher_guide"] = "teacher_guide"
    defaults["today_text"] = "today_text"
    defaults["contents_text"] = "contents_text"
    defaults["pbl_allow"] = "pbl_allow"
    defaults["pbl_lec_allow"] = "pbl_lec_allow"
    defaults.update(**kwargs)
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return ChapterContentsInfo.objects.create(**defaults)


def create_chaptermissoncheckcard(**kwargs):
    defaults = {}
    defaults["check_card_code"] = "check_card_code"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return ChapterMissonCheckCard.objects.create(**defaults)


def create_chaptermissoncheckitem(**kwargs):
    defaults = {}
    defaults["check_item_code"] = "check_item_code"
    defaults["item_text"] = "item_text"
    defaults["contents_text"] = "contents_text"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "check_card_code" not in defaults:
        defaults["check_card_code"] = create_chaptermissoncheckcard()
    if "chapter_contents_code" not in defaults:
        defaults["chapter_contents_code"] = create_chaptercontentsinfo()
    return ChapterMissonCheckItem.objects.create(**defaults)


def create_inninginfo(**kwargs):
    defaults = {}
    defaults["inning_name"] = "inning_name"
    defaults["start_date"] = "start_date"
    defaults["end_date"] = "end_date"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    return InningInfo.objects.create(**defaults)


def create_omrquestioninfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["question_level"] = "question_level"
    defaults["question_score"] = "question_score"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return OmrQuestionInfo.objects.create(**defaults)


def create_quizinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["quiz_type"] = "quiz_type"
    defaults["quiz_question"] = "quiz_question"
    defaults["quiz_media_type"] = "quiz_media_type"
    defaults["quiz_media_file"] = "quiz_media_file"
    defaults["quiz_score"] = "quiz_score"
    defaults["quiz_comment"] = "quiz_comment"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["quiz_head"] = "quiz_head"
    defaults["quiz_media_file2"] = "quiz_media_file2"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return QuizInfo.objects.create(**defaults)


def create_assignhomeworkinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return AssignHomeworkInfo.objects.create(**defaults)


def create_assignquestioninfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["question_type"] = "question_type"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return AssignQuestionInfo.objects.create(**defaults)


def create_boardinfo(**kwargs):
    defaults = {}
    defaults["board_name"] = "board_name"
    defaults["board_write_level"] = "board_write_level"
    defaults["board_read_level"] = "board_read_level"
    defaults["board_reply_level"] = "board_reply_level"
    defaults["board_new_time"] = "board_new_time"
    defaults["board_create_time"] = "board_create_time"
    defaults["admin_id"] = "admin_id"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    return BoardInfo.objects.create(**defaults)


def create_boardcontentinfo(**kwargs):
    defaults = {}
    defaults["admin_id"] = "admin_id"
    defaults["title"] = "title"
    defaults["contents"] = "contents"
    defaults["writer"] = "writer"
    defaults["view_cnt"] = "view_cnt"
    defaults["ref_code"] = "ref_code"
    defaults["ref_step"] = "ref_step"
    defaults["ref_level"] = "ref_level"
    defaults["write_time"] = "write_time"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "board_code" not in defaults:
        defaults["board_code"] = create_boardinfo()
    return BoardContentInfo.objects.create(**defaults)


def create_inninggroup(**kwargs):
    defaults = {}
    defaults["teacher_code"] = "teacher_code"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    return InningGroup.objects.create(**defaults)


def create_chaptercontentmedia(**kwargs):
    defaults = {}
    defaults["media_type"] = "media_type"
    defaults["media_desc"] = "media_desc"
    defaults["media_filename"] = "media_filename"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "chapter_contents_code" not in defaults:
        defaults["chapter_contents_code"] = create_chaptercontentsinfo()
    return ChapterContentMedia.objects.create(**defaults)


def create_chapterimginfo(**kwargs):
    defaults = {}
    defaults["filename"] = "filename"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return ChapterImgInfo.objects.create(**defaults)


def create_chaptermissoncheck(**kwargs):
    defaults = {}
    defaults["check_code"] = "check_code"
    defaults["student_code"] = "student_code"
    defaults["check_agent_code"] = "check_agent_code"
    defaults["is_check_yn"] = "is_check_yn"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "check_item_code" not in defaults:
        defaults["check_item_code"] = create_chaptermissoncheckitem()
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    return ChapterMissonCheck.objects.create(**defaults)


def create_chapterwrite(**kwargs):
    defaults = {}
    defaults["student_code"] = "student_code"
    defaults["write_content"] = "write_content"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    if "chapter_contents_code" not in defaults:
        defaults["chapter_contents_code"] = create_chaptercontentsinfo()
    return ChapterWrite.objects.create(**defaults)


def create_groupmapping(**kwargs):
    defaults = {}
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    if "group_code" not in defaults:
        defaults["group_code"] = create_inninggroup()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return GroupMapping.objects.create(**defaults)


def create_homeworkinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["level_score"] = "level_score"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["level"] = "level"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return HomeworkInfo.objects.create(**defaults)


def create_learningnote(**kwargs):
    defaults = {}
    defaults["contents_code"] = "contents_code"
    defaults["note_contents"] = "note_contents"
    defaults["note_attachment"] = "note_attachment"
    defaults.update(**kwargs)
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return LearningNote.objects.create(**defaults)


def create_courseubtinfo(**kwargs):
    defaults = {}
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "quiz_code" not in defaults:
        defaults["quiz_code"] = create_quizinfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    return CourseUbtInfo.objects.create(**defaults)


def create_lessoninfo(**kwargs):
    defaults = {}
    defaults["teacher_code"] = "teacher_code"
    defaults["start_date"] = "start_date"
    defaults["end_date"] = "end_date"
    defaults["progress"] = "progress"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["ubt_start"] = "ubt_start"
    defaults["ubt_end"] = "ubt_end"
    defaults["download_count"] = "download_count"
    defaults["download_date"] = "download_date"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    return LessonInfo.objects.create(**defaults)


def create_lessonlog(**kwargs):
    defaults = {}
    defaults["member_id"] = "member_id"
    defaults["member_ip"] = "member_ip"
    defaults["member_browser"] = "member_browser"
    defaults["member_os"] = "member_os"
    defaults["start_date"] = "start_date"
    defaults["start_time"] = "start_time"
    defaults["end_date"] = "end_date"
    defaults["end_time"] = "end_time"
    defaults["connect_date"] = "connect_date"
    defaults["connect_time"] = "connect_time"
    defaults["connect_count"] = "connect_count"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["study_time"] = "study_time"
    defaults["connect_page"] = "connect_page"
    defaults.update(**kwargs)
    if "lesson_code" not in defaults:
        defaults["lesson_code"] = create_lessoninfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return LessonLog.objects.create(**defaults)


def create_membergroup(**kwargs):
    defaults = {}
    defaults["group_name"] = "group_name"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "center_code" not in defaults:
        defaults["center_code"] = create_centerinfo()
    return MemberGroup.objects.create(**defaults)


def create_messageinfo(**kwargs):
    defaults = {}
    defaults["teacher_code"] = "teacher_code"
    defaults["message"] = "message"
    defaults["message_read"] = "message_read"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return MessageInfo.objects.create(**defaults)


def create_omranswerinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["omr_answer"] = "omr_answer"
    defaults["omr_answer_idx"] = "omr_answer_idx"
    defaults["omr_answer_correct"] = "omr_answer_correct"
    defaults["question_score"] = "question_score"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "lesson_code" not in defaults:
        defaults["lesson_code"] = create_lessoninfo()
    return OmrAnswerInfo.objects.create(**defaults)


def create_omrassigninfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return OmrAssignInfo.objects.create(**defaults)


def create_omrexampleinfo(**kwargs):
    defaults = {}
    defaults["omr_example_correct"] = "omr_example_correct"
    defaults["omr_example_idx"] = "omr_example_idx"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    return OmrExampleInfo.objects.create(**defaults)


def create_qanswerinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["question_type"] = "question_type"
    defaults["question_answer"] = "question_answer"
    defaults["question_idx"] = "question_idx"
    defaults["question_correct"] = "question_correct"
    defaults["question_score"] = "question_score"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    if "lesson_code" not in defaults:
        defaults["lesson_code"] = create_lessoninfo()
    return QAnswerInfo.objects.create(**defaults)


def create_qanswerlog(**kwargs):
    defaults = {}
    defaults["question_answer"] = "question_answer"
    defaults["question_idx"] = "question_idx"
    defaults["question_score"] = "question_score"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    return QAnswerLog.objects.create(**defaults)


def create_qexampleinfo(**kwargs):
    defaults = {}
    defaults["q_example"] = "q_example"
    defaults["q_example_correct"] = "q_example_correct"
    defaults["q_example_idx"] = "q_example_idx"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["q_example_type"] = "q_example_type"
    defaults.update(**kwargs)
    if "question_code" not in defaults:
        defaults["question_code"] = create_omrquestioninfo()
    return QExampleInfo.objects.create(**defaults)


def create_questioninfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["question_type"] = "question_type"
    defaults["question"] = "question"
    defaults["question_media_type"] = "question_media_type"
    defaults["question_media_file"] = "question_media_file"
    defaults["question_score"] = "question_score"
    defaults["question_head"] = "question_head"
    defaults["question_essay"] = "question_essay"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["question_media_file2"] = "question_media_file2"
    defaults["question_comment"] = "question_comment"
    defaults["question_level"] = "question_level"
    defaults["teacher_contents"] = "teacher_contents"
    defaults["student_contents"] = "student_contents"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    return QuestionInfo.objects.create(**defaults)


def create_quizanswerinfo(**kwargs):
    defaults = {}
    defaults["subject_code"] = "subject_code"
    defaults["quiz_type"] = "quiz_type"
    defaults["quiz_answer"] = "quiz_answer"
    defaults["quiz_answer_idx"] = "quiz_answer_idx"
    defaults["quiz_correct"] = "quiz_correct"
    defaults["quiz_score"] = "quiz_score"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["test_type"] = "test_type"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "quiz_code" not in defaults:
        defaults["quiz_code"] = create_quizinfo()
    return QuizAnswerInfo.objects.create(**defaults)


def create_quizexampleinfo(**kwargs):
    defaults = {}
    defaults["quiz_example"] = "quiz_example"
    defaults["quiz_example_correct"] = "quiz_example_correct"
    defaults["quiz_example_idx"] = "quiz_example_idx"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["quiz_example_type"] = "quiz_example_type"
    defaults.update(**kwargs)
    if "quiz_code" not in defaults:
        defaults["quiz_code"] = create_quizinfo()
    return QuizExampleInfo.objects.create(**defaults)


def create_scheduleinfo(**kwargs):
    defaults = {}
    defaults["title"] = "title"
    defaults["content"] = "content"
    defaults["start_date"] = "start_date"
    defaults["start_time"] = "start_time"
    defaults["end_date"] = "end_date"
    defaults["end_time"] = "end_time"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return ScheduleInfo.objects.create(**defaults)


def create_talkmember(**kwargs):
    defaults = {}
    defaults["use_flag"] = "use_flag"
    defaults.update(**kwargs)
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return TalkMember.objects.create(**defaults)


def create_talkroom(**kwargs):
    defaults = {}
    defaults["talk_room_cate_code"] = "talk_room_cate_code"
    defaults["use_flag"] = "use_flag"
    defaults.update(**kwargs)
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    if "inning_code" not in defaults:
        defaults["inning_code"] = create_inninginfo()
    return TalkRoom.objects.create(**defaults)


def create_talkmessage(**kwargs):
    defaults = {}
    defaults["message"] = "message"
    defaults["sender_member_code"] = "sender_member_code"
    defaults["send_date"] = "send_date"
    defaults["send_time"] = "send_time"
    defaults.update(**kwargs)
    if "talk_room_id" not in defaults:
        defaults["talk_room_id"] = create_talkroom()
    return TalkMessage.objects.create(**defaults)


def create_talkmessageread(**kwargs):
    defaults = {}
    defaults["is_read"] = "is_read"
    defaults.update(**kwargs)
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return TalkMessageRead.objects.create(**defaults)


def create_todoinfo(**kwargs):
    defaults = {}
    defaults["todo_comment"] = "todo_comment"
    defaults["todo_status"] = "todo_status"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults["teacher_code"] = "teacher_code"
    defaults["todo_title"] = "todo_title"
    defaults["start_date"] = "start_date"
    defaults["start_time"] = "start_time"
    defaults["end_date"] = "end_date"
    defaults["end_time"] = "end_time"
    defaults.update(**kwargs)
    if "chapter_code" not in defaults:
        defaults["chapter_code"] = create_chapterinfo()
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    if "course_code" not in defaults:
        defaults["course_code"] = create_courseinfo()
    return TodoInfo.objects.create(**defaults)


def create_todotinfo(**kwargs):
    defaults = {}
    defaults["todo_code"] = "todo_code"
    defaults["todo_t_flag"] = "todo_t_flag"
    defaults["use_flag"] = "use_flag"
    defaults["reg_date"] = "reg_date"
    defaults["reg_time"] = "reg_time"
    defaults["reg_agent"] = "reg_agent"
    defaults["udt_date"] = "udt_date"
    defaults["udt_time"] = "udt_time"
    defaults["udt_agent"] = "udt_agent"
    defaults.update(**kwargs)
    if "member_code" not in defaults:
        defaults["member_code"] = create_memberinfo()
    return TodoTInfo.objects.create(**defaults)


class ProfileViewTest(unittest.TestCase):
    '''
    Tests for Profile
    '''
    def setUp(self):
        self.client = Client()

    def test_list_profile(self):
        url = reverse('profile_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_profile(self):
        url = reverse('profile_create')
        data = {
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_profile(self):
        profile = create_profile()
        url = reverse('profile_detail', args=[profile.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        profile = create_profile()
        data = {
        }
        url = reverse('profile_update', args=[profile.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CenterInfoViewTest(unittest.TestCase):
    '''
    Tests for CenterInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_centerinfo(self):
        url = reverse('centerinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_centerinfo(self):
        url = reverse('centerinfo_create')
        data = {
            "Center_Name": "Center_Name",
            "Center_Address": "Center_Address",
            "Use_Flag": "Use_Flag",
            "Register_DateTime": "Register_DateTime",
            "Register_Agent": "Register_Agent",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_centerinfo(self):
        centerinfo = create_centerinfo()
        url = reverse('centerinfo_detail', args=[centerinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_centerinfo(self):
        centerinfo = create_centerinfo()
        data = {
            "Center_Name": "Center_Name",
            "Center_Address": "Center_Address",
            "Use_Flag": "Use_Flag",
            "Register_DateTime": "Register_DateTime",
            "Register_Agent": "Register_Agent",
        }
        url = reverse('centerinfo_update', args=[centerinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MemberInfoViewTest(unittest.TestCase):
    '''
    Tests for MemberInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_memberinfo(self):
        url = reverse('memberinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_memberinfo(self):
        url = reverse('memberinfo_create')
        data = {
            "Member_ID": "Member_ID",
            "Member_Password": "Member_Password",
            "Member_Type": "Member_Type",
            "Member_Name": "Member_Name",
            "Member_Permanent_Address": "Member_Permanent_Address",
            "Member_Temporary_Address": "Member_Temporary_Address",
            "Member_BirthDate": "Member_BirthDate",
            "Member_Email": "Member_Email",
            "Member_Phone": "Member_Phone",
            "forum_avatar": "forum_avatar",
            "member_Gender": "member_Gender",
            "Use_Flag": "Use_Flag",
            "Register_DateTime": "Register_DateTime",
            "Register_Agent": "Register_Agent",
            "Member_Memo": "Member_Memo",
            "center_code": create_centerinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_memberinfo(self):
        memberinfo = create_memberinfo()
        url = reverse('memberinfo_detail', args=[memberinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_memberinfo(self):
        memberinfo = create_memberinfo()
        data = {
            "Member_ID": "Member_ID",
            "Member_Password": "Member_Password",
            "Member_Type": "Member_Type",
            "Member_Name": "Member_Name",
            "Member_Permanent_Address": "Member_Permanent_Address",
            "Member_Temporary_Address": "Member_Temporary_Address",
            "Member_BirthDate": "Member_BirthDate",
            "Member_Email": "Member_Email",
            "Member_Phone": "Member_Phone",
            "forum_avatar": "forum_avatar",
            "member_Gender": "member_Gender",
            "Use_Flag": "Use_Flag",
            "Register_DateTime": "Register_DateTime",
            "Register_Agent": "Register_Agent",
            "Member_Memo": "Member_Memo",
            "center_code": create_centerinfo().pk,
        }
        url = reverse('memberinfo_update', args=[memberinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CourseInfoViewTest(unittest.TestCase):
    '''
    Tests for CourseInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_courseinfo(self):
        url = reverse('courseinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_courseinfo(self):
        url = reverse('courseinfo_create')
        data = {
            "course_name": "course_name",
            "course_teacher": "course_teacher",
            "course_cover": "course_cover",
            "course_cover_file": "course_cover_file",
            "course_level": "course_level",
            "course_info": "course_info",
            "teacher": "teacher",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_certification": "course_certification",
            "course_provider": "course_provider",
            "cert_crit_prog": "cert_crit_prog",
            "cert_crit_post": "cert_crit_post",
            "cert_crit_ubt": "cert_crit_ubt",
            "cert_crit_issue": "cert_crit_issue",
            "center_code": create_centerinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_courseinfo(self):
        courseinfo = create_courseinfo()
        url = reverse('courseinfo_detail', args=[courseinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_courseinfo(self):
        courseinfo = create_courseinfo()
        data = {
            "course_name": "course_name",
            "course_teacher": "course_teacher",
            "course_cover": "course_cover",
            "course_cover_file": "course_cover_file",
            "course_level": "course_level",
            "course_info": "course_info",
            "teacher": "teacher",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_certification": "course_certification",
            "course_provider": "course_provider",
            "cert_crit_prog": "cert_crit_prog",
            "cert_crit_post": "cert_crit_post",
            "cert_crit_ubt": "cert_crit_ubt",
            "cert_crit_issue": "cert_crit_issue",
            "center_code": create_centerinfo().pk,
        }
        url = reverse('courseinfo_update', args=[courseinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterInfoViewTest(unittest.TestCase):
    '''
    Tests for ChapterInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chapterinfo(self):
        url = reverse('chapterinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chapterinfo(self):
        url = reverse('chapterinfo_create')
        data = {
            "chapter_no": "chapter_no",
            "chapter_name": "chapter_name",
            "topic": "topic",
            "summary": "summary",
            "page_num": "page_num",
            "vod_size": "vod_size",
            "intro": "intro",
            "target": "target",
            "top_img": "top_img",
            "bottom_img1": "bottom_img1",
            "bottom_img2": "bottom_img2",
            "bottom_img3": "bottom_img3",
            "thum_file": "thum_file",
            "vod_file": "vod_file",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "today": "today",
            "chapter_type": "chapter_type",
            "prologue_type": "prologue_type",
            "tabset": "tabset",
            "chapter_image": "chapter_image",
            "chapter_use": "chapter_use",
            "offline_file": "offline_file",
            "pre_test_type": "pre_test_type",
            "post_test_type": "post_test_type",
            "level1_avg": "level1_avg",
            "level2_avg": "level2_avg",
            "level3_avg": "level3_avg",
            "level1_hard_avg": "level1_hard_avg",
            "level1_medium_avg": "level1_medium_avg",
            "level1_easy_avg": "level1_easy_avg",
            "level2_hard_avg": "level2_hard_avg",
            "level2_medium_avg": "level2_medium_avg",
            "level2_easy_avg": "level2_easy_avg",
            "level3_hard_avg": "level3_hard_avg",
            "level3_medium_avg": "level3_medium_avg",
            "level3_easy_avg": "level3_easy_avg",
            "homework_count": "homework_count",
            "epilogue_type": "epilogue_type",
            "epilogue_img": "epilogue_img",
            "pbl_flag": "pbl_flag",
            "chapter_use_time": "chapter_use_time",
            "course_code": create_courseinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chapterinfo(self):
        chapterinfo = create_chapterinfo()
        url = reverse('chapterinfo_detail', args=[chapterinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chapterinfo(self):
        chapterinfo = create_chapterinfo()
        data = {
            "chapter_no": "chapter_no",
            "chapter_name": "chapter_name",
            "topic": "topic",
            "summary": "summary",
            "page_num": "page_num",
            "vod_size": "vod_size",
            "intro": "intro",
            "target": "target",
            "top_img": "top_img",
            "bottom_img1": "bottom_img1",
            "bottom_img2": "bottom_img2",
            "bottom_img3": "bottom_img3",
            "thum_file": "thum_file",
            "vod_file": "vod_file",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "today": "today",
            "chapter_type": "chapter_type",
            "prologue_type": "prologue_type",
            "tabset": "tabset",
            "chapter_image": "chapter_image",
            "chapter_use": "chapter_use",
            "offline_file": "offline_file",
            "pre_test_type": "pre_test_type",
            "post_test_type": "post_test_type",
            "level1_avg": "level1_avg",
            "level2_avg": "level2_avg",
            "level3_avg": "level3_avg",
            "level1_hard_avg": "level1_hard_avg",
            "level1_medium_avg": "level1_medium_avg",
            "level1_easy_avg": "level1_easy_avg",
            "level2_hard_avg": "level2_hard_avg",
            "level2_medium_avg": "level2_medium_avg",
            "level2_easy_avg": "level2_easy_avg",
            "level3_hard_avg": "level3_hard_avg",
            "level3_medium_avg": "level3_medium_avg",
            "level3_easy_avg": "level3_easy_avg",
            "homework_count": "homework_count",
            "epilogue_type": "epilogue_type",
            "epilogue_img": "epilogue_img",
            "pbl_flag": "pbl_flag",
            "chapter_use_time": "chapter_use_time",
            "course_code": create_courseinfo().pk,
        }
        url = reverse('chapterinfo_update', args=[chapterinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterContentsInfoViewTest(unittest.TestCase):
    '''
    Tests for ChapterContentsInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chaptercontentsinfo(self):
        url = reverse('chaptercontentsinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chaptercontentsinfo(self):
        url = reverse('chaptercontentsinfo_create')
        data = {
            "chapter_contents": "chapter_contents",
            "chapter_audio": "chapter_audio",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "contents_index": "contents_index",
            "chapter_type": "chapter_type",
            "thum_file": "thum_file",
            "vod_file": "vod_file",
            "today": "today",
            "front1_img": "front1_img",
            "front1_text": "front1_text",
            "back1_img": "back1_img",
            "back1_text": "back1_text",
            "pdf_file": "pdf_file",
            "front2_img": "front2_img",
            "front3_img": "front3_img",
            "front4_img": "front4_img",
            "front2_text": "front2_text",
            "front3_text": "front3_text",
            "front4_text": "front4_text",
            "back2_img": "back2_img",
            "back3_img": "back3_img",
            "back4_img": "back4_img",
            "back2_text": "back2_text",
            "back3_text": "back3_text",
            "back4_text": "back4_text",
            "c1_audio": "c1_audio",
            "c2_audio": "c2_audio",
            "c3_audio": "c3_audio",
            "c4_audio": "c4_audio",
            "vod_size": "vod_size",
            "offline_file": "offline_file",
            "teacher_guide": "teacher_guide",
            "today_text": "today_text",
            "contents_text": "contents_text",
            "pbl_allow": "pbl_allow",
            "pbl_lec_allow": "pbl_lec_allow",
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chaptercontentsinfo(self):
        chaptercontentsinfo = create_chaptercontentsinfo()
        url = reverse('chaptercontentsinfo_detail', args=[chaptercontentsinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chaptercontentsinfo(self):
        chaptercontentsinfo = create_chaptercontentsinfo()
        data = {
            "chapter_contents": "chapter_contents",
            "chapter_audio": "chapter_audio",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "contents_index": "contents_index",
            "chapter_type": "chapter_type",
            "thum_file": "thum_file",
            "vod_file": "vod_file",
            "today": "today",
            "front1_img": "front1_img",
            "front1_text": "front1_text",
            "back1_img": "back1_img",
            "back1_text": "back1_text",
            "pdf_file": "pdf_file",
            "front2_img": "front2_img",
            "front3_img": "front3_img",
            "front4_img": "front4_img",
            "front2_text": "front2_text",
            "front3_text": "front3_text",
            "front4_text": "front4_text",
            "back2_img": "back2_img",
            "back3_img": "back3_img",
            "back4_img": "back4_img",
            "back2_text": "back2_text",
            "back3_text": "back3_text",
            "back4_text": "back4_text",
            "c1_audio": "c1_audio",
            "c2_audio": "c2_audio",
            "c3_audio": "c3_audio",
            "c4_audio": "c4_audio",
            "vod_size": "vod_size",
            "offline_file": "offline_file",
            "teacher_guide": "teacher_guide",
            "today_text": "today_text",
            "contents_text": "contents_text",
            "pbl_allow": "pbl_allow",
            "pbl_lec_allow": "pbl_lec_allow",
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('chaptercontentsinfo_update', args=[chaptercontentsinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterMissonCheckCardViewTest(unittest.TestCase):
    '''
    Tests for ChapterMissonCheckCard
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chaptermissoncheckcard(self):
        url = reverse('chaptermissoncheckcard_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chaptermissoncheckcard(self):
        url = reverse('chaptermissoncheckcard_create')
        data = {
            "check_card_code": "check_card_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chaptermissoncheckcard(self):
        chaptermissoncheckcard = create_chaptermissoncheckcard()
        url = reverse('chaptermissoncheckcard_detail', args=[chaptermissoncheckcard.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chaptermissoncheckcard(self):
        chaptermissoncheckcard = create_chaptermissoncheckcard()
        data = {
            "check_card_code": "check_card_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('chaptermissoncheckcard_update', args=[chaptermissoncheckcard.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterMissonCheckItemViewTest(unittest.TestCase):
    '''
    Tests for ChapterMissonCheckItem
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chaptermissoncheckitem(self):
        url = reverse('chaptermissoncheckitem_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chaptermissoncheckitem(self):
        url = reverse('chaptermissoncheckitem_create')
        data = {
            "check_item_code": "check_item_code",
            "item_text": "item_text",
            "contents_text": "contents_text",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "check_card_code": create_chaptermissoncheckcard().pk,
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chaptermissoncheckitem(self):
        chaptermissoncheckitem = create_chaptermissoncheckitem()
        url = reverse('chaptermissoncheckitem_detail', args=[chaptermissoncheckitem.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chaptermissoncheckitem(self):
        chaptermissoncheckitem = create_chaptermissoncheckitem()
        data = {
            "check_item_code": "check_item_code",
            "item_text": "item_text",
            "contents_text": "contents_text",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "check_card_code": create_chaptermissoncheckcard().pk,
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        url = reverse('chaptermissoncheckitem_update', args=[chaptermissoncheckitem.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class InningInfoViewTest(unittest.TestCase):
    '''
    Tests for InningInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_inninginfo(self):
        url = reverse('inninginfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_inninginfo(self):
        url = reverse('inninginfo_create')
        data = {
            "inning_name": "inning_name",
            "start_date": "start_date",
            "end_date": "end_date",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "center_code": create_centerinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_inninginfo(self):
        inninginfo = create_inninginfo()
        url = reverse('inninginfo_detail', args=[inninginfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_inninginfo(self):
        inninginfo = create_inninginfo()
        data = {
            "inning_name": "inning_name",
            "start_date": "start_date",
            "end_date": "end_date",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "center_code": create_centerinfo().pk,
        }
        url = reverse('inninginfo_update', args=[inninginfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class OmrQuestionInfoViewTest(unittest.TestCase):
    '''
    Tests for OmrQuestionInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_omrquestioninfo(self):
        url = reverse('omrquestioninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_omrquestioninfo(self):
        url = reverse('omrquestioninfo_create')
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_level": "question_level",
            "question_score": "question_score",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_omrquestioninfo(self):
        omrquestioninfo = create_omrquestioninfo()
        url = reverse('omrquestioninfo_detail', args=[omrquestioninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_omrquestioninfo(self):
        omrquestioninfo = create_omrquestioninfo()
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_level": "question_level",
            "question_score": "question_score",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('omrquestioninfo_update', args=[omrquestioninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuizInfoViewTest(unittest.TestCase):
    '''
    Tests for QuizInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_quizinfo(self):
        url = reverse('quizinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_quizinfo(self):
        url = reverse('quizinfo_create')
        data = {
            "subject_code": "subject_code",
            "quiz_type": "quiz_type",
            "quiz_question": "quiz_question",
            "quiz_media_type": "quiz_media_type",
            "quiz_media_file": "quiz_media_file",
            "quiz_score": "quiz_score",
            "quiz_comment": "quiz_comment",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_head": "quiz_head",
            "quiz_media_file2": "quiz_media_file2",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_quizinfo(self):
        quizinfo = create_quizinfo()
        url = reverse('quizinfo_detail', args=[quizinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_quizinfo(self):
        quizinfo = create_quizinfo()
        data = {
            "subject_code": "subject_code",
            "quiz_type": "quiz_type",
            "quiz_question": "quiz_question",
            "quiz_media_type": "quiz_media_type",
            "quiz_media_file": "quiz_media_file",
            "quiz_score": "quiz_score",
            "quiz_comment": "quiz_comment",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_head": "quiz_head",
            "quiz_media_file2": "quiz_media_file2",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('quizinfo_update', args=[quizinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AssignHomeworkInfoViewTest(unittest.TestCase):
    '''
    Tests for AssignHomeworkInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_assignhomeworkinfo(self):
        url = reverse('assignhomeworkinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_assignhomeworkinfo(self):
        url = reverse('assignhomeworkinfo_create')
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_assignhomeworkinfo(self):
        assignhomeworkinfo = create_assignhomeworkinfo()
        url = reverse('assignhomeworkinfo_detail', args=[assignhomeworkinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_assignhomeworkinfo(self):
        assignhomeworkinfo = create_assignhomeworkinfo()
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        url = reverse('assignhomeworkinfo_update', args=[assignhomeworkinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AssignQuestionInfoViewTest(unittest.TestCase):
    '''
    Tests for AssignQuestionInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_assignquestioninfo(self):
        url = reverse('assignquestioninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_assignquestioninfo(self):
        url = reverse('assignquestioninfo_create')
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_assignquestioninfo(self):
        assignquestioninfo = create_assignquestioninfo()
        url = reverse('assignquestioninfo_detail', args=[assignquestioninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_assignquestioninfo(self):
        assignquestioninfo = create_assignquestioninfo()
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('assignquestioninfo_update', args=[assignquestioninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class BoardInfoViewTest(unittest.TestCase):
    '''
    Tests for BoardInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_boardinfo(self):
        url = reverse('boardinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_boardinfo(self):
        url = reverse('boardinfo_create')
        data = {
            "board_name": "board_name",
            "board_write_level": "board_write_level",
            "board_read_level": "board_read_level",
            "board_reply_level": "board_reply_level",
            "board_new_time": "board_new_time",
            "board_create_time": "board_create_time",
            "admin_id": "admin_id",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_boardinfo(self):
        boardinfo = create_boardinfo()
        url = reverse('boardinfo_detail', args=[boardinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_boardinfo(self):
        boardinfo = create_boardinfo()
        data = {
            "board_name": "board_name",
            "board_write_level": "board_write_level",
            "board_read_level": "board_read_level",
            "board_reply_level": "board_reply_level",
            "board_new_time": "board_new_time",
            "board_create_time": "board_create_time",
            "admin_id": "admin_id",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
        }
        url = reverse('boardinfo_update', args=[boardinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class BoardContentInfoViewTest(unittest.TestCase):
    '''
    Tests for BoardContentInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_boardcontentinfo(self):
        url = reverse('boardcontentinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_boardcontentinfo(self):
        url = reverse('boardcontentinfo_create')
        data = {
            "admin_id": "admin_id",
            "title": "title",
            "contents": "contents",
            "writer": "writer",
            "view_cnt": "view_cnt",
            "ref_code": "ref_code",
            "ref_step": "ref_step",
            "ref_level": "ref_level",
            "write_time": "write_time",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "board_code": create_boardinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_boardcontentinfo(self):
        boardcontentinfo = create_boardcontentinfo()
        url = reverse('boardcontentinfo_detail', args=[boardcontentinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_boardcontentinfo(self):
        boardcontentinfo = create_boardcontentinfo()
        data = {
            "admin_id": "admin_id",
            "title": "title",
            "contents": "contents",
            "writer": "writer",
            "view_cnt": "view_cnt",
            "ref_code": "ref_code",
            "ref_step": "ref_step",
            "ref_level": "ref_level",
            "write_time": "write_time",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "board_code": create_boardinfo().pk,
        }
        url = reverse('boardcontentinfo_update', args=[boardcontentinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class InningGroupViewTest(unittest.TestCase):
    '''
    Tests for InningGroup
    '''
    def setUp(self):
        self.client = Client()

    def test_list_inninggroup(self):
        url = reverse('inninggroup_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_inninggroup(self):
        url = reverse('inninggroup_create')
        data = {
            "teacher_code": "teacher_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
            "inning_code": create_inninginfo().pk,
            "course_code": create_courseinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_inninggroup(self):
        inninggroup = create_inninggroup()
        url = reverse('inninggroup_detail', args=[inninggroup.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_inninggroup(self):
        inninggroup = create_inninggroup()
        data = {
            "teacher_code": "teacher_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
            "inning_code": create_inninginfo().pk,
            "course_code": create_courseinfo().pk,
        }
        url = reverse('inninggroup_update', args=[inninggroup.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterContentMediaViewTest(unittest.TestCase):
    '''
    Tests for ChapterContentMedia
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chaptercontentmedia(self):
        url = reverse('chaptercontentmedia_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chaptercontentmedia(self):
        url = reverse('chaptercontentmedia_create')
        data = {
            "media_type": "media_type",
            "media_desc": "media_desc",
            "media_filename": "media_filename",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "reg_agent": "reg_agent",
            "udt_agent": "udt_agent",
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chaptercontentmedia(self):
        chaptercontentmedia = create_chaptercontentmedia()
        url = reverse('chaptercontentmedia_detail', args=[chaptercontentmedia.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chaptercontentmedia(self):
        chaptercontentmedia = create_chaptercontentmedia()
        data = {
            "media_type": "media_type",
            "media_desc": "media_desc",
            "media_filename": "media_filename",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "reg_agent": "reg_agent",
            "udt_agent": "udt_agent",
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        url = reverse('chaptercontentmedia_update', args=[chaptercontentmedia.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterImgInfoViewTest(unittest.TestCase):
    '''
    Tests for ChapterImgInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chapterimginfo(self):
        url = reverse('chapterimginfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chapterimginfo(self):
        url = reverse('chapterimginfo_create')
        data = {
            "filename": "filename",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chapterimginfo(self):
        chapterimginfo = create_chapterimginfo()
        url = reverse('chapterimginfo_detail', args=[chapterimginfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chapterimginfo(self):
        chapterimginfo = create_chapterimginfo()
        data = {
            "filename": "filename",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('chapterimginfo_update', args=[chapterimginfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterMissonCheckViewTest(unittest.TestCase):
    '''
    Tests for ChapterMissonCheck
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chaptermissoncheck(self):
        url = reverse('chaptermissoncheck_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chaptermissoncheck(self):
        url = reverse('chaptermissoncheck_create')
        data = {
            "check_code": "check_code",
            "student_code": "student_code",
            "check_agent_code": "check_agent_code",
            "is_check_yn": "is_check_yn",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "check_item_code": create_chaptermissoncheckitem().pk,
            "inning_code": create_inninginfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chaptermissoncheck(self):
        chaptermissoncheck = create_chaptermissoncheck()
        url = reverse('chaptermissoncheck_detail', args=[chaptermissoncheck.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chaptermissoncheck(self):
        chaptermissoncheck = create_chaptermissoncheck()
        data = {
            "check_code": "check_code",
            "student_code": "student_code",
            "check_agent_code": "check_agent_code",
            "is_check_yn": "is_check_yn",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "check_item_code": create_chaptermissoncheckitem().pk,
            "inning_code": create_inninginfo().pk,
        }
        url = reverse('chaptermissoncheck_update', args=[chaptermissoncheck.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ChapterWriteViewTest(unittest.TestCase):
    '''
    Tests for ChapterWrite
    '''
    def setUp(self):
        self.client = Client()

    def test_list_chapterwrite(self):
        url = reverse('chapterwrite_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_chapterwrite(self):
        url = reverse('chapterwrite_create')
        data = {
            "student_code": "student_code",
            "write_content": "write_content",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "inning_code": create_inninginfo().pk,
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_chapterwrite(self):
        chapterwrite = create_chapterwrite()
        url = reverse('chapterwrite_detail', args=[chapterwrite.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_chapterwrite(self):
        chapterwrite = create_chapterwrite()
        data = {
            "student_code": "student_code",
            "write_content": "write_content",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "inning_code": create_inninginfo().pk,
            "chapter_contents_code": create_chaptercontentsinfo().pk,
        }
        url = reverse('chapterwrite_update', args=[chapterwrite.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class GroupMappingViewTest(unittest.TestCase):
    '''
    Tests for GroupMapping
    '''
    def setUp(self):
        self.client = Client()

    def test_list_groupmapping(self):
        url = reverse('groupmapping_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_groupmapping(self):
        url = reverse('groupmapping_create')
        data = {
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
            "group_code": create_inninggroup().pk,
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_groupmapping(self):
        groupmapping = create_groupmapping()
        url = reverse('groupmapping_detail', args=[groupmapping.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_groupmapping(self):
        groupmapping = create_groupmapping()
        data = {
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
            "group_code": create_inninggroup().pk,
            "member_code": create_memberinfo().pk,
        }
        url = reverse('groupmapping_update', args=[groupmapping.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class HomeworkInfoViewTest(unittest.TestCase):
    '''
    Tests for HomeworkInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_homeworkinfo(self):
        url = reverse('homeworkinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_homeworkinfo(self):
        url = reverse('homeworkinfo_create')
        data = {
            "subject_code": "subject_code",
            "level_score": "level_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "level": "level",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_homeworkinfo(self):
        homeworkinfo = create_homeworkinfo()
        url = reverse('homeworkinfo_detail', args=[homeworkinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_homeworkinfo(self):
        homeworkinfo = create_homeworkinfo()
        data = {
            "subject_code": "subject_code",
            "level_score": "level_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "level": "level",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('homeworkinfo_update', args=[homeworkinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LearningNoteViewTest(unittest.TestCase):
    '''
    Tests for LearningNote
    '''
    def setUp(self):
        self.client = Client()

    def test_list_learningnote(self):
        url = reverse('learningnote_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_learningnote(self):
        url = reverse('learningnote_create')
        data = {
            "contents_code": "contents_code",
            "note_contents": "note_contents",
            "note_attachment": "note_attachment",
            "inning_code": create_inninginfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_learningnote(self):
        learningnote = create_learningnote()
        url = reverse('learningnote_detail', args=[learningnote.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_learningnote(self):
        learningnote = create_learningnote()
        data = {
            "contents_code": "contents_code",
            "note_contents": "note_contents",
            "note_attachment": "note_attachment",
            "inning_code": create_inninginfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('learningnote_update', args=[learningnote.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CourseUbtInfoViewTest(unittest.TestCase):
    '''
    Tests for CourseUbtInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_courseubtinfo(self):
        url = reverse('courseubtinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_courseubtinfo(self):
        url = reverse('courseubtinfo_create')
        data = {
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_code": create_quizinfo().pk,
            "course_code": create_courseinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_courseubtinfo(self):
        courseubtinfo = create_courseubtinfo()
        url = reverse('courseubtinfo_detail', args=[courseubtinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_courseubtinfo(self):
        courseubtinfo = create_courseubtinfo()
        data = {
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_code": create_quizinfo().pk,
            "course_code": create_courseinfo().pk,
        }
        url = reverse('courseubtinfo_update', args=[courseubtinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LessonInfoViewTest(unittest.TestCase):
    '''
    Tests for LessonInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_lessoninfo(self):
        url = reverse('lessoninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_lessoninfo(self):
        url = reverse('lessoninfo_create')
        data = {
            "teacher_code": "teacher_code",
            "start_date": "start_date",
            "end_date": "end_date",
            "progress": "progress",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "ubt_start": "ubt_start",
            "ubt_end": "ubt_end",
            "download_count": "download_count",
            "download_date": "download_date",
            "course_code": create_courseinfo().pk,
            "member_code": create_memberinfo().pk,
            "center_code": create_centerinfo().pk,
            "inning_code": create_inninginfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_lessoninfo(self):
        lessoninfo = create_lessoninfo()
        url = reverse('lessoninfo_detail', args=[lessoninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_lessoninfo(self):
        lessoninfo = create_lessoninfo()
        data = {
            "teacher_code": "teacher_code",
            "start_date": "start_date",
            "end_date": "end_date",
            "progress": "progress",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "ubt_start": "ubt_start",
            "ubt_end": "ubt_end",
            "download_count": "download_count",
            "download_date": "download_date",
            "course_code": create_courseinfo().pk,
            "member_code": create_memberinfo().pk,
            "center_code": create_centerinfo().pk,
            "inning_code": create_inninginfo().pk,
        }
        url = reverse('lessoninfo_update', args=[lessoninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LessonLogViewTest(unittest.TestCase):
    '''
    Tests for LessonLog
    '''
    def setUp(self):
        self.client = Client()

    def test_list_lessonlog(self):
        url = reverse('lessonlog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_lessonlog(self):
        url = reverse('lessonlog_create')
        data = {
            "member_id": "member_id",
            "member_ip": "member_ip",
            "member_browser": "member_browser",
            "member_os": "member_os",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "connect_date": "connect_date",
            "connect_time": "connect_time",
            "connect_count": "connect_count",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "study_time": "study_time",
            "connect_page": "connect_page",
            "lesson_code": create_lessoninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_lessonlog(self):
        lessonlog = create_lessonlog()
        url = reverse('lessonlog_detail', args=[lessonlog.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_lessonlog(self):
        lessonlog = create_lessonlog()
        data = {
            "member_id": "member_id",
            "member_ip": "member_ip",
            "member_browser": "member_browser",
            "member_os": "member_os",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "connect_date": "connect_date",
            "connect_time": "connect_time",
            "connect_count": "connect_count",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "study_time": "study_time",
            "connect_page": "connect_page",
            "lesson_code": create_lessoninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        url = reverse('lessonlog_update', args=[lessonlog.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MemberGroupViewTest(unittest.TestCase):
    '''
    Tests for MemberGroup
    '''
    def setUp(self):
        self.client = Client()

    def test_list_membergroup(self):
        url = reverse('membergroup_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_membergroup(self):
        url = reverse('membergroup_create')
        data = {
            "group_name": "group_name",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_membergroup(self):
        membergroup = create_membergroup()
        url = reverse('membergroup_detail', args=[membergroup.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_membergroup(self):
        membergroup = create_membergroup()
        data = {
            "group_name": "group_name",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "center_code": create_centerinfo().pk,
        }
        url = reverse('membergroup_update', args=[membergroup.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MessageInfoViewTest(unittest.TestCase):
    '''
    Tests for MessageInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_messageinfo(self):
        url = reverse('messageinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_messageinfo(self):
        url = reverse('messageinfo_create')
        data = {
            "teacher_code": "teacher_code",
            "message": "message",
            "message_read": "message_read",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_messageinfo(self):
        messageinfo = create_messageinfo()
        url = reverse('messageinfo_detail', args=[messageinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_messageinfo(self):
        messageinfo = create_messageinfo()
        data = {
            "teacher_code": "teacher_code",
            "message": "message",
            "message_read": "message_read",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        url = reverse('messageinfo_update', args=[messageinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class OmrAnswerInfoViewTest(unittest.TestCase):
    '''
    Tests for OmrAnswerInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_omranswerinfo(self):
        url = reverse('omranswerinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_omranswerinfo(self):
        url = reverse('omranswerinfo_create')
        data = {
            "subject_code": "subject_code",
            "omr_answer": "omr_answer",
            "omr_answer_idx": "omr_answer_idx",
            "omr_answer_correct": "omr_answer_correct",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
            "lesson_code": create_lessoninfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_omranswerinfo(self):
        omranswerinfo = create_omranswerinfo()
        url = reverse('omranswerinfo_detail', args=[omranswerinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_omranswerinfo(self):
        omranswerinfo = create_omranswerinfo()
        data = {
            "subject_code": "subject_code",
            "omr_answer": "omr_answer",
            "omr_answer_idx": "omr_answer_idx",
            "omr_answer_correct": "omr_answer_correct",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
            "lesson_code": create_lessoninfo().pk,
        }
        url = reverse('omranswerinfo_update', args=[omranswerinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class OmrAssignInfoViewTest(unittest.TestCase):
    '''
    Tests for OmrAssignInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_omrassigninfo(self):
        url = reverse('omrassigninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_omrassigninfo(self):
        url = reverse('omrassigninfo_create')
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_omrassigninfo(self):
        omrassigninfo = create_omrassigninfo()
        url = reverse('omrassigninfo_detail', args=[omrassigninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_omrassigninfo(self):
        omrassigninfo = create_omrassigninfo()
        data = {
            "subject_code": "subject_code",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
        }
        url = reverse('omrassigninfo_update', args=[omrassigninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class OmrExampleInfoViewTest(unittest.TestCase):
    '''
    Tests for OmrExampleInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_omrexampleinfo(self):
        url = reverse('omrexampleinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_omrexampleinfo(self):
        url = reverse('omrexampleinfo_create')
        data = {
            "omr_example_correct": "omr_example_correct",
            "omr_example_idx": "omr_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_omrexampleinfo(self):
        omrexampleinfo = create_omrexampleinfo()
        url = reverse('omrexampleinfo_detail', args=[omrexampleinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_omrexampleinfo(self):
        omrexampleinfo = create_omrexampleinfo()
        data = {
            "omr_example_correct": "omr_example_correct",
            "omr_example_idx": "omr_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_code": create_omrquestioninfo().pk,
        }
        url = reverse('omrexampleinfo_update', args=[omrexampleinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QAnswerInfoViewTest(unittest.TestCase):
    '''
    Tests for QAnswerInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_qanswerinfo(self):
        url = reverse('qanswerinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_qanswerinfo(self):
        url = reverse('qanswerinfo_create')
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "question_answer": "question_answer",
            "question_idx": "question_idx",
            "question_correct": "question_correct",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
            "lesson_code": create_lessoninfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_qanswerinfo(self):
        qanswerinfo = create_qanswerinfo()
        url = reverse('qanswerinfo_detail', args=[qanswerinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_qanswerinfo(self):
        qanswerinfo = create_qanswerinfo()
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "question_answer": "question_answer",
            "question_idx": "question_idx",
            "question_correct": "question_correct",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
            "lesson_code": create_lessoninfo().pk,
        }
        url = reverse('qanswerinfo_update', args=[qanswerinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QAnswerLogViewTest(unittest.TestCase):
    '''
    Tests for QAnswerLog
    '''
    def setUp(self):
        self.client = Client()

    def test_list_qanswerlog(self):
        url = reverse('qanswerlog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_qanswerlog(self):
        url = reverse('qanswerlog_create')
        data = {
            "question_answer": "question_answer",
            "question_idx": "question_idx",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_qanswerlog(self):
        qanswerlog = create_qanswerlog()
        url = reverse('qanswerlog_detail', args=[qanswerlog.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_qanswerlog(self):
        qanswerlog = create_qanswerlog()
        data = {
            "question_answer": "question_answer",
            "question_idx": "question_idx",
            "question_score": "question_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "course_code": create_courseinfo().pk,
            "member_code": create_memberinfo().pk,
            "question_code": create_omrquestioninfo().pk,
        }
        url = reverse('qanswerlog_update', args=[qanswerlog.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QExampleInfoViewTest(unittest.TestCase):
    '''
    Tests for QExampleInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_qexampleinfo(self):
        url = reverse('qexampleinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_qexampleinfo(self):
        url = reverse('qexampleinfo_create')
        data = {
            "q_example": "q_example",
            "q_example_correct": "q_example_correct",
            "q_example_idx": "q_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "q_example_type": "q_example_type",
            "question_code": create_omrquestioninfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_qexampleinfo(self):
        qexampleinfo = create_qexampleinfo()
        url = reverse('qexampleinfo_detail', args=[qexampleinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_qexampleinfo(self):
        qexampleinfo = create_qexampleinfo()
        data = {
            "q_example": "q_example",
            "q_example_correct": "q_example_correct",
            "q_example_idx": "q_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "q_example_type": "q_example_type",
            "question_code": create_omrquestioninfo().pk,
        }
        url = reverse('qexampleinfo_update', args=[qexampleinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuestionInfoViewTest(unittest.TestCase):
    '''
    Tests for QuestionInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_questioninfo(self):
        url = reverse('questioninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_questioninfo(self):
        url = reverse('questioninfo_create')
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "question": "question",
            "question_media_type": "question_media_type",
            "question_media_file": "question_media_file",
            "question_score": "question_score",
            "question_head": "question_head",
            "question_essay": "question_essay",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_media_file2": "question_media_file2",
            "question_comment": "question_comment",
            "question_level": "question_level",
            "teacher_contents": "teacher_contents",
            "student_contents": "student_contents",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_questioninfo(self):
        questioninfo = create_questioninfo()
        url = reverse('questioninfo_detail', args=[questioninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_questioninfo(self):
        questioninfo = create_questioninfo()
        data = {
            "subject_code": "subject_code",
            "question_type": "question_type",
            "question": "question",
            "question_media_type": "question_media_type",
            "question_media_file": "question_media_file",
            "question_score": "question_score",
            "question_head": "question_head",
            "question_essay": "question_essay",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "question_media_file2": "question_media_file2",
            "question_comment": "question_comment",
            "question_level": "question_level",
            "teacher_contents": "teacher_contents",
            "student_contents": "student_contents",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
        }
        url = reverse('questioninfo_update', args=[questioninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuizAnswerInfoViewTest(unittest.TestCase):
    '''
    Tests for QuizAnswerInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_quizanswerinfo(self):
        url = reverse('quizanswerinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_quizanswerinfo(self):
        url = reverse('quizanswerinfo_create')
        data = {
            "subject_code": "subject_code",
            "quiz_type": "quiz_type",
            "quiz_answer": "quiz_answer",
            "quiz_answer_idx": "quiz_answer_idx",
            "quiz_correct": "quiz_correct",
            "quiz_score": "quiz_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "test_type": "test_type",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "quiz_code": create_quizinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_quizanswerinfo(self):
        quizanswerinfo = create_quizanswerinfo()
        url = reverse('quizanswerinfo_detail', args=[quizanswerinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_quizanswerinfo(self):
        quizanswerinfo = create_quizanswerinfo()
        data = {
            "subject_code": "subject_code",
            "quiz_type": "quiz_type",
            "quiz_answer": "quiz_answer",
            "quiz_answer_idx": "quiz_answer_idx",
            "quiz_correct": "quiz_correct",
            "quiz_score": "quiz_score",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "test_type": "test_type",
            "course_code": create_courseinfo().pk,
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "quiz_code": create_quizinfo().pk,
        }
        url = reverse('quizanswerinfo_update', args=[quizanswerinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuizExampleInfoViewTest(unittest.TestCase):
    '''
    Tests for QuizExampleInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_quizexampleinfo(self):
        url = reverse('quizexampleinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_quizexampleinfo(self):
        url = reverse('quizexampleinfo_create')
        data = {
            "quiz_example": "quiz_example",
            "quiz_example_correct": "quiz_example_correct",
            "quiz_example_idx": "quiz_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_example_type": "quiz_example_type",
            "quiz_code": create_quizinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_quizexampleinfo(self):
        quizexampleinfo = create_quizexampleinfo()
        url = reverse('quizexampleinfo_detail', args=[quizexampleinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_quizexampleinfo(self):
        quizexampleinfo = create_quizexampleinfo()
        data = {
            "quiz_example": "quiz_example",
            "quiz_example_correct": "quiz_example_correct",
            "quiz_example_idx": "quiz_example_idx",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "quiz_example_type": "quiz_example_type",
            "quiz_code": create_quizinfo().pk,
        }
        url = reverse('quizexampleinfo_update', args=[quizexampleinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ScheduleInfoViewTest(unittest.TestCase):
    '''
    Tests for ScheduleInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_scheduleinfo(self):
        url = reverse('scheduleinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_scheduleinfo(self):
        url = reverse('scheduleinfo_create')
        data = {
            "title": "title",
            "content": "content",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_scheduleinfo(self):
        scheduleinfo = create_scheduleinfo()
        url = reverse('scheduleinfo_detail', args=[scheduleinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_scheduleinfo(self):
        scheduleinfo = create_scheduleinfo()
        data = {
            "title": "title",
            "content": "content",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        url = reverse('scheduleinfo_update', args=[scheduleinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TalkMemberViewTest(unittest.TestCase):
    '''
    Tests for TalkMember
    '''
    def setUp(self):
        self.client = Client()

    def test_list_talkmember(self):
        url = reverse('talkmember_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_talkmember(self):
        url = reverse('talkmember_create')
        data = {
            "use_flag": "use_flag",
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_talkmember(self):
        talkmember = create_talkmember()
        url = reverse('talkmember_detail', args=[talkmember.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_talkmember(self):
        talkmember = create_talkmember()
        data = {
            "use_flag": "use_flag",
            "member_code": create_memberinfo().pk,
        }
        url = reverse('talkmember_update', args=[talkmember.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TalkRoomViewTest(unittest.TestCase):
    '''
    Tests for TalkRoom
    '''
    def setUp(self):
        self.client = Client()

    def test_list_talkroom(self):
        url = reverse('talkroom_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_talkroom(self):
        url = reverse('talkroom_create')
        data = {
            "talk_room_cate_code": "talk_room_cate_code",
            "use_flag": "use_flag",
            "course_code": create_courseinfo().pk,
            "inning_code": create_inninginfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_talkroom(self):
        talkroom = create_talkroom()
        url = reverse('talkroom_detail', args=[talkroom.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_talkroom(self):
        talkroom = create_talkroom()
        data = {
            "talk_room_cate_code": "talk_room_cate_code",
            "use_flag": "use_flag",
            "course_code": create_courseinfo().pk,
            "inning_code": create_inninginfo().pk,
        }
        url = reverse('talkroom_update', args=[talkroom.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TalkMessageViewTest(unittest.TestCase):
    '''
    Tests for TalkMessage
    '''
    def setUp(self):
        self.client = Client()

    def test_list_talkmessage(self):
        url = reverse('talkmessage_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_talkmessage(self):
        url = reverse('talkmessage_create')
        data = {
            "message": "message",
            "sender_member_code": "sender_member_code",
            "send_date": "send_date",
            "send_time": "send_time",
            "talk_room_id": create_talkroom().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_talkmessage(self):
        talkmessage = create_talkmessage()
        url = reverse('talkmessage_detail', args=[talkmessage.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_talkmessage(self):
        talkmessage = create_talkmessage()
        data = {
            "message": "message",
            "sender_member_code": "sender_member_code",
            "send_date": "send_date",
            "send_time": "send_time",
            "talk_room_id": create_talkroom().pk,
        }
        url = reverse('talkmessage_update', args=[talkmessage.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TalkMessageReadViewTest(unittest.TestCase):
    '''
    Tests for TalkMessageRead
    '''
    def setUp(self):
        self.client = Client()

    def test_list_talkmessageread(self):
        url = reverse('talkmessageread_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_talkmessageread(self):
        url = reverse('talkmessageread_create')
        data = {
            "is_read": "is_read",
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_talkmessageread(self):
        talkmessageread = create_talkmessageread()
        url = reverse('talkmessageread_detail', args=[talkmessageread.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_talkmessageread(self):
        talkmessageread = create_talkmessageread()
        data = {
            "is_read": "is_read",
            "member_code": create_memberinfo().pk,
        }
        url = reverse('talkmessageread_update', args=[talkmessageread.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TodoInfoViewTest(unittest.TestCase):
    '''
    Tests for TodoInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_todoinfo(self):
        url = reverse('todoinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_todoinfo(self):
        url = reverse('todoinfo_create')
        data = {
            "todo_comment": "todo_comment",
            "todo_status": "todo_status",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "teacher_code": "teacher_code",
            "todo_title": "todo_title",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "course_code": create_courseinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_todoinfo(self):
        todoinfo = create_todoinfo()
        url = reverse('todoinfo_detail', args=[todoinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_todoinfo(self):
        todoinfo = create_todoinfo()
        data = {
            "todo_comment": "todo_comment",
            "todo_status": "todo_status",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "teacher_code": "teacher_code",
            "todo_title": "todo_title",
            "start_date": "start_date",
            "start_time": "start_time",
            "end_date": "end_date",
            "end_time": "end_time",
            "chapter_code": create_chapterinfo().pk,
            "member_code": create_memberinfo().pk,
            "course_code": create_courseinfo().pk,
        }
        url = reverse('todoinfo_update', args=[todoinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TodoTInfoViewTest(unittest.TestCase):
    '''
    Tests for TodoTInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_todotinfo(self):
        url = reverse('todotinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_todotinfo(self):
        url = reverse('todotinfo_create')
        data = {
            "todo_code": "todo_code",
            "todo_t_flag": "todo_t_flag",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_todotinfo(self):
        todotinfo = create_todotinfo()
        url = reverse('todotinfo_detail', args=[todotinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_todotinfo(self):
        todotinfo = create_todotinfo()
        data = {
            "todo_code": "todo_code",
            "todo_t_flag": "todo_t_flag",
            "use_flag": "use_flag",
            "reg_date": "reg_date",
            "reg_time": "reg_time",
            "reg_agent": "reg_agent",
            "udt_date": "udt_date",
            "udt_time": "udt_time",
            "udt_agent": "udt_agent",
            "member_code": create_memberinfo().pk,
        }
        url = reverse('todotinfo_update', args=[todotinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


