from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template import loader
import MySQLdb
from django.http import HttpResponse

connect = MySQLdb.connect(host='localhost',database='db_moneta',user='moneta_user',password='db_password')
mycursor = connect.cursor()



# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'user_profile/change_password.html', {
#         'form': form

#     })

def change_password(request, user):
    #user = "cocain@gmail.com"
    old_passw = ""#input("Please input old password: ")
    query = "SELECT password FROM user WHERE email = 'cocain@gmail.com'";
    #args = (user)
    mycursor.execute(query)
    old_pass_from_db = mycursor.fetchone()
    print(old_pass_from_db[0])
    if old_passw == old_pass_from_db[0]:
            new_pass = input("Input new password ")
            confirming = input("Please repeat new password: ")
            if new_pass == confirming:
                sql = "UPDATE user SET password = %s WHERE email = %s"
                args = (new_pass, user)
                mycursor.execute(sql, args)
                connect.commit()
                #update_session_auth_hash(request, user)
                print("Password was successfully changed!")
            else:
                #print("Passwords don't match")
                change_password(request.POST)
    else:
        print("Wrong old pass, try more")
        change_password(request.POST)


# change_password()
# def delete_user(request): #delete and hide
#     # u = User.objects.get(username=request.user)
#     # u.delete()
#     sql = "DELETE FROM users WHERE user = %s"
#     args = (request.user)
#     mycursor.execute(sql, args)
#     mycursor.commit()
#     print("The user is deleted")
#     return redirect('registration.html') #delete cascade from db
#
#
# def hide_user(request):
#     sql = "UPDATE users SET is_activated = %s WHERE email = %s"
#     args = (0, request.user)
#     mycursor.execute(sql, args)
#     connect.commit()
#     print("User profile successfully disabled")
#     return redirect('login.html')

#hide_user()
#     # context = ""
#     # user = User.object.get(username=request.user)
#     # user.is_active = False
#     # user.save()
#     # context['msg'] = 'Profile successfully disabled.'
#     # return redirect()
#
#
#
# def change_currency(request):
#     pass



