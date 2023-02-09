from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time, random, os, pygame
from mutagen.mp3 import MP3

# Définition de l'interface du MP

MP = tk.Tk()
MP.geometry("650x500")
MP.title("Player Music")

# Initialisation de pygame et son module mixer permettant la lecture d'audios
pygame.init()
pygame.mixer.init()

## Définition de mes fonctions

# Ajouter l'ensemble des fichiers d'un dossier
def add_songs():
    # invitation à ajouter un fichier de type ".mp3"
    musics = filedialog.askopenfilenames(title="Choisir un morceau", filetypes=(("mp3 Files", "*.mp3"), ))
    
    # Boucle pour ajouter à la playlist les morceaux sélectionné à la suite et leur retirer le chemin absolu
    for music in musics:
        music = os.path.split(music)[1]
        
        # Ajouter à la file, dans la playlist
        playlist.insert(END, music)

# Lire le ficher selectionné et afficher le titre
def play():
    # Reset la barre de lecture 
    lecture.config(value=0)
    time_label.config(text="")
    # Determiné l'état initial de la fonction play (stop_state) pour pouvoir lancer de nouveau la barre de lecture en lisant un nouvant titre
    global stop_state
    stop_state = False
    # cibler le titre séléctionné
    music = playlist.get(tk.ANCHOR)

    # chemin d'accès du fichier à lire (le modifier si code exécuté ou testé sur une autre machine que la mienne)
    music = f'musique/{music}'

    try:
        # charger le titre selectionné
        pygame.mixer.music.load(music)

        # et le lire
        pygame.mixer.music.play(loops=0)

        # substituer le nom du fichier de sont chemin absolu
        titre = os.path.split(music)[1]
        # Clear le label titre
        titre_label.config(text="")
        # afficher le titre lu dans le label titre
        titre_label.config(text=titre)

    # Si pas de titre selectionné, afficher message warning
    except:
        messagebox.showwarning(title="Attention", message="Selectionner un titre avant de cliquer sur Play.")
    
    play_time()

# Jouer la piste suivante
def next():
    # Reset la barre de lecture 
    lecture.config(value=0)
    time_label.config(text="")

    # Determiner le titre actuellement séléctionné
    cur_one = playlist.curselection()
    # L'incrémenter d'1 pour avoir le morceau suivant
    next_one = cur_one[0]+1
    # Sélectionner le morceau incrémenté
    music = playlist.get(next_one)
    music = f'musique/{music}'
    
    # s'il y a un morceau qui suit le morceau actuel, excecute les tâches suivantes
    try:
        # Jouer le morceau incrémenté
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loops=0)
        titre = os.path.split(music)[1]
        titre_label.config(text="")
        titre_label.config(text=titre)

        # Actualisé la barre de séléction
        playlist.select_clear(0, END)
        playlist.activate(next_one)
        playlist.selection_set(next_one, last=None)
    
    # sinon stop la lecture de la playlist
    except:
        stop()

def prev():
    # Reset la barre de lecture 
    lecture.config(value=0)
    time_label.config(text="")
    # Determiner le titre actuellement séléctionné
    cur_one = playlist.curselection()
    # Le décrémenter d'1 pour avoir le morceau qui précède
    prev_one = cur_one[0]-1
    # Sélectionner le morceau décrémenté
    music = playlist.get(prev_one)
    music = f'musique/{music}'
    
    # s'il y a un morceau qui précéde, excecute les tâches suivantes 
    try:
        # Jouer le morceau décrémenté
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loops=0)
        # MAJ du titre actuellement joué dans le Label dédié
        titre = os.path.split(music)[1]
        titre_label.config(text="")
        titre_label.config(text=titre)

        # Actualisé la barre de séléction
        playlist.select_clear(0, END)
        playlist.activate(prev_one)
        playlist.selection_set(prev_one, last=None)
    
    # sinon rejoue le morceau actuel du début
    except:
        play()
# Variable globale pour l'état de pause
global pause_state
pause_state = False
# Mettre la lecture sur pause
def pause():
    global pause_state
    # Si l'état pause actif/activé, la lecture passe sur pause et son état est désactivé (False)
    if pause_state:
        pygame.mixer.music.unpause()
        pause_state = False
    # Si l'état pause inactif/désactivé, la lecture reprend et son état est activé (True)
    else:
        pygame.mixer.music.pause()
        pause_state = True

