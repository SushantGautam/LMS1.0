# LMS Version 1.0
Continued version of previous LMS
https://gitlab.com/nsdevil/lms

Changes in structure of the project, files and directory
Changes in database model and fields
Unessaery files and code has been removed if necessary to take reference please look at the previous repo

# Clone the project to the directory LMS V1
1. Make a new directory in your preffered location with "LMS V1" name or you can give it other name also
2. Browse the directory through cmd and type **git clone "clone_address_is_given_above" .** to clone in the same directory

# Installation Notes(In Pycharm):
1. Check out a project in Pycharm - [see here for help](Open%20lms%20folder%20using%20Pycharm)
URL of the remote repository: **https://gitlab.com/nsdevil/lms.git**
4.  [Create Virtual Environment](https://www.jetbrains.com/help/pycharm-edu/creating-virtual-environment.html)
5. Restart Pycharm
6. On the Pycharm's terminal run the following code to Install Requirements : **pip install -r requirements.txt**

**For Windows user:**
If you get problem in installing **Twisted** library:
Download Suitable Version of pre compilled library from: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) and install from venv activated Pycharm terminal using :
**pip install *filename*.whl** 
and again Install Requirements.<br>
After all the requirements get installed, you additionally need to install Win32API from venv activated Pycharm terminal:
**pip install pypiwin32**

5. Migrate Database: **python manage.py makemigrations WebApp**
6. Migrate Database: **python manage.py migrate**
7. After that, run the app using Django manage.py: **python manage.py runserver**
8. Access the homepage on     http://localhost:8000
 
## Creating an admin user
First we’ll need to create a user who can login to the admin site. Run the following command:

`$ python manage.py createsuperuser` <br>
Enter your desired username and press enter. <br>

`Username: admin ` <br>
You will then be prompted for your desired email address: <br>

`Email address: admin@example.com` <br>
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first. <br>

```
Password: **********<br>
Password (again): *********<br>
Superuser created successfully.<br>
```


## Django Admin
The Django admin site is activated by default after running `$ python manage.py runserver`<br>
Now, open a Web browser and go to “/admin/” on your local domain – e.g., http://127.0.0.1:8000/admin/. You should see the admin’s login screen.


## APIs
Visit http://127.0.0.1:8000/api/v1/ to explore the API. You only can explore APIs after you login to Django Admin screen using superuser access.


# Live Deployment:
Check  http://lms-nsd.sushant.info.np for latest updated website. The website gets automically updated after around 5 minutes of commits pushed to Gitlab.


# Project Management Links
### Gitlab Board > [https://gitlab.com/nsdevil/lms/boards](https://gitlab.com/nsdevil/lms/boards)
### Bitrix Tasks > [https://nsdevil.bitrix24.com/extranet/workgroups/group/109/tasks/](https://nsdevil.bitrix24.com/extranet/workgroups/group/109/tasks/)

