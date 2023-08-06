def launch():
	from audioplayer import AudioPlayer #used to play sound
	import tkinter as tkr #used to develop GUI
	from tkinter.filedialog import askdirectory #it permit to select dir
	import os #it permits to interact with the operating system
	music_player = tkr.Tk() 
	music_player.title("Life In Music") 
	music_player.geometry("800x600")
	directory = askdirectory()
	var = tkr.StringVar() 
	song_title = tkr.Label(music_player, font="Helvetica 12 bold", textvariable=var)
	os.chdir(directory) #it permits to chenge the current dir
	song_list = os.listdir() #it returns the list of files song

	play_list = tkr.Listbox(music_player, font="Helvetica 12 bold", bg="yellow", selectmode=tkr.SINGLE)
	pos = 0
	for item in song_list:
		if ".mp3" in item:
			play_list.insert(pos, item)
			pos += 1
		elif ".wav" in item:
			play_list.insert(pos,item)
			pos += 1
		elif ".ogg" in item:
			play_list.insert(pos,item)
			pos += 1
	def play():
		song = AudioPlayer(play_list.get(tkr.ACTIVE))
		var.set(play_list.get(tkr.ACTIVE))
		song.play()
	def stop():
	    song.stop()
	def pause():
	    song.pause()
	def unpause():
	    song.resume()
	Button1 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PLAY", command=play, bg="blue", fg="white")
	Button2 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="STOP", command=stop, bg="red", fg="white")
	Button3 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PAUSE", command=pause, bg="purple", fg="white")
	Button4 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="UNPAUSE", command=unpause, bg="orange", fg="white")
	song_title.pack()
	Button1.pack(fill="x")
	Button2.pack(fill="x")
	Button3.pack(fill="x")
	Button4.pack(fill="x")
	play_list.pack(fill="both", expand="yes")
	music_player.mainloop()
