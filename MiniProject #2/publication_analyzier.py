#Berkan Ozbabacan / ENGR 212 A / 212990794
#Bekir Zahit Demiray / ENGR 212 A / 212062166

from Tkinter import *
import Tkinter,Tkconstants,tkFileDialog
from tkFileDialog import *
import ttk
from bs4 import BeautifulSoup
import urllib2
import string
from clusters import *

class TkFileDialogExample(Tkinter.Frame):
    def __init__(self,root):
        Tkinter.Frame.__init__(self,root)

        #Enter URL part
        self.url_text=Text(root,bg='white',font='Times 6 italic')
        self.url_text.place(x=10,y=40,width=400,height=164)
        label_for_URL=Label(root,text='        Please enter Google Scholar profile URLs(one URL per line)',font='Times 9 italic',height=2,width=45,bg="#a9cef5")
        label_for_URL.place(x=20,y=2)

        #Download Part
        self.download_text=Listbox(root,height=10,width=35,bg='white')
        self.download_text.place(x=480,y=40)
        download_publications_profiles=Tkinter.Button(root,text='Download Publications Profiles',command=self.Downloaded_part,bg='#f5aaa9',width=29,height=1,font='Times 10 italic' )
        download_publications_profiles.place(x=480,y=5)

        #View Publications for a Researcher
        General_label_1=Label(root,height=10,width=57,bg='white')
        General_label_1.place(x=10,y=260)
        View_publications=Label(root,text='View Publications for a Researcher', font='Times 10 italic',height=2,width=32,bg='orange')
        View_publications.place(x=10,y=224)
        Choose_researcher=Label(root,text='Choose a\nresearcher:',font='Times 8 italic',height=2,width=10,bg='white')
        Choose_researcher.place(x=12,y=270)
        label_for_group=Label(root,text='Group by:',font='Times 8 italic',height=1,width=8,bg='white')
        label_for_group.place(x=242,y=281)
        self.combovar=StringVar()
        self.box = ttk.Combobox(textvariable = self.combovar,width=20,height=4,font='Times 8 italic' )
        self.box.place(x=97,y=280)
        self.v=IntVar()
        group_by_year=Radiobutton(root,text='Year',variable=self.v,padx=25,value=1,font='Times 8 italic',bg='white')
        group_by_year.place(x=292,y=268)
        group_by_type=Radiobutton(root,text='Type',variable=self.v,padx=25,value=0,font='Times 8 italic',bg='white' )
        group_by_type.place(x=292,y=288)
        group_by_none=Radiobutton(root,text='None',variable=self.v,padx=25,value=2,font='Times 8 italic',bg='white')
        group_by_none.place(x=292,y=308)
        self.v.set(1)
        label_for_sort=Label(root,text='Sort by:',height=1,width=8,bg='white',font='Times 8 italic')
        label_for_sort.place(x=242,y=335)
        self.y=IntVar()
        sort_by_year=Radiobutton(root,text='Year',variable=self.y,padx=25,value=1,font='Times 8 italic',bg='white')
        sort_by_year.place(x=290,y=336)
        sort_by_citation_count=Radiobutton(root,text='Citation Count',variable=self.y,padx=25,value=0,font='Times 8 italic',width=5,bg='white' )
        sort_by_citation_count.place(x=308,y=356)
        self.y.set(1)
        list_publications=Tkinter.Button(root,text='List Publications',command=self.View_Publications_for_a_Researcherss,bg='#f5aaa9',width=20,height=1,font='Times 10 italic' )
        list_publications.place(x=258,y=384)

        #Cluster Researchers
        General_label_2=Label(root,bg='white',height=10,width=29)
        General_label_2.place(x=482,y=260)
        Clusters_researchers=Label(root,text='Clusters Researchers',bg='orange',height=2,width=20,font='Times 10 italic')
        Clusters_researchers.place(x=482,y=224)
        label_for_clustering_method=Label(root,text='Clustering Method:',height=1,width=15,bg='white',font='Times 8 italic')
        label_for_clustering_method.place(x=488,y=270)
        label_for_k=Label(root,text='k:',height=1,width=2,bg='white')
        label_for_k.place(x=615,y=325)
        self.z=IntVar()
        hierarchical_clustering=Radiobutton(root,text='Hierarchical',variable=self.z,padx=25,value=1,font='Times 8 italic',bg='white')
        hierarchical_clustering.place(x=484,y=300)
        self.k_means_entry=Entry(root,bg='green',width=4)
        self.k_means_entry.place(x=650,y=326)
        self.k_means_entry.insert(END,'5')
        k_means_clustering=Radiobutton(root,text='K-Means',bg='white',variable=self.z,padx=25,value=int(self.k_means_entry.get()),font='Times 8 italic' )
        k_means_clustering.place(x=484,y=324)
        self.z.set(1)        
        view_cluster=Tkinter.Button(root,text='View Clusters',command=None,bg='#a9cef5',width=15,height=1,font='Times 10 italic' )
        view_cluster.place(x=570,y=383)

        #Final Listbox
        self.final_text=Listbox(root,bg='white',font='Times 10 italic')
        self.final_text.place(x=10,y=430,height=260,width=683)
        final_scrollbar = Scrollbar(self.final_text)
        final_scrollbar.pack(side=RIGHT,fill=Y)
        final_scrollbar.config(command = self.final_text.yview)
        
    #Help us to get the URL's of articles    
    def Convert_url(self,url):
        list1=url.split('citations')
        return list1[0]

    #BiggestDictionary={'Ali Hoca':{'Article1':{'Author':'ali hoca, other authors,'Publication Date':'2008'}}} <- That's the structure..
    def Create_dictionary_as_databese(self,given_urls):
        self.databese_dictionary={}
        self.match_url_with_writer={}
        #keys match to names of the teachers and values match to the websites of the teachers
        self.match_writer_with_url={}
        
        for urll in given_urls:
            url=urll.encode()
            
            self.list_of_second_url=[]
            data=urllib2.urlopen(url)
            data2=data.read()
            soup=BeautifulSoup(data2)
            self.list_of_citations=[]
            self.databese_dictionary.setdefault(url,{})
            
            for writerr in soup.findAll('div',{'id':'gsc_prf_in'}):
                writer1=writerr.get_text()
                writer=writer1.encode()
            self.match_url_with_writer[url]=writer
            self.match_writer_with_url[writer]=url
            self.download_text.insert(END,writer+'(Downloaded)')    

            for i in soup.findAll('a',{'class':'gsc_a_at'}):
                    second_url=self.Convert_url(url)+i.get('href')
                    self.list_of_second_url.append(second_url.encode())
                    self.databese_dictionary[url][second_url.encode()]={}
                
            for k in soup.findAll('td',{'class':'gsc_a_c'}):
                if k.get_text()==u'\xa0':
                    self.list_of_citations.append('0')
                else:
                    self.list_of_citations.append(k.get_text())

            for url2 in self.list_of_second_url:
                list_of_value=[]
                list_of_field=[]
                data_for_second=urllib2.urlopen(url2)
                data2_for_second=data_for_second.read()
                soup2=BeautifulSoup(data2_for_second)

                for field in soup2.findAll('div',{'class':'gsc_field'}):
                    field_str=field.get_text()
                    list_of_field.append(field_str.encode())
                for value in soup2.findAll('div',{'class':'gsc_value'}):
                    list_of_value.append(value.get_text())
                for title in soup2.findAll('div',{'id':'gsc_title'}):
                    self.databese_dictionary[url][url2.encode()]['Title']=title.get_text()
                for k in range(0,len(list_of_field)):
                    self.databese_dictionary[url][url2.encode()][list_of_field[k]]=list_of_value[k]

            for k in range(0,len(self.list_of_second_url)):
                self.databese_dictionary[url][self.list_of_second_url[k]]['Total citations']=self.list_of_citations[k]
            
            for items in self.list_of_second_url:
                if 'Publication date' not in self.databese_dictionary[url][items]:
                    list1=['1000']
                    self.databese_dictionary[url][items]['Publication date']=list1[0]

        self.list_of_researchers = [keys for keys in self.match_writer_with_url]
        self.box['value'] = tuple(self.list_of_researchers)
        return self.databese_dictionary
            
    #[([date1],url's of the articles),.....] <- That's the structure
    def Sorting_with_year(self,dictionary):
        self.list_for_sorting_with_year=[]
        for keys in dictionary:
            list1=dictionary[keys]['Publication date'].encode().split('/')
            list2=[int(items) for items in list1]
            value,article=list2,keys
            self.list_for_sorting_with_year.append((value,keys))
        self.list_for_sorting_with_year.sort(reverse=True)
        return self.list_for_sorting_with_year
      
     #[(citation number,url's of the articles),.....] <- That's the structure
    def Sorting_with_citation_count(self,dictionary):
        self.list_for_sorting_with_citation=[]
        for keys in dictionary:
            value,article=int(dictionary[keys]['Total citations'].encode()),keys
            self.list_for_sorting_with_citation.append((value,article))
        self.list_for_sorting_with_citation.sort(reverse=True)
        return self.list_for_sorting_with_citation

    def group_by_year(self,dictionary):
        self.list_of_year=[]
        self.dictionary_for_group_by_year={}
        for key in dictionary:
            if int((dictionary[key]['Publication date']).encode()[0:4]) not in self.list_of_year:
                self.list_of_year.append(int((dictionary[key]['Publication date'].encode())[0:4]))
                self.dictionary_for_group_by_year.setdefault((dictionary[key]['Publication date'].encode())[0:4],{})
        #The years that are assing are in this list in order from the biggest to the smallest
        self.list_of_year.sort(reverse=True)
        for dates in self.list_of_year:
            for key in dictionary:
                if dates == (dictionary[key]['Publication date'].encode())[0:4]:
                    self.dictionary_for_group_by_year[dates][key]=dictionary[key]['Publication date']
        return self.dictionary_for_group_by_year
    
    #[[list of journals' article urls],[list of conferences' article urls],......] <- That's the structure
    def group_by_type(self,dictionary):
        self.list_of_journal=[]
        self.list_of_conference=[]
        self.list_of_book=[]
        self.list_of_patent_office=[]
        self.list_of_technical_work=[]
        for key in dictionary:
            for keys in dictionary[key]:
                if keys=='Conference':
                    self.list_of_conference.append(key)
                elif keys=='Journal':
                    self.list_of_journal.append(key)
                elif keys=='Book':
                    self.list_of_book.append(key)
                elif keys=='Patent office':
                    self.list_of_patent_office.append(key)
        self.list_of_total=[]
        self.list_of_total.append(self.list_of_journal)
        self.list_of_total.append(self.list_of_conference)
        self.list_of_total.append(self.list_of_book)
        self.list_of_total.append(self.list_of_patent_office)
        return self.list_of_total
            
    #It helps us to write final results in the listbox
    def help_to_write(self,dictionary):
        list_of_subjects_to_write=['Authors','Title','Journal','Conference','Volume','Issue','Page numbers','Publication date','Total citations']
        self.list_of_subjects_to_write=""
        for items in list_of_subjects_to_write:
            if items not in dictionary:
                continue
            elif items=='Authors':
                self.list_of_subjects_to_write+=dictionary[items]+"."
            elif items=='Title':
                self.list_of_subjects_to_write+= '"'+dictionary[items]+'"'+'.'
            elif items=='Total citations':
                self.list_of_subjects_to_write+="["+dictionary[items]+' citation'+']'

            elif items=='Publication date':
                if dictionary[items]!= 1000 :
                    self.list_of_subjects_to_write+=dictionary[items]+'.'
                else:
                    continue
            else:
                pass

        length_of_string=len(self.list_of_subjects_to_write)
        repeat_number_float=float(length_of_string)/111
        repeat_number=length_of_string/111
        k=0
        self.final_help=[]

        if length_of_string<112:
            self.final_help.append(self.list_of_subjects_to_write)
        else:
            if k<repeat_number and repeat_number==repeat_number_float :
                while k<repeat_number:

                    self.final_help.append(self.list_of_subjects_to_write[k*111:(k+1)*111])
                    k+=1
            else:
                while k<repeat_number_float:
                    while k<repeat_number:
                        self.final_help.append(self.list_of_subjects_to_write[k*111:(k+1)*111])
                        k+=1
                    self.final_help.append(self.list_of_subjects_to_write[k*111:])
                    k+=1    
        
        return self.final_help

    #Downloaded part
    def Downloaded_part(self):
        a=self.url_text.get(0.0,END)
        self.list_of_urls=a.split('\n')
        space=len(self.list_of_urls)
        del self.list_of_urls[space-1]
        self.Create_dictionary_as_databese(self.list_of_urls)

    #List Publications
    def group_by_year_with_sorting_year(self,person):
        self.Sorting_with_year(self.databese_dictionary[self.match_writer_with_url[person]])
        self.group_by_year(self.databese_dictionary[self.match_writer_with_url[person]])
        self.list_help_to_write=[]
        for items in self.list_of_year:
            list1=[]
            for item in self.list_for_sorting_with_year:
                (date,second_url)=item
                if items==int(date[0]):
                    list1.append(second_url)
            self.list_help_to_write.append(list1)
        
        #It helps to enumerate the articles
        j=0
        for i in range(0,len(self.list_of_year)):
                self.final_text.insert(END, self.list_of_year[i])
                for second_urls in self.list_help_to_write[i]:
                    self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][second_urls])
                    if len(self.final_help)==1:
                        for items in self.final_help:
                            self.final_text.insert(END,str((j+1))+'. '+items)
                        j+=1   
                    else:
                        self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                        for items in self.final_help[1:]:
                            self.final_text.insert(END,items)
                        j+=1

    def group_by_year_with_sorting_citation(self,person):
        self.Sorting_with_citation_count(self.databese_dictionary[self.match_writer_with_url[person]])
        self.group_by_year(self.databese_dictionary[self.match_writer_with_url[person]])
        self.list_help_to_write=[]
        for items in self.list_of_year:
            list1=[]
            for item in self.list_for_sorting_with_citation:
                (citation,second_url)=item
                if items==self.databese_dictionary[self.match_writer_with_url[person]][second_url]['Publication date'][0:4]:
                    list1.append(second_url)

            (self.list_help_to_write).append(list1)

        for k in range(0,len(self.list_of_year)):
            self.final_text.insert(END, self.list_of_year[k]+':')
            j=0
            for second_urls in self.list_help_to_write[k]:

                self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][second_urls])
                if len(self.final_help)==1:
                    for items in self.final_help:
                        self.final_text.insert(END,str((j+1))+'. '+items)
                    j+=1   
                else:
                    self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                    for items in self.final_help[1:]:
                        self.final_text.insert(END,items)
                    j+=1

    def group_by_type_with_sorting_year(self,person):
        self.Sorting_with_year(self.databese_dictionary[self.match_writer_with_url[person]])
        self.group_by_type(self.databese_dictionary[self.match_writer_with_url[person]])
        self.list_help_to_write_journal=[]
        self.list_help_to_write_conference=[]
        self.list_help_to_write_book=[]
        self.list_help_to_write_patent_office=[]

        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[0]:
                if item==second_url:
                    self.list_help_to_write_journal.append(second_url)
        
        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[1]:
                if item==second_url:
                    self.list_help_to_write_conference.append(second_url)

        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[2]:
                if item==second_url:
                    self.list_help_to_write_book.append(second_url)

        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[3]:
                if item==second_url:
                    self.list_help_to_write_patent_office.append(second_url)

        self.final_text.insert(END,'Journal Papers:')
        j=0
        for items in self.list_help_to_write_journal:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1
            
        self.final_text.insert(END,'Conference Papers:')
        for items in self.list_help_to_write_conference:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1

        self.final_text.insert(END,'Book:')
        j=0
        for items in self.list_help_to_write_book:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1

        self.final_text.insert(END,'Patent office:')
        j=0
        for items in self.list_help_to_write_patent_office:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1

    def group_by_type_with_sorting_citation(self,person):
        self.group_by_type(self.databese_dictionary[self.match_writer_with_url[person]])
        self.Sorting_with_citation_count(self.databese_dictionary[self.match_writer_with_url[person]])
        self.list_help_to_write_journal=[]
        self.list_help_to_write_conference=[]
        self.list_help_to_write_book=[]
        self.list_help_to_write_patent_office=[]

        for items in self.list_for_sorting_with_citation:
            (citation,second_url)=items
            for item in self.list_of_total[0]:
                if item==second_url:
                    self.list_help_to_write_journal.append(second_url)
        
        for items in self.list_for_sorting_with_citation:
            (citation,second_url)=items
            for item in self.list_of_total[1]:
                if item==second_url:
                    self.list_help_to_write_conference.append(second_url)

        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[2]:
                if item==second_url:
                    self.list_help_to_write_book.append(second_url)

        for items in self.list_for_sorting_with_year:
            (date,second_url)=items
            for item in self.list_of_total[3]:
                if item==second_url:
                    self.list_help_to_write_patent_office.append(second_url)

        self.final_text.insert(END,'Journal Papers:')
        j=0
        
        for items in self.list_help_to_write_journal:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for items in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+items)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for items in self.final_help[1:]:
                    self.final_text.insert(END,items)
                j+=1
            
        self.final_text.insert(END,'Conference Papers:')
        for items in self.list_help_to_write_conference:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1

        self.final_text.insert(END,'Book:')
        j=0
        for items in self.list_help_to_write_book:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1

        self.final_text.insert(END,'Patent office:')
        j=0
        for items in self.list_help_to_write_patent_office:
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][items])
            if len(self.final_help)==1:
                for item in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+item)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for item in self.final_help[1:]:
                    self.final_text.insert(END,item)
                j+=1
                
    def group_by_none_with_sorting_year(self,person):
        self.Sorting_with_year(self.databese_dictionary[self.match_writer_with_url[person]])
        j=0
        for item in self.list_for_sorting_with_year:
            (date,second_url)=item
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][second_url])
            if len(self.final_help)==1:
                for items in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+items)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for items in self.final_help[1:]:
                    self.final_text.insert(END,items)
                j+=1
            
    def group_by_none_with_sorting_citation(self,person):
        self.Sorting_with_citation_count(self.databese_dictionary[self.match_writer_with_url[person]])
        j=0
        for item in self.list_for_sorting_with_citation:
            (citation,second_url)=item
            self.help_to_write(self.databese_dictionary[self.match_writer_with_url[person]][second_url])
            if len(self.final_help)==1:
                for items in self.final_help:
                    self.final_text.insert(END,str((j+1))+'. '+items)
                j+=1   
            else:
                self.final_text.insert(END,str((j+1))+'. '+self.final_help[0])
                for items in self.final_help[1:]:
                    self.final_text.insert(END,items)
                j+=1
                    
    def View_Publications_for_a_Researcherss(self):
        if self.v.get()==1 and self.y.get()==1:
            self.final_text.delete(0,END)
            self.group_by_year_with_sorting_year(self.combovar.get())
        elif self.v.get()==1 and self.y.get()==0:
            self.final_text.delete(0,END)
            self.group_by_year_with_sorting_year(self.combovar.get())
        elif self.v.get()==0 and self.y.get()==1:
            self.final_text.delete(0,END)
            self.group_by_type_with_sorting_year(self.combovar.get())
        elif self.v.get()==0 and self.y.get()==0:
            self.final_text.delete(0,END)
            self.group_by_type_with_sorting_citation(self.combovar.get())
        elif self.v.get()==2 and self.y.get()==1:
            self.final_text.delete(0,END)
            self.group_by_none_with_sorting_year(self.combovar.get())
        elif self.v.get()==2 and self.y.get()==0:
            self.final_text.delete(0,END)
            self.group_by_none_with_sorting_citation(self.combovar.get())
                                                     
if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("ADVISOR'S RECOMMENDATIONS")
    root.tk_setPalette("#a9cef5")
    root.geometry('700x700+15+100')
    root.resizable(width=False,height=False)
    TkFileDialogExample(root).pack()
    root.mainloop()
