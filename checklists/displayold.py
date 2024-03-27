from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import CheckList_Trans_Header,History,CheckList_Trans_Details
from administration.models import CheckList_Header,CheckList_Footer,Projects,Sites,Structural_Element
from django.shortcuts import render, get_object_or_404
#from Logfile import logdata
from .forms import CheckList_Trans_DetailsFormFill,CheckListTransHeaderFormfill,CheckList_Trans_DetailsFormFill2,ProjectQAForm,ProjectHeadForm,assigned_to_ProjectQAForm,assigned_to_ProjectHeadForm,rejected_from_ProjectQAForm,CheckListForm#,CombinedCheckListForm,CheckListForm,CheckListDetailsForm
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
import datetime
import dev.config as cfg
from administration.authlib import CheckAuthorization
import inspect 
from administration.models import Users
#from checklists.Logdata import logdata

#from sms import sendsms
def create_checklist_detailpre(request):
    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]
   
    if not request.user.is_superuser:
        AppName = inspect.stack()[0][3].strip()
        AppID = cfg.Apps[AppName]
        UserID = request.user.UserID
        if not CheckAuthorization(AppID=AppID, UserID=UserID):
            messages.info(request,'You are not authorized for this application')
            return redirect('/home')
    if request.method == 'POST':
        form = CheckListTransHeaderFormfill(request.POST)
        if form.is_valid():
            return redirect('preview_checklist', data=form.cleaned_data)
    else:
        form = CheckListTransHeaderFormfill()

        context = { 'form' : form,
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'usernames':usernames,
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                  }         
    return render(request, 'checklists/formlookpre.html', context)

def preview_checklist_detailpre(request):
    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]
    if request.method == 'POST':
        form_data = request.POST
        form = CheckListTransHeaderFormfill(form_data)
        # checklistname = CheckList_Header.objects.get(CheckList_ID=form_data['CheckList_ID']).CheckList_Title
        # projectname = Projects.objects.get(Project_ID=form_data['Project_Name']).Project_Name
        # logdata(form_data['Project_Name'])
        # logdata(projectname)
        # sitename =  Sites.objects.get(Site_ID=form_data['Site_ID']).Site_Name
        # structuralElename = Structural_Element.objects.get(Structural_Element_ID=form_data['Structural_Element_ID']).Structural_Element
        if form.is_valid():
            context = { 'form' : form,
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'usernames':usernames,
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                    'form_data':form_data,
                    # 'checklistname':checklistname,
                    # 'projectname':projectname,
                    # 'sitename':sitename,
                    # 'structuralElename':structuralElename,
                  }         
            return render(request, 'checklists/form_preview.html',context)
    else:
        # return redirect('create_checklist')

     return redirect('create_checklist')



from .Logdata import logdata
def save_checklist(request):

    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]

    if request.method == 'POST':
        form_data = request.POST
        form = CheckListTransHeaderFormfill(form_data)
        if form.is_valid():
            variable = form.save(commit=False)
            variable.Name_Of_ABLStaff = request.user
            variable.checklist_status = 'Pending_By_SiteEngineer'
            #variable.assigned_to = usernames
            #variable.assigned_to = usernames
            variable.save()
            saved_form = form.save()
            saved_form1=saved_form.Doc_ID
            checklist_title = saved_form.CheckList_ID.CheckList_Title  
            idcheck = CheckList_Header.objects.get(CheckList_Title=checklist_title)
            return redirect('start1_one',checklist_id=idcheck.CheckList_ID,saved_form1=saved_form1)
        else: 
            messages.warning(request,'Something went wrong...!')
            return redirect('checklist_detail')
    else:
        form = CheckListTransHeaderFormfill()
    
    return render(request, 'checklists/formlook.html', {'form': form, 'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
              'customer_name' : 'Ashoka Buildcon Limited'})

def initialize_and_disable_fields(form, header, trans_header):
    form.fields['CheckList_ID'].initial = header.CheckList_ID
    form.fields['CheckList_ID'].disabled = True
    form.fields['Project_Name'].initial = trans_header.Project_Name
    form.fields['Project_Name'].disabled = True
    form.fields['Site_Name'].initial = trans_header.Site_Name
    form.fields['Site_Name'].disabled = True
    form.fields['Contractor'].initial = trans_header.Contractor
    form.fields['Contractor'].disabled = True
    form.fields['Location'].initial = trans_header.Location
    form.fields['Location'].disabled = True
    form.fields['Structural_Element'].initial = trans_header.Structural_Element
    form.fields['Structural_Element'].disabled = True
    form.fields['Chainage'].initial = trans_header.Chainage
    form.fields['Chainage'].disabled = True

