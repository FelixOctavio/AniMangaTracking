import sqlite3
import os
import tkinter as tk
from tkinter import ttk

top = tk.Tk()

conn = sqlite3.connect('anime.db')
c = conn.cursor()

def print_func():
    l = c.fetchall()
    print(*l, sep='\n')
    conn.commit()
    conn.close()
    
def printone_func():
    l = c.fetchone()
    test = map(str, l)
    print(list(test))
    # conn.commit()
    # conn.close()

def pause():
    input("Press the ENTER key to continue...")
    
def layar_pilihan_update(inputpilihanupdate):
    c.execute("SELECT Anime FROM AnimeList WHERE AnimeID = %s" % (inputpilihanupdate))
    outputtitle = c.fetchone()
    for x in outputtitle:
        title = inputpilihanupdate + ".", x
        
    titleFrame(title).grid(column=0, row=0)
    updateEditFrame(inputpilihanupdate).grid(column=0, row=1)
    backButtonFrame(backUpdate).grid(column=0, row=3)
    
def titleFrame(title):
    TitleFrame.columnconfigure(0, weight=1)
    tk.Label(TitleFrame, text = title).grid(column=0, row=0)
                
    for widget in TitleFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return TitleFrame
            
def updateEditFrame(inputpilihanupdate): 
    UpdateEditFrame.columnconfigure(0, weight=1)
    UpdateEditFrame.columnconfigure(0, weight=3)
    
    header = ["Anime", "Release", "Genres", "Type", "Status", "Season", "LastCompleted", "EpisodeSelesai", "EpisodeTotal", "OVAselesai", "OVAtotal"]
    
    m=1
    
    for i in header:
        tk.Label(UpdateEditFrame, text = str(m) + ". " + i).grid(column=0, row=m, sticky='w')
        try:
            c.execute("SELECT %s FROM AnimeList WHERE AnimeID = %s" % (i, inputpilihanupdate))
        except sqlite3.Error as er:
            c.execute("SELECT %s FROM WatchedAnime WHERE AnimeID = %s" % (i, inputpilihanupdate))
        output = c.fetchone()
        for x in output:
            globals()[i.lower()+"Entry"] = tk.Entry(UpdateEditFrame)
            globals()[i.lower()+"Entry"].insert(tk.END, x)
            globals()[i.lower()+"Entry"].grid(column=1, row=m, sticky='w')
        
        m+=1
    
    enterButtonFrame(lambda: enterUpdateClean(animeEntry, releaseEntry, genresEntry, typeEntry, statusEntry, seasonEntry, lastcompletedEntry, episodeselesaiEntry, episodetotalEntry, ovaselesaiEntry, ovatotalEntry, inputpilihanupdate)).grid(column=0, row=11)
            
    for widget in UpdateEditFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return UpdateEditFrame
  
def insertEntry(Anime, Release, Genres, Type, Status, Season, LastCompleted, EpisodeSelesai, EpisodeTotal, OVAselesai, OVAtotal):
    c.execute("INSERT INTO AnimeList (Anime, Release, Genres, Type, Status, Season, EpisodeTotal, OVAtotal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)" , (Anime, Release, Genres, Type, Status, Season, EpisodeTotal, OVAtotal))
    #c.execute("INSERT INTO WatchedAnime (LastCompleted, EpisodeSelesai, OVAselesai) VALUES (?, ?, ?)" , (LastCompleted, EpisodeSelesai, OVAselesai))
    conn.commit()
    
def insertEntryButton():
    clear_frame()
    insertEntryFrame().grid(column=0, row=0)
    backButtonFrame(backMaraton).grid(column=0, row=1)
    
def insertEntryFrame(): 
    InsertEntryFrame.columnconfigure(0, weight=1)
    InsertEntryFrame.columnconfigure(0, weight=3)
    
    list = ["Anime", "Release", "Genres", "Type", "Status", "Season", "LastCompleted", "EpisodeSelesai", "EpisodeTotal", "OVAselesai", "OVAtotal"]
    
    k=1
    
    for i in list:
        tk.Label(InsertEntryFrame, text = str(k) + ". " + i).grid(column=0, row=k, sticky='w')
        globals()[i.lower()+"Entry"] = tk.Entry(InsertEntryFrame)
        globals()[i.lower()+"Entry"].grid(column=1, row=k, sticky='w')
        k+=1
    
    enterButtonFrame(lambda: enterInsertClean(animeEntry, releaseEntry, genresEntry, typeEntry, statusEntry, seasonEntry, lastcompletedEntry, episodeselesaiEntry, episodetotalEntry, ovaselesaiEntry, ovatotalEntry)).grid(column=0, row=11)
            
    for widget in InsertEntryFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return InsertEntryFrame
  
