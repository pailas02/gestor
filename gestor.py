import os
import tkinter as tk
import shutil
from NaryTree import NaryTree
from NaryTree import Archivo
from tkinter import ttk, filedialog, messagebox, simpledialog



class DirectoryExplorer:

    def __init__(self, master):
        self.master = master
        self.master.title("Explorador de Archivos")
        self.tree = NaryTree() #iniciacion del arbol binario
        self.current_path = os.getcwd() #obtiene la ruta en la que se encuentra

        self.path_var = tk.StringVar()
        self.path_var.set(self.current_path)
        
        self.path_copy = None  #la ruta que el usuario escoge para copiar
        self.is_copiar = False  #para saber si el usuario escogio copiar
        self.ruta_origen = None  #La ruta que el usuario escoge para cortar

        self.treeview = ttk.Treeview(self.master) #declara el arbol visual
        self.treeview.pack(fill=tk.BOTH, expand=True) 

        self.populate_treeview() #Metodo que llena simultanea y recursivamente el arbol binario y el visual
            

        self.treeview.bind('<<TreeviewOpen>>', self.on_open)
        self.treeview.bind('<Double-Button-1>', self.on_select)

        button_frame = tk.Frame(self.master)
        button_frame.pack()
        
        self.entry = tk.Entry(self.master)  #Input para buscar
        self.entry.place(relx=1, y=0, anchor="ne")  #lo coloca

        self.entry.bind("<KeyRelease>", lambda event: self.find_archive())



