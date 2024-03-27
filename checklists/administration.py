from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ProjectForm,stucturalElemForm,SiteForm,DepartmentForm,EditUserForm,CheckList_HeaderForm,CheckList_FooterForm,CheckList_Trans_HeaderForm,addUserForm,ChangePasswordForm
from django.contrib import messages
from administration.models import Projects,Users,Sites,CheckList_Header,CheckList_Footer,Structural_Element
from .models import History
#from Logfile import logdata


'''def add_project(request):
    projects = Project_Master.objects.all().order_by('Project_Name')

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project_name = form.cleaned_data['Project_Name']
            project_name = project_name.upper()

            # Check if a project with the same name already exists
            if Project_Master.objects.filter(Project_Name=project_name).exists():
                form.add_error('Project_Name', 'A project with this name already exists.')
                messages.warning(request, 'A project with this name already exists.')
                return render(request, 'checklists/add_project.html', {'form': form, 'projects': projects})

            form.cleaned_data['Project_Name'] = project_name  # Set the cleaned_data with capitalized project name
            logdata(form.cleaned_data['Project_Name'])
            form.save()
            History.objects.create(Doc_ID=f"Project-Added", Comment=f"{request.user} Added Project ")
            messages.info(request, 'Project added successfully')
            return redirect('add_project')

        else:
            messages.warning(request, 'Something went wrong! Please check form input.')

    else:
        form = ProjectForm()

    context = {
        'form': form,
        'isActive': True,
        'page_title': 'Ashoka Buildcon Limited',
        'customer_name': 'Ashoka Buildcon Limited',
        'projects': projects,
    }
    return render(request, 'checklists/add_project.html', context)



def edit_project(request,pk):
    if request.method == 'POST':
        project = Project_Master.objects.get(Project_ID=pk)
        editprojectform = ProjectForm(request.POST, instance=project)
        logdata(editprojectform)
        if editprojectform.is_valid():
            editprojectform.save()
            History.objects.create(Doc_ID=f"{project} edited ",Comment=f"{request.user} edited project {project} ")
            #messages.success(request, 'User details updated successfully.')
            return redirect('add_project')
            
    else:
        project = Project_Master.objects.get(Project_ID=pk)
        editprojectform = ProjectForm(instance=project)
        
    return render(request, 'checklists/editProjectForm.html', {'editprojectform': editprojectform, 'project': project,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
     
def delete_project(request,pk):   
    if request.method == 'POST':
        project = Project_Master.objects.get(Project_ID=pk) 
        project.delete()
        History.objects.create(Doc_ID=f"{project} deleted ",Comment=f"{request.user} deleted project {project} ")
        return redirect('add_project')
      
def add_site(request):
    sites = Site_Master.objects.all().order_by('Site_Name')
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(Doc_ID=f"site added ",Comment=f"{request.user} added site ")
            messages.info(request,'Site added successfully')
            return redirect('add_site')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('add_site')
    else:
        form = SiteForm()
        context = {
            'form': form,
            'isActive': True,
            'sites':sites,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
        return render(request, 'checklists/add_site.html', context)
       
def edit_site(request,pk):
    if request.method == 'POST':
        site = Site_Master.objects.get(Site_ID=pk)
        editsiteform = SiteForm(request.POST, instance=site)
        if editsiteform.is_valid():
            editsiteform.save()
            History.objects.create(Doc_ID=f"{site} edited ",Comment=f"{request.user} edited site {site} ")
            #messages.success(request, 'User details updated successfully.')
            return redirect('add_site')
            
    else:
        site = Site_Master.objects.get(Site_ID=pk)
        editsiteform = SiteForm(instance=site)
        
    return render(request, 'checklists/editSiteForm.html', {'editsiteform': editsiteform, 'site': site,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
    
def delete_site(request,pk):
    if request.method == 'POST':
        site = Site_Master.objects.get(Site_ID=pk) 
        site.delete()
        History.objects.create(Doc_ID=f"{site} deleted ",Comment=f"{request.user} deleted site {site} ")
        
        return redirect('add_site')
    
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(Doc_ID=f"Department added ",Comment=f"{request.user} add department ")
            
            messages.info(request,'Department added successfully')
            return redirect('add_department')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('add_department')
    else:
        form = DepartmentForm()
        context = {
            'form': form,
            'isActive': True,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
        return render(request, 'checklists/add_department.html', context)   '''
    