def start1_one(request,checklist_id,saved_form1):
    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]



    CheckListTransHeaders = CheckList_Header.objects.get(CheckList_ID=checklist_id) #MNB/VUP/LVUP/PUP/CUP/BC
    CheckListTransHeaders1 = CheckList_Trans_Header.objects.get(Doc_ID=saved_form1) # Doc ID: 132, CheckList ID: MNB/VUP/LVUP/PUP/CUP/BC
    
    form1 = CheckListTransHeaderFormfill()
    initialize_and_disable_fields(form1, CheckListTransHeaders, CheckListTransHeaders1)
   

    checklist_trans_header = get_object_or_404(CheckList_Trans_Header, Doc_ID=saved_form1)  # Doc ID: 132, CheckList ID: MNB/VUP/LVUP/PUP/CUP/BC
    checklist_trans_details = CheckList_Trans_Details.objects.filter(Doc_ID=checklist_trans_header.Doc_ID)
    checklist_items = CheckList_Footer.objects.filter(CheckList_ID=checklist_id)
   
    checklist_item_desc_list = [item.CheckList_Item_Desc for item in checklist_items]
   
  
    prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_desc_list)+1)] 
    if request.method == 'POST':
        any_form_valid = False
        for prefix, item_desc in zip(prefixes, checklist_item_desc_list):
            form = CheckList_Trans_DetailsFormFill(request.POST, prefix=prefix)
            if form.is_valid():
                return redirect('start1_two',checklist_id=checklist_id,saved_form1=saved_form1, data=form.cleaned_data)
                
    else:
        forms_with_items = list(zip([CheckList_Trans_DetailsFormFill(prefix=prefix) for prefix in prefixes], checklist_item_desc_list))
       
        forms_and_checklist_items = list(zip([CheckList_Trans_DetailsFormFill(prefix=prefix) for prefix in prefixes], checklist_items))

        context = { 'form':form1,
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'forms_with_items': forms_with_items,
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'usernames':usernames,
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                    'checklist_id':checklist_id,
                    'checklist_items':checklist_items,
                    'forms_and_checklist_items':forms_and_checklist_items,
                    'saved_form1':saved_form1

                  }         
    return render(request, 'checklists/start1_one.html',context)

def start1_two(request,checklist_id,saved_form1):
    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]



    CheckListTransHeaders = CheckList_Header.objects.get(CheckList_ID=checklist_id) #MNB/VUP/LVUP/PUP/CUP/BC
    CheckListTransHeaders1 = CheckList_Trans_Header.objects.get(Doc_ID=saved_form1) # Doc ID: 132, CheckList ID: MNB/VUP/LVUP/PUP/CUP/BC
    
    form1 = CheckListTransHeaderFormfill()
    initialize_and_disable_fields(form1, CheckListTransHeaders, CheckListTransHeaders1)
    if request.method == 'POST':
        form_data = request.POST
        checklist_items = CheckList_Footer.objects.filter(CheckList_ID=checklist_id)
        checklist_item_desc_list = [item.CheckList_Item_Desc for item in checklist_items]
        prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_desc_list)+1)] 
        forms_with_items = list(zip([CheckList_Trans_DetailsFormFill(prefix=prefix) for prefix in prefixes], checklist_item_desc_list))
      
        all_forms_valid = True
        for prefix in prefixes:
            form = CheckList_Trans_DetailsFormFill(prefix=prefix, data=form_data)
            if not form.is_valid():
                all_forms_valid = False
                break
        forms_with_items = list(zip([CheckList_Trans_DetailsFormFill(prefix=prefix, data=form_data) for prefix in prefixes], checklist_item_desc_list))
        all_forms_valid = all(form.is_valid() for form, _ in forms_with_items)
        if all_forms_valid:
            filled_forms = [form for form, _ in forms_with_items]
            forms_with_items = zip(filled_forms, checklist_item_desc_list)
           
            forms_and_checklist_items = zip(filled_forms, checklist_items)

            context = { 
                'forms_with_items': forms_with_items,
                'forms_and_checklist_items':forms_and_checklist_items,
                'form_data': form_data,
                'form':form1,
                'formme':form,
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title': 'Fill Checklist',
                'isForm' : True,
                'usernames':usernames,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'username': request.user.get_full_name(), 
                'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'checklist_id': checklist_id,
                'saved_form1': saved_form1

                  }     
            return render(request, 'checklists/start1_two.html',context)
        else:
            return redirect('home')

    return redirect('home')
   
def start1_three(request,checklist_id,saved_form1):
        
        CheckListTransHeaders1 = CheckList_Trans_Header.objects.get(Doc_ID=saved_form1) # Doc ID: 132, CheckList ID: MNB/VUP/LVUP/PUP/CUP/BC
        CheckListTransHeaders1.checklist_status = 'Completed_By_SiteEngineer & Active_At_DHEQA'
        CheckListTransHeaders1.save()
        form_data = request.POST
        checklist_items = CheckList_Footer.objects.filter(CheckList_ID=checklist_id)
        checklist_item_desc_list = [item.CheckList_Item_Desc for item in checklist_items]
        prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_desc_list) + 1)]
        forms_with_items = list(zip([CheckList_Trans_DetailsFormFill(prefix=prefix) for prefix in prefixes], checklist_item_desc_list))
        History.objects.create(Doc_ID=CheckListTransHeaders1,Comment=f"{request.user} created checklist and assigned to {CheckListTransHeaders1.assigned_to}")
       
        all_forms_valid = True
        valid_forms = [] 
        for prefix in prefixes:
            form = CheckList_Trans_DetailsFormFill(prefix=prefix, data=form_data)
            if not form.is_valid():
                all_forms_valid = False
                break
            else:
                valid_forms.append(form)  

        if all_forms_valid:
            for form, item_desc in zip(valid_forms, checklist_item_desc_list):
                variable = form.save(commit=False)
                variable.Doc_ID = CheckListTransHeaders1
                variable.CheckList_ID = CheckListTransHeaders1
                variable.CheckList_Item_ID = item_desc
                variable.save()
                
            messages.info(request,'Checklist submited to DHEQA Successfully..!')

            context = {
                    'page_title': 'Ashoka Buildcon Limited',
                    'forms_with_items': forms_with_items,
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                    'customer_name' : 'Ashoka Buildcon Limited',
                    'checklist_id': checklist_id,
                    'saved_form1': saved_form1}
            return render(request, 'checklists/home.html',context)
        else:
            return redirect('home')

