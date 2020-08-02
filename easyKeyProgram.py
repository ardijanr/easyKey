import easyKeyFunc as easyFunc
import tkinter as tk
import tkinter.filedialog
import threading
import os
from functools import partial

class GUI_easyKey:
    def __init__(self):
        self.window= tk.Tk()
        self.window.title("easyKey Translations")
        self.window.resizable(False,False)

        self.input_key1="Start typing in any field to search"
        self.input_key2="Start typing in any field to search"
        self.input_translation_ALT=""
        self.input_translation_EN=""
        self.status_text=tk.StringVar()
        self.status_text.set("Load files to begin")
        self.dict_EN=None
        self.dict_ALT=None
        self.dict_EN_path=""
        self.dict_ALT_path=""
        self.changed_lists=""
        self.Last_deleted_EN=None
        self.Last_deleted_ALT=None
        self.test=False
        self.overwrite_files=False

        self.reversed=False
        self.search_results_type=''
        self.visible_results_KEY=[]
        self.visible_results_EN=[]
        self.visible_results_ALT=[]

        self.wait=False
        self.resolve_index=0
        self.resolve_state=False
        self.file_missing=True
        self.last_ingored_key=[]


        self.frame1=tk.Frame(self.window, borderwidth=20)
        self.frame2=tk.Frame(self.window,padx=20,pady=0)
        self.frame3=tk.Frame(self.window,padx=20)
        self.status=tk.Frame(self.window,padx=20,pady=2)


        self.frame1.grid(row=0,sticky='we')
        self.status.grid(row=1,sticky='we',padx=20)
        self.frame2.grid(row=2)
        self.frame3.grid(row=3,sticky='we')

        self.frame1.columnconfigure(2,weight=1)
        self.frame3.columnconfigure(1,weight=1)
        self.frame3.columnconfigure(3,weight=1)
        self.frame2.columnconfigure(0,weight=1)
        self.frame2.columnconfigure(1,weight=1)
        # self.frame1.columnconfigure(5,weight=1)
        self.menu=tk.Menu(self.window,tearoff=0)

        self.filemenu=tk.Menu(self.menu,tearoff=0)

        self.menu.add_separator()

        # self.menu_buttons=tk.Menu(self.menu,tearoff=0)

        self.menu.add_cascade(label='File', menu=self.filemenu)

        self.menu.add_command(label='Reload Files',command=self.reload_files)




        self.filemenu.add_command(label="Select Files",command=self.select_file_menu)

        self.filemenu.add_command(label="Save Files", command=self.save_to_subfolder)




        tk.Label(self.frame1, text="INPUT KEY:").grid(row=0,column=0,sticky='e',pady=5)
        tk.Label(self.frame1, text="INPUT ENLISH:").grid(row=1,column=0,sticky='e',pady=5)
        tk.Label(self.frame1, text="INPUT ALBANIAN:").grid(row=2,column=0,sticky='e',pady=5)

        self.input_key_field=tk.Entry(self.frame1,width=50)
        self.input_key_field.grid(row=0, column=1)

        self.clear_button=tk.Button(self.frame1,text="Clear Input",command=self.clear_input_fields)
        self.clear_button.grid(column=2,row=1,sticky="nw",padx=5)


        self.input_translation_EN_field=tk.Entry(self.frame1,width=50)
        self.input_translation_EN_field.grid(row=1, column=1)


        self.input_translation_ALT_field=tk.Entry(self.frame1,width=50)
        self.input_translation_ALT_field.grid(row=2, column=1)

        self.search_button=tk.Button(self.frame1,text="CHECK FILE MISMATCH",width=20,command=self.checkKeyMismatch)
        self.search_button.grid(row=0,column=5,sticky='e')


        tk.Label(self.status, text="STATUS:").grid(row=3,column=0,pady=0,sticky='sw',padx=5)
        tk.Label(self.status,fg="blue", textvariable=self.status_text).grid(row=3,column=1,sticky='sw',pady=0)


        self.textDisplay1=tk.Text(self.frame2,height=20,width=50,font="arial,32")
        self.textDisplay1.grid(column=0,row=2,rowspan=14)
        self.textDisplay1.insert('0.0',self.input_key1)
        self.textDisplay1.config(state='disabled')

        self.button_i=[]
        self.frame2.rowconfigure(14,weight=1)
        for i in range(11):
            self.button_i.append(tk.Button(self.frame2,text="----------",font=('Helvetica', '2'),command= partial(self.set_input_value,i) ))
            self.button_i[i].grid(column=1,row=3+i,sticky='we',pady=(1,0))

        self.button_i[0].grid(pady=(1.5,0))

 


        self.textDisplay2=tk.Text(self.frame2,height=20,width=50,font="arial,32")
        self.textDisplay2.grid(column=2,row=2,rowspan=14)
        self.textDisplay2.insert('0.0',self.input_key2)
        self.textDisplay2.config(state='disabled')


        self.undo_button=tk.Button(self.frame3,text="UNDO LAST",width=15,pady=10,command=self.undo_last_change)
        self.undo_button.grid(row=3,column=2,pady=5)
        self.add_button=tk.Button(self.frame3,text="ADD",width=15,pady=10,command=self.add_new_value)
        self.add_button.grid(row=3,column=4,sticky='e',pady=5)
        self.del_button=tk.Button(self.frame3,text="DELETE",width=15,command=self.delete_word)
        self.del_button.grid(row=3,column=0,sticky='w')
        self.del_button=tk.Button(self.frame3,text="OVERWRITE",width=15,command=self.overwrite_value)
        self.del_button.grid(row=3,column=1,sticky='w')





        self.window.bind("<Key>", lambda e:self.autosearch())
        self.window.bind("<Control-Key-s>", lambda e:self.save_to_subfolder())
        self.window.bind("<F5>", lambda e:self.self.reload_files())
        self.window.bind("<F1>", lambda e:self.load_current_dir())
        self.window.bind("<F12>", lambda e:self.overwrite_files_toggle())
        self.window.update()
        self.window.config(menu=self.menu)
        self.window.mainloop()

    def overwrite_files_toggle(self):
        self.overwrite_files=self.overwrite_files!=True
        #print(self.overwrite_files)

        status_text=['Overwrite Files DISABLED','Overwrite Files ENABLED']

        self.changeStatus(status_text[self.overwrite_files])

    def changeStatus(self,value):
        self.status_text.set(value)

    def add_Value1(self,value):
        self.textDisplay1.config(state='normal')
        self.textDisplay1.insert('0.0',str(value))
        self.textDisplay1.config(state='disabled')

    def add_Value2(self,value):
        self.textDisplay2.config(state='normal')
        self.textDisplay2.insert('0.0',str(value))
        self.textDisplay2.config(state='disabled')

    def clear_text(self):
        self.textDisplay2.config(state='normal')
        self.textDisplay2.delete('0.0',tk.END)
        self.textDisplay2.config(state='disabled')

        self.textDisplay1.config(state='normal')
        self.textDisplay1.delete('0.0',tk.END)
        self.textDisplay1.config(state='disabled')


    def select_file_menu(self):

        self.select_file_window=tk.Tk()
        self.select_file_window.geometry("300x400")
        self.select_file_window.wm_title("Select Files")
        self.select_file_window.rowconfigure(3,weight=1)
        self.select_file_window.columnconfigure(0,weight=1)

        label= tk.Label(self.select_file_window,text="Select Files",font="arial,32")
        label.grid(row=0,padx=5,pady=30)

        play_btn=tk.Button(self.select_file_window,text="Select en.json file", command=self.openBrowser_EN)
        play_btn.grid(row=1,padx=5,pady=5,sticky='we')

        choose_calc=tk.Button(self.select_file_window,text="Select alt.json file",command=self.openBrowser_ALT)
        choose_calc.grid(row=2,padx=5,pady=5,sticky='we')

        ex_btn=tk.Button(self.select_file_window,text="Finished",pady=2, command=self.finishedUploading)
        ex_btn.grid(row=4,padx=5,pady=5,sticky='we')

        self.select_file_window.mainloop()

    def reload_files(self):
        if self.file_missing==False:
            self.dict_EN = easyFunc.generateDict(self.dict_EN_path)
            self.dict_ALT = easyFunc.generateDict(self.dict_ALT_path)
            self.autosearch()
            self.changeStatus("Reloaded files")
        else:
            self.changeStatus("Please load files first")

    def load_current_dir(self):
        path=os.getcwd()
        self.dict_EN_path=''
        self.dict_ALT_path=''
        files=[]
        for r,d,f in os.walk(path):
            for file in f:
                if '.json' == file[-5:] and r == path: #.json = 5 chars
                    if 'en.json'== file:
                        self.dict_EN_path=os.path.join(r,file)
                    else:
                        files.append(os.path.join(r,file))

        if self.dict_EN_path=='' or files==[]:
            self.changeStatus("Failed to load from current dir, check filenames")
        else:
            self.file_missing=False
            self.dict_ALT_path=files[0]
            self.reload_files()

            self.changeStatus("Successfully loaded files from current dir")






    def finishedUploading(self):
        if (self.dict_EN!=None) and (self.dict_ALT!=None):
            self.file_missing=False
            self.changeStatus("Files loaded, ready to search")

        self.select_file_window.destroy()


    def openBrowser_EN(self):
        self.dict_EN_path = tk.filedialog.askopenfilename(title="Choose en.json file",filetypes=[("javascript file","*.json")])
        self.dict_EN = easyFunc.generateDict(self.dict_EN_path)
        self.select_file_window.attributes('-topmost',True)



    def openBrowser_ALT(self):
        self.dict_ALT_path = tk.filedialog.askopenfilename(title="Choose alt.json file",filetypes=[("javascript file","*.json")])
        self.dict_ALT = easyFunc.generateDict(self.dict_ALT_path)
        self.select_file_window.attributes('-topmost',True)


    def set_input_value(self,button_index):
        self.clear_input_fields()

        if self.reversed==False:
            self.visible_results_KEY.reverse()
            self.visible_results_EN.reverse()
            self.visible_results_ALT.reverse()
            self.reversed=True

        if len(self.visible_results_EN)<2 and (len(self.visible_results_ALT)<2) and len(self.visible_results_KEY)<2:
            button_index=0

        self.input_key_field.insert(0,self.visible_results_KEY[button_index]  )
        self.input_translation_EN_field.insert(0,self.visible_results_EN[button_index]  )
        self.input_translation_ALT_field.insert(0,self.visible_results_ALT[button_index]  )



    def clear_input_fields(self):
        self.input_key_field.delete(0,tk.END)
        self.input_translation_EN_field.delete(0,tk.END)
        self.input_translation_ALT_field.delete(0,tk.END)



    def autosearch(self):
        input_key_field=self.input_key_field.get()
        input_EN_field=self.input_translation_EN_field.get().lower()
        input_ALT_field=self.input_translation_ALT_field.get().lower()
        self.visible_results_KEY=[]
        self.visible_results_EN=[]
        self.visible_results_ALT=[]
        self.reversed=False

        if self.test==True:
            self.testing()
            self.test=False

        if (input_key_field!="" and input_EN_field=="" and input_ALT_field==""):  #KEYSEARCH
            self.search_dictionairy(self.dict_EN,self.dict_ALT, input_key_field,'KEY')

        elif input_key_field=="" and input_EN_field!="" and input_ALT_field =="": #EN SEARCH
            self.search_dictionairy(self.dict_EN,self.dict_ALT, input_EN_field,'EN')

        elif input_key_field=="" and input_EN_field=="" and input_ALT_field !="": #ALT
            self.search_dictionairy(self.dict_ALT,self.dict_EN,input_ALT_field,'ALT')
        else:
            self.search_dictionairy(self.dict_EN,self.dict_ALT, input_key_field,'KEY')


    def autosearch_no_status(self):
        input_key_field=self.input_key_field.get()
        input_EN_field=self.input_translation_EN_field.get().lower()
        input_ALT_field=self.input_translation_ALT_field.get().lower()
        self.visible_results_KEY=[]
        self.visible_results_EN=[]
        self.visible_results_ALT=[]
        self.reversed=False

        if self.test==True:
            self.testing()
            self.test=False

        if (input_key_field!="" and input_EN_field=="" and input_ALT_field==""):  #KEYSEARCH
            self.search_dictionairy_no_status(self.dict_EN,self.dict_ALT, input_key_field,'KEY')

        elif input_key_field=="" and input_EN_field!="" and input_ALT_field =="": #EN SEARCH
            self.search_dictionairy_no_status(self.dict_EN,self.dict_ALT, input_EN_field,'EN')

        elif input_key_field=="" and input_EN_field=="" and input_ALT_field !="": #ALT
            self.search_dictionairy_no_status(self.dict_ALT,self.dict_EN,input_ALT_field,'ALT')
        else:
            self.search_dictionairy_no_status(self.dict_EN,self.dict_ALT, input_key_field,'KEY')

    def search_dictionairy_no_status(self,dict_EN,dict_ALT,input_line,searchType):

        self.clear_text()
        currentVal_in_EN = input_line
        # currentVal_in_EN = input_translation_EN_field.get()
        # currentVal_in_ALT = input_translation_AL_field.get()

        search_results_EN=[]
        search_results_ALT=[]
        n_chars=len(currentVal_in_EN)
        ordered_search_EN=""

        for i in range(len(dict_EN.dict)):

            n_results_EN=len(search_results_EN)

            if n_results_EN>10:
                break
            else:
                if searchType=="KEY":
                    ordered_search_EN=dict_EN.dict[i].key[0:n_chars]

                else:
                    ordered_search_EN=dict_EN.dict[i].translation[0:n_chars].lower().replace("ë","e") #simpler albanian search

                if currentVal_in_EN == ordered_search_EN:
                    search_results_EN.append(i)

                    for t in range(len(dict_ALT.dict)):

                        if dict_EN.dict[i].key==dict_ALT.dict[t].key:
                            search_results_ALT.append(t)
                            break

        self.search_results_type=searchType

        for i in range(len(search_results_EN)):
            try:
                if searchType=="EN":
                    #self.changeStatus("Searching ENG values, ignoring capitalization")
                    self.add_Value1(f"{dict_EN.dict[search_results_EN[i]].translation}\n")
                    self.add_Value2(f"{dict_ALT.dict[search_results_ALT[i]].translation}\n")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_EN.dict[search_results_EN[i]].translation)
                    self.visible_results_ALT.append(dict_ALT.dict[search_results_ALT[i]].translation)

                elif searchType=="ALT":
                    #self.changeStatus("Searching AL values, ignoring capitalization") #EN IS ALLWAYS WHAT IS SEARCHED ON! ALT IS WHAT WE TRY TO MATCH AGAINST LOOK AT WHERE IT WRITES THE OUTPUT
                    self.add_Value2(f"{dict_EN.dict[search_results_EN[i]].translation}\n")
                    self.add_Value1(f"{dict_ALT.dict[search_results_ALT[i]].translation}\n")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_ALT.dict[search_results_ALT[i]].translation)
                    self.visible_results_ALT.append(dict_EN.dict[search_results_EN[i]].translation)

                elif searchType=="KEY":
                    #self.changeStatus("Searching KEY values, capitalization matters")
                    self.add_Value1(f"{dict_EN.dict[search_results_EN[i]]}")
                    self.add_Value2(f"{dict_ALT.dict[search_results_ALT[i]]}")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_EN.dict[search_results_EN[i]].translation)
                    self.visible_results_ALT.append(dict_ALT.dict[search_results_ALT[i]].translation)
            except:
                pass

    def search_dictionairy(self,dict_EN,dict_ALT,input_line,searchType):

        self.clear_text()
        currentVal_in_EN = input_line
        # currentVal_in_EN = input_translation_EN_field.get()
        # currentVal_in_ALT = input_translation_AL_field.get()

        search_results_EN=[]
        search_results_ALT=[]
        n_chars=len(currentVal_in_EN)
        ordered_search_EN=""

        for i in range(len(dict_EN.dict)):

            n_results_EN=len(search_results_EN)

            if n_results_EN>10:
                break
            else:
                if searchType=="KEY":
                    ordered_search_EN=dict_EN.dict[i].key[0:n_chars]

                else:
                    ordered_search_EN=dict_EN.dict[i].translation[0:n_chars].lower().replace("ë","e") #simpler albanian search

                if currentVal_in_EN == ordered_search_EN:
                    search_results_EN.append(i)

                    for t in range(len(dict_ALT.dict)):

                        if dict_EN.dict[i].key==dict_ALT.dict[t].key:
                            search_results_ALT.append(t)
                            break

        self.search_results_type=searchType

        for i in range(len(search_results_EN)):
            try:
                if searchType=="EN":
                    self.changeStatus("Searching ENG values, ignoring capitalization")
                    self.add_Value1(f"{dict_EN.dict[search_results_EN[i]].translation}\n")
                    self.add_Value2(f"{dict_ALT.dict[search_results_ALT[i]].translation}\n")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_EN.dict[search_results_EN[i]].translation)
                    self.visible_results_ALT.append(dict_ALT.dict[search_results_ALT[i]].translation)

                elif searchType=="ALT":
                    self.changeStatus("Searching AL values, ignoring capitalization") #EN IS ALLWAYS WHAT IS SEARCHED ON! ALT IS WHAT WE TRY TO MATCH AGAINST LOOK AT WHERE IT WRITES THE OUTPUT
                    self.add_Value2(f"{dict_EN.dict[search_results_EN[i]].translation}\n")
                    self.add_Value1(f"{dict_ALT.dict[search_results_ALT[i]].translation}\n")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_ALT.dict[search_results_ALT[i]].translation)
                    self.visible_results_ALT.append(dict_EN.dict[search_results_EN[i]].translation)

                elif searchType=="KEY":
                    self.changeStatus("Searching KEY values, capitalization matters")
                    self.add_Value1(f"{dict_EN.dict[search_results_EN[i]]}")
                    self.add_Value2(f"{dict_ALT.dict[search_results_ALT[i]]}")

                    self.visible_results_KEY.append(dict_EN.dict[search_results_EN[i]].key)
                    self.visible_results_EN.append(dict_EN.dict[search_results_EN[i]].translation)
                    self.visible_results_ALT.append(dict_ALT.dict[search_results_ALT[i]].translation)
            except:
                pass


    def testing(self):
        self.dict_EN_path = ''#INSERT PATH
        self.dict_EN = easyFunc.generateDict(self.dict_EN_path)
        self.dict_ALT_path = '' #INSERT PATH
        self.dict_ALT = easyFunc.generateDict(self.dict_ALT_path)
        self.file_missing=False



    def overwrite_value(self,rewrite=False):
        self.autosearch()
        input_key_field=self.input_key_field.get()

        if rewrite==False:
            input_EN_field=self.input_translation_EN_field.get()
            input_ALT_field=self.input_translation_ALT_field.get()

        elif rewrite==True:

            input_EN_field=self.Last_deleted_EN.translation
            input_ALT_field=self.Last_deleted_ALT.translation

        # print(input_EN_field)
        # print(input_ALT_field)

        if input_EN_field!="" and input_ALT_field!="" and input_key_field!="":
            #search for the key
            #delete it in both langs
            #add existing values

            for i in range(len(self.dict_EN.dict)):
                if input_key_field==self.dict_EN.dict[i].key:
                    self.Last_deleted_EN=self.dict_EN.dict.pop(i)
                    break

            for i in range(len(self.dict_ALT.dict)):
                if input_key_field==self.dict_ALT.dict[i].key:
                    self.Last_deleted_ALT=self.dict_ALT.dict.pop(i)
                    break



            word_object_EN=easyFunc.TranslationValue(input_key_field,input_EN_field)
            word_object_ALT=easyFunc.TranslationValue(input_key_field,input_ALT_field)

            self.dict_EN.dict.append(word_object_EN)
            self.dict_ALT.dict.append(word_object_ALT)
            # print(self.dict_EN.dict[-1])
            # print(self.dict_ALT.dict[-1])
            #self.changed_lists="REMOVED"\
            self.changed_lists="OVERWRITE"


            self.autosearch() #update

            self.changeStatus(f"Overwritten the KEY {input_key_field}")

        else:
            self.changeStatus(f"Missing input")

        self.autosearch()


    def add_new_value(self):
        self.autosearch()
        input_key_field=self.input_key_field.get()
        input_EN_field=self.input_translation_EN_field.get()
        input_ALT_field=self.input_translation_ALT_field.get()

        #print(self.resolve_index)

        #print(self.changed_lists)
        #print("----->"+self.textDisplay1.get(0.0,10.0)+"<-----")
        if ((self.textDisplay1.get(0.0,10.0)=="\n" and self.textDisplay2.get(0.0,10.0)=="\n") or self.resolve_state==True):


            if input_EN_field!="" and input_ALT_field!="" and input_key_field!="":
                if self.resolve_state==True:
                    self.delete_word()

                word_object_EN=easyFunc.TranslationValue(input_key_field,input_EN_field)
                word_object_ALT=easyFunc.TranslationValue(input_key_field,input_ALT_field)

                self.dict_EN.dict.append(word_object_EN)
                self.dict_ALT.dict.append(word_object_ALT)
                # print(self.dict_EN.dict[-1])
                # print(self.dict_ALT.dict[-1])

                self.autosearch() #update

                if self.resolve_state==True:
                    self.wait=False
                    self.clear_input_fields()
                    self.resolve_missing_keys()

                self.changed_lists="ADDED"
                self.changeStatus(f"Added the KEY {input_key_field}")

            else:
                self.changeStatus(f"Missing input")


    def undo_last_change(self):
        # print(self.changed_lists)
        if self.changed_lists =="ADDED":
            self.Last_deleted_EN=self.dict_EN.dict.pop(-1)
            self.Last_deleted_ALT=self.dict_ALT.dict.pop(-1)
            self.autosearch()
            self.changed_lists="REMOVED"

            self.changeStatus(f"REMOVED the key {self.Last_deleted_EN.key}")

        elif self.changed_lists=="REMOVED":
            self.dict_EN.dict.append(self.Last_deleted_EN)
            self.dict_ALT.dict.append(self.Last_deleted_ALT)
            self.autosearch()
            self.Last_deleted_EN=None
            self.Last_deleted_ALT=None
            self.changed_lists="ADDED"

            self.changeStatus(f"ADDED back the KEY {self.dict_EN.dict[-1].key}")


        elif self.changed_lists=="IGNORE":
            #print('I GOT TOOOOOOOOOO HERE')
            self.ignore(True)

        elif self.changed_lists=="OVERWRITE":
            # print("INSIDE OVERWRITE")
            self.overwrite_value(True)
            self.changed_lists=f"Reversed overwrite of {self.dict_EN.dict[-1].key}"


    def delete_word(self):
        input_key_field=self.input_key_field.get()
        if input_key_field!="":

            for i in range(len(self.dict_EN.dict)):
                if input_key_field==self.dict_EN.dict[i].key:
                    self.Last_deleted_EN=self.dict_EN.dict.pop(i)
                    break

            for i in range(len(self.dict_ALT.dict)):
                if input_key_field==self.dict_ALT.dict[i].key:
                    self.Last_deleted_ALT=self.dict_ALT.dict.pop(i)
                    break

            if self.Last_deleted_EN!=None or self.Last_deleted_ALT!=None:
                self.changeStatus(f"Deleted the values with KEY: {self.Last_deleted_EN.key}")
                self.changed_lists="REMOVED"
                self.autosearch()

            else:
                self.dict_EN.dict.append(self.Last_deleted_EN)
                self.dict_ALT.dict.append(self.Last_deleted_ALT)
                self.changeStatus(f"Deletetion Failed or nothing to delete")
                # print("Deletetion Failed or nothing to delete")

            if self.resolve_state==True:
                self.resolve_missing_keys()

        else:
            self.changeStatus("Finished deletion, nothing to delete")




    def checkKeyMismatch(self):

        if self.file_missing==False and self.resolve_state==False:
            result_EN=None
            result_ALT=None
            self.dict_EN.regen_keylist()
            self.dict_ALT.regen_keylist()
            result_EN, result_ALT = easyFunc.keymissmatch_check(self.dict_EN,self.dict_ALT)

            if result_EN==None and result_ALT==None:
                self.changeStatus("Compared files, no missmatch found")

            elif result_EN!=None and result_ALT!=None:
                self.changeStatus(f"Compared files, found {len(result_EN)+len(result_ALT)} missmatches, please reslove")
                self.resolve_missing_keys()
            else:
                self.changeStatus(f"Something went wrong")


        elif self.resolve_state==True: #Set ignore at buttonpress
            self.ignore()
            self.changed_lists="IGNORE"
            self.resolve_missing_keys()

        elif self.file_missing==True:
            self.changeStatus(f"Please choose files first")

        else:
            self.changeStatus(f"Something is wrong")


    def ignore(self,undo=False):
        input_key_field=self.input_key_field.get()
        input_EN_field=self.input_translation_EN_field.get()
        input_ALT_field=self.input_translation_ALT_field.get()

        if undo==True:
            input_key_field=self.last_ingored_key.key

        self.changed_lists="IGNORE"

        for i in range(len(self.dict_EN.dict)):
            if input_key_field==self.dict_EN.dict[i].key:
                self.dict_EN.dict[i].ignore=self.dict_EN.dict[i].ignore!=True
                self.last_ingored_key=self.dict_EN.dict[i]
                # print(self.dict_EN.dict[i].ignore,self.last_ingored_key.ignore)

        for i in range(len(self.dict_ALT.dict)):
            if input_key_field==self.dict_ALT.dict[i].key:
                self.dict_ALT.dict[i].ignore=self.dict_ALT.dict[i].ignore!=True
                self.last_ingored_key=self.dict_ALT.dict[i]
                # print(self.dict_ALT.dict[i].ignore,self.last_ingored_key.ignore)

        if self.last_ingored_key.ignore==True:
            self.changeStatus(f"Ignoring the KEY {self.last_ingored_key.key}")
        elif self.last_ingored_key.ignore==False:
            self.changeStatus(f"Not ignoring the KEY {self.last_ingored_key.key}")



    def resolve_missing_keys(self):
        self.clear_input_fields()
        self.dict_EN.regen_keylist()
        self.dict_ALT.regen_keylist()
        result_EN, result_ALT = easyFunc.keymissmatch_check(self.dict_EN,self.dict_ALT)
        n_checkresults=0

        # for i in range(len(result_EN)):
        #     print(result_EN[i])
        # for i in range(len(result_ALT)):
        #     print(result_ALT[i])

        # print(len(result_ALT)+len(result_EN))


        if len(result_EN)>=1:
            n_checkresults=len(result_EN)
            checkresults_list=result_EN
            checklang="EN"
            self.resolve_state=True
        elif len(result_ALT)>=1:
            n_checkresults=len(result_ALT)
            checkresults_list=result_ALT
            checklang="ALT"
            self.resolve_state=True
        else:
            self.changeStatus("Finished, no missing KEYS found")
            self.resolve_state=False

        if n_checkresults>0 and self.wait==False and self.resolve_state==True:
                self.input_key_field.insert(0,checkresults_list[0].key)

                if checklang=="EN":
                    #print(checkresults_list)
                    self.input_translation_EN_field.insert(0,checkresults_list[0].translation)
                elif checklang=="ALT":
                    self.input_translation_ALT_field.insert(0,checkresults_list[0].translation)


                self.changeStatus(f"Waiting!  Please correct values for this KEY, {n_checkresults} remaining. Press 'CHECK FILES MISSMATCH' to skip this value")
                self.resolve_state=True



        elif self.resolve_state==False:
            self.changeStatus("Finished resolve, or no missing KEYS found")
        else:
            self.changeStatus("Something went wrong")
        self.autosearch_no_status()
        #self.autosearch()

    def save_to_subfolder(self):
        folder_path=self.dict_EN_path[0:-8]
        en_name=self.dict_EN_path[-7:]
        alt_name=self.dict_ALT_path[-7:]
        path_en=f"{folder_path}/easyKey/{en_name}"
        path_alt=f"{folder_path}/easyKey/{alt_name}"

        if ("easyKey" in self.dict_EN_path) or self.overwrite_files==True:
            path_en = self.dict_EN_path
            path_alt = self.dict_ALT_path


        # print(folder_path)
        # print(path_en)
        # print(path_alt)

        os.makedirs(os.path.dirname(path_en), exist_ok=True)
        write_en = open(path_en, "w")


        write_en.write("{\n")

        for i in range(len(self.dict_EN.skipped_lines)):
            #print(self.dict_EN.skipped_lines)
            write_en.write(self.dict_EN.skipped_lines[i])

        for i in range(len(self.dict_EN.dict)-1):
            write_en.write(f'  "{self.dict_EN.dict[i].key}": "{self.dict_EN.dict[i].translation}",\n')

        write_en.write(f'  "{self.dict_EN.dict[-1].key}": "{self.dict_EN.dict[-1].translation}"\n')
        write_en.write("}\n")


        write_en.close()


        os.makedirs(os.path.dirname(path_alt), exist_ok=True)
        write_alt = open(path_alt, "w")


        write_alt.write("{\n")

        for i in range(len(self.dict_ALT.skipped_lines)):
            #print(self.dict_EN.skipped_lines)
            write_alt.write(self.dict_ALT.skipped_lines[i])

        for i in range(len(self.dict_ALT.dict)-1):
            write_alt.write(f'  "{self.dict_ALT.dict[i].key}": "{self.dict_ALT.dict[i].translation}",\n')

        write_alt.write(f'  "{self.dict_ALT.dict[-1].key}": "{self.dict_ALT.dict[-1].translation}"\n')
        write_alt.write("}\n")


        write_alt.close()

        self.changeStatus(f"Finished wrinting to path:{folder_path}/easyKey")



if __name__ == "__main__":
    gui=GUI_easyKey()
    gui.window.mainloop()

