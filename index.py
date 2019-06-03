from tkinter import ttk
from tkinter import *

#https://docs.python.org/dev/library/tkinter.ttk.html


import sqlite3


# clase product. 
# Encargada de gestion de los metodos de las ventanas y productos

class product:

    db_name = 'database.db'

# __init__ no tiene valor de retorno. Es el primer metodo que se ejecutara de forma automatica cuando se instancie la clase.

    def __init__ (self,window):

        self.window = window
        self.window.title('Lista de productos')

        #frame (contenedor), dentro de window
        
        frame = LabelFrame(self.window, text = "Registrar nuevo producto")
        frame.grid(row = 0 , column = 0, columnspan = 3, pady = 20)
        
        #label: Nombre

        Label(frame, text = 'Nombre: ').grid(row=1,column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid (row= 1, column=1)

        #label: Precio

        Label(frame, text= 'Precio: ').grid(row=2,column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2,column=1)

        #botones: Guardar producto - Eliminar - Editar

        Button(frame, text='Agregar producto' , command = self.add_productos ).grid(row=3,columnspan=2,sticky = W + E)

        Button(text='Eliminar',command = self.delete_producto ).grid(row=5,column=0,sticky = W + E)

        Button(text='Editar',command=self.edit_producto ).grid(row=5,column=1,sticky = W + E)

        #mensaje confirmacion

        self.mensaje = Label(text = '', fg = 'green')
        self.mensaje.grid( row=3 , column = 0 , columnspan = 2 , sticky = W + E)

        #table - Treeview

        self.tree = ttk.Treeview(height=20,columns=2)
        self.tree.grid(row=4,column=0,columnspan = 2)
        self.tree.heading('#0',text='Nombre', anchor = CENTER)
        self.tree.heading('#1',text='Precio', anchor = CENTER)

        #consulto db - productos 

        self.get_productos()


    #definir query

    def run_query(self , query , parameters = () ):
        
        with sqlite3.connect(self.db_name) as connection:
            
            cursor = connection.cursor() #retorna posicion en database
            result = cursor.execute(query,parameters)
            connection.commit #ejecuta query

        return result
    
    #consultando datos

    def get_productos(self):

        #limpiar tabla

        datos = self.tree.get_children() #lista de datos
        
        for elemento in datos:
            
            self.tree.delete(elemento) #eliminar elemento
    
        #consultar datoss

        query = 'SELECT * FROM productos ORDER BY nombre DESC'
        db_rows = self.run_query(query)

        #exportar datos

        for row in db_rows:
            self.tree.insert ('', 0 , text = row[1] , values = row[2])


    #validar datos a ingresar

    def validacion (self):

        val = len( self.nombre.get() ) != 0 and len( self.precio.get()) != 0 #obtengo True si ingresaron datos en ambos campos
        return val 
    
    #ingresar datos 

    def add_productos (self):

        if self.validacion():

           query = 'INSERT INTO productos VALUES (NULL, ?, ?)'
           parameters = ( self.nombre.get() , self.precio.get() )
           self.run_query (query , parameters)
           self.mensaje['fg'] = 'green'
           self.mensaje['text'] = '{} agregado correctamente'.format( self.nombre.get() )

           #limpio Entry

           self.nombre.delete (0,END)
           self.precio.delete (0,END)
           

        else:

           self.mensaje['fg'] = 'red'
           self.mensaje['text'] = 'Precio y nombre son requeridos'                    
        
        self.get_productos()

    def delete_producto(self):
        
        try:

            self.tree.item(self.tree.selection())['text'][1] #Modificar elemento seleccionado
            
        except  IndexError as error:
            
            self.mensaje['fg'] = 'red'
            self.mensaje['text']='Debe selecionar un elemento'
            
            return

        query = 'DELETE FROM productos WHERE nombre = ?'
         
        nombre = self.tree.item(self.tree.selection())['text']
         
        self.run_query(query, (nombre,))

        self.mensaje['fg'] = 'green'

        self.mensaje['text']= ' {} eliminado correctamente'.format(nombre)

        self.get_productos() #actualizo la tabla
         

    
    def edit_producto(self):

        try:

            self.tree.item(self.tree.selection())['text'][1] #Modificar elemento seleccionado
            
        except  IndexError as error:
            
            self.mensaje['fg'] = 'red'
            self.mensaje['text']='Debe selecionar un elemento'
            
            return

        nombre_actual=self.tree.item(self.tree.selection())['text']
        
        precio_actual=self.tree.item(self.tree.selection())['values'] [0]

        #ventana emergente

        self.edit_window = Toplevel()  #Crear la ventana emergente

        self.edit_window.title = 'Editar producto'

        #nuevo nombre

        Label(self.edit_window, text = 'Nombre actual').grid(row=0,column=1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value= nombre_actual), state = 'readonly').grid(row=0,column=2)


        Label(self.edit_window, text = 'Nuevo nombre').grid(row=1,column=1)
        nombre_nuevo = Entry(self.edit_window)
        nombre_nuevo.grid(row=1,column=2)
       
        #nuevo precio

        Label(self.edit_window, text = 'Precio actual').grid(row=2,column=1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = precio_actual), state = 'readonly').grid(row=2,column=2)


        Label(self.edit_window, text = 'Nuevo precio').grid(row=3,column=1)
        precio_nuevo = Entry(self.edit_window)
        precio_nuevo.grid(row=3,column=2)

        Button(self.edit_window,text='Guardar',command= lambda: self.save_producto(nombre_nuevo.get(),nombre_actual,precio_nuevo.get(),precio_actual)).grid(row=4,column=2,sticky = W + E)


    def save_producto(self,nombre_nuevo,nombre_actual,precio_nuevo,precio_actual):
    
        query = 'UPDATE productos SET nombre = ? , precio = ? WHERE nombre = ? AND precio = ?'
        parameters = (nombre_nuevo,precio_nuevo,nombre_actual,precio_actual)
        self.run_query(query,parameters)
       
        self.edit_window.destroy() #cerrar la ventana

        self.mensaje['text'] = '{} actualizado correctamente'.format(nombre_nuevo) #mensaje principal

        self.get_productos () #actualizo la tabla
    



if __name__ == '__main__':

    window = Tk() # Tk() retorna una ventana.
    aplication = product(window)
    window.mainloop() # muestra en pantalla