#------------checklist DH Preview------------------
def repeated(form1,checklist):
     form1.fields['CheckList_ID'].initial =checklist.CheckList_ID
     form1.fields['CheckList_ID'].disabled = True
     form1.fields['Project_Name'].initial = checklist.Project_Name
     form1.fields['Project_Name'].disabled = True
     form1.fields['Site_Name'].initial = checklist.Site_Name
     form1.fields['Site_Name'].disabled = True
     form1.fields['Contractor'].initial = checklist.Contractor
     form1.fields['Contractor'].disabled = True
     form1.fields['Location'].initial = checklist.Location
     form1.fields['Location'].disabled = True
     form1.fields['Structural_Element'].initial = checklist.Structural_Element
     form1.fields['Structural_Element'].disabled = True
     form1.fields['Chainage'].initial = checklist.Chainage
     form1.fields['Chainage'].disabled = True
    #  form1.fields['assigned_to'].initial = checklist.assigned_to
    #  form1.fields['assigned_to'].disabled = True

def DHPre_one(request,pk):    
     #--------Default sending of checklist-----#
     user_project_name =request.user.Project_Name 
     Project_QA = Users.objects.filter(Project_Name=user_project_name,is_ProjectQA=True)
     Project_QA_usernames = [user.username for user in Project_QA]
     Project_head = Users.objects.filter(Project_Name=user_project_name,is_ProjectHead=True)
     Project_Head_usernames = [user.username for user in Project_head]
     #--------Default sending of checklist-----#

     checklist = CheckList_Trans_Header.objects.get(pk=pk)
     checklist_items = CheckList_Footer.objects.filter(CheckList_Title=checklist.CheckList_ID)
     answer = CheckList_Footer.objects.filter(answer=checklist.CheckList_ID)

     #------- tring rejection case------
     if request.method == 'POST':
        formR = rejected_from_ProjectQAForm(request.POST,instance=checklist) 
        if formR.is_valid():
            #formR.save()
            formR.save(commit=False)
            # Set additional fields on the checklist object
            checklist.rejected_byDHEQA = True
            checklist.checklist_status = 'Rejected'
            checklist.save()

            # Save the form again to ensure the rejection_comment is saved
            formR.save()
            return redirect('/home')
     else:
         formR = rejected_from_ProjectQAForm()

     
     Name_Created_Checklist_by = checklist.Name_Of_ABLStaff
     form1 = CheckListTransHeaderFormfill()
     repeated(form1,checklist)

     details_records = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
     
     checklist_item_ids = []
     site_engineer_statuses = []
     site_engineer_comments = []
     
     for record in details_records:
            checklist_item_ids.append(record.CheckList_Item_ID)
            site_engineer_statuses.append(record.Site_Engineer_Status)
            site_engineer_comments.append(record.Site_Engineer_Comment)
            
     checklist_data = zip(checklist_item_ids, site_engineer_statuses, site_engineer_comments,)

     prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_ids)+1)] 
     if request.method == 'POST':
          any_form_valid = False
          for prefix, item_desc in zip(prefixes, checklist_item_ids): 
            form = CheckList_Trans_DetailsFormFill2(request.POST, prefix=prefix)
            if form.is_valid():
                #logdata(data=form.cleaned_data)
                return redirect('DHPre_two',pk=pk,data=form.cleaned_data)
                
     else:
            forms_with_items = list(zip([CheckList_Trans_DetailsFormFill2(prefix=prefix) for prefix in prefixes],checklist_item_ids))
           #----trying----
            tryingredcolor = list(zip([CheckList_Trans_DetailsFormFill2(prefix=prefix) for prefix in prefixes],checklist_items))

           #-----trying---
     context = {'form1':form1,
                'checklist_data': checklist_data,
                'forms_with_items':forms_with_items,
                'pk':pk,
                'Name_Created_Checklist_by':Name_Created_Checklist_by,
                'checklist':checklist,
                #'formA':formA,
                'formR':formR,
                'Project_QA_usernames': Project_QA_usernames,
                'Project_Head_usernames':Project_Head_usernames,
                'checklist_items':checklist_items,
                'tryingredcolor':tryingredcolor,
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',
                }
     return render(request,'checklists/DHPre_one.html',context)

