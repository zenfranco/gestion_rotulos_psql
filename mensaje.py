from PyQt5 import QtCore, QtGui, uic,QtWidgets


class Mensaje():

	def cartel(self,titulo,mensaje,tipo):
	
		msgBox=QtWidgets.QMessageBox()
		msgBox.setIcon(tipo)
		msgBox.setWindowTitle(titulo)
		msgBox.setText(mensaje)
		msgBox.exec_()
		
	def cartel_opcion(self,titulo,mensaje,tipo):
		msgBox=QtWidgets.QMessageBox()
		msgBox.setIcon(tipo)
		msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		
		msgBox.setWindowTitle(titulo)
		msgBox.setText(mensaje)
		r= msgBox.exec_()
		
		
		return r