# Stopper la lecture
global stop_state
stop_state = False
def stop():
    # Reset la barre de lecture 
    lecture.config(value=0)
    time_label.config(text="")
    # Arreter la lecture
    pygame.mixer.music.stop()
    playlist.select_clear(ACTIVE)
    # Reset l'affichage
    titre_label.config(text="")
    time_label.config(text="00:00 of 00:00")

    # variable stop
    global stop_state
    stop_state = True

# Supprimer le fichier séléctionné depuis la playlist
def delete():
    stop()
    playlist.delete(tk.ACTIVE)
# Supprimer tout les fichiers de la playlist
def del_all():
    stop()
    playlist.delete(0, END)

# Définir le volume en fonction de la position du slider (x en paramètre par défaut, car un argument est nécéssaire à la fonction slide)
def volume(x):
    pygame.mixer.music.set_volume(slider.get())

def pos_lecture(x):
    #time_label.config(text=f'{int(lecture.get())} of {int(music_len)}')
    music = playlist.get(tk.ACTIVE)
    music = f'musique/{music}'
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(loops=0, start=int(lecture.get()))

# fonction pour convertir les info audio en format lisible
def play_time():
    # si l'action stop est avérée, on ignore l'execution de cette fonction
    if stop_state:
        return
    
    cur_time = pygame.mixer.music.get_pos() / 1000
    # convertir le tps de lecture actuel sous format minutes:secondes
    conv_cur_time = time.strftime("%M:%S", time.gmtime(cur_time))
    # Determiner le titre actuellement séléctionné
    music = playlist.get(ACTIVE)

    music = f'musique/{music}'
    # Charger le morceau avec Mutagen
    music_mut = MP3(music)
    # Récupérer la durée totale du morceau
    global music_len
    music_len = music_mut.info.length
    # Convertir la durée totale du morceau sous format minutes:secondes
    conv_musc_len = time.strftime("%M:%S", time.gmtime(music_len))

    # Incrémenter le temps de lecture actuel par 1
    cur_time += 1

    # si le tps de lecture = durée totale du morcean alors la fonction morceau suivant est appelée
    if int(lecture.get()) == int(music_len):
        time_label.config(text=f'{conv_musc_len} of {conv_musc_len}')
        # si loop on et random on j'ai décidé de prioriser l'action de loop sur le random, celà me parait plus cohérent dans ce sens là
        if loop_state and random_state:
            play()
        elif loop_state:
            play()
        elif random_state:
            random_play()
        else:
            next()
       
    # sinon si l'état pause est avéré, rien ne se passe 
    elif pause_state:
        pass

    elif int(lecture.get()) == int(cur_time):
        # MAJ barre de lecture
        lect_pos = int(music_len)
        lecture.config(to=lect_pos, value=int(cur_time))
        
    else:
        # MAJ barre de lecture
        lect_pos = int(music_len)
        lecture.config(to=lect_pos, value=int(lecture.get()))

        conv_cur_time = time.strftime("%M:%S", time.gmtime(int(lecture.get())))

        time_label.config(text=f'{conv_cur_time} of {conv_musc_len}')

        n_time = int(lecture.get()) + 1
        lecture.config(value=n_time)

    time_label.after(1000, play_time)

# Déterminer l'état du mode loop (lecture en boucle)
global loop_state
loop_state = False
def loop():
    # Etat initialement inactif
    global loop_state
    # passe d'inactif à actif si fonction executée via la commande/bouton loop
    if loop_state == False:
        loop_state = True
        # MAJ du label dédié
        loop_label.config(text="loops on", foreground="green")
        # print("loops on")
    # passe d'actif à inactif si fonction executée via la commande/bouton loop
    else:
        loop_state = False
        # MAJ du label dédié
        loop_label.config(text="loops off", foreground="red")
        # print("loops off")

# Déterminer l'état du mode random (lecture aléatoire)
global random_state
random_state = False
def random_():
    global random_state
    # passe d'inactif à actif si fonction executée via la commande/bouton loop
    if random_state == False:
        random_state = True
        # MAJ du label dédié
        random_label.config(text="random on", foreground="green")
    # passe d'actif à inactif si fonction executée via la commande/bouton loop
    else:
        random_state = False
        # MAJ du label dédié
        random_label.config(text="random off", foreground="red")

