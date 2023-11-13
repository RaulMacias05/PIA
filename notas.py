import os
import datetime
import time
from rich import print
from rich.table import Table
from email_validator import validate_email, EmailNotValidError
import sqlite3
from time import sleep
import pandas as pd


def comprobar_servicio(detalles_totales):


    conn = conectar_bd()
    mi_cursor = conn.cursor()
    mi_cursor.execute("SELECT clave, nombre FROM servicios")
    servicios = mi_cursor.fetchall()
    conn.close()

    if servicios:
        print("[#7AFFFF]-- Listado de Servicios Registrados --[/#7AFFFF]")
        for clave, nombre in servicios:
            print(f"Clave: {clave} - Nombre: {nombre}")
    else:
        print("[red]No hay servicios registrados en el sistema[/red]")


    while True:
        try:
            clave_servicio = int(input(f"\nIngrese la clave del servicio {detalles_totales}: Presione -1 para dejar de agregar servicios "))
            if clave_servicio == -1:
                seguir = 20
                servicio = None
                precio_del_servicio = None
                return servicio, precio_del_servicio, seguir


            # Aqui verifico si la clave qu eme dio el usuario esta en la base de datos de la tabla servicios
            conn = conectar_bd()
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT COUNT(*) FROM servicios WHERE clave=?", (clave_servicio,))
            if mi_cursor.fetchone()[0] == 1:

                conn = conectar_bd()
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT nombre FROM servicios WHERE clave = ?", (clave_servicio,))
                servicio = mi_cursor.fetchone()[0] 
                conn.close()

                conn = conectar_bd()
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT costo FROM servicios WHERE clave = ?", (clave_servicio,))
                precio_del_servicio = mi_cursor.fetchone()[0]
                conn.close()

                seguir = False

                return servicio, precio_del_servicio, seguir
            else:
                print("[red]La clave de servicio ingresada no es válida. Intente de nuevo.[/red]")
        except ValueError:
            print("[red]Por favor, ingrese un número entero.[/red]")
        except Exception as e:
            print(f"[red]Ocurrió un error: {e}[/red]")


def comprobar_fecha():
    fecha_actual = datetime.date.today()
    print('[#9999FF](No posterior a la fecha actual)[/#9999FF]')
    while True:
        try:
            while True:
                fecha_proporcionada = input('Fecha de la nota (dd/mm/aaaa): ')
                fecha_de_nota = datetime.datetime.strptime(fecha_proporcionada,"%d/%m/%Y").date()
                if fecha_de_nota <= fecha_actual:
                        break
                else:
                    print('La fecha no puede ser posterior a la actual del sistema\n')
        except ValueError:
            print('Tipo de formato no válido. Intente de nuevo\n')
        except Exception as error:
            print(f'Ocurrió un problema: {error}\n')
        else:
            break

    return fecha_de_nota


def conectar_bd():
        conn = sqlite3.connect("taller_mecanico_DB.db")
        return conn