def Add_CheckList_Header(request):
    checklists = CheckList_Header.objects.all().order_by('CheckList_ID')
    # logdata(checklists)
    if request.method == 'POST':
        form = CheckList_HeaderForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(Doc_ID=f"Checklist name added",Comment=f"{request.user} added Checklist name")
            
            messages.info(request,'Add_CheckList_HeaderForm added successfully')
            return redirect('Add_CheckList_Header')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('Add_CheckList_Header')
    else:
        form = CheckList_HeaderForm()
        context = {
            'form': form,
            'isActive': True,
            'checklists':checklists,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
    return render(request, 'checklists/Add_CheckList_HeaderForm.html', context)
    
def edit_CheckList_Header(request,pk):
     if request.method == 'POST':
        checklist = CheckList_Header.objects.get(CheckList_ID=pk)
        editchecklist_headerform = CheckList_HeaderForm(request.POST, instance=checklist)
        if editchecklist_headerform.is_valid():
            editchecklist_headerform.save()
            History.objects.create(Doc_ID=f"{checklist} edited ",Comment=f"{request.user} edited {checklist} ")
            
            #messages.success(request, 'User details updated successfully.')
            return redirect('Add_CheckList_Header')   
     else:
        checklist = CheckList_Header.objects.get(CheckList_ID=pk)
        editchecklist_headerform = CheckList_HeaderForm(instance=checklist)
        
     return render(request, 'checklists/editchecklist_NameForm.html', {'editchecklist_headerform': editchecklist_headerform, 'checklist': checklist,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
 
def delete_CheckList_Header(request,pk):
    if request.method == 'POST':
        checklist = CheckList_Header.objects.get(CheckList_ID=pk) 
        checklist.delete()
        History.objects.create(Doc_ID=f"{checklist} deleted ",Comment=f"{request.user} deleted {checklist} ")
        
        return redirect('Add_CheckList_Header')

def Add_CheckList_Footer(request):
    checklistQuestions = CheckList_Footer.objects.all().order_by('CheckList_ID')
    if request.method == 'POST':
        form = CheckList_FooterForm(request.POST)
        if form.is_valid():
            form.save()
            
            History.objects.create(Doc_ID=f"checklist Question added",Comment=f"{request.user} added checklist Question")
            messages.info(request,'Add_CheckList_FooterForm added successfully')
            return redirect('Add_CheckList_Footer')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('Add_CheckList_Footer')
    else:
        form = CheckList_FooterForm()
        context = {
            'form': form,
            'isActive': True,
            'checklistQuestions':checklistQuestions,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
        return render(request, 'checklists/Add_CheckList_Footer.html', context)
    
def edit_CheckList_Footer(request,pk):
     if request.method == 'POST':
        checklistQues = CheckList_Footer.objects.get(CheckList_Item_ID=pk)
        editchecklist_Questionform = CheckList_FooterForm(request.POST, instance=checklistQues)
        if editchecklist_Questionform.is_valid():
            editchecklist_Questionform.save()
            History.objects.create(Doc_ID=f"{checklistQues} edited ",Comment=f"{request.user} edited {checklistQues} ")
            #messages.success(request, 'User details updated successfully.')
            return redirect('Add_CheckList_Footer')
            
     else:
        checklistQues = CheckList_Footer.objects.get(CheckList_Item_ID=pk)
        editchecklist_Questionform = CheckList_FooterForm(instance=checklistQues)
        
     return render(request, 'checklists/editchecklist_QuestionForm.html', {'editchecklist_Questionform': editchecklist_Questionform, 'checklistQues': checklistQues,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
    
def delete_CheckList_Footer(request,pk):
    if request.method == 'POST':
        checklistQuestion = CheckList_Footer.objects.get(CheckList_Item_ID=pk) 
        checklistQuestion.delete()
        History.objects.create(Doc_ID=f"{checklistQuestion} deleted ",Comment=f"{request.user} edited {checklistQuestion} ")
        
        return redirect('Add_CheckList_Footer')
def Add_CheckList_Trans_Header(request):
    if request.method == 'POST':
        form = CheckList_Trans_HeaderForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Add_CheckList_Trans_Headerform added successfully')
            return redirect('Add_CheckList_Trans_Header')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('Add_CheckList_Trans_Header')
    else:
        form = CheckList_Trans_HeaderForm()
        context = {
            'form': form,
            'isActive': True,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
        return render(request, 'checklists/Add_CheckList_Trans_Header.html', context)   
    
def Add_Structural_Elements(request):
    elements = Structural_Element.objects.all()
    if request.method == 'POST':
        form = stucturalElemForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(Doc_ID=f"added structural Element",Comment=f"{request.user} added structural Element")
            
            messages.info(request,'Structural Element added successfully')
            return redirect('Add_Structural_Elements')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('Add_Structural_Elements')
    else:
        form = stucturalElemForm()
        context = {
            'form': form,
            'isActive': True,
            'elements':elements,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
        }
        return render(request,'checklists/AddStructuralElement.html', context)
    
def edit_Structural_Elements(request,pk):
     if request.method == 'POST':
        element = Structural_Element.objects.get(Struc_Ele_ID=pk)
        editstructural_elem = stucturalElemForm(request.POST, instance=element)
        if editstructural_elem.is_valid():
            editstructural_elem.save()
            History.objects.create(Doc_ID=f"{element} edited ",Comment=f"{request.user} edited {element} ")
            
            messages.success(request, 'Structural Element  updated successfully.')
            return redirect('Add_Structural_Elements')   
     else:
        element = Structural_Element.objects.get(Struc_Ele_ID=pk)
        editstructural_elem = stucturalElemForm(instance=element)
        
     return render(request, 'checklists/editStructural_ElemForm.html', {'editstructural_elem': editstructural_elem, 'element': element,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
 
def delete_Structural_Elements(request,pk):
     if request.method == 'POST':
        element = Structural_Element.objects.get(Struc_Ele_ID=pk) 
        element.delete()
        History.objects.create(Doc_ID=f"{element} deleted ",Comment=f"{request.user} deleted {element} ")
        
        return redirect('Add_CheckList_Footer')
 
      
def addUser(request):
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(Doc_ID=f"added user",Comment=f"{request.user} added user")
            
            messages.info(request,'User added successfully')
            return redirect('addUser')
        else:
            messages.warning(request, 'Something went wrong! Please check form input.')
            return HttpResponse('addUser')
            
        
    else:
        form = addUserForm()
    users = Users.objects.all()
    context = {
            'form': form,
            'isActive': True,
            'users':users,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited'
        }
    return render(request, 'checklists/addUserForm.html', context)
    
def edit_user(request,user_id):
    if request.method == 'POST':
        user = Users.objects.get(User_ID=user_id)
        edituserform = EditUserForm(request.POST, instance=user)
       
        # logdata(edituserform)
        if edituserform.is_valid():
            edituserform.save()
            History.objects.create(Doc_ID=f"{user} edited ",Comment=f"{request.user} edited {user} ")
            return redirect('addUser')
            
    else:
        user = Users.objects.get(User_ID=user_id)
        edituserform = EditUserForm(instance=user)
       
    return render(request, 'checklists/editUserForm.html', {'edituserform': edituserform, 'user': user,'isActive': True,'page_title': 'Ashoka Buildcon Limited',
                'customer_name' : 'Ashoka Buildcon Limited'})
    
def delete_user(request, user_id):
    if request.method == 'POST':
        user = Users.objects.get(User_ID=user_id) 
        user.delete()
        History.objects.create(Doc_ID=f"{user} deleted  ",Comment=f"{request.user} deleted {user} ")

        return redirect('addUser')
    
    
    
def history(request):
    history = History.objects.all()
    context = {
          
            'isActive': True,
            'page_title': 'Ashoka Buildcon Limited',
            'customer_name' : 'Ashoka Buildcon Limited',
            'history':history  
    }
    return render(request,'checklists/history.html', context)
    