# Jouer morceaux de la playlist de manière aléatoire
def random_play():
    # Reset la barre de lecture 
    lecture.config(value=0)
    time_label.config(text="")

    # récupérer les titres présents dans la playlist
    music = playlist.get(0, END)
    # en choirir un au hasard
    rand_music = random.choice(music)
    # Determiner l'index de notre titre random
    r_index = music.index(rand_music)

    # chemin d'accès du fichier à lire (le modifier si code exécuté ou testé sur une autre machine que la mienne)
    rand_music = f'musique/{rand_music}'

    # charger le titre random
    pygame.mixer.music.load(rand_music)
    # et le lire
    pygame.mixer.music.play(loops=0)   

    # substituer le nom du fichier de sont chemin absolu
    titre = os.path.split(rand_music)[1]
    # Clear le label titre
    titre_label.config(text="")
    # afficher le titre lu dans le label titre
    titre_label.config(text=titre)
   
    # Actualisé la barre de séléction
    playlist.select_clear(0, END)
    playlist.activate(r_index)
    playlist.selection_set(r_index, last=None)


## Création du menu
menu = Menu(MP)
MP.config(menu=menu)

# Ajouter le menu d'ajout de pistes
add_menu = Menu(menu)
menu.add_cascade(label="Add Songs", menu=add_menu)
# Ajouter une piste au menu
add_menu.add_command(label="Ajouter un/des morceaux", command=add_songs)

# Supprimer morceaux
remove_menu = Menu(menu)
menu.add_cascade(label="Supprimer morceaux", menu=remove_menu)
remove_menu.add_command(label="Supprimer un morceau de la playlist", command=delete)
remove_menu.add_command(label="Supprimer la playlist", command=del_all)

## Définition de la playlist
playlist_frame = ttk.LabelFrame(MP, text="Playlist")
playlist_frame.pack(ipady=10)
playlist = tk.Listbox(playlist_frame, width=60, background="black", fg='white', borderwidth=30)
playlist.grid(row=0, column=1)
music_title = tk.StringVar()
# Création de la barre déroulante de la playlist
scrollbar = ttk.Scrollbar(playlist_frame, orient="vertical", command=playlist.yview)
scrollbar.grid(row=0, column=2, sticky=NS)
playlist.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=playlist.yview)
# affichage volume
volume_frame = ttk.LabelFrame(playlist_frame, text='Volume')
volume_frame.grid(row=0, column=0)
# Slider pour manipuler le volume sonore
current_value = tk.DoubleVar()
slider = ttk.Scale(volume_frame, from_=1, to=0, orient='vertical', variable=current_value, command=volume)
slider.pack()
# Position de la lecture
lecture = ttk.Scale(playlist_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=pos_lecture, length=350)
lecture.grid(row=1, column=1)

# Définition Label durée
time_label = ttk.Label(playlist_frame, text="00:00 of 00:00", border=1)
time_label.grid(row=2, column=1)

# Définition Label affichant le titre joué
titre_label = ttk.Label(MP, text="", foreground="blue", font=("comicsans",25), anchor="center")
titre_label.pack()

# affichage boutons de commandes
commands_frame = ttk.Labelframe(MP, text="commandes")
commands_frame.pack()
play_btn = Button(commands_frame, text="Play", command=play, borderwidth=10).grid(row=0, column=1, padx=10, pady=10)
pause_btn = Button(commands_frame, text="Pause", command=pause, borderwidth=10).grid(row=0, column=2, padx=10, pady=10)
previous_btn = Button(commands_frame, text="<", command=prev, borderwidth=10).grid(row=0, column=0, padx=40, pady=10)
next_btn = Button(commands_frame, text=">", command=next, borderwidth=10).grid(row=0, column=4, padx=40, pady=10)
stop_btn = Button(commands_frame, text="Stop", command=stop, borderwidth=10).grid(row=0, column=3, padx=10, pady=10)
random_btn = Button(commands_frame, text="random", command=random_, borderwidth=10).grid(row=1, column=1, padx=10, pady=10)
loop_btn = Button(commands_frame, text="loop", command=loop, borderwidth=10).grid(row=1, column=3, padx=10, pady=10)

# Labels état du loop 
loop_label = ttk.Label(commands_frame, text="loops off", foreground="red" )
loop_label.grid(row=1, column=4, padx=10, pady=10)
# Labels état du random 
random_label = ttk.Label(commands_frame, text="random off", foreground="red")
random_label.grid(row=1, column=0, padx=10, pady=10)


MP.mainloop()