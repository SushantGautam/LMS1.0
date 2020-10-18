import cx_Oracle
host = '203.246.120.110'
port = 1521

dsn_tns = cx_Oracle.makedsn(host, port, service_name='CUEDB')
conn = cx_Oracle.connect(user='nsdevil', password='nsdevil03', dsn=dsn_tns)
c = conn.cursor()
username = 'cue20121051'
username = username.replace('cue','')
c.execute("SELECT LEEV_YUMU FROM nesys.v_online WHERE STNT_NUMB = '%s'" % username)
result = c.fetchall()
if not result:
    print("Can't Login NO DATA")
else:
    for row in result:
        if row[0] == 'N':
            print("Can't Login")
        else:
            print("Submitted")

c.execute("SELECT * FROM nesys.v_online WHERE LEEV_YUMU = Y")
result = c.fetchall()
print(result)
conn.close()