#_____________________________________BOTONES____________________________________________
        up_button = tk.Button(button_frame, text="Subir", command=self.go_up)
        up_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Agregar", command=self.agregar)
        rename_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Crear Archivo", command=self.agregar_archivo)
        rename_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Renombrar", command=self.rename)
        rename_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Copiar", command=self.copiar)
        rename_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Cortar", command=self.cortar)
        rename_button.pack(side=tk.LEFT)
        
        rename_button = tk.Button(button_frame, text="Pegar", command=self.pegar)
        rename_button.pack(side=tk.LEFT)

        delete_button = tk.Button(button_frame, text="Eliminar", command=self.delete)
        delete_button.pack(side=tk.LEFT)

        quit_button = tk.Button(button_frame, text="Salir", command=self.quit)
        quit_button.pack(side=tk.RIGHT)
        
        
        

    def populate_treeview(self):
        self.treeview.delete(*self.treeview.get_children()) #elimina todo los nodos del arbol grafico
        self.add_directory("", self.current_path) 

    def add_directory(self, parent, path, obj = None):
        name = os.path.basename(path)
        item = self.treeview.insert(parent, "end", text=name, open=False)
        archivo = Archivo(name,path,os.path.isdir(path),item,obj)
        self.tree.add_node(archivo, obj)
        
        if os.path.isdir(path):
            for item_name in os.listdir(path):
                item_path = os.path.join(path, item_name)
                
                self.add_directory(item, item_path,archivo)

    def on_open(self, event):
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if os.path.isdir(path):
            pass
            # self.treeview.delete(*self.treeview.get_children(item))
            # self.add_directory(item, path)
        else:
          
            os.startfile(path)
        

    def on_select(self, event):
        item = self.treeview.focus()
        path = self.get_item_path(item)
        
        if os.path.isdir(path):
            pass
            # self.treeview.delete(*self.treeview.get_children(item))
            # self.add_directory(item, path)
        else:
        
            os.startfile(path)
        
        
    #Aqui se filtra por el id para encontrar el nombre del archivo
    #referenciado y buscarlo en el arbol
    #return una ruta del archivo
    def get_item_path(self, item) -> str:
        path = ""
        
        text = self.treeview.item(item, "text")

        return self.tree.find_node(text,item).data.path
    
    
    def agregar(self): #Carpetas 
        item = self.treeview.focus() #Id de la carpeta seleccionada 
        path = self.get_item_path(item) # ruta de esa carpeta
        new_name = simpledialog.askstring("Crear Carpeta", f"Ingrese el nombre") #nombre de la carpeta
        if new_name:
            ruta_completa = os.path.join(path, new_name) #Ruta de la nueva carpeta
            try:
                os.makedirs(ruta_completa) #Se crea esa carpeta
                self.populate_treeview()   #Se actualiza el arbol de vistas
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo crear la carpeta")   # si hay un error aparece esta ventana emergente
                
    def agregar_archivo(self): #Archivos
        item = self.treeview.focus()   #Id de la carpeta seleccionada 
        path = self.get_item_path(item)  # ruta de esa carpeta
        new_name = simpledialog.askstring("Crear Archivo", "Ingrese el nombre") #Nombre del nuevo archivo 
        if new_name:
            ruta_completa = os.path.join(path, new_name) #Ruta del nuevo archivo
            try:
                archivo = open(ruta_completa, "w") #Creacion de archivo
                archivo.close()                    #Cerrar el archivo
                self.populate_treeview()           #actualizar el arbol
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo crear el Archivo") #si hay un error aparece esta ventana emergente
          
        

    def go_up(self):
        global cont
        carpeta = filedialog.askdirectory()    #Ventana de dialogo para esocger el archivo a subir
        self.tree.vaciar_arbol()               # Vaciar arbol
        # Imprime la ruta del documento seleccionado
        self.treeview.delete(*self.treeview.get_children()) #eliminar el arbol visual
        self.current_path = carpeta
        self.add_directory("", carpeta)    #Adicionar las nuevas carpetas a los 2 arboles


    
    #tampoco funciona
    def rename(self):
        item = self.treeview.focus()
        path = self.get_item_path(item)
        

        if path:
            new_name = simpledialog.askstring("Renombrar", f"Ingrese el nuevo nombre para '{os.path.basename(path)}'")
          
            if new_name:

                new_path = os.path.join(os.path.dirname(path), new_name)
                
                try:
                    os.rename(path, new_path)        #renombra el archivo
                    self.populate_treeview()

                except OSError as error:
                  
                    messagebox.showerror("Error", f"No se pudo renombrar '{os.path.basename(path)}'")

    #no funciona
    def delete(self):
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if path:
            confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de que deseas eliminar '{os.path.basename(path)}'?")
            if confirm:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)  # Elimina el directorio y su contenido
                        
                    else:
                        os.remove(path)  # Elimina el archivo
                        node = self.tree.find_node(os.path.basename(path), item)
                        self.populate_treeview()
                  
                except OSError:
                    messagebox.showerror("Error", f"No se pudo eliminar '{os.path.basename(path)}'")

        
    def quit(self):
        self.master.quit()
        
        
        
    def copiar(self): #Archivos
        item = self.treeview.focus()
        path = self.get_item_path(item)
        self.path_copy = path       #Ruta a copiar
        self.is_copiar = True
    
    def cortar(self): #Archivos
        item = self.treeview.focus()
        path = self.get_item_path(item) 
        self.is_copiar = False
        self.ruta_origen = path        #Ruta a cortar
        
    
    def pegar(self): #Archivos
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if self.is_copiar:    #se utiliza la opcion de presionar copiar?
            if os.path.isdir(path):
                try:
                    archivo_destino = os.path.join(path, os.path.basename(self.path_copy))
                    if not os.path.exists(archivo_destino):
                        shutil.copy(self.path_copy, path)
                        
                    else:
                        base_ruta = ""
                        if "." in os.path.basename(self.path_copy):
                            partes = os.path.basename(self.path_copy).split(".")
                            base_ruta = partes[0] + "_copy." + partes[1] 
                        else:
                            base_ruta = os.path.basename(self.path_copy) + "_copy" #Añade _copy si la el archivo ya existe
                            
                        new_path = os.path.join(path, base_ruta)  
          
                        shutil.copy(self.path_copy, new_path) #Lo pega
                    self.populate_treeview()
        

                except Exception as e:
              
                    messagebox.showerror("Error", f"No se pudo copiar '{os.path.basename(self.path_copy)}'")
        else:
            try:
                if os.path.dirname(self.ruta_origen) != path:
                    shutil.move(self.ruta_origen, path)
                    self.populate_treeview()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cortar '{os.path.basename(self.path_copy)}'")
            
          
    def find_archive(self):
        valor = self.entry.get() #El valor del input de busqueda
        
        if valor != "":
            node_list = self.tree.search_node(valor) #Busqueda pero de todos los que tengan algo parecido con el valor
            #Devuelve una lista de todas las coincidencias
            
        else:
            node_list = None

        if node_list is not None:  #si la lista de similares contiene algo
            self.treeview.delete(*self.treeview.get_children()) #Elimina
            for obj in node_list:
                self.add_directory("",obj.data.path)     #agrega todas las rutas similares a la lista
        else:  # si no se llena con la ruta raiz actual
            self.treeview.delete(*self.treeview.get_children())
            self.add_directory("",self.current_path)
        


if __name__ == "__main__":
    root = tk.Tk()
    DirectoryExplorer(root)
    root.mainloop()