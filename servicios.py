import sqlite3
from sqlite3 import Error
from rich import print
from rich.table import Table
import os
from time import sleep
import pandas as pd
import datetime


def comprobar_nombre():
    while True:
        nombre_del_servicio = input('\nNombre del servicio: ')
        if nombre_del_servicio.strip():
            break
        else:
            print('El nombre del servicio no debe quedar vacío. Intente de nuevo')

    return nombre_del_servicio

def comprobar_costo():
    while True:
        try:
            costo_servicio = float(input("Costo del servicio: "))
            if costo_servicio > 0.00:
                break
            else:
                print('El costo debe ser superior a 0.00. Intente de nuevo')
        except ValueError:
            print('El costo debe ser un número entero o con decimales')
    return costo_servicio

def listado():

    os.system('cls')

    try:
        with sqlite3.connect("taller_mecanico_DB.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT clave, nombre FROM servicios WHERE estado = 1")
            registros = mi_cursor.fetchall()

            if registros:
                print("Claves\tNombre")
                print("*" * 30)
                for clave, nombre in registros:
                    print(f"{clave:^6}\t{nombre}")
                return True

            else:
                print("No se encontraron registros en la respuesta")
                input('Enter')
                return False

    except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input("Enter")
            return False

    except Exception as e:
            print(f'[red]{e}[/red]')
            input("Enter")
            return False

    finally:
            if conn:
                conn.close()


