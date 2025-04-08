import customtkinter as ctk
from customtkinter import filedialog
import numpy as np
from PIL import Image, ImageTk

BLUE = "#1f6aa5"

layerNum = 0
voxelPos = np.zeros((8, 8, 8))

button_dict = {}

ctk.set_appearance_mode("dark")
ctk.set_appearance_mode("blue")



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

def fill():
    global voxelPos
    voxelPos = np.ones((8,8,8))
    renderGrid()

def clear():
    global voxelPos
    voxelPos = np.zeros((8,8,8))
    renderGrid()

def create():
    top = "#include <SPI.h>\n\n"

    listFromNp = voxelPos.tolist()
    list_str = str(listFromNp).replace('[', '{').replace(']', '}').replace('.0', '')
    voxelString = f"int voxelPositions[8][8][8] = {list_str};\n\n"

    file = open("./template/template.ino", "r")
    template = file.read()
    file.close()

    file = open("./output/pattern.ino", 'w')
    file.write(top + voxelString + template)
    file.close()

def ImageGet():
    filePath = filedialog.askopenfilename( 
        title="Select an image file",
        filetypes=[("Image file", "*.jpg *png")]
    )

    if filePath:
        global voxelPos
        img = Image.open(filePath).convert("L")
        img = img.resize((8,8))
        imgData = np.array(img)
        a  = (imgData/255.0 * 7).astype(int)
        voxelPos = np.zeros((8,8,8))

        for layer in range(8):
            for row in range(8):
                for col in range(8):
                    if a[7-layer][col] < 5:
                        voxelPos[layer][7-row][col] = 1

        '''
        for row in range(8):
            for col in range (8):
                depth = a[row][col]
                for z in range(depth + 1):
                    voxelPos[z][7-row][col]=1
        '''
       
        renderGrid()
        #print(voxelPos)

        #print(filePath)

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

    fill_cube = ctk.CTkButton(root, text="Fill", width=100, height=40, command=lambda: fill())
    fill_cube.grid(row=11, column=0, padx=5, pady=5)

    clear_cube = ctk.CTkButton(root, text="Clear", width=100, height=40, command=lambda: clear())
    clear_cube.grid(row=11, column=1, padx=5, pady=5)

    import_image = ctk.CTkButton(root, text="Import Image", width = 100, height = 40, command=lambda:ImageGet())
    import_image.grid(row=12, column = 0, padx=4, pady = 4)

    root.mainloop()

if __name__ == "__main__":
    main()
