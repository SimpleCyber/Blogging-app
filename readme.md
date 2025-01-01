1.  🌿 django-admin startproject project-name

2. open the project-name 
    🌿  python manage.py makemigrations
    🌿  python manage.py migrate       


   <!-- Now we will create our apps in project -->
   python manage.py startapp home

3. Resister [app]
   After my [app] has been created (home)
    - home/apps.py 
    copy function name "HomeConfig"
    and 
    paste it in the [project] (usersproject)

    - usersproject/settings.py
        Installed_apps= [
            'home.apps.HomeConfig',
        ]

     🌿 python manage.py startapp home

4. Allowed_hosts =[]
   usersproject/settings.py
    define the allowed hosts = ["http://localhost:8000, "satyam.com"]
    else it will throw an error


5. create an static and templates folder
   - home
   - usersproject
   - static
   - templates

6. set static dirs in django
   usersproject/settings.py
     at the end paste this
     STATICFILES_DIRS = [
        os.path.join(BASE_DIR ,"static"),
    ]

7. set templates 
    usersproject/settings.py
    update :  'DIRS': [os.path.join(BASE_DIR ,"templates"),],


    <!-- 🌿🌿🌿 PROJECT SETUP COMPLETED 🌿🌿🌿 -->
    # Start server : py manage.py runserver 


<!-- Let's begin with the project -->
1. Create the html files
   1. templates/index.html
   2. templates/login.html



2. update the userproject/urls.py
    - from django.urls import path => from django.urls import path , include
    - urlpatterns = [
        path('admin/', admin.site.urls),
        <!-- Start adding the urls routes to the apps -->
        path('', include('home.urls')),
    ]

    - [app] home
      create a new file name home/urls.py : this will handle all of the home files routing

      home/urls.py
        from django.contrib import admin
        from django.urls import path , include
        from home import views

        urlpatterns = [
            path('', views.index, name="home"),
            path('login', views.login, name="login"),
            path('logout', views.logout, name="logout"),
        ]

    - [app] home/views.py  : now i need to create all of the functions too
  
        from django.shortcuts import render, redirect
        # Create your views here.
        def index(request):
            return render(request,'index.html')
        def login(request):
            return render(request,'login.html')
        def logout(request):
            return render(request,'index.html')









   
