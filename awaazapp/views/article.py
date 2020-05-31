# -*- coding: utf-8 -*-

from django.shortcuts import redirect

from django.shortcuts import render
from django.http import Http404,HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from awaazapp.common.db import query, getquery
import simplejson
import json
import projectname.settings as settings
domain_url = settings.SITE_URL
# Create your views here.


def listing(request):
    resp = get_all_articles()
    return render(request, "showarticle.html", {'all_projects':resp,'base_url':domain_url})

def postinfo(request):
    if(request.method == 'POST'):
        title = request.POST.get('project_name','')
        content = request.POST.get('project_desc','')
        project_duration = request.POST.get('project_duration','')
        qe = "INSERT INTO project( project_name,project_desc, project_duration) VALUES('{}','{}','{}')".format(str(title),str(content),str(project_duration))
        # values = (title,content)
        resp = query(qe)
        print(resp)
        resp = get_all_articles()
        return render(request, "showarticle.html", {'all_projects': resp, 'base_url': domain_url})
    return render(request, "addproject.html", {'base_url':domain_url})

def redirect_view():
    response = redirect('/v1/view-project/')
    return response

def deleteinfo(request):
    print(request)
    table = request.GET.get('table')
    print(table)
    table_auto_id = request.GET.get('table_auto_id')
    print(table_auto_id)
    table_primary_col = request.GET.get('table_primary_col')
    print(table_primary_col)

    qe = "DELETE FROM {} WHERE {} = {}".format(str(table), str(table_primary_col), str(table_auto_id))
    resp = query(qe)
    print(resp)

    return redirect_view()

def showtasks(request):
    project_id = request.GET.get('project_id', '')
    project_name = request.GET.get('project_name', '')
    resp = get_all_tasks(project_id)
    return render(request, "showtask.html", {'all_tasks': resp,'project_name': project_name, 'base_url': domain_url})

def posttask(request):
    project_name = request.GET.get('project_name','')
    project_id = request.GET.get('project_id','')
    particular_task_id = request.GET.get('taskid')

    if particular_task_id != None:
        get_particular_task_details = get_all_tasks(project_id, task_id=particular_task_id)
    else:
        get_particular_task_details = ""
    # get_particular_task_details = json.dumps(get_particular_task_details)
    all_users = User.objects.all()
    if(request.method == 'POST'):
        title = request.POST.get('task_name','')
        taskcontent = request.POST.get('task_desc','')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')
        project_id = request.POST.get('project_id','')
        assignee = request.POST.get('assignee','')
        qe = "INSERT INTO task(task_name,task_desc, project_id, assignee, start_date, end_date) VALUES('{}','{}','{}','{}','{}','{}')".format(str(title),str(taskcontent),str(project_id), str(assignee),start_date,end_date)

        resp = query(qe)
        print(resp)
        resp = get_all_tasks(project_id)
        return render(request, "showtask.html", {'all_tasks': resp, 'base_url': domain_url})
    return render(request, "addtask.html", {'all_users': all_users, 'get_particular_task_details': get_particular_task_details,'project_name': project_name, 'base_url':domain_url})

def welcome(request): 
    return render(request, "welcome.html", {})

def get_all_articles():
    get_article = "select * from project"
    response = getquery(get_article)
    return response        

def get_all_tasks(project_id, task_id=None):
    get_article = "select * from task where project_id = {}".format(project_id)

    if task_id != None:
        get_article += " and taskid = {}".format(task_id)
    response = getquery(get_article)
    return response
