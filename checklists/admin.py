from django.contrib import admin
from .models import History,CheckList_Header,CheckList_Footer,CheckList_Trans_Header,CheckList_Trans_Details ,Structural_Element
from django.contrib.auth.admin import UserAdmin

# class adminCustomUser(UserAdmin):
#     fieldsets = (
#        *UserAdmin.fieldsets,
#        (
#            'Custom Field Heading',
#            {
#                'fields':(
#                    'is_SiteEngineer',
#                    'is_DHEQA',
#                    'is_ProjectQA',
#                    'is_ProjectHead',
                   
#                )
#            }
#        )
#    )
# admin.site.register(CustomUser,adminCustomUser)


class adminCheckList_Trans_Header(admin.ModelAdmin):

    list_display = ['Doc_ID','CheckList_ID','Project_Name','Site_Name','Name_Of_ABLStaff','inspection_Start_Date','Contractor','Location','Structural_Element','Well_implimented_Quality_Checks','Fairly_implimented_Quality_Checks','Poorly_implimented_Quality_Checks','Quality_Engineer_Comment','Project_Head_Status','assigned_to','assigned_to_ProjectQA','assigned_to_ProjectHead','is_resolved','checklist_status','rejected_byDHEQA']
 
admin.site.register(CheckList_Trans_Header,adminCheckList_Trans_Header)

class adminCheckList_Trans_Details(admin.ModelAdmin):
    list_display = ['CheckList_Trans_Details_ID','Doc_ID','CheckList_ID','CheckList_Item_ID','Site_Engineer_Status','Site_DH_EQA_Status','Site_Engineer_Comment','Site_DH_EQA_Comment']
  
    
admin.site.register(CheckList_Trans_Details,adminCheckList_Trans_Details)
