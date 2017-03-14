#Berkan Ozbabacan / ENGR 212 A / 212990794
#Bekir Zahit Demiray / ENGR 212 A / 212062166

from Tkinter import *
import Tkinter,Tkconstants,tkFileDialog
import ttk
import searchengine
import os
import re
import linecache
import time

class Miniproject3(Tkinter.Frame):
    def __init__(self,root):
        Tkinter.Frame.__init__(self,root)
        self.label1=Label(root,text="Digital Library Search Engine",bg='#20413A',font='Times 15 italic')
        self.label1.place(x=10,y=10,height=50,width=680)
        self.text1=Text(root,bg='#A52A2A',font='Times 15 italic')
        self.text1.place(x=50,y=70,height=30,width=600)
        self.button1=Button(root,text='Initialize',command=self.initialize,bg='#A52A2A',font='Times 12 italic')
        self.button1.place(x=290,y=110,height=30,width=100)
        #Shows results
        self.listbox1=Listbox(bg='#A52A2A',font='Times 11 italic')
        self.listbox1.place(x=10,y=170,height=390,width=680)
        #Shows number of articles and time
        self.listbox2=Listbox(bg='#A52A2A',font='Times 10 italic')
        self.listbox2.place(x=20,y=150,height=20,width=180)
        #Page label
        self.label2=Label(root,text='Page:',bg='#A52A2A',font='Times 12 italic')
        self.label2.place(x=439,y=560,height=25,width=50)
        #Previous button
        self.button_previous=Button(root,text='Previous',command=self.Previous_functions,bg='#A52A2A',font='Times 12 italic')
        self.button_previous.place(x=499,y=560,height=25,width=70)
        #Page number
        self.listbox_page_number=Listbox(bg='#A52A2A',font='Times 12 italic')
        self.listbox_page_number.place(x=579,y=560,height=25,width=30)
        #Next button
        self.button_next=Button(root,text='Next',command=self.Next_functions,bg='#A52A2A',font='Times 12 italic')
        self.button_next.place(x=619,y=560,height=25,width=70)
        #Dictionaries
        self.citations={}
        self.wordlocations={}
        self.citationcounts={}
        self.match_id_with_Title={}
        self.PageRankk={}
        self.dictionary_as_database={}

    def separate_words(self,text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    #This function helps us to find word locations and match papers' ids with their titles
    def Metadata_data(self):
        self.directory=os.getcwd()
        list_of_directories=os.listdir(self.directory)
        for keys in list_of_directories:
            if keys=='metadata':
                os.chdir(keys)

        for file in os.listdir(os.getcwd()):
            a=''
            with open(file) as f:
                line=f.readlines()
                for lines in line:
                    a+=lines
                b=a.split('Paper:')
                c=a.split('\nFrom:')
                id=c[0][len(b[0])+14:]
                b=a.split('\n\n')
                c=a.split('\nAuthor')
                Title=c[0][len(b[0])+9:]
                d=a.split('\\\n')
                abstract=d[len(d)-2]
                location=0

                for words in self.separate_words(Title):
                    self.wordlocations.setdefault(words,{})
                    self.wordlocations[words].setdefault(id,[])
                    self.wordlocations[words][id].append(location)
                    location+=1

                for word in self.separate_words(abstract):
                    self.wordlocations.setdefault(word,{})
                    self.wordlocations[word].setdefault(id,[])
                    self.wordlocations[word][id].append(location)
                    location+=1
            self.match_id_with_Title[id]=Title

    #This function provides filling the citations and citationcounts dictionaries 
    def Citations_data(self):
        os.chdir(self.directory)
        k=0

        for lines in open('citations.txt'):
            if k<2:
                k+=1
                continue
            else:
                list1=lines.split('\t')
                (fromId,toId)=list1[0],list1[1][:len(list1[1])-1]
                self.citations.setdefault(toId,[])
                self.citations[toId].append(fromId)
                self.citationcounts.setdefault(fromId,0)
                self.citationcounts[fromId]+=1
        return self.citations

    '''First we look for the entries, separate these entries to words, put the papers which include first of the separated words into list which is named as
    list_of_papers, then we compare the papers which include first of the separated word with the other papers which include other separated words of the entry,
    if the papers, which is including first separated word, are not included in the other papers, which are including other separated ones, we delete that papers
    which are including first separated word of the entry and finally we find the papers including the separated words of the entries in common'''
    def searching_words(self):
        self.list_of_results={}
        list1=[words for words in self.separate_words(self.text1.get(0.0,END))]
        list_of_papers=[papers for papers in self.wordlocations[list1[0]]]

        for papers in self.wordlocations[list1[0]]:
            k=1
            while k<len(list1):
                if papers not in self.wordlocations[list1[k]]:
                    list_of_papers.remove(papers)
                    k+=len(list1)
                else:
                    k+=1

        for papers in list_of_papers:
            score=1
            for words in list1:
                score=score*len(self.wordlocations[words][papers])
            self.list_of_results[papers]=score
        self.list_of_results=self.normalizescoress(self.list_of_results)
        return self.list_of_results

    def normalizescoress(self,scores,smallIsBetter=0):
        vsmall = 0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    #This function calculates pagerank scores
    def PageRankscores(self):
        #for ids in self.match_id_with_Title:
            #self.PageRankk[ids]=1.0

        for ids in self.citations:
            self.PageRankk[ids]=1.0

        for ids in self.citationcounts:
            self.PageRankk[ids]=1.0
        PageRank1=self.PageRankk

        for i in range(20):
            for id in PageRank1:
                pr=0.15
                if id in self.citations:
                    for keys in self.citations[id]:
                        linkingpr=PageRank1[keys]
                        linkincount=self.citationcounts[keys]
                        pr+=0.85*float((linkingpr/linkincount))
                        self.PageRankk[id]=pr
            PageRank1=self.PageRankk

        for idss in self.match_id_with_Title:
            self.PageRankk.setdefault(idss,1)
        self.PageRankk=self.normalizescoress(self.PageRankk)
        return   self.PageRankk

    #This function add up page rank score and content based score, then normalise it
    def PageRank_and_Content_based(self):
        self.list_of_tuple=[]
        for id in self.list_of_results:
            self.list_of_results[id]=self.list_of_results[id]+self.PageRankk[id]
        self.list_of_results=self.normalizescoress(self.list_of_results)

        for keys in self.list_of_results:
            self.list_of_tuple.append((self.list_of_results[keys],keys))
        self.list_of_tuple.sort(reverse=True)

    def initialize(self):
        list1=['Please wait while the search engine performs the initialize phase:','Loading Paper Metadata (In progress)','Loading Paper Metadata (Completed)','Loading Citation Data (In progress)','Loading Citation Data (Completed)','Computing PageRank Scores (In progress)','Computing PageRank Scores (Completed)']

        self.listbox1.insert(END,list1[0])
        self.listbox1.insert(END,list1[1])
        self.listbox1.update()
        self.Metadata_data()
        self.listbox1.delete(0,END)
        self.listbox1.insert(END,list1[0])
        self.listbox1.insert(END,list1[2])
        self.listbox1.insert(END,list1[3])
        self.listbox1.update()

        self.Citations_data()
        self.listbox1.delete(0,END)
        self.listbox1.insert(END,list1[0])
        self.listbox1.insert(END,list1[2])
        self.listbox1.insert(END,list1[4])
        self.listbox1.insert(END,list1[5])
        self.listbox1.update()

        self.PageRankscores()
        self.listbox1.delete(0,END)
        self.listbox1.insert(END,list1[0])
        self.listbox1.insert(END,list1[2])
        self.listbox1.insert(END,list1[4])
        self.listbox1.insert(END,list1[6])
        self.listbox1.update()
        self.button1.configure(text='Search',command=self.Show_results)

    #We linked this to the search button, it simply shows the results
    def Show_results(self):
        try:
            start_time=time.time()
            self.listbox1.delete(0,END)
            self.searching_words()
            self.PageRank_and_Content_based()
            self.total_page_with_float=len(self.list_of_tuple)/float(20)
            self.total_page=len(self.list_of_tuple)/20
            self.result=1
            if self.total_page_with_float>1:
                k=1
                for items in self.list_of_tuple[:20]:
                    (value,id)=items
                    self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                    k+=1
            else:
                k=1
                for items in self.list_of_tuple:
                    (value,id)=items
                    self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                    k+=1
            self.listbox2.delete(0,END)
            self.listbox_page_number.delete(0,END)
            self.listbox2.insert(END,str(len(self.list_of_tuple))+' Papers '+'('+('%s'%(time.time()-start_time))+')')
            self.listbox_page_number.insert(END,str(self.result))
        except:
            self.listbox1.delete(0,END)
            self.listbox2.delete(0,END)
            self.listbox1.insert(END,'The word or words you are looking for are not included in the database.')

    def Next_functions(self):
        self.listbox1.delete(0,END)
        self.listbox_page_number.delete(0,END)
        if len(self.list_of_tuple)<=20:
            k=1
            for items in self.list_of_tuple:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.listbox_page_number.insert(END,self.result)
        elif self.result<self.total_page:
            k=1+self.result*20
            for items in self.list_of_tuple[(self.result)*20:(self.result+1)*20]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.result+=1
            self.listbox_page_number.insert(END,str(self.result))
        elif self.result<self.total_page_with_float:
            k=1+self.result*20
            for items in self.list_of_tuple[self.result*20:]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.result+=1
            self.listbox_page_number.insert(END,str(self.result))
        else:
            k=1+(self.result-1)*20
            for items in self.list_of_tuple[(self.result-1)*20:]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
                self.listbox_page_number.insert(END,str(self.result))

    def Previous_functions(self):
        self.listbox1.delete(0,END)
        self.listbox_page_number.delete(0,END)
        if len(self.list_of_tuple)<=20:
            k=1
            for items in self.list_of_tuple:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.listbox_page_number.insert(END,self.result)
        elif self.result>self.total_page_with_float:
            self.result-=1
            k=1+(self.result-1)*20
            for items in self.list_of_tuple[(self.result-1)*20:self.result*20]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.listbox_page_number.insert(END,self.result)
        elif self.result>1 and self.result<=self.total_page_with_float:
            self.result-=1
            k=1+(self.result-1)*20
            for items in self.list_of_tuple[(self.result-1)*20:self.result*20]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.listbox_page_number.insert(END,self.result)
        else:
            k=1+(self.result-1)*20
            for items in self.list_of_tuple[(self.result-1)*20:self.result*20]:
                (value,id)=items
                self.listbox1.insert(END,str(k)+'-) '+str(self.match_id_with_Title[id])+'    '+str(value))
                k+=1
            self.listbox_page_number.insert(END,self.result)
            
if __name__=='__main__':
  root = Tkinter.Tk()
  root.title("SEARCH ENGINE")
  root.tk_setPalette("#20413A")
  root.geometry('700x600+15+100')
  root.resizable(width=False,height=False)
  Miniproject3(root).pack()
  root.mainloop()
