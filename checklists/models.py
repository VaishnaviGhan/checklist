from django.db import models
from django.db import models
from administration.models import Users,Projects,Sites,CheckList_Footer,CheckList_Header,Structural_Element
from django.db.models import Max
from django.utils import timezone

Site_Engineer_Status = (
    
    ('Yes','Yes'),
    ('No','No'),
    ('Na','NA'),
    ('Partial','Partial'), 
    ('Not_Observed','Not Observed'),
)
Site_DH_EQA_Status = (
    ('Yes',' Yes'),
    ('No',' No'),
    ('NA',' NA'),
    ('Partial',' Partial'),  
)

Project_Head_Status = (
    ('Noted, for necessary action..!','Noted, for necessary action..!'),

)

class CheckList_Trans_Header(models.Model):
    Status_choices = (
        ('Completed_By_SiteEngineer & Active_At_DHEQA','Completed_By_SiteEngineer & Active_At_DHEQA'),
        ('PQA and ProjectHead Queue','PQA and ProjectHead Queue'),
        ('Completed_By_DHEQA & Active_At_ProjectQA','Completed_By_DHEQA & Active_At_ProjectQA'),
        ('Completed_By_DHEQA & Active_At_ProjectHead','Completed_By_DHEQA & Active_At_ProjectHead'),
        ('Completed_By_ProjectQA & Active_At_ProjectHead','Completed_By_ProjectQA & Active_At_ProjectHead'),
        ('Completed_By_ProjectHead','Completed_By_ProjectHead'),
        ('Rejected','Rejected'),
    )
    Doc_ID = models.AutoField(primary_key=True)   
    CheckList_ID = models.ForeignKey(CheckList_Header, on_delete=models.CASCADE)
    Project_Name = models.ForeignKey(Projects,on_delete=models.CASCADE)
    Site_Name = models.ForeignKey(Sites,on_delete=models.CASCADE,default=True)
    Name_Of_ABLStaff = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='created_by')
    inspection_Start_Date = models.DateTimeField(auto_now_add=True)
    inspection_End_Date = models.DateTimeField(null=True, blank=True)
    Contractor = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Structural_Element = models.ForeignKey(Structural_Element,on_delete=models.CASCADE, blank=True, null=True)
    Chainage = models.CharField(max_length=100)
    Well_implimented_Quality_Checks = models.CharField(max_length=20,default=None,null=True,blank=True)
    Fairly_implimented_Quality_Checks = models.CharField(max_length=20,default=None,null=True,blank=True)
    Poorly_implimented_Quality_Checks = models.CharField(max_length=20,default=None,null=True,blank=True)
    Quality_Engineer_Comment = models.CharField(max_length=220,editable=True,blank=True)
    Project_Head_Status = models.CharField(max_length=70, choices=Project_Head_Status,default='Unspecified')
    assigned_to = models.JSONField(default=list)
    assigned_to_ProjectQA = models.JSONField(default=list)
    assigned_to_ProjectHead = models.JSONField(default=list)
    is_resolved = models.BooleanField(default=False)
    checklist_status = models.CharField(max_length=70,choices=Status_choices)
    rejected_byDHEQA = models.BooleanField(default=False)
    rejection_comment = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"Doc ID: {self.Doc_ID}, CheckList ID: {self.CheckList_ID}"
    
class CheckList_Trans_Details(models.Model):
    CheckList_Trans_Details_ID = models.AutoField(primary_key=True)   
    Doc_ID = models.ForeignKey(CheckList_Trans_Header, on_delete=models.CASCADE,related_name='doc_id_details')
    CheckList_ID = models.ForeignKey(CheckList_Trans_Header, on_delete=models.CASCADE, related_name='checklist_id_details')
    CheckList_Item_ID = models.CharField(max_length=500)
    Site_Engineer_Status = models.CharField(max_length=70, choices=Site_Engineer_Status,default='Unspecified')
    Site_DH_EQA_Status = models.CharField(max_length=70, choices=Site_DH_EQA_Status,default='Unspecified')
    Site_Engineer_Comment = models.CharField(max_length=220,editable=True,blank=True)
    Site_DH_EQA_Comment = models.CharField(max_length=220,editable=True,blank=True)
    
    def __str__(self):
        return f"Doc ID: {self.Doc_ID}"

class History(models.Model):
    History_ID = models.AutoField(primary_key=True)
    Doc_ID =  models.CharField(max_length=100)
    Date_Time = models.DateTimeField()
    Comment =  models.CharField(max_length=100,null=True)
    
    def save(self, *args, **kwargs):
        if not self.Date_Time:
            self.Date_Time = timezone.now()
        super().save(*args, **kwargs)



