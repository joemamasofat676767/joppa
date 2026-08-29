import tkinter as tk
from pathlib import Path
from json import load

KNOWLEDGE_PATH = Path(__file__).parent.parent/"main"/"knowledge.json"

with open(KNOWLEDGE_PATH, "r") as knowledge:
	knowledge = [word[1] for word in load(knowledge).values()]

window = tk.Tk()
window.geometry("400x400")
window.configure(bg="#505050")
canvas = tk.Canvas(window, width=400, height=400, bg="#ededed")

knowledge2 = knowledge.copy()
for embedding in knowledge:
	x, y, z = embedding
	x, y, z = (x+2.5)*225, (y+2.5)*225, (z+3)*2
	knowledge2.remove(embedding)
	for other in knowledge2:
		x2, y2, z2 = other
		x2, y2, z2 = (x2+2.5)*225, (y2+2.5)*225, (z2+3)*2
		canvas.create_line(x, y, x2, y2, fill="lightgray", width=1, dash=(1,2))

for i in range(len(knowledge)):
	x, y, z = knowledge[i]
	x, y, z = (x+2.5)*225, (y+2.5)*225, (z+3)*2
	canvas.create_oval(int(x-z),int(y-z),int(x+z),int(y+z),fill="#c2c2c2", outline="")

canvas.pack(fill="both", expand=True, padx=20, pady=20)
tk.mainloop()
