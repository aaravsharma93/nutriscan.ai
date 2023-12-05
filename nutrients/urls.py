from django.urls import path

from .views import copyright,index, upload_excel_file, picture_Upload, loginRequest, registerRequest, logoutRequest, family_member,delete_member,getmemberdetails,edit_members

app_name = "nutriscan"

urlpatterns = [
    path('upload_file/', index, name='index'),
    path('nutrients/', upload_excel_file, name='nutrients'),
    path('api/', picture_Upload, name="getDailyAllowance"),
    path('login/', loginRequest, name="login"),
    path('register/', registerRequest, name="register"),
    path('logout/', logoutRequest, name="logout"),
    path('getmember/', getmemberdetails, name="getmember"),
    path('addmember/', family_member, name="addmember"),
    path('editmember/', edit_members, name="editmember"),
    path('deletemember/', delete_member, name="deletemember"),
    path('copyright/', copyright, name="copyright"),
    


]
