# import cx_Oracle
# host = '203.246.120.110'
# port = 1521

# dsn_tns = cx_Oracle.makedsn(host, port, service_name='CUEDB')
# conn = cx_Oracle.connect(user='nsdevil', password='nsdevil03', dsn=dsn_tns)
# c = conn.cursor()
# username = 'cue20121051'
# username = username.replace('cue','')
# c.execute("SELECT LEEV_YUMU FROM nesys.v_online WHERE STNT_NUMB = '%s'" % username)
# result = c.fetchall()
# if not result:
#     print("Can't Login NO DATA")
# else:
#     for row in result:
#         if row[0] == 'N':
#             print("Can't Login")
#         else:
#             print("Submitted")

# c.execute("SELECT * FROM nesys.v_online WHERE LEEV_YUMU = Y")
# result = c.fetchall()
# print(result)
# conn.close()

# The following code is only for chinju university student account in login view
# center_obj = form.get_user().Center_Code
# if center_obj.Center_Name == '진주교육대학교' and center_obj.pk == 2:
#     dsn_tns = cx_Oracle.makedsn('203.246.120.110', 1521, service_name='CUEDB')
#     conn = cx_Oracle.connect(user='nsdevil', password='nsdevil03', dsn=dsn_tns)
#     c = conn.cursor()
#     username = form.get_user().username.replace('cue', '')
#     c.execute("SELECT LEEV_YUMU FROM nesys.v_online WHERE STNT_NUMB = '%s'" % username)
#     result = c.fetchall()
#     msg = """[원격수업강의 평가]를 완료하지 않았습니다.
#
#             [두류포털]-[종합정보]-[강의관리]-[원격수업강의평가]에서
#
#             [원격수업 강의 평가]를 완료하셔야 사이트 접속이 승인됩니다.
#
#             * [두류포털] 접속을 위해서는 Internet Explorer 이용해 주세요."""
#     if not result:
#         return JsonResponse({'type': 'submit_survey', 'msg': msg})
#     for row in result:
#         if row[0] == 'N':
#             return JsonResponse({'type': 'submit_survey', 'msg': msg})