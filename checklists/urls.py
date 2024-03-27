"""
URL configuration for dev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from checklists import views
from checklists import display
from checklists import administration


urlpatterns = [
    path('Add_CheckList_Header/',administration.Add_CheckList_Header,name='Add_CheckList_Header'),
    path('Add_CheckList_Footer/',administration.Add_CheckList_Footer,name='Add_CheckList_Footer'),
    path('Add_CheckList_Trans_Header/',administration.Add_CheckList_Trans_Header,name='Add_CheckList_Trans_Header'),
    path('checklistbyyou/',display.Checklist_By_You,name='checklistbyyou'),
    path('checklist_avtar/<int:pk>/',display.checklist_avtar,name='checklist_avtar'),
    #------------- Checklist Header part ---------------------------
    path('create_checklistpre/', display.create_checklist_detailpre, name='create_checklist'),
    #------------ Checklist Footer part with site Engineer 
    path('start1_one/<str:checklist_id>/<str:saved_form1>/',display.start1_one, name='start1_one'),
    #------------ Checklist Footer part with DH Status and comment
    path('DHPre_one/<int:pk>/',display.DHPre_one, name='DHPre_one'),
    path('DHEReject/<int:pk>/',display.DHEReject,name='DHEReject'),
    #--------------Other mechanism-----
    path('DHEQA_workspace/',display.DHEQA_workspace,name='DHEQA_workspace'),
    path('ProjectQA_workspace/',display.ProjectQA_workspace,name='ProjectQA_workspace'),
    path('ProjectHead_workspace/',display.ProjectHead_workspace,name='ProjectHead_workspace'),
    path('closed-checklist/<int:pk>/',display.closed_checklist,name='closed-checklist'),
    path('all-closed-checklists/',display.all_closed_checklists,name='all-closed-checklists'),
    path('all_checklist_sendTo_ProjectQA/',display.all_checklist_sendTo_ProjectQA,name='all_checklist_sendTo_ProjectQA'),
    path('all_checklist_sendTo_ProjectHead/',display.all_checklist_sendTo_ProjectHead,name='all_checklist_sendTo_ProjectHead'),
    #-----------Project AQ Work---------
    path('observation-PQA/<int:pk>/',display.observation,name="observation-PQA"),
    path('observation_PQA_Queue/',display.observation_PQA_Queue,name='observation_PQA_Queue'),
    path('project_head/<int:pk>/',display.project_head,name="project_head"),
    path('rejected/<int:pk>/',display.Rejected_checklist,name='Rejected_checklist'),
    path('rejected_chechlists/',display.rejected_checklists,name='rejected_chechlists'),
    path('edit_checklist/<int:pk>/',display.edit_checklist, name='edit_checklist'), 
    #  #-------------------Checklist Name-------------------------------------
    path('edit_checklistname/<int:pk>/', administration.edit_CheckList_Header, name='edit_checklistname'),
    path('delete_checklistname/<int:pk>/', administration.delete_CheckList_Header, name='delete_checklistname'),
    # #-------------------Checklist Questions-------------------------------------
    path('edit_checklistQuestion/<int:pk>/', administration.edit_CheckList_Footer, name='edit_checklistQuestion'),
    path('delete_checklistQuestion/<int:pk>/', administration.delete_CheckList_Footer, name='delete_checklistQuestion'),
    # #-------------------Add_Structural-Elements----------------
    path('Add_Structural_Elements/',administration.Add_Structural_Elements,name='Add_Structural_Elements'),
    path('edit_Structural_Elements/<int:pk>/',administration.edit_Structural_Elements,name='edit_Structural_Elements'),
    path('delete_Structural_Elements/<int:pk>/',administration.delete_Structural_Elements,name='delete_Structural_Elements'),
    # #------------------------history--------------------------
    path('history/',administration.history,name='history'),
    path('all_checklists/',display.all_checklists,name='all_checklists'),
   
    
]

