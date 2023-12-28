import psycopg2

class bdquery():

		def __init__(self):
			self.conexion = psycopg2.connect(host="192.168.0.50",database="casem", user="postgres",password="casem1234")
			
			
			

		def cargapedido (self,Numpedido,registro,cantidad,ini,fin,dispoini,dispofin,estado,fechapedido,serie):
			cur=self.conexion.cursor()
			cur.execute("INSERT INTO pedidos (num_pedido,rncyfs,cantidad,inicio,fin,disponibleinicio,disponiblefin,estado,fecha_pedido,serie) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[Numpedido,registro,cantidad,ini,fin,dispoini,dispofin,estado,fechapedido,serie])
			self.conexion.commit()
			cur.close()
			
		def cargasubepedido (self,numpedido,inicio,fin,cantidad,variedad,especie,camp,kg,categoria,registro,fechasubpedido):
			cur=self.conexion.cursor()
			cur.execute("INSERT INTO subpedidos (num_pedido,num_reg,cantidad,inicio,fin,kg,variedad,especie,categoria,camp,fecha_subpedido) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[numpedido,registro,cantidad,inicio,fin,kg,variedad,especie,categoria,camp,fechasubpedido])
			self.conexion.commit()
			cur.close()

		def carga_estampillas (self,rncyfs,dav,especie,categoria,campana,cantidad,variedad,inicial,final,envase,fecha):
			cur=self.conexion.cursor()
			cur.execute("insert into estampillas (rncyfs,dav,especie,categoria,camp,cantidad,variedad,inicio,fin,envase,fecha) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[rncyfs,dav,especie,categoria,campana,cantidad,variedad,inicial,final,envase,fecha] )
			self.conexion.commit()
			cur.close()

		def carga_estampillas_anexo (self,rncyfs,especie,campana,cantidad,inicial,final,fecha):
			cur=self.conexion.cursor()
			cur.execute("insert into anexos (rncyfs,especie,camp,cantidad,inicio,fin,fecha) values (%s,%s,%s,%s,%s,%s,%s)",[rncyfs,especie,campana,cantidad,inicial,final,fecha] )
			self.conexion.commit()
			cur.close()

		def corregir_rango(self,indice,inicio,fin):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE "Datos" SET inicial= %s,final=%s WHERE indice =%s ''',[inicio,fin,indice])
			self.conexion.commit()
			cur.close()

		def corregirInicio(self,inicio,indice):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE "Datos" SET inicial= %s WHERE indice =%s ''',[inicio,indice])
			self.conexion.commit()
			cur.close()

		def corregirPedido(self,inicio,num_pedido):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE Pedidos SET disponibleinicio= %s WHERE num_pedido =%s ''',[inicio,num_pedido])
			self.conexion.commit()
			cur.close()

		


		def recuperabd(): #recuperar numero de pedido y rango general
			#self.conexion.execute("select numpedido,inicio,final from Datos")
			pass
		
		def actualizabd(self,inicio,fin,numpedido): #actualizar numero de pedido y rango general
			pass
			
		def traeultimopedido(self):
			cur =self.conexion.cursor()
			cur.execute('''SELECT MAX(numpedido) from "Datos"''')
			dato =cur.fetchone()
			cur.close()
			
			
			return dato
			
		def incrementanpedido(self,numpedido):
			
			cur=self.conexion.cursor()
			cur.execute('''UPDATE "Datos" SET numpedido= (%s) WHERE indice = 1''',[numpedido])
			self.conexion.commit()
			cur.close()
		
		def recuperarango(self,indice):
			cur= self.conexion.cursor()
			cur.execute('''SELECT inicial, final FROM "Datos" where indice = %s''',[(indice)])
			rango=cur.fetchone()
			cur.close()
			return rango
				
		def actualizarangoenbd(self,inicio,final,indice):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE "Datos" SET inicial = (%s) where indice=%s''',[inicio,indice])
			cur.execute('''UPDATE "Datos" SET final = %s where indice=%s''',[final,indice])
			self.conexion.commit()
			cur.close()
			
		def verpedido(self,rncyfs):
			cur=self.conexion.cursor()
			cur.execute('''select num_pedido,disponibleinicio || '-' || disponiblefin,disponiblefin-disponibleinicio+1, serie from pedidos
			where rncyfs =%s and disponiblefin-disponibleinicio+1 !=0 order by disponibleinicio''',[rncyfs])
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
		def recuperaSubpedidos(self,num_pedido):
			cur=self.conexion.cursor()
			cur.execute(''' select cantidad,inicio,fin,variedad,especie,categoria,camp,fecha_subpedido from subpedidos where num_pedido = %s order by inicio desc ''',[num_pedido])
			listaSpedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listaSpedidos

		
		def recuperaEstampillas(self,asociado):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,rncyfs,inicio,fin,cantidad,variedad,especie,categoria,envase,dav,camp,fecha from estampillas e
			inner join asociados a on a.num_reg = e.rncyfs where razon_social LIKE %s order by inicio desc''',[asociado])
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
		
		def recuperaEstampillasFecha(self,asociado,desde,hasta):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,rncyfs,inicio,fin,cantidad,variedad,especie,categoria,envase,dav,camp,fecha from estampillas e
			inner join asociados a on a.num_reg = e.rncyfs where razon_social LIKE %s and fecha between %s and %s order by inicio desc''',[asociado,desde,hasta])
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
		
		def recuperaAnexos(self):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,rncyfs,inicio,fin,cantidad,'-',especie,'-','-','-',camp,fecha from anexos anx
			inner join asociados a on a.num_reg = anx.rncyfs order by inicio desc''')
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos

			
			
		def getpedido(self,numpedido):
			cur=self.conexion.cursor()
			cur.execute("SELECT * FROM pedidos WHERE num_pedido =%s",[numpedido])
			listapedidos=cur.fetchone()
			self.conexion.commit()
			cur.close()
			return listapedidos
		
		def getpedidos(self):
			cur=self.conexion.cursor()
			cur.execute('''SELECT a.razon_social,cantidad,inicio ||'-' || fin,serie,num_pedido,fecha_pedido FROM pedidos p INNER JOIN asociados a on a.num_reg = p.rncyfs ORDER BY num_pedido DESC LIMIT 5''')
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
			
		def actualizaremanente(self,numpedido,inicioremanente):
			cur=self.conexion.cursor()
			cur.execute("UPDATE pedidos SET disponibleinicio = (%s) WHERE num_pedido = (%s)",([inicioremanente,numpedido]))
			self.conexion.commit()
			cur.close()
			
		def actualizaestado(self,numpedido,estado):
			cur=self.conexion.cursor()
			cur.execute("UPDATE pedidos SET estado = (%s) WHERE num_pedido = (%s)",([estado,numpedido]))
			self.conexion.commit()
			cur.close()
			
			
		def traerasociados(self):
			cur=self.conexion.cursor()
			cur.execute(''' select razon_social from asociados order by razon_social''')
			listado=cur.fetchall()
			self.conexion.commit()
			cur.close
			return listado
			
		def traerasociadosFILTRO(self,nombre):
			cur=self.conexion.cursor()
			cur.execute(''' select razon_social from asociados where razon_social LIKE %s order by razon_social''',([nombre]))
			listado=cur.fetchall()
			self.conexion.commit()
			cur.close
			return listado
			
		def getrncyfs(self,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social = (%s)''',[nombre])
			registro=cur.fetchone()
			self.conexion.commit()
			cur.close
			return registro
			
			
			
		def listaxregistro(self,campo,radiobutton):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||'-'|| p.fin,estado,coalesce(s.cantidad,0),coalesce(s.inicio|| '-' || s.fin,'SIN USAR'),
			coalesce((p.fin-s.fin),p.cantidad),coalesce(kg,0),coalesce(variedad,''),coalesce(especie,''),coalesce(categoria,''),coalesce(camp,0),coalesce(fecha_subpedido,'')
   			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE rncyfs=%s and estado LIKE %s order by s.inicio''',[campo,radiobutton])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaxregistrofecha(self,campo,radiobutton,fecha_desde,fecha_hasta):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||'-'|| p.fin,estado,coalesce(s.cantidad,0),coalesce(s.inicio|| '-' || s.fin,'SIN USAR'),
			coalesce((p.fin-s.fin),p.cantidad),coalesce(kg,0),coalesce(variedad,''),coalesce(especie,''),coalesce(categoria,''),coalesce(camp,0),coalesce(fecha_subpedido,'')
   			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE rncyfs=%s and estado LIKE %s and fecha_subpedido >= %s and fecha_subpedido <= %s order by s.inicio''',[campo,radiobutton,fecha_desde,fecha_hasta])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaxpedido(self,campo,radiobutton):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||'-'|| p.fin,estado,coalesce(s.cantidad,0),coalesce(s.inicio|| '-' || s.fin,'SIN USAR'),
			coalesce((p.fin-s.fin),p.cantidad),coalesce(kg,0),coalesce(variedad,''),coalesce(especie,''),coalesce(categoria,''),coalesce(camp,0),coalesce(fecha_subpedido,'')
   			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE p.num_pedido=%s and estado LIKE %s order by s.inicio''',[campo,radiobutton])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
		def listaxpedidofecha(self,campo,radiobutton,fecha_desde,fecha_hasta):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||'-'|| p.fin,estado,coalesce(s.cantidad,0),coalesce(s.inicio|| '-' || s.fin,'SIN USAR'),
			coalesce((p.fin-s.fin),p.cantidad),coalesce(kg,0),coalesce(variedad,''),coalesce(especie,''),coalesce(categoria,''),coalesce(camp,0),coalesce(fecha_subpedido,'')
   			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE p.num_pedido=%s and estado LIKE %s and fecha_subpedido >= %s and fecha_subpedido <= %s order by s.inicio''',[campo,radiobutton,fecha_desde,fecha_hasta])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
		def listaraexcell(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(s.cantidad)Cantidad_Solicitada,s.inicio|| '-' || s.fin,variedad,especie,categoria,kg
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE p.num_pedido=%s order by s.inicio''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaraexcellall(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(s.cantidad)Cantidad_Solicitada,s.inicio|| '-' || s.fin,variedad,especie,categoria,kg
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE p.rncyfs=%s order by s.inicio''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
			
			
		def listaxtodo(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,rncyfs,p.cantidad,p.inicio,p.fin,estado,disponibleinicio,disponiblefin,
			s.inicio,s.fin,s.dav,variedad,especie,categoria,camp from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE rncyfs=%s''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
			
		def listarrendicion(self,desde,hasta,registro,especie,cultivar,categoria,camp):
			cur=self.conexion.cursor()
			cur.execute(''' select s.inicio||'-'||s.fin,s.cantidad,s.num_reg,a.razon_social,kg,especie,variedad,categoria,camp,fecha_subpedido,s.num_pedido
			from subpedidos s
			inner join asociados a
			on a.num_reg = s.num_reg
			where fecha_subpedido >= %s and fecha_subpedido <= %s and s.num_reg LIKE %s 
			and especie LIKE %s and variedad LIKE %s and categoria LIKE %s and camp =%s
   			order by s.inicio''',([desde,hasta,registro,especie,cultivar,categoria,camp]))
			listado = cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listado
			
		def listarrendicionsolopedidos(self,desde,hasta,registro):
			cur=self.conexion.cursor()
			cur.execute(''' select inicio|| '-'||fin,cantidad,p.rncyfs,a.razon_social,fecha_pedido,num_pedido from pedidos p
			inner join asociados a on a.num_reg = p.rncyfs where fecha_pedido >= %s and fecha_pedido <= %s and p.rncyfs LIKE %s 
			order by inicio''',([desde,hasta,registro]))
			listado = cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listado
			
		def insertarenlocker(self,numpedido,locker,fechaingreso,estado):
			cur=self.conexion.cursor()
			cur.execute(''' insert into lockers (num_pedido,num_locker,fecha_ingreso,estado) values (%s,%s,%s,%s)''',([numpedido,locker,fechaingreso,estado]))
			self.conexion.commit()
			cur.close()
			
			
		def definircantidadlockers(self,num,estado):
			cur=self.conexion.cursor()
			cur.execute ('''insert into lockers (num_locker,estado) values (%s,%s)''',([num,estado]))
			self.conexion.commit()
			cur.close()
			
		def recuperalockers(self):
			cur=self.conexion.cursor()
			cur.execute('''select num_locker from lockers where estado ='Disponible' order by num_locker''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def modificalocker(self,locker,pedido,fecha):
			cur=self.conexion.cursor()
			cur.execute("UPDATE lockers SET num_pedido = %s WHERE num_locker =%s",[pedido,locker])
			cur.execute("UPDATE lockers SET fecha_ingreso = %s WHERE num_locker =%s",[fecha,locker])
			cur.execute("UPDATE lockers SET estado = %s WHERE num_locker =%s",["Ocupado",locker])
			self.conexion.commit()
			cur.close()
			
		def liberalocker(self,locker):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE lockers SET estado = 'Disponible',num_pedido=0,fecha_ingreso='' WHERE num_locker =%s''',[locker])
				
			self.conexion.commit()
			cur.close()
			
			
			
		def verlockers(self):
			cur=self.conexion.cursor()
			cur.execute('''SELECT num_locker,l.num_pedido,disponibleinicio||' - '||disponiblefin,disponiblefin-disponibleinicio+1 cantidad,p.rncyfs, a.razon_social
						from lockers l 
						inner join pedidos p on p.num_pedido = l.num_pedido
						inner join asociados a on p.rncyfs=a.num_reg
						order by num_locker
						''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def verlockers_filtrado(self,asociado):
			cur=self.conexion.cursor()
			cur.execute('''SELECT num_locker,l.num_pedido,disponibleinicio||'-'||disponiblefin,disponiblefin-disponibleinicio+1 cantidad,p.rncyfs,razon_social
			from lockers l inner join pedidos p ON p.num_pedido=l.num_pedido
			inner join asociados a ON a.num_reg =p.rncyfs
			where razon_social LIKE %s
   			order by num_locker''',([asociado.upper()]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def altaasociado(self,reg,razonsocial):
			cur= self.conexion.cursor()
			cur.execute(''' insert into asociados (num_reg,razon_social) values (%s,%s)''',([reg,razonsocial]))
			self.conexion.commit()
			cur.close()
			
		def altagestion(self,reg,tipo,estado,fecha,cantidad):
			cur= self.conexion.cursor()
			cur.execute(''' insert into gestiones (num_reg,tipo,estado,fecha_inicio,cantidad) values (%s,%s,%s,%s,%s)''',([reg,tipo,estado,fecha,cantidad]))
			self.conexion.commit()
			cur.close()
			
			
		def altarotulo(self,registro,especie,tipo,cantidad,estado,categoria,fecha,gestion):
			cur= self.conexion.cursor()
			cur.execute(''' insert into rotulos (num_reg,especie,tipo,cantidad,estado,categoria,fecha_impresion,gestion) values (%s,%s,%s,%s,%s,%s,%s,%s)''',([registro,especie,tipo,cantidad,estado,categoria,fecha,gestion]))
			self.conexion.commit()
			cur.close()
			
		def traerotulos(self,estado,tipo,especie,razon):
			cur=self.conexion.cursor()
			cur.execute('''select indice, fecha_impresion,estado,cantidad,a.razon_social,especie,categoria,tipo from rotulos r
			inner join asociados a on a.num_reg=r.num_reg where estado LIKE %s and tipo LIKE %s and especie like %s and a.razon_social LIKE %s order by indice DESC''',([estado,tipo,especie,razon]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traerotulosFecha(self,estado,tipo,especie,inicio,fin):
			cur=self.conexion.cursor()
			cur.execute('''select indice, fecha_impresion,estado,cantidad,a.razon_social,especie,categoria,tipo from rotulos r
			inner join asociados a on a.num_reg=r.num_reg where estado LIKE %s and tipo LIKE %s and especie like %s and fecha_impresion >= %s and fecha_impresion <=%s order by indice DESC''',([estado,tipo,especie,inicio,fin]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traenombre(self,registro):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social from asociados where num_reg=%s''',([registro]))
			self.conexion.commit()
			asociado=cur.fetchone()
			cur.close()
			return asociado
			
		def traerncyfs(self,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social=%s''',([nombre]))
			self.conexion.commit()
			asociado=cur.fetchone()
			cur.close()
			return asociado
			
			
		def traergestiones(self,estado,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,estado,cantidad,'',tipo,fecha_inicio, indice from gestiones g
			inner join asociados a on a.num_reg = g.num_reg where estado LIKE %s and razon_social LIKE %s order by fecha_inicio ''',([estado, nombre]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		
		def traergestionesActivas(self,estado,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,estado,cantidad,'',tipo,fecha_inicio, indice from gestiones g
			inner join asociados a on a.num_reg = g.num_reg
   			where estado LIKE %s and estado != 'FINALIZADO'  and razon_social LIKE %s order by fecha_inicio ASC ''',([estado, nombre]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traenotas(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select coalesce(observaciones,'') from gestiones where indice=%s''',([indice]))
			self.conexion.commit()
			obs=cur.fetchone()
			return obs
			
		def updategestion(self,indice,estado):
			cur=self.conexion.cursor()
			cur.execute("UPDATE gestiones SET estado = (%s) WHERE indice = (%s)",([estado,indice]))
			self.conexion.commit()
			cur.close()
		def insertarnota(self,indice,obs):
			cur=self.conexion.cursor()
			cur.execute("UPDATE gestiones SET observaciones = (%s) WHERE indice = (%s)",([obs,indice]))
			self.conexion.commit()
			cur.close()
			
			
			
		def definirestadorotulo(self,estado,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE rotulos SET estado = (%s) WHERE indice = (%s)",([estado,indice]))
			self.conexion.commit()
			cur.close()
		
		def modificarCantidadImpresion(self,indice,cant):
			cur=self.conexion.cursor()
			cur.execute("UPDATE rotulos SET cantidad = (%s) WHERE indice = (%s)",([cant,indice]))
			self.conexion.commit()
			cur.close()
			
			
		def nuevorango(self,inicio,fin,cantidad,serie):
			cur= self.conexion.cursor()
			cur.execute(''' insert into rangos_disponibles (inicio,fin,cantidad,serie,estado) values (%s,%s,%s,%s,%s)''',([inicio,fin,cantidad,serie,"DISPONIBLE"]))
			self.conexion.commit()
			cur.close()
			
		def traerangos(self,estado,serie):
			cur=self.conexion.cursor()
			cur.execute('''select inicio,fin,cantidad,serie,estado from rangos_disponibles where estado LIKE %s and serie=%sorder by inicio''',([estado,serie]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def definirrango(self,inicio,fin,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE Datos SET (inicial,final) = (%s,%s) WHERE indice = (%s)",([inicio,fin,indice]))
			cur.execute('''UPDATE rangos_disponibles SET (estado) = "EN USO" WHERE inicio = (%s)''',([inicio]))
			self.conexion.commit()
			cur.close()
		
		def cancelarrango(self,inicio):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE rangos_disponibles SET estado = 'TERMINADO' WHERE inicio = (%s)''',([inicio]))
			self.conexion.commit()
			cur.close()
			
		def busquedaxrotulo(self,rotulo):
			cur=self.conexion.cursor()
			cur.execute(''' select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||'-'|| p.fin,estado,coalesce(s.cantidad,0),coalesce(s.inicio|| '-' || s.fin,'SIN USAR'),
			coalesce((p.fin-s.fin),p.cantidad),coalesce(kg,0),coalesce(variedad,''),coalesce(especie,''),coalesce(categoria,''),coalesce(camp,0),coalesce(fecha_subpedido,'')
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido 
			WHERE %s BETWEEN p.inicio AND p.fin''',([rotulo]))
			self.conexion.commit()
			pedido=cur.fetchall()
			cur.close()
			return pedido
				
		def validarasociado(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select count(*) from asociados where num_reg =%s''',[(reg)])
			self.conexion.commit()
			result=cur.fetchone()
			cur.close()
			return result
		
		def borrargestion(self,indice):
			cur=self.conexion.cursor()
			cur.execute(''' delete from gestiones where indice =%s''',([indice]))
			self.conexion.commit()
			cur.close()
			
		def borrarimpresion(self,indice):
			cur=self.conexion.cursor()
			cur.execute(''' delete from rotulos where indice =%s''',([indice]))
			self.conexion.commit()
			cur.close()
		
		def eliminarLinea(self,inicio):
			cur=self.conexion.cursor()
			cur.execute(''' delete from estampillas where inicio =%s''',([inicio]))
			self.conexion.commit()
			cur.close()

		def eliminarLineaSubpedido(self,inicio,num_pedido):
			cur=self.conexion.cursor()
			cur.execute(''' delete from subpedidos where inicio =%s and num_pedido=%s''',([inicio,num_pedido]))
			self.conexion.commit()
			cur.close()

		def traerazonsocial(self,numpedido):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social from asociados a
			inner join pedidos p on p.rncyfs = a.num_reg
			where num_pedido = %s''',([numpedido]))
			self.conexion.commit()
			razon=cur.fetchone()
			cur.close()
			return razon
			
		def getstock(self):
			cur=self.conexion.cursor()
			cur.execute('''select denominacion, cantidad from stock_rotulos''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def subpedidosporfecha(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select sum(cantidad),especie,fecha_subpedido from subpedidos where num_reg LIKE %s group by fecha_subpedido,especie ORDER BY fecha_subpedido DESC''',reg)
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		
		def estampillasPorFecha(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select sum(cantidad),especie,fecha from estampillas where rncyfs LIKE %s group by fecha,especie ORDER BY fecha DESC''',reg)
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		
		def anexosPorFecha(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select sum(cantidad),especie,fecha from anexos where rncyfs LIKE %s group by fecha,especie ORDER BY fecha DESC''',reg)
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def recuperastock(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select cantidad from stock_rotulos where indice=%s''',([indice]))
			self.conexion.commit()
			cantidad=cur.fetchone()
			cur.close()
			return cantidad
			
		def actualizar_stock(self,cantidad,indice):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE stock_rotulos SET cantidad= %s WHERE indice =%s''',([cantidad,indice]))
			self.conexion.commit()
			cur.close()
			
		def traerregistro(self,asociado):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social =%s''',([asociado]))
			self.conexion.commit()
			registro=cur.fetchone()
			cur.close()
			return registro
			
		def insertarEnvio(self,fecha_envio,registro,cantidad,tipo,rotulos,fecha_emision,bultos,estado,especie,detalle,obs):
			cur= self.conexion.cursor()
			cur.execute(''' insert into envios (fecha_envio,num_reg,cantidad,tipo,r,subpedido_fecha,bultos,estado,especie,detalle,obs) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',([fecha_envio,registro,cantidad,tipo,rotulos,fecha_emision,bultos,estado,especie,detalle,obs]))
			self.conexion.commit()
			cur.close()
			
		def getEnvios(self,registro,estado,tipo):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id_envio,tipo,detalle,obs,guia
			from envios e inner join asociados a on a.num_reg = e.num_reg
			where e.num_reg = %s and estado LIKE %s and tipo LIKE %s order by fecha_envio DESC''',[registro,estado,tipo])
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado

		def getEnviosPorFecha(self,registro,desde,hasta,estado,tipo):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id_envio,tipo,detalle,obs,guia
			from envios e inner join asociados a on a.num_reg = e.num_reg
			where e.num_reg = %s and fecha_envio >= %s and fecha_envio <= %s and estado LIKE %s and tipo LIKE %s order by fecha_envio DESC''',[registro,desde,hasta,estado,tipo])
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado

		def getEnvios_ALL(self,estado,tipo):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id_envio,tipo,detalle,obs,guia
			from envios e inner join asociados a on a.num_reg = e.num_reg
			where estado LIKE %s and tipo LIKE %s order by fecha_envio DESC''',[estado,tipo])
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		def getEnvios_ALLporFecha(self,desde,hasta,estado,tipo):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id_envio,tipo,detalle,obs,guia
			from envios e inner join asociados a on a.num_reg = e.num_reg
			where fecha_envio <= %s and fecha_envio >= %s and estado LIKE %s and tipo LIKE %s order by fecha_envio DESC''',[hasta,desde,estado,tipo])
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		

		def agregarGuia(self,guia,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE envios SET guia = (%s) WHERE id_envio = (%s)",([guia,indice]))
			self.conexion.commit()
			cur.close()

		def definirEnvioFacturado(self,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE envios SET estado = 'FACTURADO' WHERE id_envio = (%s)",([indice]))
			self.conexion.commit()
			cur.close()

			
		def traeIndiceGestion(self):
			cur=self.conexion.cursor()
			cur.execute('''select max(indice)+1 from gestiones''')
			self.conexion.commit()
			gestion=cur.fetchone()
			cur.close()
			return gestion
			
		def traerIDgestion(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select gestion from rotulos where indice=%s''',([indice]))
			self.conexion.commit()
			indice=cur.fetchone()
			cur.close()
			return indice
			
		def traeSubpedido(self,num_pedido,fechaSub):
			cur=self.conexion.cursor()
			cur.execute('''select * from subpedidos where num_pedido =%s and fecha_subpedido=%s order by inicio''',([num_pedido,fechaSub]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def traeRangoInicial(self,num_pedido,fechaSub):
			cur=self.conexion.cursor()
			cur.execute('''select min(inicio) from subpedidos where num_pedido =%s and fecha_subpedido=%s order by inicio''',([num_pedido,fechaSub]))
			self.conexion.commit()
			inicial=cur.fetchone()
			cur.close()
			return inicial
			
		
			
			
	
			
			

		






#conexion a base de datos
		#conexion = sqlite3.connect('bd.db')
		#cursor= conexion.cursor()
		#conexion.execute("INSERT INTO pedidos (num_pedido,rncyfs,cantidad,inicio,fin) values (%s,%s,%s,%s,%s)",[Numpedido,registro,cantidad,Rango[0],Rango[0]+cantidad-1])
		#conexion.commit()
		#conexion.close()
		
		#q= bdquery()
		#q.cargabd(Numpedido,registro,cantidad,Rango[0],Rango[0]+cantidad-1)
