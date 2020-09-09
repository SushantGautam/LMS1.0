import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LMS.settings")

import django

django.setup()

from WebApp.models import ChapterInfo, AssignmentInfo, SessionMapInfo
from django.contrib.contenttypes.models import ContentType


class MigrateData:
    def migrateChapters(self):
        # Get all chapter objects
        chapters = ChapterInfo.objects.all()
        for chapter in chapters:
            # Check if the chapter belongs to any innings
            # If Yes, Create Inning Map
            if chapter.Course_Code.innings_of_this_course().exists():
                for session in chapter.Course_Code.innings_of_this_course():
                    sessionmap = SessionMapInfo.objects.create(
                        Start_Date=chapter.Start_Date,
                        End_Date=chapter.End_Date,
                        target_content_type=ContentType.objects.get_for_model(chapter.__class__),
                        target_object_id=chapter.id,
                        Session_Code=session
                    )
                    sessionmap.save()
        print("Success Mapping Chapter to InningMap")

    def migrateAssignments(self):
        # Get all assignments objects
        assignments = AssignmentInfo.objects.all()
        for assignment in assignments:
            # Check if the assignment belongs to any innings
            # If Yes, Create Inning Map
            if assignment.Course_Code.innings_of_this_course().exists():
                for session in assignment.Course_Code.innings_of_this_course():
                    sessionmap = SessionMapInfo.objects.create(
                        Start_Date=assignment.Assignment_Start,
                        End_Date=assignment.Assignment_Deadline,
                        target_content_type=ContentType.objects.get_for_model(assignment.__class__),
                        target_object_id=assignment.id,
                        Session_Code=session
                    )
                    sessionmap.save()
        print("Success Mapping Assignment to InningMap")


def main():
    MigrateData().migrateChapters()
    MigrateData().migrateAssignments()


if __name__ == '__main__':
    main()