class RegistrarNota:
    def __init__(self):

        os.system('cls')

        
        self.informacion_de_nota()
        self.detalles_de_nota()
        self.detalles_de_nota_a_str()
        self.retornar_datos()
        self.mostrar_nota()
        self.aceptacion_de_nota()


    def informacion_de_nota(self):
        os.system('cls')
        print('[#7AFFFF]--Listado de clientes existentes, seleccione el cliente que dese hacer la nota--[#/7AFFFF]\n')

        conn = conectar_bd()
        mi_cursor = conn.cursor()
        mi_cursor.execute("SELECT clave, nombre FROM clientes")
        clientes = mi_cursor.fetchall()
        conn.close()

        if clientes:
            print("[#7AFFFF]-- Listado de Clientes Registrados --[/#7AFFFF]")
            for clave, nombre in clientes:
                print(f"Clave: {clave} - Nombre: {nombre}")

            print('[#7AFFFF]--Ingrese el numero de clave del cliente: --[#/7AFFFF]\n')
            clave_cliente = int(input())
            
            # Verificar si la clave existe
            cliente_encontrado = False
            for clave, nombre in clientes:
                if clave == clave_cliente:
                    cliente_encontrado = True
                    break
            
            if not cliente_encontrado:
                print("[red]La clave de cliente ingresada no existe[/red]")
                return
                
            print('[#7AFFFF]--Información de la Nota a Registrar--[#/7AFFFF]\n')

            
            conn = conectar_bd()
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT nombre FROM clientes WHERE clave = ?", (clave_cliente,))
            self.nombre_del_cliente = mi_cursor.fetchall()
            conn.close()

            self.clave_cliente = clave_cliente



            self.fecha_de_nota = comprobar_fecha()
            ##Checar


            conn = conectar_bd()
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT rfc FROM clientes WHERE clave = ?", (clave_cliente,))
            self.RFC_del_cliente = mi_cursor.fetchall()
            conn.close()


            conn = conectar_bd()
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT correo FROM clientes WHERE clave = ?", (clave_cliente,))
            self.correo_del_cliente= mi_cursor.fetchall()
            conn.close()
            

    def detalles_de_nota(self):
        os.system('cls')
        print('[#7AFFFF]--Detalles de la Nota--[#/7AFFFF]\n')

        self.monto_total = 0
        self.detalles = {}

        while True:  
            servicio, precio_del_servicio, seguir = comprobar_servicio(self.detalles)
            if seguir == 20:
                break
                
            

            self.detalles[servicio] = precio_del_servicio
            self.monto_total += precio_del_servicio
        

    def detalles_de_nota_a_str(self):
        self.detallesNota = '[#9999FF]|[/#9999FF] '
        for servicio, precio in self.detalles.items():
            self.detallesNota += f'{servicio}: {precio} [#9999FF]|[/#9999FF] '


    def retornar_datos(self):

        datos_recolectados = (self.fecha_de_nota, self.nombre_del_cliente, self.RFC_del_cliente, self.correo_del_cliente, self.monto_total, self.detallesNota)

        return datos_recolectados

    def mostrar_nota(self):
        os.system('cls')
        nota = Table(title='[#7AFFFF]--Nueva nota registrada--[/#7AFFFF]')
    
        nota.add_column("Detalles", justify="left", style="#9999FF")
        nota.add_column("Datos", justify="left", style="white")

        nota.add_row('Fecha', f'{self.fecha_de_nota}')
        nota.add_row('Nombre del cliente', f'{self.nombre_del_cliente[0][0]}')
        nota.add_row('RFC', f'{self.RFC_del_cliente[0][0]}')
        nota.add_row('Correo', f'{self.correo_del_cliente[0][0]}')
        nota.add_row('Monto a pagar', f'{self.monto_total}')
        nota.add_row('Detalle de nota', f'{self.detallesNota}')
        print(nota, '\n')
    
    def aceptacion_de_nota(self):
        while True:
            aceptar = input('¿Desea registrar esta nota?| s - Sí | n - No |\n\n')
            print()
            if aceptar.upper() in ('S', 'SI', 'SÍ'):

                try:
                    with sqlite3.connect("taller_mecanico_DB.db") as conn:
                        mi_cursor = conn.cursor()

                        datos1 = (self.fecha_de_nota, self.clave_cliente, self.monto_total, 1)

                        mi_cursor.execute("INSERT INTO notas (fecha, cliente, monto, estado) VALUES (?,?,?,?) ", datos1)
                        folio_nota = mi_cursor.lastrowid

                except sqlite3.Error as e:
                    print(f'[red]{e}[/red]')
                    input("Enter")

                except Exception as e:
                    print(f'[red]{e}[/red]')
                    input("Enter")

                finally:
                    if conn:
                        conn.close()

                try:
                    with sqlite3.connect("taller_mecanico_DB.db") as conn:
                        mi_cursor = conn.cursor()

                        for servicio, precio in self.detalles.items():
                            
                            mi_cursor.execute("SELECT clave FROM servicios WHERE nombre = ?", (servicio,))
                            clave_servicio = mi_cursor.fetchone()[0] 
                            
                            precio = precio 

                            datos2 = (folio_nota, clave_servicio)
                            mi_cursor.execute("INSERT INTO detalles_nota VALUES (?,?) ", datos2)

                except sqlite3.Error as e:
                    print(f'[red]{e}[/red]')
                    input("Enter")

                except Exception as e:
                    print(f'[red]{e}[/red]')
                    input("Enter")

                finally:
                    if conn:
                        conn.close()

                for i in range(3):
                    time.sleep(.3)
                    print('[green].[/green]', end='  ')
                print('[green]Registro completado[/green]')
                time.sleep(.8)
                return True
            
            elif aceptar.upper() in ('N', 'NO'):
                for i in range(3):
                    time.sleep(.3)
                    print('[red].[/red]', end='  ')
                print('[red]Registro cancelado[/red]')
                time.sleep(.8)
                return False
            else:
                print('Opción no válida. Intente de nuevo')




