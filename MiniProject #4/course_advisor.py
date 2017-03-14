#Berkan Ozbabacan / ENGR 212 A / 212990794
#Bekir Zahit Demiray / ENGR 212 A / 212062166




from Tkinter import *
from bs4 import BeautifulSoup
import Tkinter
import ttk
import urllib2
import optimization

import time
import copy
class Mini_project_4(Tkinter.Frame):
    def __init__(self,root):
        Tkinter.Frame.__init__(self,root)
        name_of_program=Label(root,text='Course Schedule Advisor',bg='#a9cef5',fg='grey',font='Times 20 italic')
        name_of_program.place(x=20,y=10,height=35,width=560)
        label1=Label(root,text='Provide Course Offering URL:',bg='#a9cef5',font='Times 12 italic')
        label1.place(x=-60,y=55,height=18,width=400)
        self.Url=Text(root,bg='white',font='Times 10 italic')
        self.Url.place(x=40,y=75,height=25,width=430)
        self.button_of_fetching_course=Button(root,text='Fetch Course\nOfferings',command=self.Create_database,bg='grey',font='Times 8 italic')
        self.button_of_fetching_course.place(x=500,y=69,height=40,width=80)
        label2=Label(root,text='Select\nCourse\nCodes',bg="#a9cef5",font='Times 10 italic')
        label2.place(x=40,y=120,height=50,width=40)
        self.Listbox_for_courses=Listbox(root,bg='white',selectmode='multiple',font='Times 10 italic')
        self.Listbox_for_courses.place(x=90,y=120,height=120,width=120)
        course_scrollbar = Scrollbar(self.Listbox_for_courses)
        course_scrollbar.pack(side=RIGHT,fill=Y)
        course_scrollbar.config(command = self.Listbox_for_courses.yview)

        label3=Label(root,text='Provide the \nNumber of \nCourses:',font='Times 10 italic',bg='#a9cef5')
        label3.place(x=240,y=120,height=50,width=70)
        self.Entry_for_number_of_courses=Entry(root,bg='white')
        self.Entry_for_number_of_courses.place(x=315,y=135,height=25,width=30)

        self.v=IntVar()
        radio1=Radiobutton(root,text='Hill Climbing',variable=self.v,value=0,font='Times 8 italic')
        radio1.place(x=435,y=120,height=15,width=130)
        label4=Label(root,text='Choose the\noptimization\nmethod:',bg='#a9cef5',font='Times 10 italic')
        label4.place(x=360,y=120,height=50,width=100)
        radio2=Radiobutton(root,text='Simulated Annealing',variable=self.v,value=1,font='Times 8 italic')
        radio2.place(x=450,y=145,height=15,width=130)
        radio3=Radiobutton(root,text='Genetic Optimization',variable=self.v,value=2,font='Times 8 italic')
        radio3.place(x=450,y=170,height=15,width=130)
        radio4=Radiobutton(root,text='Random Optimization',variable=self.v,value=3,font='Times 8 italic')
        radio4.place(x=452,y=195,height=15,width=130)
        self.button_for_Create_Schedules=Button(root,text='Create Course Schedule',command=self.Last_process,bg='grey',font='Times 10 italic')
        self.button_for_Create_Schedules.place(x=40,y=260,height=20,width=180)
        self.result_listbox=Listbox(root,bg='white',font='Times 10 italic')
        self.result_listbox.place(x=20,y=300,height=280,width=560)
        final_scrollbar = Scrollbar(self.result_listbox)
        final_scrollbar.pack(side=RIGHT,fill=Y)
        final_scrollbar.config(command = self.result_listbox.yview)

    def separate_words(self,text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']


    """Convert time to minute"""
    def getminutes(self,t):
        x=time.strptime(t,'%H:%M')
        return x[3]*60+x[4]
    """Convert minute to time"""
    def conver_to_minutes_to_time(self,minutess):
        minutess=int(minutess)
        # a=minutess/60
        # b=minutess%60
        # return str(a)+':'+str(b)
        h,m=divmod(minutess,60)
        return "%02d:%02d"%(h,m)


    """It creates 2 main database which are self.database_dictionary and self.database_dictionary_list_version.
    self.database_dictionary={'Lecture Code(ARAB 101 01)':['Lecture name(Arabic 1)',[(day1,start_time1,finish_time1),(day2,start_time2,finish_time2)...],....}
    self.database_dictionary_list_version={'Departmental codes(ARAB)':['Lecture code1(ARAB 101 1)','Lecture code2'...],...}
    We take information from four column which are column of the Course Code, column of the Course Name, column of the days offered and column of the start-end time.
    We put the information four list.Then we eliminate some lectures which have unspecific lecture time. We find the departmental codes from course code. 
    We create self.listbox_course_list which is a list to add departmental codes into listbox.""" 
    def Create_database(self):
        data=urllib2.urlopen(self.Url.get(1.0,END))
        data=data.read()
        soup=BeautifulSoup(data)
        self.database_dictionary={}
        self.database_dictionary_list_versiyon={}
        self.listbox_course_list=[]
        list_of_lecture_code=[]
        list_of_days=[]
        list_of_times=[]
        list_of_remove=[]
        list_of_names=[]
        for item in soup.findAll('td',{'width':'8%'}):
            list_of_lecture_code.append(item.get_text().split('\n')[1])
        del list_of_lecture_code[0]
        for items in soup.findAll('td',{'width':'15%'}):
            items=self.separate_words(items.get_text())
            list_of_days.append(items)
        del list_of_days[0]
        for itemss in soup.findAll('td',{'width':'7%'}):
            itemss=itemss.get_text().replace('\n','')
            itemss=itemss.replace('  ',' ')
            itemss=itemss.replace('\r','')
            list_of_times.append(itemss.split(' '))
        del list_of_times[0]

        for itemm in soup.findAll('td',{'width':'33%'}):
            list_of_names.append(itemm.get_text())
        del list_of_names[0]

        k=0
        for i in list_of_days:
            if i==[]:
                list_of_remove.append(k)
                k+=1
            else:
                k+=1
        list_of_remove.sort(reverse=True)
        for index in list_of_remove:
            del list_of_days[index]
            del list_of_lecture_code[index]
            del list_of_names[index]
            del list_of_times[index]

        i=-1
        for lecture_code in list_of_lecture_code:
            i+=1
            lecture_code1=lecture_code.split(' ')[0]
            self.database_dictionary[lecture_code]=[]
            self.database_dictionary[lecture_code].append(list_of_names[i])
            self.database_dictionary_list_versiyon.setdefault(lecture_code1,[])
            self.database_dictionary_list_versiyon[lecture_code1].append(lecture_code)
            if len(list_of_days[i])==len(list_of_times[i]):
                helpl=[]
                for k in range(len(list_of_days[i])):
                    helpl.append((list_of_days[i][k],self.getminutes(list_of_times[i][k].split('-')[0]),self.getminutes(list_of_times[i][k].split('-')[1])))
                self.database_dictionary[lecture_code].append(helpl)
            else:
                helpl=[]
                for k in range(len(list_of_days[i])):
                    helpl.append((list_of_days[i][k],self.getminutes(list_of_times[i][0].split('-')[0]),self.getminutes(list_of_times[i][0].split('-')[1])))
                self.database_dictionary[lecture_code].append(helpl)


        for keys in self.database_dictionary_list_versiyon:
            #self.Listbox_for_courses.insert(END,keys)
            self.listbox_course_list.append(keys)
        self.listbox_course_list.sort()
        for courses in self.listbox_course_list:
            self.Listbox_for_courses.insert(END,courses)
        return self.database_dictionary_list_versiyon
    """It creates  available course list and domain."""

    def Create_available_course_list(self):
        a=self.Listbox_for_courses.curselection()
        self.Number_of_lecture=self.Entry_for_number_of_courses.get()
        self.list_of_available_course=[]
        for item in a:
            for course in self.database_dictionary_list_versiyon[self.listbox_course_list[int(item)]]:
                self.list_of_available_course.append(course)


        self.domainn=[]
        for i in range(int(self.Number_of_lecture)):
            self.domainn.append((0,len(self.list_of_available_course)-1-i))
        #print self.domainn
        #print  len(self.list_of_available_course)
    """ We calculate given day cost. cost1=Intersection cost,cost2=Break time cost. Input of function is list_of_tuple=[(start_time1,finish_time1),(start_time2,finish_time2)..]
    If input is empty list which means that day there is no lecture, total cost return -1000.When we calculate cost1, we select a item and compare others then select next item compare something like that.
    In case of cost2, first we delete some items which are included other lecture times,then we calculate cost2. Final step is that add cost1 and cost2."""



    def Calculate_cost(self,list_of_tuple):#list_of_tuple=[(starttime,finishtime),...]

         if len(list_of_tuple)==0:
            total_cost1=-1000
            return total_cost1
         else:
            list_of_tuple.sort()
            helping_list=copy.deepcopy(list_of_tuple)
            cost1=0
            cost2=1
            listt=[]
            for k in range(len(list_of_tuple)-1):
                for i in range(k+1,len(list_of_tuple)):
                    start1,finish1=list_of_tuple[k][0],list_of_tuple[k][1]
                    start2,finish2=list_of_tuple[i][0],list_of_tuple[i][1]
                    if start2>start1 and finish1>start2:
                        if finish1>finish2:
                            cost1+=(finish2*1000-start2*1000)
                            listt.append(i)
                        else:
                            cost1+=(finish1-start2)*1000
                    elif start2==start1:
                        cost1+=(finish1-start1)*1000
            for index in listt:
                    try:
                        list_of_tuple.remove(helping_list[index])
                    except:
                        continue
            for k in range(len(list_of_tuple)-1):
                start1,finish1=list_of_tuple[k][0],list_of_tuple[k][1]
                start2,finish2=list_of_tuple[k+1][0],list_of_tuple[k+1][1]
                if start2>=start1 and finish1>start2:
                    continue
                elif start2>finish1:
                    cost2*=(start2-finish1)
            cost2=float(cost2)/1000

            total_cost1=cost1+cost2
            return total_cost1


    """ We calculate the cost day by day thanks to above function.Input is this funtion a list which is solution list which is coming from optimization method.
    In the begining, we create seven list for each day. For each day, we calculate the cost, then add them. We check monday and friday, if there is no lecture we substract
    1000 from the cost. If solution list has one course more than one times(Some courses have more than one section), we add 10000000 to the cost to prevent this."""


    def Cost_function(self,solution_list):
        self.total_cost=0

        copy_list_of_available_course=copy.deepcopy(self.list_of_available_course)
        list_of_monday=[]
        list_of_tuesday=[]
        list_of_wednesday=[]
        list_of_thursday=[]
        list_of_friday=[]
        list_of_saturday=[]
        list_of_sunday=[]
        list_of_lecture_name=[]
        for index in solution_list:
            item=copy_list_of_available_course[index]
            list_of_lecture_name.append(self.database_dictionary[item][0])
            for times in self.database_dictionary[item][1]:
                day,start,finish=times
                if day==u'monday':
                    list_of_monday.append((start,finish))
                elif day==u'tuesday':
                    list_of_tuesday.append((start,finish))
                elif day==u'wednesday':
                    list_of_wednesday.append((start,finish))
                elif day==u'thursday':
                    list_of_thursday.append((start,finish))
                elif day==u'friday':
                    list_of_friday.append((start,finish))
                elif day==u'saturday':
                    list_of_saturday.append((start,finish))
                elif day==u'sunday':
                    list_of_sunday.append((start,finish))
                else:
                    print 'Wrong'
            del copy_list_of_available_course[index]
        m=0
        n=0
        for m in range(len(list_of_lecture_name)-1):
            name=list_of_lecture_name[m]
            n=m+1
            for n in range(len(list_of_lecture_name)):
                if list_of_lecture_name[n]==name:
                    self.total_cost+=1000000


        self.total_cost+=self.Calculate_cost(list_of_monday)
        self.total_cost+=self.Calculate_cost(list_of_tuesday)
        self.total_cost+=self.Calculate_cost(list_of_wednesday)
        self.total_cost+=self.Calculate_cost(list_of_thursday)
        self.total_cost+=self.Calculate_cost(list_of_friday)
        self.total_cost+=self.Calculate_cost(list_of_saturday)
        self.total_cost+=self.Calculate_cost(list_of_sunday)
        if len(list_of_friday)==0:
            self.total_cost-=1000
        if len(list_of_monday)==0:
            self.total_cost-=1000
        return self.total_cost

    """ It helps to write result into final listbox. It works same idea of calculate cost funtion. Input is the list which represent given days.list=[(start_time1,finish_time1,lecture code)....]
    """



    def Help_to_write(self,list1):#[(start,finish,code),]
        list1.sort()
        if len(list1)>0:
            for material in list1:
                to_write=''
                start,finish,code=material
                to_write=self.conver_to_minutes_to_time(start)+'-'+self.conver_to_minutes_to_time(finish)+' ('+str(code)+')'
                self.result_listbox.insert(END,to_write)
        else:
            self.result_listbox.insert(END,'NO CLASS!!!')

    """ It writes the rsult into final listbox.Input is solution list. It creates seven list for each day, then using above function it shows the result""" 

    



    def write_listbox(self,llistt):#llistt=final solution list
        self.result_listbox.delete(0,END)
        course_list=copy.deepcopy(self.list_of_available_course)
        llist_of_monday=[]
        llist_of_tuesday=[]
        llist_of_wednesday=[]
        llist_of_thursday=[]
        llist_of_friday=[]
        llist_of_saturday=[]
        llist_of_sunday=[]
        for index in llistt:
            item=course_list[index]
            for times in self.database_dictionary[item][1]:
                day,start,finish=times
                if day==u'monday':
                    llist_of_monday.append((start,finish,item))
                elif day==u'tuesday':
                    llist_of_tuesday.append((start,finish,item))
                elif day==u'wednesday':
                    llist_of_wednesday.append((start,finish,item))
                elif day==u'thursday':
                    llist_of_thursday.append((start,finish,item))
                elif day==u'friday':
                    llist_of_friday.append((start,finish,item))
                elif day==u'saturday':
                    llist_of_saturday.append((start,finish,item))
                elif day==u'sunday':
                    llist_of_sunday.append((start,finish,item))
                else:
                    print 'Wrong'
            del course_list[index]
        self.result_listbox.insert(END,'Monday')
        self.Help_to_write(llist_of_monday)
        self.result_listbox.insert(END,'Tuesday')
        self.Help_to_write(llist_of_tuesday)
        self.result_listbox.insert(END,'Wednesday')
        self.Help_to_write(llist_of_wednesday)
        self.result_listbox.insert(END,'Thursday')
        self.Help_to_write(llist_of_thursday)
        self.result_listbox.insert(END,'Friday')
        self.Help_to_write(llist_of_friday)
        self.result_listbox.insert(END,'Saturday')
        self.Help_to_write(llist_of_saturday)
        self.result_listbox.insert(END,'Sunday')
        self.Help_to_write(llist_of_sunday)

    """It is final step. According  to our choice, it runs second part of the program"""



    def Last_process(self):
        self.Create_available_course_list()

        if self.v.get()==0:
            solution_listt=optimization.hillclimb(self.domainn,self.Cost_function)
            self.write_listbox(solution_listt)
        elif self.v.get()==1:
            solution_listt=optimization.annealingoptimize(self.domainn,self.Cost_function)
            self.write_listbox(solution_listt)
        elif self.v.get()==2:
            solution_listt=optimization.geneticoptimize(self.domainn,self.Cost_function)
            self.write_listbox(solution_listt)
        elif self.v.get()==3:
            solution_listt=optimization.randomoptimize(self.domainn,self.Cost_function)
            self.write_listbox(solution_listt)




if __name__=='__main__':
  root = Tkinter.Tk()
  root.title("Course Schedule Advisor")
  root.tk_setPalette("#a9cef5")
  root.geometry('600x600+15+100')
  root.resizable(width=False,height=False)
  Mini_project_4(root).pack()
  root.mainloop()
