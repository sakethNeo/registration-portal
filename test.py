import tkinter as tk
from tkinter import messagebox as mb

class Person:
    def __init__(self, id, password):
        self.id = id
        self.password = password

class Teacher(Person):
    def __init__(self, id, password, subject):
        super().__init__(id, password)
        self.subject = subject

class Student(Person):
    def __init__(self, id, password, hall):
        super().__init__(id, password)
        self.hall = hall

class UGStudent(Student):
    def __init__(self, id, password, hall, dept):
        super().__init__(id, password, hall)
        self.dept = dept

class PGStudent(Student):
    def __init__(self, id, password, hall, specialization):
        super().__init__(id, password, hall)
        self.specialization = specialization


# helper object to take id input
class GetId:
    def __init__(self,master):

        self.id_label=tk.Label(master,text="ID : ")
        self.enter_id=tk.Entry(master)
        
        self.id_label.grid(row=3, column=0)
        self.enter_id.grid(row=3, column=1)
        
# helper object to take password input
class GetPass:
    def __init__(self,master):

        self.password_label=tk.Label(master,text="Password : ")
        self.enter_password=tk.Entry(master,show="*")

        self.password_label.grid(row=10, column=0)
        self.enter_password.grid(row=10, column=1)



class Display(tk.Tk):
    def __init__(self):

        super().__init__()
        self.users=[]
        self.load_users_from_file()
        self.widgets()

    def widgets(self):
    
        self.home_btn = tk.Button(self, text="Home", command=self.home_func)
        self.register_btn = tk.Button(self, text="Register", command=self.register_user)
        self.sign_in_btn = tk.Button(self, text="Sign In", command=self.sign_in)
        self.edit_profile_btn = tk.Button(self, text="Edit", command=self.edit_profile)
        self.exit_btn = tk.Button(self, text="Exit", command=self.exit_func)

        # Arrange buttons in a grid with proper padding
        buttons_col = 1
        for btn in [self.home_btn, self.register_btn, self.sign_in_btn, self.edit_profile_btn, self.exit_btn]:
            btn.grid(row=1, column=buttons_col,padx=10,pady=5)
            buttons_col += 1

        info_label_text = "sign in to send deregister request or you can simply enter the wrong password thrice XD"
        self.label_info = tk.Label(self, text=info_label_text, pady=10)
        self.label_info.grid(row=2, column=1, columnspan=4)



############################## HELPER FUNCTIONS ##############################



    # helper function to reset everything
    def reset_form(self):
        for widget in self.winfo_children():
            widget.destroy()

    # function to reset and put widgets (home button)
    def home_func(self):
        self.reset_form()
        self.widgets()

    # function to quit the program
    def exit_func(self):
        quit()

    # function to check if the entered password is valid or not
    def is_valid_password(self, password_entry):

        if 8 <= len(password_entry) <= 12: # check length
            special_characters = {'!', '@', '#', '$', '%', '&', '*'} 

            # check if it has a digit
            has_digit = any(char.isdigit() for char in password_entry) 

            # check if it has a lower case
            has_lower_case = any(char.islower() for char in password_entry) 

            # check if it has an upper case
            has_upper_case = any(char.isupper() for char in password_entry) 

            # check if it has a special character
            has_special_char = any(char in special_characters for char in password_entry) 

            # if it has all the above then return true
            return has_digit and has_lower_case and has_upper_case and has_special_char
        
        else:
            return False
        
    # function to save all the users data into file
    def save_users_to_file(self,filename="text.txt"):

        with open(filename,"w") as file:
            for user in self.users:

                if isinstance(user,Teacher):
                    file.write(f"Teacher,{user.id},{user.password},{user.subject}\n")

                elif isinstance(user,UGStudent):
                    file.write(f"UGStudent,{user.id},{user.password},{user.hall},{user.dept}\n")

                elif isinstance(user,PGStudent):
                    file.write(f"PGStudent,{user.id},{user.password},{user.hall},{user.specialization}\n")

    # function to load the users data from file
    def load_users_from_file(self,filename="text.txt"):

        self.users=[]

        with open(filename,"r") as file:
            for line in file:

                data=line.strip().split(",")

                if len(data)>=3:
                    user_type=data[0]
                    user_id=data[1]
                    user_password=data[2]

                    if user_type=="Teacher":
                        user_subject=data[3]
                        self.users.append(Teacher(user_id,user_password,user_subject))

                    elif user_type=="UGStudent":
                        user_hall=data[3]
                        user_dept=data[4]
                        self.users.append(UGStudent(user_id,user_password,user_hall,user_dept))

                    elif user_type=="PGStudent":
                        user_hall=data[3]
                        user_specialization=data[4]
                        self.users.append(PGStudent(user_id,user_password,user_hall,user_specialization))

    # function to print the user's info in the tkinter window
    def print_info(self,user_id):

        self.load_users_from_file()
        text_info=""

        for user in self.users:
            if user.id==user_id:

                if isinstance(user,Teacher):
                    text_info=f"id={user.id}\nprof=Teacher\nsubject={user.subject}\n"

                elif isinstance(user,UGStudent):
                    text_info=f"id={user.id}\nprof=UG student\nhall={user.hall}\ndept={user.dept}\n"

                elif isinstance(user,PGStudent):
                    text_info=f"id={user.id}\nprof=PG student\nhall={user.hall}\nspecialization={user.specialization}\n"

        display_string=tk.Label(self,text=text_info)
        display_string.grid(row=14,column=0)