class ConsultasYReportes:

    def __init__(self):
        
        while True:
            os.system('cls')
            self.menu_consultas_y_reportes()

            match self.eleccion_consulta:
                case 1:
                    self.consulta_por_periodo()
                case 2:
                    self.consulta_por_folio()
                case 3:
                    break

    def menu_consultas_y_reportes(self):
        print('''
[#9999FF]CONSULTAS Y REPORTES[/#9999FF]
              
[#7AFFFF]--Menú Consultas--[/#7AFFFF]

1 - Consulta por período
2 - Consulta por folio
3 - Volver al menú de notas
              
''')
        while True:
            try:
                self.eleccion_consulta = int(input('Elija una opción (indicando su respectivo número): '))
            except ValueError:
                print('Opción no válida. Intente de nuevo')
            else:
                if self.eleccion_consulta > 0 and self.eleccion_consulta <= 4:
                    break
                else:
                    print('Opción no válida. Intente de nuevo')
        
                    
    def consulta_por_periodo(self):

        os.system('cls')

        print('[#7AFFFF]--Consulta por periodo--[#/7AFFFF]\n')
        
        while True:
            try:
                self.respuesta = input('Ingrese su fecha inicial (dd/mm/aaaa) o presione enter para omitir y se le designara la fecha inicial en 01/01/2000:  ')
                if self.respuesta == "":
                    self.fecha_inicial = datetime.datetime.strptime("01/01/2000","%d/%m/%Y").date()
                else:
                    self.fecha_inicial = datetime.datetime.strptime(self.respuesta,"%d/%m/%Y").date()
        
                while True:
                    self.respuesta = input('Ingrese su fecha final (dd/mm/aaaa) o presione enter para asignar la fecha actual del sistema como fecha final: ')
                    if self.respuesta == "":
                        self.fecha_final = datetime.date.today()
                        break
                    else:
                        self.respuesta = datetime.datetime.strptime(self.respuesta,"%d/%m/%Y").date()
                        if self.respuesta >= self.fecha_inicial:
                            self.respuesta = datetime.datetime.strftime(self.respuesta,"%d/%m/%Y")
                            self.fecha_final = datetime.datetime.strptime(self.respuesta,"%d/%m/%Y").date()
                            break
                        else:
                            print ("La fecha final debe ser igual o posterior a la fecha inicial, intentelo de nuevo")

                
            except ValueError:
                print('Tipo de formato no válido. Intente de nuevo\n')
            except Exception as error:
                print(f'Ocurrió un problema: {error}\n')
            else:
                break

        notas_del_periodo = Table(title="\n[#7AFFFF]--Notas dentro del perído--[/#7AFFFF]")
        notas_del_periodo.add_column("Folio", justify="left", style="#9999FF")
        notas_del_periodo.add_column("Fecha", justify="left", style="white")
        notas_del_periodo.add_column("Cliente", justify="left", style="white")
        notas_del_periodo.add_column("Monto", justify="left", style="white")
        
        conn = conectar_bd()
        mi_cursor = conn.cursor()
        mi_cursor.execute("SELECT folio, fecha, cliente, monto FROM notas WHERE estado = 1")
        registros = mi_cursor.fetchall()

        contador = 0
        lista_folios =  []
        lista_notas = []
        suma_montos = 0
        for folio, fecha, cliente, monto in registros:
            fecha_convertida = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_convertida >= self.fecha_inicial and fecha_convertida <= self.fecha_final:
                notas_del_periodo.add_row(str(folio), fecha, str(cliente), str(monto))
                lista_folios.append(folio)
                lista_notas.append([fecha, cliente, monto])
                contador += 1
        
        print (f"Se esta haciendo una consulta por periodo de la fecha {self.fecha_inicial} a  {self.fecha_final}")

        if contador == 0:
            print('\n[red]No existen notas dentro de este período[/red]\n')
        else:
            print(notas_del_periodo)
            suma_montos = 0
            for folio in lista_folios:
                mi_cursor.execute("SELECT monto FROM notas WHERE folio = ? AND estado = 1", (folio,))
                registro = mi_cursor.fetchone()

                for monto in registro:
                    suma_montos += monto

            promedio_montos = suma_montos / len(lista_folios) 
            print (f"El promedio de los montos en este periodo es: {promedio_montos}")
                
            input('Presione Enter para continuar\n')

            df_lista_notas = pd.DataFrame(lista_notas)
            df_lista_notas.columns = ["Fecha", "Cliente", "Monto"]
            df_lista_notas.index = lista_folios
            
            self.menu_exportacion(df_lista_notas, self.fecha_inicial, self.fecha_final)

    
    def consulta_por_folio(self):

        os.system('cls')

        print('[#7AFFFF]--Consulta por folio--[#/7AFFFF]\n')

        try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT N.folio, N.fecha, C.nombre FROM notas AS N\
                                  JOIN clientes AS C ON N.cliente = C.clave WHERE estado = 1 ORDER BY folio")
                registros = mi_cursor.fetchall()
                
                t_notas_actuales = Table(title=f'[#7AFFFF]--Notas en el sistema--[/#7AFFFF]')

                t_notas_actuales.add_column("Folio", justify="center", style="#9999FF")
                t_notas_actuales.add_column("Fecha", justify="center", style="white")
                t_notas_actuales.add_column("Nombre del Cliente", justify="center", style="white")

                for folio, fecha, nombre in registros:
                    t_notas_actuales.add_row(str(folio), fecha, nombre)

                print(t_notas_actuales)

        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()

        print('\n[#9999FF](En número entero)[#/9999FF]')
         
        while True:
            try:
                folio_consutado = int(input('Folio a Consultar: '))
            except ValueError:
                print('Ese no es un número válido.\n')
            except Exception as error:
                print('Ocurrió un problema. Intente de nuevo')
            else:
                try:
                    with sqlite3.connect("taller_mecanico_DB.db") as conn:
                        mi_cursor = conn.cursor()
                        mi_cursor.execute("SELECT N.folio, N.fecha, C.nombre, C.rfc, C.correo, N.monto, S.nombre, S.costo \
                                          FROM notas AS N\
                                          JOIN clientes AS C ON N.cliente = C.clave \
                                          JOIN detalles_nota AS D ON D.folio_nota = N.folio\
                                          JOIN servicios AS S ON D.clave_servicio = S.clave\
                                          WHERE folio = ? AND estado = 1", (folio_consutado,))
                        registros = mi_cursor.fetchall()
                except sqlite3.Error as e:
                    print(e)
                except Exception as e:
                    print(e)
                finally:
                    if conn:
                        conn.close()
                
                if registros:
                    break
                else:
                    print("La nota no se encuentra en el sistema o corresponde a una nota cancelada, vuelve a intentarlo\n")
                    input('Presione Enter para continuar')
                    return True

        os.system('cls')
        
        nota_consultada = Table(title=f'[#7AFFFF]--Nota consultada--[/#7AFFFF]')

        nota_consultada.add_column("Detalles", justify="left", style="#9999FF")
        nota_consultada.add_column("Datos", justify="left", style="white")

        nota_consultada.add_row('Folio', str(registros[0][0]))
        nota_consultada.add_row('Fecha', str(registros[0][1]))
        nota_consultada.add_row('Nombre del cliente', registros[0][2])
        nota_consultada.add_row('RFC', registros[0][3].upper())
        nota_consultada.add_row('Correo', registros[0][4])
        nota_consultada.add_row('Monto a pagar', str(registros[0][5]))
        nota_consultada.add_row('Detalle de nota', self.detalles_de_nota_a_str(registros))

        print(nota_consultada)

        input('Presione Enter para continuar\n')
    
    def detalles_de_nota_a_str(self, registros):
        detallesNota = '[#9999FF]|[/#9999FF] '
        for _,_,_,_,_,_, servicio, precio in registros:
            detallesNota += f'{servicio}: {precio} [#9999FF]|[/#9999FF] '
        return detallesNota
    
    def menu_exportacion(self, df_lista_notas, fecha_inicial, fecha_final):
        print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
            
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al menú de reportes
                          
