from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,UserCreationForm
from .models import CheckList_Trans_Header,CheckList_Trans_Details,CheckList_Trans_Details
from administration.models import Structural_Element,CheckList_Header,CheckList_Footer
from administration.models import Users,Structural_Element,Projects,Sites,Departments
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Q
from crispy_forms.bootstrap import InlineRadios

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password= forms.CharField(label='Password', widget=forms.PasswordInput())

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Repeat New Password', widget=forms.PasswordInput())

class CheckMaterialStockForm(forms.Form):
    materialcode = forms.CharField(label='Material Code', widget=forms.TextInput())
    agingdate = forms.DateField(label='Date Of Aging', widget=forms.DateInput(attrs={'type': 'date'}))
    
class addUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['first_name','password1','password2','last_name','is_superuser','email','is_staff','is_active','username','is_SiteEngineer','is_DHEQA','is_ProjectQA','is_ProjectHead']
      
class EditUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name','last_name','is_superuser','email','is_staff','is_active','username','is_SiteEngineer','is_DHEQA','is_ProjectQA','is_ProjectHead']    

class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['email','username','password1']
        
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['Project_Name']
        
        def clean(self):
            cleaned_data = super().clean()
            project_name = cleaned_data.get('Project_Name')

            # Convert project name to uppercase
            if project_name:
                cleaned_data['Project_Name'] = project_name.upper()

            return cleaned_data
        
class SiteForm(forms.ModelForm):
    class Meta:
        model = Sites
        fields = ['Site_Name','Project_Name']
        
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['Department_Name']
        
class CheckList_HeaderForm(forms.ModelForm):
    class Meta:
        model = CheckList_Header
        fields = ['CheckList_Title']
        
        
class CheckList_FooterForm(forms.ModelForm):
    class Meta:
        model = CheckList_Footer
        fields = ['CheckList_Title','is_important','CheckList_Item_Desc','answer']
  
        
class CheckList_Trans_HeaderForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        #fields = ['CheckList_ID','Project_Name','inspection_Start_Date','inspection_End_Date','Contractor','Location','Structural_Element']
        fields = ['CheckList_ID','Project_Name','inspection_End_Date','Contractor','Location','Structural_Element']

        
class CheckListTransHeaderFormfill(forms.ModelForm):
    CheckList_ID = forms.ModelChoiceField(
        queryset= CheckList_Header.objects.all(),empty_label="Select a Checklist Name")
    
    Project_Name = forms.ModelChoiceField(
        queryset= Projects.objects.all(),empty_label="Select a Project Name")
    
    Site_Name = forms.ModelChoiceField(
        queryset= Sites.objects.all(),empty_label="Select a Sites Name")
    
    Structural_Element = forms.ModelChoiceField(
        queryset= Structural_Element.objects.all(),empty_label="Select a Structural Element ")
    class Meta:
        model = CheckList_Trans_Header
        fields = ['CheckList_ID','Project_Name','Site_Name','Contractor','Location','Structural_Element','Chainage']
  
    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit','Save'))

            
class stucturalElemForm(forms.ModelForm):
    class Meta:
        model = Structural_Element       
        fields = ['Structural_Element']   
            
class CheckList_Trans_DetailsFormFill(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Details
        fields = ['Site_Engineer_Status','Site_Engineer_Comment']
        widgets = {
            'Site_Engineer_Status': forms.RadioSelect(attrs={'class': 'horizontal-radio'}),
        }

class CheckList_Trans_DetailsFormFill2(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Details
        fields = ['Site_DH_EQA_Status','Site_DH_EQA_Comment']
        widgets = {
            'Site_DH_EQA_Status': forms.RadioSelect(),
        }

class ProjectQAForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['Well_implimented_Quality_Checks','Fairly_implimented_Quality_Checks','Poorly_implimented_Quality_Checks','Quality_Engineer_Comment']
        widgets = {
            'Quality_Engineer_status': forms.RadioSelect()
        }
        labels = {'Well_implimented_Quality_Checks':'',
                  'Fairly_implimented_Quality_Checks':'',
                  'Poorly_implimented_Quality_Checks':''}

class ProjectHeadForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['Project_Head_Status']
        widgets = {
            'Project_Head_Status': forms.RadioSelect()
        }

class assigned_to_ProjectQAForm(forms.ModelForm):
    assigned_to_ProjectQA = forms.ModelMultipleChoiceField(
        queryset=Users.objects.filter(Q(is_ProjectQA=True) | Q(is_ProjectHead=True)),
        widget=forms.CheckboxSelectMultiple,
        label='Submitted to - ProjectQA',
    )

    class Meta:
        model = CheckList_Trans_Header
        fields = ['assigned_to_ProjectQA']


class rejected_from_ProjectQAForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['rejected_byDHEQA','rejection_comment']
       
        
class assigned_to_ProjectHeadForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['assigned_to_ProjectHead']
        
        
    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['assigned_to_ProjectHead'].queryset = Users.objects.filter(is_ProjectHead=True)
       
#--trying----
class CheckListForm(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['CheckList_ID','Project_Name','Site_Name','Contractor','Location','Structural_Element','Chainage','assigned_to']


class CheckListForm1(forms.ModelForm):
    class Meta:
        model = CheckList_Trans_Header
        fields = ['CheckList_ID','Project_Name','Site_Name','Contractor','Location','Structural_Element','Chainage','assigned_to','checklist_status','rejected_byDHEQA']