def DHPre_two(request,pk):
      #--------Default sending of checklist-----#
     user_project_name =request.user.Project_Name 
     Project_QA = Users.objects.filter(Project_Name=user_project_name,is_ProjectQA=True)
     Project_QA_usernames = [user.username for user in Project_QA]
     Project_head = Users.objects.filter(Project_Name=user_project_name,is_ProjectHead=True)
     Project_Head_usernames = [user.username for user in Project_head]
     #--------Default sending of checklist-----#

     checklist = CheckList_Trans_Header.objects.get(pk=pk)
     checklist_items = CheckList_Footer.objects.filter(CheckList_Title=checklist.CheckList_ID)
     Name_Created_Checklist_by = checklist.Name_Of_ABLStaff
     form1 = CheckListTransHeaderFormfill()

     if request.method == 'POST':
        formA = assigned_to_ProjectQAForm(request.POST,instance=checklist)
        
        if formA.is_valid():
            formA.save()
     else:
         formA = assigned_to_ProjectQAForm()

     repeated(form1,checklist)
     details_records = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
     checklist_item_ids = []
     site_engineer_statuses = []
     site_engineer_comments = []

     for record in details_records:
            checklist_item_ids.append(record.CheckList_Item_ID)
            site_engineer_statuses.append(record.Site_Engineer_Status)
            site_engineer_comments.append(record.Site_Engineer_Comment)

     checklist_data = zip(checklist_item_ids, site_engineer_statuses, site_engineer_comments)
    
     if request.method == 'POST':
         form_data = request.POST
         prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_ids)+1)] 
         forms_with_items = list(zip([CheckList_Trans_DetailsFormFill2(prefix=prefix) for prefix in prefixes],checklist_item_ids))
         all_forms_valid = True
         for prefix in prefixes:
            form = CheckList_Trans_DetailsFormFill2(prefix=prefix, data=form_data)
           
            if not form.is_valid():
                all_forms_valid = False
                break
         forms_with_items = list(zip([CheckList_Trans_DetailsFormFill2(prefix=prefix, data=form_data) for prefix in prefixes], checklist_item_ids))
         all_forms_valid = all(form.is_valid() for form, _ in forms_with_items)
         if all_forms_valid:
            filled_forms = [form for form, _ in forms_with_items]
            forms_with_items = zip(filled_forms, checklist_item_ids)
           
            zipped_data = zip(filled_forms, checklist_item_ids,site_engineer_statuses,site_engineer_comments)
            #----trying----
            tryingredcolor = zip(filled_forms, checklist_items,site_engineer_statuses,site_engineer_comments)

           #-----trying---
            return render(request, 'checklists/DHPre_two.html', {
                'forms_with_items': forms_with_items,
                'form_data': form_data,
                'form1':form1,
                'checklist_data': checklist_data,
                'formme':form,
                'pk':pk,
                'Name_Created_Checklist_by':Name_Created_Checklist_by,
                'zipped_data': zipped_data, 
                'Project_QA_usernames': Project_QA_usernames,
                'Project_Head_usernames':Project_Head_usernames,
                'checklist':checklist,
                'formA':formA,
                'tryingredcolor':tryingredcolor,
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',
            })
         else:
            return redirect('home')

     return redirect('home')
    
def DHPre_three(request, pk):
        #--------Default sending of checklist-----#
        user_project_name =request.user.Project_Name 
        Project_QA = Users.objects.filter(Project_Name=user_project_name,is_ProjectQA=True)
        Project_QA_usernames = [user.username for user in Project_QA]
        Project_head = Users.objects.filter(Project_Name=user_project_name,is_ProjectHead=True)
        Project_Head_usernames = [user.username for user in Project_head]
        #--------Default sending of checklist-----#
        checklist_current_status = CheckList_Trans_Header.objects.get(Doc_ID=pk)
        checklist_current_status.checklist_status = 'PQA and ProjectHead Queue'
        checklist_current_status.assigned_to_ProjectQA = Project_QA_usernames
        checklist_current_status.assigned_to_ProjectHead = Project_Head_usernames
        checklist_current_status.save()
        
        details_records = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
        checklist_item_ids = [record.CheckList_Item_ID for record in details_records]

        form_data = request.POST
        prefixes = ['form{}'.format(i) for i in range(1, len(checklist_item_ids) + 1)]
        forms_with_items = list(zip([CheckList_Trans_DetailsFormFill2(prefix=prefix, data=form_data) for prefix in prefixes], checklist_item_ids))

        all_forms_valid = True
        valid_forms = [] 
        
        for prefix in prefixes:
            form = CheckList_Trans_DetailsFormFill2(prefix=prefix,data=form_data)
            if not form.is_valid():
                all_forms_valid = False
                break
            else: 
                valid_forms.append(form) 

        if all_forms_valid :
            for form, item_desc in zip(valid_forms, checklist_item_ids):
                form_instance = form.save(commit=False)  
                instance = get_object_or_404(CheckList_Trans_Details, Doc_ID=pk, CheckList_Item_ID=item_desc)    
                instance.Site_DH_EQA_Status = form.cleaned_data['Site_DH_EQA_Status']
                instance.Site_DH_EQA_Comment = form.cleaned_data['Site_DH_EQA_Comment'] 
                instance.save()
                
            messages.info(request,'Checklist submited to Project_QA Successfully..!')
            return render(request, 'checklists/home.html', {
                'forms_with_items': forms_with_items,
                'isActive': True,
                'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'pk': pk,
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',
            })
        else:
            return render(request, 'checklists/DHPre_three.html', {
                'forms_with_items': forms_with_items,
                'isActive': True,
                'pk': pk,
                'error_message': 'Some forms are invalid. Please check your inputs.',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',
            })
                 
