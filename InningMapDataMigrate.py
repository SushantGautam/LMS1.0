# This code is used to transfer chapter and assigment previous startdatetime and enddatetime to new mapping
# Delete all sessionmapping ahead if there is any
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LMS.settings")

import django
django.setup()

from WebApp.models import ChapterInfo, AssignmentInfo, InningInfo, SessionMapInfo
from django.contrib.contenttypes.models import ContentType

def migrateChapters():
	sessions = InningInfo.objects.all()
	for session in sessions:
		courses = set(session.Course_Group.all())
		for course in courses:
			chapters = ChapterInfo.objects.filter(Course_Code=course.Course_Code)
			for chapter in chapters:
				sessionmap = SessionMapInfo()
				sessionmap.Start_Date = chapter.Start_Date
				sessionmap.End_Date = chapter.End_Date
				sessionmap.content_type = ContentType.objects.get_for_model(chapter)
				sessionmap.object_id = chapter.id
				sessionmap.Session_Code = session
				sessionmap.save()
				print(session, chapter, '\n')
	print('----------------------------------------------------')
	print(' ALL CHAPTERS DONE ')

def migrateAssignments():
	sessions = InningInfo.objects.all()
	for session in sessions:
		courses = set(session.Course_Group.all())
		for course in courses:
			assignments = AssignmentInfo.objects.filter(Course_Code=course.Course_Code)
			for assignment in assignments:
				sessionmap = SessionMapInfo()
				sessionmap.Start_Date = assignment.Assignment_Start
				sessionmap.End_Date = assignment.Assignment_Deadline
				sessionmap.content_type = ContentType.objects.get_for_model(assignment)
				sessionmap.object_id = assignment.id
				sessionmap.Session_Code = session
				sessionmap.save()
				print(session, assignment, '\n')
	print('----------------------------------------------------')
	print(' ALL ASSIGNMENTS DONE ')

def main():
    migrateChapters()
    migrateAssignments()

if __name__ == '__main__':
    main()
