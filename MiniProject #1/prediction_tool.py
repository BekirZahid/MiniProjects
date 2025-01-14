#Berkan Ozbabacan / ENGR 212 A / 212990794
#Bekir Zahit Demiray / ENGR 212 A / 212062166

from Tkinter import *
from tkFileDialog import askopenfilename
import Tkinter,Tkconstants,tkFileDialog
from tkFileDialog import askopenfilenames
from xlrd import open_workbook,cellname
from recommendations import *
import ttk

class TkFileDialogExample(Tkinter.Frame):
    def __init__(self,root):
        Tkinter.Frame.__init__(self,root)
        past_grades=Tkinter.Button(root,text='Load Past Student Grades',command=self.Add_past_student_grades,bg='#f5aaa9',width=25,height=3,font='Times 10 italic' )
        past_grades.place(x=2,y=38)
        current_grades=Tkinter.Button(root,text='Your Current Student Transcript',command=self.Add_current_grades,bg='#f5aaa9',width=25,height=3,font='Times 10 italic' )
        current_grades.place(x=305,y=38)
        get_recommendationss=Tkinter.Button(root,text='See the Recommended Courses',command=self.Show_recommendations,bg='#a9f5d0',width=25,height=3,font='Times 12 italic')
        get_recommendationss.place(x=140,y=233)
        #RadioButtons for filtering
        self.v=IntVar()
        radio1=Radiobutton(root,text='User-Based',variable=self.v,padx=25,value=1,font='Times 8 italic')
        radio2=Radiobutton(root,text='Item-Based',variable=self.v,padx=25,value=0,font='Times 8 italic' )
        radio1.place(x=75,y=133)
        radio2.place(x=75,y=173)
        Label_to_radio_button=Label(root,text='Collaborative\n Filtering Type:',height=4,width=13,bg='#f5d0a9',font='Times 10 italic' )
        Label_to_radio_button.place(x=2,y=133)
        self.v.set(1)
        Label_to_heading=Label(root,text='Virtual Advisor v1.0',height=2,width=15,bg='#fdefef',fg='#130202',font='Times 10 italic' )
        Label_to_heading.place(x=190,y=0)
        #Similarity Measures
        self.combovar = StringVar()
        self.box = ttk.Combobox(textvariable =self.combovar,value=['Pearson','Euclidean','Jaccard'],width=15,height=4,font='Times 8 italic' )
        self.box.place(x=380,y=143)
        Label_to_similarity=Label(root,text='Similarity\nMeasure',bg='#f5d0a9',height=4,width=9,font='Times 10 italic' )
        Label_to_similarity.place(x=305,y=133)
        self.combovar.set('Pearson')
        #User-Based Dictionary
        self.User_based_dictionary=dict()
        #Item-Based Dictionary
        self.Item_based_dictionary=dict()
        #It represents the values of grade
        self.Dictionary_of_Grade_and_Their_Value={'A+':4.1,'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,'C-':1.7,'D+':1.3,'D':1.0,'D-':0.5,'F':0.0}
        #It represents the lecture codes
        self.Dictionary_of_Matching_Code_and_Name=dict()

    def Convert_Value_to_Letter_Grade(self,input1):
        if input1>4:
            return 'A+'
        elif 4>=input1 and input1>3.7:
            return 'A'
        elif 3.7>=input1 and input1>3.3:
            return 'A-'
        elif 3.3>=input1 and input1>3.0:
            return 'B+'
        elif 3.0>=input1 and input1>2.7:
            return 'B'
        elif 2.7>=input1 and input1>2.3:
            return 'B-'
        elif 2.3>=input1 and input1>2.0:
            return 'C+'
        elif 2.0>=input1 and input1>1.7:
            return 'C'
        elif 1.7>=input1 and input1>1.3:
            return 'C-'
        elif 1.3>=input1 and input1>1.0:
            return 'D+'
        elif 1.0>=input1 and input1>0.5:
            return 'D'
        elif 0.5>=input1 and input1>0.1:
            return 'D-'
        elif 0.1>=input1:
            return 'F'

    def Create_User_Based_Dictionary(self,filename):
        """It helps to create user-based dictionary which is used in all other functions"""
        book=open_workbook(filename)
        sheet=book.sheet_by_index(0)
        list_of_all_elements=list()
        self.Dictionary_of_code_and_grade=dict()
        for col_index in range(sheet.ncols):
            for row_index in range(sheet.nrows):
              list_of_all_elements.append(sheet.cell(row_index,col_index).value)
        for k in range(sheet.nrows-1):
            self.Dictionary_of_Matching_Code_and_Name[list_of_all_elements[k+1]]=list_of_all_elements[k+sheet.nrows+1]
            self.Dictionary_of_code_and_grade[list_of_all_elements[k+1]]=self.Dictionary_of_Grade_and_Their_Value[list_of_all_elements[k+(2*sheet.nrows)+1]]
        self.User_based_dictionary[filename]=self.Dictionary_of_code_and_grade
        return self.User_based_dictionary

    def help_to_write(self,list3):
        """It helps us to reach the elements of tuples by writing them in listbox"""
        """Final list which is list4 helps us to write the followings in order: the code of the lecture, the name of the lecture,
        by which letter grade the user passed that course, and the floating number values of the grades"""
        list4=list()
        for keys in list3:
            (grade,code)=keys
            list4.append(code)
            list4.append(self.Dictionary_of_Matching_Code_and_Name[code])
            list4.append(self.Convert_Value_to_Letter_Grade(grade))
            list4.append(grade)
        return list4

    def Create_Item_Based_Dictionary(self):
        """It converts the user-based dictionary to item-based dictionary"""
        self.Item_based_dictionary=calculateSimilarItems(self.User_based_dictionary)
        return self.Item_based_dictionary

    def Getting_recomendations(self,filename,similarities,dictionary):
        """It creates the recommendations of lectures"""
        recomendationss=getRecommendations(dictionary,filename,similarity=similarities)[0:6]
        return recomendationss

    def Add_past_student_grades(self):
        open_files=askopenfilenames()
        for Files in open_files:
            self.Create_User_Based_Dictionary(Files)
        return self.User_based_dictionary

    def Add_current_grades(self):
        self.opened_transcript=askopenfilename()
        self.Create_User_Based_Dictionary(self.opened_transcript)
        return self.User_based_dictionary

    def Show_recommendations(self):
        """  First we choose which collaborative filtering we use, then we choose which similarity measure we use.
        Also, the 'b' in the function is a tuple which gives the floating number value of the grade and the lecture
        code and 'a' is a list which is equal to 'list4' which is explained above in 'help_to_write function'.
        'a' is used to make adding the needed final result to 'Listbox'  """
        try:
            if self.v.get()==1:
                if self.combovar.get()=="Pearson":
                    b=self.Getting_recomendations(self.opened_transcript,sim_pearson,self.User_based_dictionary)
                    a=self.help_to_write(b)
                    self.liste=Listbox(bg='#9d0000',width=50,fg='white',font='Times 10 italic')
                    self.liste2=Listbox(bg='#9d0000',fg='white',width=30,font='Times 10 italic')
                    self.liste.insert(END,'Recommended Courses')
                    self.liste2.insert(END,'Predicted Grade')
                    i=0
                    while i<len(a):
                        code_and_lecture_name=str(a[i])+'   '+str(a[i+1])
                        letter_and_grade=str(a[i+2])+'(',str(a[i+3])+')'
                        self.liste.insert(END,code_and_lecture_name)
                        self.liste2.insert(END,letter_and_grade)
                        i+=4
                    self.liste.place(x=2,y=310)
                    self.liste2.place(x=305,y=310)
                elif self.combovar.get()=="Euclidean":
                    b=self.Getting_recomendations(self.opened_transcript,sim_distance,self.User_based_dictionary)
                    a=self.help_to_write(b)
                    self.liste=Listbox(bg='#9d0000',width=50,fg='white',font='Times 10 italic')
                    self.liste2=Listbox(bg='#9d0000',fg='white',width=30,font='Times 10 italic')
                    self.liste.insert(END,'Recommended Courses')
                    self.liste2.insert(END,'Predicted Grade')
                    i=0
                    while i<len(a):
                        code_and_lecture_name=str(a[i])+'   '+str(a[i+1])
                        letter_and_grade=str(a[i+2])+'(',str(a[i+3])+')'
                        self.liste.insert(END,code_and_lecture_name)
                        self.liste2.insert(END,letter_and_grade)
                        i+=4
                    self.liste.place(x=2,y=310)
                    self.liste2.place(x=305,y=310)
                elif self.combovar.get()=="Jaccard":
                    b=self.Getting_recomendations(self.opened_transcript,sim_jaccard2,self.User_based_dictionary)
                    a=self.help_to_write(b)
                    self.liste=Listbox(bg='#9d0000',width=50,fg='white',font='Times 10 italic')
                    self.liste2=Listbox(bg='#9d0000',fg='white',width=30,font='Times 10 italic')
                    self.liste.insert(END,'Recommended Courses')
                    self.liste2.insert(END,'Predicted Grade')
                    i=0
                    while i<len(a):
                        code_and_lecture_name=str(a[i])+'   '+str(a[i+1])
                        letter_and_grade=str(a[i+2])+'(',str(a[i+3])+')'
                        self.liste.insert(END,code_and_lecture_name)
                        self.liste2.insert(END,letter_and_grade)
                        i+=4
                    self.liste.place(x=2,y=310)
                    self.liste2.place(x=305,y=310)
            elif self.v.get()==0:
                self.Create_Item_Based_Dictionary()
                B=getRecommendedItems(self.User_based_dictionary, self.Item_based_dictionary, self.opened_transcript)
                self.liste3=Listbox(bg='#9d0000',width=50,fg='white',font='Times 10 italic')
                self.liste4=Listbox(bg='#9d0000',fg='white',width=30,font='Times 10 italic')
                A=self.help_to_write(B)
                i=0
                self.liste3.insert(END,'Recommended Courses')
                self.liste4.insert(END,'Predicted Grade')
                while i<24:
                    code_and_lecture_name=str(A[i])+'   '+str(A[i+1])
                    letter_and_grade=str(A[i+2])+'(',str(A[i+3])+')'
                    self.liste3.insert(END,code_and_lecture_name)
                    self.liste4.insert(END,letter_and_grade)
                    i+=4
                self.liste3.place(x=2,y=310)
                self.liste4.place(x=305,y=310)
        except:
            self.liste6=Listbox(bg='#9d0000',width=80,fg='white',font='Times 10 italic')
            self.liste6.insert(END,'Input files need to be provided first')
            self.liste6.place(x=2,y=310)
                
if __name__=='__main__':
  root = Tkinter.Tk()
  root.title("ADVISOR'S RECOMMENDATIONS")
  root.tk_setPalette("#a9cef5")
  root.geometry('500x500+15+100')
  root.resizable(width=False,height=False)
  TkFileDialogExample(root).pack()
  root.mainloop()