#-------Checklist Queue Part for all members----------
def ProjectHead_checklist_Queue(request):
   
    checklists = CheckList_Trans_Header.objects.filter(
    Q(Q(checklist_status='Completed_By_ProjectQA & Pending_By_ProjectHead') | Q(checklist_status='Completed_By_DHEQA & Pending_By_ProjectQA_AND_Pending_By_ProjectHead')) &
    (Q(assigned_to_ProjectQA=request.user) | Q(assigned_to_ProjectHead=request.user))
).order_by('-inspection_Start_Date')
    list = []
    for checklist in checklists:
     if checklist.Poorly_implimented_Quality_Checks is not None and checklist.Poorly_implimented_Quality_Checks != "":
        list.append(checklist.Doc_ID) 


    
    context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'list':list,
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/ProjectHead_checklist_Queue.html',context)

def ProjectQA_checklist_Queue(request):
    
    checklists = CheckList_Trans_Header.objects.filter(Q(checklist_status='Completed_By_DHEQA & Pending_By_ProjectQA_AND_Pending_By_ProjectHead') & Q(assigned_to_ProjectQA=request.user)).order_by('-inspection_Start_Date')
    context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    
    return render(request,'checklists/ProjectQA_checklist_Queue.html',context)
    
def DHEQA_checklist_Queue(request):
    
    checklists = CheckList_Trans_Header.objects.filter(
        Q(checklist_status='Completed_By_SiteEngineer & Pending_By_DHEQA') & Q(assigned_to=request.user)
    ).order_by('-inspection_Start_Date')

    mismatched_checklists = set()
    matched_checklists = set()

    for checklist in checklists:
        questions = CheckList_Trans_Details.objects.filter(
            Doc_ID=checklist
        ).values('Doc_ID', 'CheckList_Item_ID', 'Site_Engineer_Status')

        checklist_id = checklist.CheckList_ID
        questions_and_answers = CheckList_Footer.objects.filter(
            CheckList_Title=checklist_id
        ).values('CheckList_Item_Desc', 'answer')

        local_mismatched_checklists = set()
        local_matched_checklists = set()

        for question in questions:
            doc_id = question['Doc_ID']
            checklist_item_id = question['CheckList_Item_ID']
            site_engineer_answer = question['Site_Engineer_Status']

            
            original_answer = next(
                (item['answer'] for item in questions_and_answers if item['CheckList_Item_Desc'] == checklist_item_id),
                None
            )

            if original_answer is not None and site_engineer_answer != original_answer:
                local_mismatched_checklists.add(doc_id)
            elif original_answer is not None:
                local_matched_checklists.add(doc_id)

        
        if local_mismatched_checklists:
            mismatched_checklists.update(local_mismatched_checklists)
        elif local_matched_checklists:
            matched_checklists.update(local_matched_checklists)

    #-----just trying ----
    context = {'checklists':checklists,
               'isActive' : True,
               'mismatched_checklists':mismatched_checklists,
               'matched_checklists':matched_checklists,
               
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,}
    return render(request,'checklists/DHEQA_checklist_Queue.html',context)

def closed_checklist(request,pk):
    checklist = CheckList_Trans_Header.objects.get(pk=pk)
    checklist.checklist_status = 'Completed'
    checklist.is_resolved = True
    checklist.save()
    History.objects.create(Doc_ID=checklist,Comment=f"{request.user} Closed checklist ")
    messages.info(request,'Checklist has been send to Project QA! Thank You ')
    return redirect('checklist_queue')

