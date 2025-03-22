import customtkinter
import numpy as np

BLUE = "#1f6aa5"

layerNum = 0
voxelPos = np.zeros((8, 8, 8))

button_dict = {}

customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("blue")

import customtkinter as ctk

def on_button_click(row, col):
    if button_dict[f"button_{row}_{col}"].cget("text") == "off":
        button_dict[f"button_{row}_{col}"].configure(text = "on")
        button_dict[f"button_{row}_{col}"].configure(fg_color=BLUE)
        voxelPos[layerNum][7-row][col] = 1
    else:
        button_dict[f"button_{row}_{col}"].configure(text = "off")
        button_dict[f"button_{row}_{col}"].configure(fg_color="transparent")
        voxelPos[layerNum][7-row][col] = 0

def create_8x8_grid(root):
    for row in range(8):
        for col in range(8):
            button_id = f"button_{row}_{col}"

            button = ctk.CTkButton(root, text="off", width=100, height=40, fg_color="transparent", border_color="blue",
                                   command=lambda r=row, c=col: on_button_click(r, c))
            button.grid(row=row+1, column=col, padx=5, pady=5)

            button_dict[button_id] = button

def renderGrid():
    for row in range(8):
        for col in range(8):
            if voxelPos[layerNum][7-row][col] == 1:
                button_dict[f"button_{row}_{col}"].configure(text="on")
                button_dict[f"button_{row}_{col}"].configure(fg_color=BLUE)
            else:
                button_dict[f"button_{row}_{col}"].configure(text="off")
                button_dict[f"button_{row}_{col}"].configure(fg_color="transparent")

def create():
    top = "#include <SPI.h>\n\n"

    listFromNp = voxelPos.tolist()
    list_str = str(listFromNp).replace('[', '{').replace(']', '}').replace('.0', '')
    voxelString = f"uint voxelPosition[8][8][8] = {list_str};\n\n"

    file = open("./template/template.ino", "r")
    template = file.read()
    file.close()

    file = open("./output/pattern.ino", 'w')
    file.write(top + voxelString + template)
    file.close()



def main():

    def prev():
        global layerNum
        if layerNum == 0:
            layerNum=7
        else:
            layerNum = layerNum - 1
        layer.configure(text=f"Layer {layerNum}")
        renderGrid()

    def nextL():
        global layerNum
        if layerNum == 7:
            layerNum = 0
        else:
            layerNum = layerNum + 1
        layer.configure(text=f"Layer {layerNum}") 
        renderGrid()       

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()

    root.title("Cube Editor")
    root.geometry("900x700") 

    layer = ctk.CTkLabel(root, width=100, height=40, text=f"Layer {layerNum}") 
    layer.grid(row=0, column=0, padx=5, pady=5)

    create_8x8_grid(root)

    empty_label = ctk.CTkLabel(root, text="")
    empty_label.grid(row=10, column=3)

    prev_button = ctk.CTkButton(root, text="Prev Layer", width=100, height=40, command=lambda: prev())
    prev_button.grid(row=11, column=3, padx=5, pady=5)

    next_button = ctk.CTkButton(root, text="Next Layer", width=100, height=40, command=lambda: nextL())
    next_button.grid(row=11, column=4, padx=5, pady=5)

    create_button = ctk.CTkButton(root, text="Create", width=100, height=40, command=lambda: create())
    create_button.grid(row=11, column=7, padx=5, pady=5)



    root.mainloop()

if __name__ == "__main__":
    main()
