# This is a basic application where a user can enter as either an admin or a simple user and make changes to a database accordingly.

There is an existing database with two tables: "users" which consists of users' profiles (users' data), and "admin" which consists of the usernames and passwords required to verify an admin login to the application.

At first, the user is presented with the choice to enter as a user or as an admin.

+++ If they choose to enter as a user, they are redirected to /add_user_profile where there is a form with the fields "Name", "Telephone", "Mobile Number", "Email" and "Home Address". The "Name" field cannot be left empty, as well as at least one of the fields "Telephone" and "Mobile Number". After they fill in the form, they are to click on the "Submit" button. There is a data validation check and if all requirements are met, the new user profile is created successfully, the user is redirected to /new_profile where they are presented with the new user profile along with a message "Profile created successfully".

+++ If the user chooses to enter as an admin, they are redirected to /login where they need to insert the correct username and password to a login form to enter. If they don't, an appropriate message flashes. If they do, they are redirected to /users where they are presented with a full table of the user profiles, where they can choose to "Create new profile", and/or "Edit" or "Delete" an existing one.

In the first case, they are redirected to /add_user_profile where they fill in a form, same way as a simple user would. However, after successfully creating the user profile they are redirected to /users again, where the new profile is added to the table.

If they choose to edit an existing user profile, they are redirected to /edit_user_profile where they are presented with a form already filled in with the data of the existing profile. The admin can make changes as they please and then hit submit, which will redirect them to /users, where the table will be updated accordingly. 

Finally, if the admin chooses to delete an existing profile, they are simply redirected to /users after hitting the "delete" button, where the table will be updated.
   
   
#########################

Software used: Python3, Flask, MySQL, HTML
