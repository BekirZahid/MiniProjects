#Berkan Ozbabacan / ENGR 212 A / 212990794
#Bekir Zahit Demiray / ENGR 212 A / 212062166





#!/usr/bin/env python
#-- coding: utf-8 -*-
from Tkinter import *
from bs4 import BeautifulSoup
import Tkinter
import docclass
import ttk
import urllib2
import copy
class Mini_project_5(Tkinter.Frame):
    def __init__(self,root):
        Tkinter.Frame.__init__(self,root)
        name_of_program=Label(root,text='Guess My Department',bg='#a9cef5',fg='black',font='Times 20 italic')#Label for name of program
        name_of_program.place(x=20,y=10,height=40,width=660)
        label1=Label(root,text='Provide SEHIR Faculty List URL:',bg='#a9cef5',font='Times 12 italic')#Label
        label1.place(x=-60,y=65,height=18,width=400)
        self.Url=Text(root,bg='white',font='Times 10 italic')#Text to write URl
        self.Url.place(x=40,y=95,height=25,width=620)
        self.button_of_fetching_course=Button(root,text='Fetch Faculty Profiles',command=self.Create_database,bg='grey',font='Times 8 italic')#Button for getting information from URL
        self.button_of_fetching_course.place(x=42,y=130,height=20,width=140)
        self.Listbox_for_write_first_part=Listbox(root,bg='white',font='Times 10 italic')#Listbox to show process
        self.Listbox_for_write_first_part.place(x=40,y=160,height=120,width=620)
        course_scrollbar = Scrollbar(self.Listbox_for_write_first_part)#Scrollbar
        course_scrollbar.pack(side=RIGHT,fill=Y)
        course_scrollbar.config(command = self.Listbox_for_write_first_part.yview)
        label2=Label(root,text='Choose the\nClassification\nMethod:',bg='#a9cef5',font='Times 12 italic')#Label
        label2.place(x=40,y=300,height=50,width=90)
        self.v=IntVar()
        radio1=Radiobutton(root,text='Naive Bayes',variable=self.v,value=0,font='Times 8 italic')#Radiobutton for Naive Bayes
        radio1.place(x=135,y=300,height=15,width=90)
        radio2=Radiobutton(root,text='Fisher',variable=self.v,value=1,font='Times 8 italic')#Radiobutton for Fisher
        radio2.place(x=135,y=330,height=15,width=64)
        label3=Label(root,text='Select a\nProfessor:',bg='#a9cef5',font='Times 12 italic')#Label
        label3.place(x=40,y=370,height=50,width=70)
        self.combovar=StringVar()
        self.box = ttk.Combobox(textvariable = self.combovar,width=25,height=4,font='Times 8 italic' )#Combobox for list of lecturers
        self.box.place(x=120,y=390)
        label4=Label(root,text='Set the Thresholds:',bg='#a9cef5',font='Times 12 italic')#Label
        label4.place(x=320,y=280,height=30,width=130)
        self.Listbox_for_Threshold=Listbox(root,bg='white',font='Times 10 italic')#Listbox for threshold
        self.Listbox_for_Threshold.place(x=320,y=310,height=150,width=240)
        self.remove=Button(root,text='Remove\nSelected',command=self.Remove_from_thresholds,bg='grey',font='Times 8 italic')#Button for delete item for threshold
        self.remove.place(x=565,y=310,height=40,width=90)
        self.combovar2=StringVar()
        self.box2 = ttk.Combobox(textvariable = self.combovar2,width=36,height=4,font='Times 8 italic' )#Combobox for list of departments
        self.box2.place(x=320,y=480)
        self.entry1=Entry(root,bg='white',width=6)#Entry for determine score of item
        self.entry1.place(x=565,y=480)
        self.set1=Button(root,text='Set',command=self.Add_department_into_thresholds,bg='grey',font='Times 8 italic')#Button to add item into threshold
        self.set1.place(x=620,y=479,height=20,width=40)
        self.Final_button=Button(root,text='Guess the Departmental of the Selected Professor',command=self.Final_step,bg='grey',font='Times 10 italic')#Button to show result
        self.Final_button.place(x=42,y=550,height=30,width=300)
        label5=Label(root,text='Predicted Department:',bg='#a9cef5',font='Times 12 italic')#Label
        label5.place(x=40,y=600,height=25,width=160)
        self.Listbox_for_result=Listbox(root,bg='#a9cef5',font='Times 10 italic')#Listbox to show result
        self.Listbox_for_result.place(x=220,y=600,height=25,width=440)
        self.list_of_thresholds=[]
    def makesoup_get_text(self,url):#It return given URL's text
        data=urllib2.urlopen(url)
        data2=data.read()
        soup2=BeautifulSoup(data2.decode('utf-8'))
        for text in soup2.findAll('div',{'class':'egitim'}):
            text=text.get_text()
            return text

    def help_to_write(self,prediction):#It determine that prediction is True or False.According to result, it determine the color of the listbox,then it shows the result.
        try:
            self.Listbox_for_result.delete(0,END)
        except:
            pass
        if prediction==self.dictionary_professor_with_department[self.combovar.get()]:

            self.Listbox_for_result.config(bg='green')
            self.Listbox_for_result.insert(END,prediction)
        elif prediction==None:
            self.Listbox_for_result.config(bg='yellow')
            self.Listbox_for_result.insert(END,'Unknown')
        else:
            self.Listbox_for_result.config(bg='red')
            self.Listbox_for_result.insert(END,str(prediction)+' ('+self.dictionary_professor_with_department[self.combovar.get()]+')')

    def Determine_department(self,list1):
        del list1[0]
        list_help=[]
        for i in range(len(list1)-1):
            if list1[i].isupper()==True:
                if list1[i+1].isupper()==False:
                    list_help.append(i)
        k=copy.deepcopy(list1)
        for index in list_help:
            list1.remove(k[index])
        return list1


    def Create_database(self):
        response=urllib2.urlopen(self.Url.get(1.0,END))
        html_version = response.read()
        soup = BeautifulSoup(html_version.decode('utf-8'))
        self.list_of_department=[]##Department list with order
        self.list_of_lecturer=[]#Lecturer Name with order(included 'name')
        self.list_of_links=[]#professors links with order
        self.dictionary_of_department_and_professor={}#key=department ,value=list of lecturer with order
        self.dictionary_as_database={}#key=professor,value=text
        self.dictionary_professor_with_department={}#key=professor,value=department of professor
        self.Listbox_for_write_first_part.insert(END,'Fetching Department and Professor List(In Progress)')

        for i in soup.findAll(  'h3',{'class':'ms-rteElement-H3B'}):
            if i.get_text()==u'\n' or i.get_text()==u'':
                continue
            else:
                self.list_of_department.append(i.get_text())##Add the department and faculty name into the list
        for k in soup.findAll('td',{'class':'ms-rteTableEvenCol-6'}):
            self.list_of_lecturer.append(k.get_text())#Add the lecture name and year of the completion into the list.
            try:
                link='http://www.sehir.edu.tr/'+k.find('a').get('href')
                self.list_of_links.append(link)#Add the professor page links into list
            except:
                continue

        k=0
        a=len(self.list_of_lecturer)
        while k<a/2:
            del self.list_of_lecturer[k+1]##Delete year of the completion from list
            k+=1

        self.Determine_department(self.list_of_department)

        list_help=[]#To find indexes of 'names' because they help to separate professors according to departments.
        for index in range(len(self.list_of_lecturer)):
            if self.list_of_lecturer[index]==u'\nName \n' or self.list_of_lecturer[index]==u'\nName\n':
                list_help.append(index)

        for item in self.list_of_department:
            self.dictionary_of_department_and_professor.setdefault(item,[])
        for k in range(len(self.list_of_department)-1):
            self.dictionary_of_department_and_professor[self.list_of_department[k]]=[x for x in self.list_of_lecturer[list_help[k]+1:list_help[k+1]]]#We create a dictionary keys=departments values=list of professors
        self.dictionary_of_department_and_professor[self.list_of_department[len(self.list_of_department)-1]]=[x for x in self.list_of_lecturer[(list_help[len(list_help)-1])+1:]]

        a=0
        sorted_list_lecturer=[]
        b=-1

        self.Listbox_for_write_first_part.delete(0,END)
        self.Listbox_for_write_first_part.insert(END,'Fetching Department and Professor List(DONE)')
        self.Listbox_for_write_first_part.update()
        for department in self.list_of_department:
            self.Listbox_for_write_first_part.insert(END,'%s (Pending)'%(department))
            self.Listbox_for_write_first_part.update()

        for k in range(len(self.list_of_lecturer)):
            if k in list_help:
                if b==-1:
                    b+=1
                    self.Listbox_for_write_first_part.delete(b+1,END)
                    self.Listbox_for_write_first_part.insert(END,self.list_of_department[b]+('(In Progress)'))
                    self.Listbox_for_write_first_part.update()
                    for department in self.list_of_department[b+1:]:
                        self.Listbox_for_write_first_part.insert(END,department+'(Pending)')
                        self.Listbox_for_write_first_part.update()
                    continue
                else:
                    try:
                        self.Listbox_for_write_first_part.delete(b+1,END)
                        self.Listbox_for_write_first_part.insert(END,self.list_of_department[b]+'(Done)')
                        b+=1
                        self.Listbox_for_write_first_part.insert(END,self.list_of_department[b]+'(In Progress)')
                        self.Listbox_for_write_first_part.update()
                        for department in self.list_of_department[b+1:]:
                            self.Listbox_for_write_first_part.insert(END,department+'(Pending)')
                            self.Listbox_for_write_first_part.update()
                        continue
                    except:
                        continue
            else:
                self.dictionary_as_database[self.list_of_lecturer[k]]=self.makesoup_get_text(self.list_of_links[a])#keys=professor values=text of professor
                self.dictionary_professor_with_department[self.list_of_lecturer[k]]=self.list_of_department[b]#key=professor value=department of professor
                sorted_list_lecturer.append(self.list_of_lecturer[k])#list of professors
                a+=1

        self.Listbox_for_write_first_part.delete(b+1,END)
        self.Listbox_for_write_first_part.insert(END,self.list_of_department[b]+'(Done)')
        self.Listbox_for_write_first_part.update()
        sorted_list_departmental=copy.deepcopy(self.list_of_department)
        sorted_list_departmental.sort()
        self.box2['value']=tuple(sorted_list_departmental)#Add the departments into combobox
        sorted_list_lecturer.sort()
        self.box['value']=tuple(sorted_list_lecturer)#Add the professors into combobox

    def Add_department_into_thresholds(self):
        self.list_of_thresholds.append((self.combovar2.get(),float(self.entry1.get())))#We add a tuple into a list because we use this list to set threshold
        self.Listbox_for_Threshold.insert(END,self.entry1.get()+'--'+self.combovar2.get())#Add the items into threshold
        return self.list_of_thresholds

    def Remove_from_thresholds(self):#Same logic with above function,only differences delete item from threshold.
        try:
            a=self.Listbox_for_Threshold.curselection()
            del self.list_of_thresholds[a[0]]
            self.Listbox_for_Threshold.delete(ACTIVE)
        except:
            pass


    def Bayes_prediction(self):
        cl=docclass.naivebayes(docclass.getwords)
        for category in self.list_of_department:##Category=departmnet
            for teacher in self.dictionary_of_department_and_professor[category]:
                if teacher==self.combovar.get():
                    continue
                else:
                    cl.train(self.dictionary_as_database[teacher],category)#self.dictionary_as_database[teacher]=professor's information

        for item in self.list_of_thresholds:
            department,score=item
            cl.setthreshold(department,score)
        prediction= cl.classify(self.dictionary_as_database[self.combovar.get()],default=None)
        self.help_to_write(prediction)


    def Fisher_prediction(self):
        cll=docclass.fisherclassifier(docclass.getwords)
        for category in self.list_of_department:#Category=department
            for teacher in self.dictionary_of_department_and_professor[category]:
                if teacher==self.combovar.get():
                    continue
                else:
                    cll.train(self.dictionary_as_database[teacher],category)#self.dictionary_as_database[teacher]=professor's information
        for item in self.list_of_thresholds:
            department,score=item
            cll.setminimum(department,score)

        prediction=cll.classify(self.dictionary_as_database[self.combovar.get()],default=None)
        self.help_to_write(prediction)

    def Final_step(self):
        if self.v.get()==0:
            self.Bayes_prediction()
        elif self.v.get()==1:
            self.Fisher_prediction()

if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("Course Schedule Advisor")
    root.tk_setPalette("#a9cef5")
    root.geometry('700x675+100+20')
    root.resizable(width=False,height=False)
    Mini_project_5(root).pack()
    root.mainloop()