def watchedList():
    clear_frame()
    output = c.execute("SELECT a.Anime, a.Release, a.Type, a.Status, a.Season FROM AnimeList AS a, WatchedAnime AS w WHERE (w.AnimeID=a.AnimeID AND w.SeriesID=a.SeriesID) AND ((w.EpisodeSelesai=a.EpisodeTotal OR w.OVAselesai=a.OVAtotal) AND w.CompleteCount>=1)")
   
    gridFrame(output).grid(column=0, row=0)
    backButtonFrame(backMain).grid(column=1,row=0)
    conn.commit()
    
def updateNeverWatchList():
    clear_frame()
    output = c.execute("SELECT w.AnimeID, w.SeriesID, a.SpinOff, a.Anime, a.Release, a.Genres, a.Type, a.Status, a.Season, w.LastCompleted, w.EpisodeSelesai, a.EpisodeTotal, w.OVAselesai, a.OVAtotal FROM WatchedAnime AS w, AnimeList AS a WHERE (w.AnimeID=a.AnimeID AND w.SeriesID=a.SeriesID) AND ((w.EpisodeSelesai!=a.EpisodeTotal OR w.OVAselesai!=a.OVAtotal) AND w.CompleteCount=0) ORDER BY ((w.EpisodeSelesai) + (w.OVAselesai)) DESC")
    gridFrame(output).grid(column=0, row=0)
    updateGridFrame().grid(column=0, row=1)
    conn.commit()
    
def updateGridFrame():
    tk.Label(UpdateGridFrame, text = "Pilih anime yang ingin diubah: ").grid(column=0, row=0)
    entryupdate = tk.Entry(UpdateGridFrame)
    entryupdate.bind('<Return>',lambda entryupdate:enter(entryupdate)) # Masih Error
    entryupdate.grid(column=0, row=1)
    backButtonFrame(backMaraton).grid(column=0,row=2)
    
    Enter = tk.Button(UpdateGridFrame, text ="Enter", command=lambda: enter(entryupdate))
    Enter.grid(row=1, column=1)
    
    for widget in UpdateGridFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return UpdateGridFrame
    
def backMain():
    clear_frame()
    MainMenu = mainMenuFrame()
    MainMenu.grid(column=0, row=0)
    
def backMaraton():
    neverWatchList()
    
def backUpdate():
    updateNeverWatchList()
    
def enterUpdateClean(a, b, c, d, e, f, g, h, i ,j, k, l):
    Anime = a.get()
    Release = b.get()
    Genres = c.get()
    Type = d.get()
    Status= e.get()
    Season = f.get()
    LastCompleted = g.get()
    EpisodeSelesai = h.get()
    EpisodeTotal = i.get()
    OVAselesai = j.get()
    OVAtotal = k.get()
    AnimeID = l
    
    enterUpdate(Anime, Release, Genres, Type, Status, Season, LastCompleted, EpisodeSelesai, EpisodeTotal, OVAselesai, OVAtotal, AnimeID)
    
def enterInsertClean(a, b, c, d, e, f, g, h, i ,j, k):
    Anime = a.get()
    Release = b.get()
    Genres = c.get()
    Type = d.get()
    Status= e.get()
    Season = f.get()
    LastCompleted = g.get()
    EpisodeSelesai = h.get()
    EpisodeTotal = i.get()
    OVAselesai = j.get()
    OVAtotal = k.get()
    
    insertEntry(Anime, Release, Genres, Type, Status, Season, LastCompleted, EpisodeSelesai, EpisodeTotal, OVAselesai, OVAtotal)    
    
def enterUpdate(Anime, Release, Genres, Type, Status, Season, LastCompleted, EpisodeSelesai, EpisodeTotal, OVAselesai, OVAtotal, AnimeID):
    c.execute("UPDATE AnimeList SET Release = ?, Genres = ?, Type = ?, Status = ?, Season = ?, EpisodeTotal = ?, OVAtotal = ? WHERE AnimeID = ?" , (Release, Genres, Type, Status, Season, EpisodeTotal, OVAtotal, AnimeID))
    c.execute("UPDATE WatchedAnime SET LastCompleted = ?, EpisodeSelesai = ?, OVAselesai = ? WHERE AnimeID = ?" , (LastCompleted, EpisodeSelesai, OVAselesai, AnimeID))
    c.execute("SELECT a.Anime, a.Release, a.Type, a.Season, w.EpisodeSelesai, a.EpisodeTotal, w.OVAselesai, a.OVAtotal FROM WatchedAnime AS w, AnimeList AS a WHERE w.AnimeID = ? AND a.AnimeID = ?" , (AnimeID, AnimeID))
    printone_func()
    
def enter(entryupdate):
    inputpilihanupdate = entryupdate.get()
    clear_frame()
    layar_pilihan_update(inputpilihanupdate)
    