def DHEQA_workspace(request):
    checklists = CheckList_Trans_Header.objects.filter(
        Q(checklist_status='Completed_By_SiteEngineer & Active_At_DHEQA') &
        Q(assigned_to__icontains=request.user.username) &
        Q(is_resolved=False)
        ).order_by('-inspection_Start_Date')

    mismatched_checklists = set()
    matched_checklists = set()

    for checklist in checklists:
        questions = CheckList_Trans_Details.objects.filter(
            Doc_ID=checklist
        ).values('Doc_ID', 'CheckList_Item_ID', 'Site_Engineer_Status')

        checklist_id = checklist.CheckList_ID
        questions_and_answers = CheckList_Footer.objects.filter(
            CheckList_Title=checklist_id
        ).values('CheckList_Item_Desc', 'answer')

        local_mismatched_checklists = set()
        local_matched_checklists = set()

        for question in questions:
            doc_id = question['Doc_ID']
            checklist_item_id = question['CheckList_Item_ID']
            site_engineer_answer = question['Site_Engineer_Status']

            
            original_answer = next(
                (item['answer'] for item in questions_and_answers if item['CheckList_Item_Desc'] == checklist_item_id),
                None
            )

            if original_answer is not None and site_engineer_answer != original_answer:
                local_mismatched_checklists.add(doc_id)
            elif original_answer is not None:
                local_matched_checklists.add(doc_id)

        
        if local_mismatched_checklists:
            mismatched_checklists.update(local_mismatched_checklists)
        elif local_matched_checklists:
            matched_checklists.update(local_matched_checklists)

    context ={'checklists':checklists,
              'isActive': True,
              'mismatched_checklists':mismatched_checklists,
              'matched_checklists':matched_checklists,
              
                    'app_title': 'Fill Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,}
    return render(request,'checklists/DHEQA_workspace.html',context)

def ProjectQA_workspace(request):
    checklists = CheckList_Trans_Header.objects.filter(
        Q(checklist_status='PQA and ProjectHead Queue') &
        Q(assigned_to_ProjectQA__icontains=request.user.username) &
        Q(is_resolved=False)
        ).order_by('-inspection_Start_Date')
    context ={'checklists':checklists,
              'isActive': True,
                'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/ProjectQA_workspace.html',context)

def ProjectHead_workspace(request):
    checklists = CheckList_Trans_Header.objects.filter(
        Q(Q(checklist_status='PQA and ProjectHead Queue') | Q(checklist_status='Completed_By_ProjectQA & Active_At_ProjectHead')) &
        Q(assigned_to_ProjectHead__icontains=request.user.username) &
        Q(is_resolved=False)
        ).order_by('-inspection_Start_Date')
    list = []
    for checklist in checklists:
     if checklist.Poorly_implimented_Quality_Checks is not None and checklist.Poorly_implimented_Quality_Checks != "":
        list.append(checklist.Doc_ID) 
    context ={'checklists':checklists,
              'isActive': True,
              'list':list,
              'page_title': 'Ashoka Buildcon Limited',
              'customer_name' : 'Ashoka Buildcon Limited',
              'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/ProjectHead_workspace.html',context)


def all_closed_checklists(request):
    checklists = CheckList_Trans_Header.objects.filter(assigned_to_ProjectHead__icontains=request.user.username,is_resolved=True).order_by('-inspection_Start_Date')
    context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/all_closed_checklists.html',context)

def all_checklist_sendTo_ProjectQA(request):

    status_values = [
    'Completed_By_SiteEngineer & Active_At_DHEQA',
    'PQA and ProjectHead Queue',
    'Completed_By_DHEQA & Active_At_ProjectQA',
    'Completed_By_DHEQA & Active_At_ProjectHead',
    'Completed_By_ProjectQA & Active_At_ProjectHead',
    'Completed_By_ProjectHead',
     ]
    query = Q()
    for status in status_values:
     query |= Q(checklist_status=status)
    checklists = CheckList_Trans_Header.objects.filter(
        Q(assigned_to__icontains=request.user.username) & query
        ).order_by('-inspection_Start_Date')

    context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/all_checklist_sendTo_ProjectQA.html',context)

def all_checklist_sendTo_ProjectHead(request):
    status_values = [
    'Completed_By_SiteEngineer & Active_At_DHEQA',
    'PQA and ProjectHead Queue',
    'Completed_By_DHEQA & Active_At_ProjectQA',
    'Completed_By_DHEQA & Active_At_ProjectHead',
    'Completed_By_ProjectQA & Active_At_ProjectHead',
    'Completed_By_ProjectHead',
     ]
    query = Q()
    for status in status_values:
     query |= Q(checklist_status=status)
    checklists = CheckList_Trans_Header.objects.filter(
        Q(assigned_to_ProjectQA__icontains=request.user.username) & query
        ).order_by('-inspection_Start_Date')

    context = {'checklists':checklists,
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/all_checklist_sendTo_ProjectHead.html',context)

def Checklist_By_You(request):
    if not request.user.is_superuser:
        AppName = inspect.stack()[0][3].strip()
        AppID = cfg.Apps[AppName]
        UserID = request.user.UserID
        if not CheckAuthorization(AppID=AppID, UserID=UserID):
            messages.info(request,'You are not authorized for this application')
            return redirect('/home')
            
    #checklists = CheckList_Trans_Header.objects.filter(Name_Of_ABLStaff=request.user).order_by('-inspection_Start_Date')
    checklists = CheckList_Trans_Header.objects.filter(
    Q(Q(checklist_status='Completed_By_SiteEngineer & Pending_By_DHEQA') | Q(checklist_status='Completed_By_SiteEngineer & Active_At_DHEQA') | Q(checklist_status='Rejected')) &
    (Q(Name_Of_ABLStaff=request.user))
).order_by('-inspection_Start_Date')
    context = {'checklists':checklists, 
              
                    'app_title': 'My Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,}
    return render(request,'checklists/Checklist_By_You.html',context)

def checklist_avtar(request,pk):
    checklist = CheckList_Trans_Header.objects.get(pk=pk) 
    checklistQuestions = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
    
    checklist_item_ids = []
    site_engineer_statuses = []
    site_engineer_comments = []
    Site_DH_EQA_Statuses = []
    Site_DH_EQA_Comments =[]
    

    for record in checklistQuestions:
            checklist_item_ids.append(record.CheckList_Item_ID)
            site_engineer_statuses.append(record.Site_Engineer_Status)
            site_engineer_comments.append(record.Site_Engineer_Comment)
            Site_DH_EQA_Statuses.append(record.Site_DH_EQA_Status)
            Site_DH_EQA_Comments.append(record.Site_DH_EQA_Comment)
            
    checklist_data = zip(checklist_item_ids, site_engineer_statuses, site_engineer_comments,Site_DH_EQA_Statuses,Site_DH_EQA_Comments)
            
            
    return render(request,'checklists/checklist_avtar.html',{'checklist':checklist,'checklist_data':checklist_data,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',})
    
#--------Project QA work -------------
def observation(request,pk):
    user_project_name =request.user.Project_Name 
    Project_Head = Users.objects.filter(Project_Name=user_project_name,is_ProjectHead=True)
    Project_Head_usernames = [user.username for user in Project_Head]
    checklist_instance = CheckList_Trans_Header.objects.get(Doc_ID=pk)
    checklist_items = CheckList_Footer.objects.filter(CheckList_Title=checklist_instance.CheckList_ID)
  

    if request.method == 'POST':
        form = ProjectQAForm(request.POST,instance=checklist_instance)
        if form.is_valid(): 
            form.save()
            checklist_instance.checklist_status = 'Completed_By_ProjectQA & Active_At_ProjectHead'
            checklist_instance.assigned_to_ProjectHead = Project_Head_usernames
            checklist_instance.save()
            History.objects.create(Doc_ID=checklist_instance,Comment=f"{request.user} send checklist to {checklist_instance.assigned_to_ProjectHead} ")
            messages.info(request,'Your Checklist has Successfully Submited to Project Head...!') 
            return redirect('/home')
    else:
        form = ProjectQAForm() 
    checklist = CheckList_Trans_Header.objects.get(Doc_ID=pk)
    checklistQuestions = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
    
    checklist_item_ids = []
    site_engineer_statuses = []
    site_engineer_comments = []
    Site_DH_EQA_Statuses = []
    Site_DH_EQA_Comments =[]
    

    for record in checklistQuestions:
            checklist_item_ids.append(record.CheckList_Item_ID)
            site_engineer_statuses.append(record.Site_Engineer_Status)
            site_engineer_comments.append(record.Site_Engineer_Comment)
            Site_DH_EQA_Statuses.append(record.Site_DH_EQA_Status)
            Site_DH_EQA_Comments.append(record.Site_DH_EQA_Comment)
            
    checklist_data = zip(checklist_item_ids, site_engineer_statuses, site_engineer_comments,Site_DH_EQA_Statuses,Site_DH_EQA_Comments)
    tryingredcolor = zip(checklist_items, site_engineer_statuses, site_engineer_comments,Site_DH_EQA_Statuses,Site_DH_EQA_Comments)
    return render(request,'checklists/observation_by_PQA.html',{'form':form,''''formA':formA,''''pk':pk,'isActive': True,'checklist':checklist,'checklist_data':checklist_data, 
                'customer_name' : 'Ashoka Buildcon Limited','tryingredcolor':tryingredcolor,
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',})

def observation_PQA_Queue(request):
    checklists = CheckList_Trans_Header.objects.filter(Q(assigned_to_ProjectQA=request.user)).order_by('-inspection_Start_Date')
    context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/observation_PQA_Queue.html',context)

def project_head(request,pk):
    checklist_instance = CheckList_Trans_Header.objects.get(Doc_ID=pk)

    if request.method == 'POST':
        form = ProjectHeadForm(request.POST,instance=checklist_instance)
       
        if form.is_valid():
            form.save()
            checklist_instance.checklist_status = 'Completed_By_ProjectHead' 
            checklist_instance.is_resolved = True
            checklist_instance.save()
            messages.info(request,'Your Checklist has Successfully Resolved...!') 
            return redirect('/home')
    else:
        form = ProjectHeadForm() 
    
    checklist = CheckList_Trans_Header.objects.get(Doc_ID=pk)
    checklistQuestions = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
    
    checklist_item_ids = []
    site_engineer_statuses = []
    site_engineer_comments = []
    Site_DH_EQA_Statuses = []
    Site_DH_EQA_Comments =[]
    

    for record in checklistQuestions:
            checklist_item_ids.append(record.CheckList_Item_ID)
            site_engineer_statuses.append(record.Site_Engineer_Status)
            site_engineer_comments.append(record.Site_Engineer_Comment)
            Site_DH_EQA_Statuses.append(record.Site_DH_EQA_Status)
            Site_DH_EQA_Comments.append(record.Site_DH_EQA_Comment)
            
    checklist_data = zip(checklist_item_ids, site_engineer_statuses, site_engineer_comments,Site_DH_EQA_Statuses,Site_DH_EQA_Comments)
            
            
    return render(request,'checklists/Project_Head.html',{'form':form,'isActive': True,'checklist':checklist,'checklist_data':checklist_data,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',})


#-----Rejection Part-----
def Rejected_checklist(request,pk):
    # if not request.user.is_superuser:
    #     AppName = inspect.stack()[0][3].strip()
    #     AppID = cfg.Apps[AppName]
    #     UserID = request.user.UserID
    #     if not CheckAuthorization(AppID=AppID, UserID=UserID):
    #         messages.info(request,'You are not authorized for this application')
    #         return redirect('/home')
    checklist = CheckList_Trans_Header.objects.get(pk=pk)
    checklist.rejected_byDHEQA = True
    checklist.checklist_status = 'Rejected'
    checklist.save()
   
    History.objects.create(Doc_ID=checklist,Comment=f"{request.user} rejected checklist")
    return redirect('/home')

def rejected_checklists(request):
    # if not request.user.is_superuser:
    #     AppName = inspect.stack()[0][3].strip()
    #     AppID = cfg.Apps[AppName]
    #     UserID = request.user.UserID
    #     if not CheckAuthorization(AppID=AppID, UserID=UserID):
    #         messages.info(request,'You are not authorized for this application')
    #         return redirect('/home')
    checklists = CheckList_Trans_Header.objects.filter(rejected_byDHEQA=True)
    '''context = {'checklists':checklists,'isActive' : True,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'
                }'''
    context = {     'checklists':checklists,
                    'app_title': 'Rejected Checklist',
                    'username': request.user.get_full_name(), 
                    'isActive' : request.user.is_authenticated,
                    'isSuperUser' : request.user.is_superuser,
                    'app_title': 'Fill Checklist',
                    'isForm' : True,
                    'isHomePage' : True,
                    'company_name' : cfg.CompanyName,
                  }         
    return render(request,'checklists/rejected_checklists.html',context)

def edit_checklist(request, pk):
    user_project_name =request.user.Project_Name
    dheqa = Users.objects.filter(Project_Name=user_project_name,is_DHEQA=True)
    usernames = [user.username for user in dheqa]

    header_instance = CheckList_Trans_Header.objects.get(pk=pk)

    # logdata(header_instance)
    
    rejection_comment = header_instance.rejection_comment
    #logdata(rejection_comment)
    header_form = CheckListForm(request.POST, instance=header_instance)   
    checklist_records = CheckList_Trans_Details.objects.filter(Doc_ID_id=pk)
    checklist_item_ids = [record.CheckList_Item_ID for record in checklist_records]
    header_instance.rejected_byDHEQA = False
    header_instance.checklist_status = 'Completed_By_SiteEngineer & Active_At_DHEQA'
    # logdata(header_instance.checklist_status)
    header_instance.assigned_to = usernames
    header_instance.save()
  
  
    if request.method == 'POST':
        if header_form.is_valid():
        
            header_form.save()
        
        forms = [CheckList_Trans_DetailsFormFill(request.POST, instance=record, prefix=str(record.CheckList_Item_ID)) for record in checklist_records]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            History.objects.create(Doc_ID=header_instance,Comment=f"{request.user} edited checklist")
            return redirect('/home') 

    else:
        forms = [CheckList_Trans_DetailsFormFill(instance=record, prefix=str(record.CheckList_Item_ID)) for record in checklist_records]
        header_form = CheckListForm(instance=header_instance)
    zipped_data = zip(forms, checklist_item_ids)
    return render(request, 'checklists/edit.html', {'isActive': True, 'zipped_data': zipped_data,'header_form':header_form,  'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited',
                'rejection_comment':rejection_comment,
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'usernames':usernames,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',})

def all_checklists(request):
    checklists = CheckList_Trans_Header.objects.all().order_by('-inspection_Start_Date')
    list = []
    for checklist in checklists:
     if checklist.Poorly_implimented_Quality_Checks is not None and checklist.Poorly_implimented_Quality_Checks != "":
        list.append(checklist.Doc_ID) 
    context ={'checklists':checklists,
              'isActive': True,
              'list':list,
              'page_title': 'Ashoka Buildcon Limited',
              'customer_name' : 'Ashoka Buildcon Limited',
              'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/all_checklists.html',context)

'''if not request.user.is_superuser:
        AppName = inspect.stack()[0][3].strip()
        AppID = cfg.Apps[AppName]
        UserID = request.user.UserID
        if not CheckAuthorization(AppID=AppID, UserID=UserID):
            messages.info(request,'You are not authorized for this application')
            return redirect('/home')
            
    checklists = CheckList_Trans_Header.objects.all().order_by('-inspection_Start_Date')
    context = {'checklists':checklists,'isActive' : True, 
                'customer_name' : 'Ashoka Buildcon Limited',
                'page_title': 'Ashoka Buildcon Limited',
                'app_title': 'Fill Checklist',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'isForm' : True,
                'isHomePage' : True,
                'company_name' : cfg.CompanyName,
                'customer_name' : 'Ashoka Buildcon Limited',}
    return render(request,'checklists/all_checklists.html',context)'''