''')    
        fecha_inicial = fecha_inicial.strftime('%m-%d-%Y')
        fecha_final = fecha_final.strftime('%m-%d-%Y')

        while True:
            seleccion_exportacion = input('Seleccione el tipo de exportación deseada: ')

            if seleccion_exportacion == '1':
                df_lista_notas.to_csv(f'ReportePorPeriodo_{fecha_inicial}_{fecha_final}.csv')
                break

            elif seleccion_exportacion == '2': 
                df_lista_notas.to_excel((f'ReportePorPeriodo_{fecha_inicial}_{fecha_final}.xlsx'))
                break

            elif seleccion_exportacion == '3': 
                return
            else: 
                print('Opcion no existente.')
                input('Presione Enter para continuar')

class CancelarNota:

    
    def __init__(self):
        self.ProcesoCancelacion()

    def ProcesoCancelacion(self):
        os.system('cls')
        try:
            FolioACancelar = int(input("\nIngrese el folio de la nota que desea cancelar: "))

            conn = conectar_bd()
            mi_cursor = conn.cursor()

            # Verificamos si la nota existe y no está cancelada
            mi_cursor.execute("SELECT * FROM notas WHERE folio = ? AND estado = 1", (FolioACancelar,))
            nota = mi_cursor.fetchone()

            if nota:
                print("[#7AFFFF]-- Detalles de la Nota a Cancelar --[/#7AFFFF]\n")
                print(f"Folio: {nota[0]}")
                print(f"Fecha: {nota[1]}")
                print(f"Cliente: {nota[2]}")
                print(f"Monto Total: {nota[3]}")

                confirmar = input("\n¿Desea cancelar esta nota? (s/n): ")

                if confirmar.lower() == 's':
                    # Actualizamos el estado de la nota a cancelada
                    mi_cursor.execute("UPDATE notas SET estado = 0 WHERE folio = ?", (FolioACancelar,))
                    conn.commit()
                    print("\n[green]La nota ha sido cancelada con éxito[/green]")
                else:
                    print("\n[red]La nota no ha sido cancelada[/red]")
            else:
                print("[red]La nota no se encuentra en el sistema o ya ha sido cancelada[/red]")
                sleep(2)


        except ValueError:
            print("[red]Ingrese solo números enteros[/red]")
        except Exception as error:
            print(f"[red]Ocurrió un problema: {error}[/red]")
        finally:
            if conn:
                conn.close()

class RecuperarNota:

    def __init__(self):
        self.mostrar_notas_canceladas()

    def mostrar_notas_canceladas(self):
        self.conn = sqlite3.connect("taller_mecanico_DB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT folio, fecha, cliente, monto FROM notas WHERE estado = 0")
        notas_canceladas = self.cursor.fetchall()
        self.conn.close()

        if notas_canceladas:
            print(f"Estos son los folios que están en estado de cancelación: \n")
            print("{:<10} {:<10} {:<20} {:<15}".format('Folio', 'Fecha', 'Cliente', 'Monto'))
            print("="*55)
            for nota in notas_canceladas:
                print("{:<10} {:<10} {:<20} {:<15}".format(nota[0], nota[1], nota[2], nota[3]))
            folio = input("\nIngrese el folio de la nota que desea recuperar (o presione Enter para cancelar): ")

            if folio:
                self.recuperar_nota(folio)
        else:
            print("No hay notas canceladas para recuperar.")

    def recuperar_nota(self, folio):
        self.conn = sqlite3.connect("taller_mecanico_DB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM notas WHERE folio = ? AND estado = 0", (folio,))
        nota_cancelada = self.cursor.fetchone()

        if nota_cancelada:
            print("\nDetalle de la nota a recuperar:")
            print("{:<10} {:<10} {:<20} {:<10} {:<10}".format('Folio', 'Fecha', 'Cliente', 'Monto', 'Estado'))
            print("="*55)
            print("{:<10} {:<10} {:<20} {:<10} {:<10}".format(nota_cancelada[0], nota_cancelada[1], nota_cancelada[2], nota_cancelada[3], nota_cancelada[4]))
            
            confirmacion = input("\n¿Desea recuperar esta nota? (S/N): ")
            
            if confirmacion.lower() == 's':
                self.cursor.execute("UPDATE notas SET estado = 1 WHERE folio = ?", (folio,))
                self.conn.commit()
                print(f"Nota con folio {folio} recuperada exitosamente.")
                sleep(2)
            else:
                print(f"Recuperación de nota cancelada para el folio {folio}.")
                sleep(2)
        else:
            print(f"No se encontró ninguna nota cancelada con el folio {folio}.")
            sleep(2)

        self.conn.close()
       
            





##Apartir de aqui empiezan las modificaciones

class Menu:
    def __init__(self) -> None:

        while True:

            self.mostrar_menu()
            
            match self.eleccion_del_menu:
                case 1:
                    self.RegistrarNota()
                case 2:
                    self.CancelarNota()
                case 3:
                    self.RecuperarNota()
                case 4:
                    self.ConsultasYReportes()
                case 5:
                    break
    
    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]CLIENTES[/#9999FF]

[#7AFFFF]--Menú Notas--[/#7AFFFF]
              
1 - Registrar una nota
2 - Cancelar una nota
3 - Recuperar una nota
4 - Consultas y Reportes
5 - Volver al menu principal
              
''')
        while True:
            try:
                self.eleccion_del_menu = int(input('Elija una opción (indicando su respectivo número): '))
            except ValueError:
                print('Opción no válida. Intente de nuevo')
            else:
                if self.eleccion_del_menu > 0 and self.eleccion_del_menu <= 5:
                    break
                else:
                    print('Opción no válida. Intente de nuevo')

    def RegistrarNota(self):
        RegistrarNota()

    def CancelarNota(self):
        CancelarNota()

    def RecuperarNota(self):
        RecuperarNota()
    
    def ConsultasYReportes(self):
        ConsultasYReportes()