def neverWatchList():
    clear_frame()
    output = c.execute("SELECT a.Anime, a.Release, a.Type, a.Season, w.EpisodeSelesai, a.EpisodeTotal, w.OVAselesai, a.OVAtotal FROM AnimeList AS a, WatchedAnime AS w WHERE (w.AnimeID=a.AnimeID AND w.SeriesID=a.SeriesID) AND ((w.EpisodeSelesai!=a.EpisodeTotal OR w.OVAselesai!=a.OVAtotal) AND w.CompleteCount=0) ORDER BY ((w.EpisodeSelesai) + (w.OVAselesai)) DESC")
    gridFrame(output).grid(column=0, row=0)
    backButtonFrame(backMain).grid(column=0,row=1)
    updateButtonFrame().grid(column=0,row=2)
    addNewEntry().grid(column=0,row=3)
    conn.commit()

def gridFrame(output):
    TableGridFrame.columnconfigure(0, weight=4)
    
    i=0
    for j in output:
        for k in range(len(j)+1):
            e = tk.Entry(TableGridFrame, fg='black') 
            e.grid(row=i, column=k) 
            if k==0:
                e.insert(tk.END, i+1)
            else:
                e.insert(tk.END, j[k-1])
        i+=1
        
    for widget in TableGridFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return TableGridFrame
         
def updateButtonFrame():   
    UpdateButtonFrame.columnconfigure(0, weight=1)
    
    Update = tk.Button(UpdateButtonFrame, text ="Update DB", command = updateNeverWatchList)
    
    Update.grid(row=0, column=0)
    
    for widget in UpdateButtonFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return UpdateButtonFrame
    
def addNewEntry():
    AddNewEntry.columnconfigure(0, weight=1)
    
    AddNewEntryButton = tk.Button(AddNewEntry, text ="Add New Entry", command = insertEntryButton)
    
    AddNewEntryButton.grid(row=0, column=0)
    
    for widget in AddNewEntry.winfo_children():
        widget.grid(padx=0, pady=3)

    return AddNewEntry
    
def backButtonFrame(mode): 
    Back = tk.Button(BackButtonFrame, text ="Kembali", command = mode)
    
    Back.grid(row=0, column=0)
    
    for widget in BackButtonFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return BackButtonFrame
    
def enterButtonFrame(mode):   
    BackButtonFrame.columnconfigure(0, weight=1)
    
    Enter = tk.Button(BackButtonFrame, text ="Enter", command = mode)
    
    Enter.grid(row=0, column=1)
    
    for widget in BackButtonFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return BackButtonFrame
    
def mainMenuFrame():
    MainMenuFrame.columnconfigure(0, weight=1)
    
    Watched = tk.Button(MainMenuFrame, text ="List Sudah Nonton", command = watchedList).grid(column=0, row=0)
    Never = tk.Button(MainMenuFrame, text ="List Maraton", command = neverWatchList).grid(column=0, row=1)
    
    for widget in MainMenuFrame.winfo_children():
        widget.grid(padx=0, pady=3)

    return MainMenuFrame
    
def clear_frame():
    for widgets in MainMenuFrame.winfo_children():
       widgets.destroy()
    MainMenu.grid_forget()
    for widgets in BackButtonFrame.winfo_children():
       widgets.destroy()
    BackButtonFrame.grid_forget()
    for widgets in UpdateButtonFrame.winfo_children():
       widgets.destroy()
    UpdateButtonFrame.grid_forget()
    for widgets in TableGridFrame.winfo_children():
       widgets.destroy()
    TableGridFrame.grid_forget()
    for widgets in UpdateGridFrame.winfo_children():
       widgets.destroy()
    UpdateGridFrame.grid_forget()
    for widgets in TitleFrame.winfo_children():
       widgets.destroy()
    TitleFrame.grid_forget()
    for widgets in UpdateEditFrame.winfo_children():
       widgets.destroy()
    UpdateEditFrame.grid_forget()
    for widgets in AddNewEntry.winfo_children():
       widgets.destroy()
    AddNewEntry.grid_forget()
    for widgets in InsertEntryFrame.winfo_children():
       widgets.destroy()
    InsertEntryFrame.grid_forget()

MainMenuFrame = ttk.Frame(top)
BackButtonFrame = ttk.Frame(top)
UpdateButtonFrame = ttk.Frame(top)
TableGridFrame = ttk.Frame(top)
UpdateGridFrame = ttk.Frame(top)
InsertEntryFrame = ttk.Frame(top)
UpdateEditFrame = ttk.Frame(top)
TitleFrame = ttk.Frame(top)
AddNewEntry = ttk.Frame(top)

top.title("Anime and Manga List")

top.columnconfigure(0, weight=1)
    
MainMenu = mainMenuFrame()
MainMenu.grid(column=0, row=0)

top.mainloop()