class Menu:
    def __init__(self) -> None:

        while True:

            self.mostrar_menu()
            
            match self.eleccion_del_menu:
                case 1:
                    self.agregar_servicio()
                case 2:
                    self.suspender_servicio()
                case 3:
                    self.recuperar_servicio()        
                case 4:
                    self.consultasyReportes()
                case 5:
                    break
    
    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]CLIENTES[/#9999FF]

[#7AFFFF]--Menú Servicios--[/#7AFFFF]
              
1 - Agregar un Servicio
2 - Suspender un Servicio
3 - Recuperar un Servicio
4 - Consultas y Reportes de Servicios
5 - Volver al Menú Principal
              
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


    def agregar_servicio(self):

        os.system('cls')

        nombre = comprobar_nombre()

        costo = comprobar_costo()

        try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:

                mi_cursor = conn.cursor()

                valores = {"nombre": nombre, "costo": costo, "estado": 1}

                mi_cursor.execute("INSERT INTO servicios (nombre, costo, estado) \
                                VALUES (:nombre, :costo, :estado)", valores)
                
                print()
                for i in range(3):
                    print("[green].[/green]", end = ' ')
                    sleep(.3)
                print("[green]Servicio agregado[/green]")
                sleep(1)

        except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        except Exception as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        finally:
            if conn:
                conn.close()

    def suspender_servicio(self):
        while True:
            os.system('cls')
            print('''
    [#9999FF]SUSPENDER SERVICIO[/#9999FF]
                
    [#7AFFFF]--Suspender Servicio--[/#7AFFFF]
    ''')
            t_servicio = Table()
            t_servicio.add_column("Clave", justify="left", style="#9999FF")
            t_servicio.add_column("Nombre", justify="left", style="#9999FF")

            try: 
                with sqlite3.connect("taller_mecanico_DB.db") as conn:
                    mi_cursor = conn.cursor()

                    mi_cursor.execute("SELECT clave, nombre FROM servicios WHERE estado = 1")
                    registros = mi_cursor.fetchall()

                    if not registros:
                        print('\n[red]No hay servicios activos.[/red]')
                        input('\nPresione Enter para continuar\n')
                        return
                    
                    t_servicio.title = '[#7AFFFF]--Servicios activos--[/#7AFFFF]'
                    for clave, nombre in registros:
                        t_servicio.add_row(str(clave), nombre)

                    os.system('cls')
                    print(t_servicio)

                    while True:
                        try:
                            clave_servicio_a_suspend = int(input("Seleccione la clave del servicio a suspender (ingrese 0 para volver): "))

                            if clave_servicio_a_suspend == 0:
                                return
                            
                            mi_cursor.execute("SELECT * FROM servicios WHERE clave=? AND estado = 1", (clave_servicio_a_suspend,))
                            servicio = mi_cursor.fetchone()

                            if not servicio:
                                print("\n[red]Servicio no encontrado.[/red]")
                                input('\nPresione Enter para continuar\n')
                                break

                            print("\nDetalles del Servicio a Suspender:")
                            print(f"Clave: {servicio[0]}")
                            print(f"Nombre: {servicio[1]}")
                            print(f"Costo: {servicio[2]}")

                            while True:
                                confirmacion = input("\n¿Desea suspender este servicio? (s/n): ").upper()

                                if confirmacion.lower() in ('s', 'si', 'sí'):
                                    mi_cursor.execute("UPDATE servicios SET estado = 0 WHERE clave=?", (clave_servicio_a_suspend,))
                                    conn.commit()

                                    print("\n[green]Servicio suspendido correctamente.[/green]")
                                    input('\nPresione Enter para continuar\n')
                                    break
                                
                                elif confirmacion.lower() in ('n', 'no'):
                                    print("\n[green]Suspensión cancelada.[/green]")
                                    input('\nPresione Enter para continuar\n')
                                    break
                                
                                else:
                                    print('Opción no válida. Intente de nuevo\n')
                            
                            break

                        except ValueError:
                            print('\n[red]La clave tiene que ser un número entero[/red]\n')

                        except Exception as e: 
                            print(f'\nSe produjo el siguiente error: {e}') 
                            input('\nPresione Enter para continuar\n')
                            break


            except sqlite3.Error as e:
                print(f'[red]{e}[/red]')
                input('\nPresione Enter para continuar\n')
                break

            except Exception as e: 
                print(f'[red]Se produjo el siguiente error: {e}[/red]') 
                input('\nPresione Enter para continuar\n')
                break

            finally: 
                if conn:
                    conn.close()

    def recuperar_servicio(self):
        while True:
            os.system('cls')
            print('''
    [#9999FF]RECUPERAR SERVICIO[/#9999FF]
                
    [#7AFFFF]--Recuperar Servicio--[/#7AFFFF]
    ''')
            t_servicio = Table()
            t_servicio.add_column("Clave", justify="left", style="#9999FF")
            t_servicio.add_column("Nombre", justify="left", style="#9999FF")

            try: 
                with sqlite3.connect("taller_mecanico_DB.db") as conn:
                    mi_cursor = conn.cursor()

                    mi_cursor.execute("SELECT clave, nombre FROM servicios WHERE estado = 0")
                    registros = mi_cursor.fetchall()

                    if not registros:
                        print('\n[red]No hay servicios suspendidos.[/red]')
                        input('\nPresione Enter para continuar\n')
                        return
                    
                    t_servicio.title = '[#7AFFFF]--Servicios actualmente suspendidos--[/#7AFFFF]'
                    for clave, nombre in registros:
                        t_servicio.add_row(str(clave), nombre)

                    os.system('cls')
                    print(t_servicio)

                    while True:
                        try:
                            clave_servicio_a_recuperar = int(input("Seleccione la clave del servicio a recuperar (ingrese 0 para volver): "))

                            if clave_servicio_a_recuperar == 0:
                                return
                            
                            mi_cursor.execute("SELECT * FROM servicios WHERE clave=? AND estado = 0", (clave_servicio_a_recuperar,))
                            servicio = mi_cursor.fetchone()

                            if not servicio:
                                print("\n[red]La clave no corresponde a un servicio suspendido[/red]")
                                input('\nPresione Enter para continuar\n')
                                break

                            print("\nDetalles del Servicio a Recuperar:")
                            print(f"Clave: {servicio[0]}")
                            print(f"Nombre: {servicio[1]}")
                            print(f"Costo: {servicio[2]}")

                            while True:
                                confirmacion = input("\n¿Desea recuperar este servicio? (s/n): ").upper()

                                if confirmacion.lower() in ('s', 'si', 'sí'):
                                    mi_cursor.execute("UPDATE servicios SET estado = 1 WHERE clave=?", (clave_servicio_a_recuperar,))
                                    conn.commit()

                                    print("\n[green]Servicio recuperado correctamente.[/green]")
                                    input('\nPresione Enter para continuar\n')
                                    break
                                
                                elif confirmacion.lower() in ('n', 'no'):
                                    print("\n[green]Recuperación cancelada.[/green]")
                                    input('\nPresione Enter para continuar\n')
                                    break
                                
                                else:
                                    print('Opción no válida. Intente de nuevo\n')
                            
                            break

                        except ValueError:
                            print('\n[red]La clave tiene que ser un número entero[/red]\n')

                        except Exception as e: 
                            print(f'\nSe produjo el siguiente error: {e}') 
                            input('\nPresione Enter para continuar\n')
                            break


            except sqlite3.Error as e:
                print(f'[red]{e}[/red]')
                input('\nPresione Enter para continuar\n')
                break

            except Exception as e: 
                print(f'[red]Se produjo el siguiente error: {e}[/red]') 
                input('\nPresione Enter para continuar\n')
                break

            finally: 
                if conn:
                    conn.close()                        

    def consultasyReportes(self):

        while True:
            os.system('cls')

            print(f'''
[#9999FF]CONSULTAS Y REPORTES DE SERVICIOS[/#9999FF]

[#7AFFFF]--Menú Consultas de Servicios--[/#7AFFFF]
            
1 - Búsqueda por clave de servicio
2 - Búsqueda por nombre de servicio
3 - Listado de servicios
4 - Volver al Menú de Servicios
            
''')
            while True:
                try:
                    self.eleccion_del_menu = int(input('Elija una opción (indicando su respectivo número): '))
                except ValueError:
                    print('Opción no válida. Intente de nuevo')
                else:
                    if self.eleccion_del_menu > 0 and self.eleccion_del_menu <= 4:
                        break
                    else:
                        print('Opción no válida. Intente de nuevo') 

            if self.eleccion_del_menu == 1:

                os.system('cls')
                
                while True:
                    registros = listado()
                    if not registros:
                        break

                    try:
                        with sqlite3.connect("taller_mecanico_DB.db") as conn:
                            mi_cursor = conn.cursor()

                            valor_clave = int(input("\nIngrese la clave del servicio para conocer su detalle: "))
                            valores = {"clave":valor_clave}
                            mi_cursor.execute("SELECT * FROM servicios WHERE clave = :clave AND estado = 1", valores)
                            registros = mi_cursor.fetchall()

                            os.system('cls')
                            if registros:
                                print("{:<10} {:<20} {:<10}".format('Clave', 'Nombre', 'Costo'))
                                print("*" * 50)
                                for clave, nombre, costo, estado in registros:
                                    print("{:<10} {:<20} {:<10}".format(clave, nombre, costo))
                                input('Enter')
                                break
                            else:
                                print(f"No se encontraron registros activos con la clave {valor_clave}")
                                input('enter')
                                break
                    
                    except ValueError:
                        print('[red]La clave debe ser un número entero[/red]')
                        input('Enter')
                    except sqlite3.Error as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    except Exception as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    finally:
                        if conn:
                            conn.close()

            elif self.eleccion_del_menu == 2:

                nombre_servicio = input("Ingrese el nombre del servicio a buscar: ")

                os.system('cls') 

                while True:
                    try:
                        with sqlite3.connect("taller_mecanico_DB.db") as conn:
                            mi_cursor = conn.cursor()
                            valor = {"nombre":nombre_servicio}
                            mi_cursor.execute("SELECT * FROM servicios WHERE UPPER(nombre) = UPPER(:nombre) AND estado = 1", valor)
                            registro = mi_cursor.fetchall()

                            if registro:
                                print("{:<10} {:<20} {:<10}".format('Clave', 'Nombre', 'Costo'))
                                print("*" * 50)
                                for clave, nombre, costo, estado in registro:
                                    print("{:<10} {:<20} {:<10}".format(clave, nombre, costo))
                                input('Enter')
                                break
                            else:
                                print(f"No se encontraron servicios activos con el nombre {nombre_servicio}")
                                input("\nPresione ENTER para volver al menú anterior")
                                break

                    except sqlite3.Error as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    except Exception as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    finally:
                        if conn:
                            conn.close()
            
            elif self.eleccion_del_menu == 3:
                self.listado_de_servicios()

            elif self.eleccion_del_menu == 4:
                break

            else:
                print('Opción no válida. Intente de nuevo')   


    def listado_de_servicios(self):
        while True:
            os.system('cls')
            print('''
[#9999FF]CONSULTAS Y REPORTES DE Servicios[/#9999FF]
            
[#7AFFFF]--Menú Consultas de Servicios--[/#7AFFFF]

1 - Ordenados por clave
2 - Ordenados por nombre
3 - Regresar al Menú de Consultas de Servicios
            
''')
            tabla_servicios = Table()
            tabla_servicios.add_column("Clave", justify="left", style="#9999FF")
            tabla_servicios.add_column("Nombre", justify="left", style="#9999FF")
            tabla_servicios.add_column("Costo", justify="left", style="#9999FF")


            try:
                with sqlite3.connect("taller_mecanico_DB.db") as conn:
                    mi_cursor = conn.cursor()
                    tipo_consulta = input("Seleccione el tipo de orden del listado que desea: ")
                    if tipo_consulta == "1":
                        mi_cursor.execute("SELECT * FROM servicios WHERE estado = 1 ORDER BY clave")
                        registros = mi_cursor.fetchall()
                        listaservicios=[]
                        listaclaves=[]
                        if registros: 
                            tabla_servicios.title = '[#7AFFFF]--Servicios ordenados por su clave--[/#7AFFFF]'
                            for clave, nombre, costo, estado in registros:
                                tabla_servicios.add_row(str(clave), nombre, str(costo))
                                listaclaves.append(clave)
                                listaservicios.append([nombre, costo])
                                os.system('cls')
                            print(tabla_servicios) 
                            print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
            
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al Menú de Listado de Servicios
            
''')
                            while True:
                                tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                                df_listaservicios = pd.DataFrame(listaservicios)
                                df_listaservicios.columns = ["Nombre", "Costo"]
                                df_listaservicios.index = listaclaves
                                Fecha_de_reporte =  datetime.date.today()
                                Fecha_de_reporte = datetime.date.today().strftime('%m-%d-%Y')

                                if tipo_exportacion == "1":
                                    df_listaservicios.to_csv(f"ReporteServiciosPorClave_{Fecha_de_reporte}.csv")
                                    break
                                elif tipo_exportacion == "2":
                                    df_listaservicios.to_excel(f"ReporteServiciosPorClave_{Fecha_de_reporte}.xlsx")
                                    break
                                elif tipo_exportacion == '3': 
                                    break
                                else: 
                                    print('Opcion no existente.')
                                    input('Presione Enter para continuar')
                            
                        else: 
                            print('No se encontraron registros')
                            input('Presione Enter para continuar')

                    elif tipo_consulta == "2":
                        mi_cursor.execute("SELECT * FROM servicios WHERE estado = 1 ORDER BY nombre")
                        registros = mi_cursor.fetchall()
                        listaservicios=[]
                        listaclaves=[]
                        if registros: 
                            tabla_servicios.title = '[#7AFFFF]--Servicios ordenados por su nombre--[/#7AFFFF]'
                            for clave, nombre, costo, estado in registros:
                                tabla_servicios.add_row(str(clave), nombre, str(costo))
                                listaclaves.append(clave)
                                listaservicios.append([nombre, costo])
                            os.system('cls')
                            print(tabla_servicios) 
                            print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
        
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al Menú de Listado de Servicios
        
''')
                            while True:
                                tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                                df_listaservicios =pd.DataFrame(listaservicios)
                                df_listaservicios.columns = ["Nombre", "Costo"]
                                df_listaservicios.index = listaclaves
                                Fecha_de_reporte =  datetime.date.today()
                                Fecha_de_reporte = datetime.date.today().strftime('%m-%d-%Y')

                                if tipo_exportacion == "1":
                                    df_listaservicios.to_csv(f"ReporteServiciosPorNombre_{Fecha_de_reporte}.csv")
                                    break
                                elif tipo_exportacion == "2":
                                    df_listaservicios.to_excel(f"ReporteServiciosPorNombre_{Fecha_de_reporte}.xlsx")
                                    break
                                elif tipo_exportacion == '3':
                                    break  
                                        
                                else: 
                                    print('Opción no existente.')
                                    input('Presione Enter para continuar')

                        else: 
                            print('No se encontraron registros')
                            input('Presione Enter para continuar')

                    elif tipo_consulta == "3":
                        break
                            
                    else:
                        print('No es una opción válida.')
                        input('Presione Enter para continuar') 

            except sqlite3.Error as e:
                print(e)
                input('Presione Enter para continuar')

            except Exception as e: 
                print(f'Se produjo el siguiente error: {e}') 
                input('Presione Enter para continuar')

            finally: 
                if conn:
                    conn.close()     