############################## END OF HELPER FUNCTIONS ##############################



    # function for registration
    def register_user(self):

        self.reset_form()
        self.widgets()
        self.label_info.grid_forget()

        self.getid=GetId(self)
        self.getpass=GetPass(self)

        # radiobuttons to select person type
        self.radioPersonType=tk.StringVar()
        self.radioTeacher=tk.Radiobutton(self,text="teacher",variable=self.radioPersonType,value="teacher",command=self.onClickPerson)
        self.radioStudent=tk.Radiobutton(self,text="student",variable=self.radioPersonType,value="student",command=self.onClickPerson)
        
        self.radioTeacher.grid(row=5, column=0)
        self.radioStudent.grid(row=5, column=1)

        self.submit_button=tk.Button(self,text="submit",command=self.submit_for_registration)

    # helper function for registration (radiobutton for person type - Teacher/Student)
    def onClickPerson(self):
            self.person_type=self.radioPersonType.get()

            if self.person_type=="teacher":

                # take subject entry if the person is a teacher
                self.subject_label=tk.Label(self,text="subject : ")
                self.subject_entry=tk.Entry(self)
                self.subject_label.grid(row=6, column=0)
                self.subject_entry.grid(row=6, column=1)

                self.submit_button.grid(row=11,column=0)

            else:
                
                # radiobuttons to select student's type (UG/PG)
                self.radioStudentType=tk.StringVar()
                self.radioUGstudent=tk.Radiobutton(self,text="UGstudent",variable=self.radioStudentType,value="UG",command=self.onClickStudent)
                self.radioPGstudent=tk.Radiobutton(self,text="PGstudent",variable=self.radioStudentType,value="PG",command=self.onClickStudent)
                
                self.radioUGstudent.grid(row=7,column=0)
                self.radioPGstudent.grid(row=7,column=1)

    # helper function for registration (radiobutton for student's type)
    def onClickStudent(self):

        # get from radiobutton
        self.student_type=self.radioStudentType.get()

        # take student's hall entry
        self.hall_label=tk.Label(self,text="hall : ")
        self.hall_entry=tk.Entry(self)
        self.hall_label.grid(row=8, column=0)
        self.hall_entry.grid(row=8, column=1)


        if self.student_type=="UG":

            # department if the student is Under Graduate
            self.dept_label=tk.Label(self,text="dept : ")
            self.dept_entry=tk.Entry(self)
            self.dept_label.grid(row=9, column=0)
            self.dept_entry.grid(row=9, column=1)

            self.submit_button.grid(row=11,column=0)

        else:

            # specialization if the student is Post Graduate
            self.specialization_label=tk.Label(self,text="specialization : ")
            self.specialization_entry=tk.Entry(self)
            self.specialization_label.grid(row=9, column=0)
            self.specialization_entry.grid(row=9, column=1)

            self.submit_button.grid(row=11,column=0)

    # finally our submit function for registration (command function for submit button)
    def submit_for_registration(self):

        self.load_users_from_file()

        # get id and password
        self.id=self.getid.enter_id.get()
        self.password=self.getpass.enter_password.get()

        # if id already exists show error
        for user in self.users:
            if user.id==self.id:
                mb.showerror("error","id already exists!")
                return

        # if the password is not valid show error
        if not self.is_valid_password(self.password):
            mb.showerror("invalid password type\n",
                         """password: A valid password should satisfy the following:\n\
                            a) It should be within 8-12 character long.\n\
                            b) It should contain at least one upper case, one digit, and one lower case.\n\
                            c) It should contains one or more special character(s) from the list [! @ # $ % & *]\n\
                            d) No blank space will be allowed.\n""")
            return


        if self.person_type=="teacher":

            # subject entry for teacher
            self.subject=self.subject=self.subject_entry.get()
            userT=Teacher(self.id,self.password,self.subject)

            self.users.append(userT)
        else:

            # hall entry for student
            self.hall=self.hall_entry.get()

            if self.student_type=="UG":
                # dept for UG student
                self.dept=self.dept_entry.get()
                userUG=UGStudent(self.id,self.password,self.hall,self.dept)

                self.users.append(userUG)
            else:     
                # specialization for PG student
                self.specialization=self.specialization_entry.get()
                userPG=PGStudent(self.id,self.password,self.hall,self.specialization)

                self.users.append(userPG)

        mb.showinfo("success","succesfully registered")
        self.save_users_to_file()

    def sign_in(self):

        self.reset_form()
        self.widgets()

        self.label_info.grid_forget()

        self.getid=GetId(self)
        self.getpass=GetPass(self)

        self.load_users_from_file()

        attempts_left=2

        # submit button
        submit_btn=tk.Button(self,text="submit",command=lambda:self.submit_for_signin(attempts_left))
        submit_btn.grid(row=11,column=0)

    def submit_for_signin(self,attempts_left):

        # get entered id
        user_id=self.getid.enter_id.get()
        user_password=None

        for user in self.users:
            if user.id==user_id:
                user_password=user.password

        # if the user doesn't exist
        if user_password==None:
            mb.showerror("error404","user not found with the given id!")
            return
        
        # get entered password
        entered_password=self.getpass.enter_password.get()

        if entered_password==user_password:
            mb.showinfo("success","succesfully signed in.")

            self.print_info(user_id)

            # show de-register button after signed in
            de_register_btn=tk.Button(self,text="de-register",command=lambda:self.remove_user(user_id))
            de_register_btn.grid(row=12,column=0)

            return
        
        # person has three attempts if wrong password is entered
        if entered_password!=user_password and attempts_left>0:
            mb.showwarning("warning",f"incorrect try again {attempts_left} attempts left.")

            attempts_left-=1
            submit_btn=tk.Button(self,text="submit",command=lambda:self.submit_for_signin(attempts_left))

            submit_btn.grid(row=11,column=0)
        
        # if three attempts are done account will be deactivated
        else:
            mb.showwarning("warning","account will be deactivated soon!")
            self.remove_user(user_id)

    # function to remove deactivated account (removes user from both list and file)
    def remove_user(self, id_to_be_removed,filename="text.txt"):

        self.load_users_from_file()
        removed_user=None

        for user in self.users:
            if user.id==id_to_be_removed:
                removed_user=user
                self.users.remove(user)

        if removed_user is not None:
            self.save_users_to_file(filename)

    # function for authorised member to edit profile
    def edit_profile(self):

        self.reset_form()
        self.widgets()

        self.label_info.grid_forget()

        self.getid=GetId(self)
        self.getpass=GetPass(self)
        
        submit_btn_to_authorise=tk.Button(self,text="submit",command=self.submit_to_authorise)
        submit_btn_to_authorise.grid(row=11,column=0)

    # submit button to check if the user is authorised or not
    def submit_to_authorise(self):

        # get id and password from entry
        admin_id=self.getid.enter_id.get()
        admin_password=self.getpass.enter_password.get()

        # we have taken a sample admin id and password
        if admin_id=="admin" and admin_password=="Admin@123":

            display_string=tk.Label(self,text="whose id you want to edit")
            display_string.grid(row=12,column=0)

            self.edit_id_label=tk.Label(self,text="id:")
            self.edit_id_label.grid(row=13,column=0)

            # take an entry id to edit the person's info
            self.edit_id_entry=tk.Entry(self)
            self.edit_id_entry.grid(row=13,column=1) 

            self.submit_to_edit_btn=tk.Button(self,text="submit to edit",command=self.submit_to_edit)
            self.submit_to_edit_btn.grid(row=20,column=0)

        # if the person is not authorised
        else:
            mb.showerror("error","only authorised users can edit others info")
            
    def submit_to_edit(self):

        # remove the submit button after the id entry is taken
        self.submit_to_edit_btn.grid_forget()
        user_id=self.edit_id_entry.get()

        user_found=False

        # find user and take appropriate entries to edit
        for user in self.users:
            if user.id==user_id:

                if isinstance(user,Teacher):
                    display_string=tk.Label(self,text=f"id={user.id}\nprof=Teacher")
                    display_string.grid(row=14,column=0)

                    edit_subject_label=tk.Label(self,text="subject=")
                    edit_subject_label.grid(row=16,column=0)

                    self.edit_subject_entry=tk.Entry(self)
                    self.edit_subject_entry.grid(row=16,column=1)

                else:
                    display_string=tk.Label(self,text=f"id={user.id}\nprof=student")
                    display_string.grid(row=14,column=0)

                    edit_hall_label=tk.Label(self,text="hall=")
                    edit_hall_label.grid(row=16,column=0)

                    self.edit_hall_entry=tk.Entry(self)
                    self.edit_hall_entry.grid(row=16,column=1)

                    if isinstance(user,UGStudent):

                        edit_dept_label=tk.Label(self,text="dept=")
                        edit_dept_label.grid(row=17,column=0)

                        self.edit_dept_entry=tk.Entry(self)
                        self.edit_dept_entry.grid(row=17,column=1)

                    else:
                        edit_specialization_label=tk.Label(self,text="specialisation=")
                        edit_specialization_label.grid(row=17,column=0)

                        self.edit_specialization_entry=tk.Entry(self)
                        self.edit_specialization_entry.grid(row=17,column=1)

                user_found=True
                break
        
        # show the save changes button if the user is found and the entries are taken
        if user_found:
            self.save_edits_btn=tk.Button(self,text="save changes",command=lambda:self.edit_info(user))
            self.save_edits_btn.grid(row=30,column=0)

        # show error if the id is not found
        else:
            mb.showerror("error","no such user found")
    
    # command for save changes button
    def edit_info(self, user):
        
        self.load_users_from_file()

        if isinstance(user,Teacher):
            # remove the user first
            self.remove_user(user.id)
            user.subject=self.edit_subject_entry.get()

        else:
            user.hall=self.edit_hall_entry.get()

            if isinstance(user,UGStudent):
                self.remove_user(user.id)
                user.dept=self.edit_dept_entry.get()

            else:
                self.remove_user(user.id)
                user.specialization=self.edit_specialization_entry.get()

        # add the user next
        self.users.append(user)
        # save them to file
        self.save_users_to_file()
        mb.showinfo("success","changes saved")
    
################################## main function 

if __name__=="__main__":


    filename="text.txt"

    # if file exists then continue
    try:
        with open(filename,"r"):
            pass
    
    # to clear the contents in the text file
        with open(filename,"w"):
            pass

    # if the file doesn't exist then create a new one
    except FileNotFoundError:
        with open(filename,"w"):
            pass

    display=Display()
    display.title("login")
    display.geometry("700x300")
    display.mainloop()

