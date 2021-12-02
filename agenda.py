from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sqlite3

#conexion = sqlite3.connect('agenda.db')
#cursor = conexion.cursor()

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("01-agenda.ui", self)
        
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        self.operacion=''
        
        self.nuevo.clicked.connect(self.on_agregar)
        self.eliminar.clicked.connect(self.on_eliminar)
        self.editar.clicked.connect(self.on_editar)
        self.cancelar.clicked.connect(self.on_cancelar)
        self.aceptar.clicked.connect(self.on_aceptar)
        self.lista.itemClicked.connect(self.on_click)
        #self.quitar_todos.clicked.connect(self.remove_all)
        
        self.cursor.execute('select * from persona')
        #usuarios = self.cursor.fetchall()
      
  # Se agregan los elementos al QListWidget
        for i in self.cursor:
            self.id = str(i[0]) 
            self.nombre = str(i[1])
            self.apellido = str(i[2])
            #self.email = str(i[2])
            #self.telefono = str(i[3])
            #self.direccion = str(i[4])
            #self.fecha_nac = str(i[5]) 
            #self.altura = str(i[6]) 
            
            #self.lista_w.addItem(self.nombre + " - " + self.apellido + " - " + self.email+ " - " + self.telefono+ " - " + self.altura)
            self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido )     
        
        
    def on_agregar(self):
        self.operacion='A'
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.cancelar.setEnabled(True)
        self.nuevo.setEnabled(False)
        self.nombre.setEnabled(True)
        self.apellido.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.fecha_n.setEnabled(True)
        self.altura.setEnabled(True) 
        self.peso.setEnabled(True)
        self.aceptar.setEnabled(True) 
        self.nombre.setText('')
        self.apellido.setText('')
        self.email.setText('')
        self.telefono.setText('')
        self.direccion.setText('')
        self.fecha_n.setText('')
        self.altura.setText('')
        self.peso.setText('')
        
        
        
        
    
        
    def on_click(self):
        self.editar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.eliminar.setEnabled(True)
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ind= self.lista_w.currentItem().text()
        
        separador = ("-")
        persona = ind.split(separador, 1)
        self.id_persona=persona[0]
        self.n_persona=persona[1]
        self.cursor.execute("select * from persona  WHERE id = " + self.id_persona)
        for i in self.cursor:
            
            self.nombre.setText(str(i[1]))
            self.apellido.setText(str(i[2]))
            self.email.setText(str(i[3]))
            self.telefono.setText(str(i[4]))
            self.direccion.setText(str(i[5]))
            self.fecha_n.setText(str(i[6])) 
            self.altura.setText(str(i[7])) 
            self.peso.setText(str(i[8])) 
            
           
    def on_editar(self):
        self.operacion='M'
        self.nuevo.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(True) 
        self.nombre.setEnabled(True)
        self.apellido.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.fecha_n.setEnabled(True)
        self.altura.setEnabled(True) 
        self.peso.setEnabled(True)
        
    def on_eliminar(self):
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ret = QMessageBox.question (self, 'Eliminar persona' , "Desea Eliminar persona '"+self.n_persona+"'  Para Confirmar click en Ok" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if ret == QMessageBox.Ok: 
                self.cursor.execute("DELETE FROM persona  WHERE id = " + self.id_persona)
                self.conexion.commit()
                self.lista_w.clear()
                self.cursor = self.conexion.cursor()
                self.cursor.execute('select * from persona')
            # Se agregan los elementos al QListWidget
                for i in self.cursor:
                    self.id = str(i[0]) 
                    self.nombre = str(i[1])
                    self.apellido = str(i[2])
                    self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido ) 
        self.habilitar_desabilitar()
        
        
        
    
    def on_aceptar(self):  
        self.nombre = self.nombre.text()
        self.apellido = self.apellido.text()
        self.email = self.email.text()
        self.telefono = self.telefono.text()
        self.direccion = self.direccion.text()
        self.fecha_nac = self.fecha_n.text()
        self.altura = self.altura.text()
        self.peso = self.peso.text()
        
        if self.nombre=='' or self.apellido=='' :
            QMessageBox.information(self, 'Informacion', " Apellido y Nombre son obligatorios ",QMessageBox.Ok)
        
        else:
            try:
                float(self.altura)
                self.it_is = True
            except ValueError:
                self.it_is = False
            try:
                float(self.peso)
                self.it_is_p = True
            except ValueError:
                self.it_is_p = False    
                
                
            if self.it_is==False or self.it_is_p == False:
                if self.it_is==False:
                    QMessageBox.information(self, 'Informacion', "El dato  Altura no es un numero real ",QMessageBox.Ok)    
                if self.it_is_p==False:
                    QMessageBox.information(self, 'Informacion', "El dato   Peso no es un numero real ",QMessageBox.Ok)    
            
            else:  
                self.conexion = sqlite3.connect('agenda.db')
                self.cursor = self.conexion.cursor()
                    
            
                if self.operacion=='A':
                    ret = QMessageBox.question (self, 'Nueva Persona' , "Para Confirmar click Ok" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Ok: 
                    
                        self.cursor.execute("INSERT INTO persona(nombre,apellido,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('"+self.nombre+"','"+self.apellido+"','"+self.email+"', '"+self.telefono+"','"+self.direccion+"','"+self.fecha_nac+"','"+self.altura+"','"+self.peso+"')")
                        
                        self.conexion.commit() 
                    
                
                if self.operacion=='M':
                    ret = QMessageBox.question (self, 'Editar Persona' , "Para Confirmar click  Ok" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Ok: 
                    
                        
                        self.cursor.execute("UPDATE persona SET nombre='"+self.nombre+"', apellido='"+self.apellido+"', email='"+self.email+"', telefono='"+self.telefono+"',direccion='"+self.direccion+"',fecha_nac='"+self.fecha_nac+"',altura='"+self.altura+"',peso='"+self.peso+"' WHERE id = " + self.id_persona)
                        self.conexion.commit()
                        
            
                
                
                    
                if ret == QMessageBox.Ok:  
                    self.lista_w.clear()
                    self.cursor = self.conexion.cursor()
                    self.cursor.execute('select * from persona')
                    # Se agregan los elementos al QListWidget
                    for i in self.cursor:
                            self.id = str(i[0]) 
                            self.nombre = str(i[1])
                            self.apellido = str(i[2])
                            self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido ) 
                self.habilitar_desabilitar()
            
    def habilitar_desabilitar(self):            
        # botones
        self.nuevo.setEnabled(True)   
        self.editar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(False)
        
        self.nombre.setEnabled(False)
        self.apellido.setEnabled(False)
        self.email.setEnabled(False)
        self.telefono.setEnabled(False)
        self.direccion.setEnabled(False)
        self.fecha_n.setEnabled(False)
        self.altura.setEnabled(False) 
        self.peso.setEnabled(False)
        
        self.nombre.setText('')
        self.apellido.setText('')
        self.email.setText('')
        self.telefono.setText('')
        self.direccion.setText('')
        self.fecha_n.setText('')
        self.altura.setText('')
        self.peso.setText('')
         
             
    def on_cancelar(self):
        self.habilitar_desabilitar()
        
        
        



app = QApplication([])

win = MiVentana()
win.show()

app.exec_()



