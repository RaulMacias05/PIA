import datetime
import sqlite3
from rich import print
import os
import pandas as pd 
from rich.table import Table  

class Menu:
    def __init__(self) -> None:
        while True:

            self.mostrar_menu()

            match self.eleccion_del_menu:
                case 1:
                    ServiciosMasPrestados()
                case 2:
                    ClientesConMasNotas()
                case 3:
                    PromedioMontos()
                case 4:
                    break


    def mostrar_menu(self):
        os.system('cls')
        print('''
[#9999FF]ESTADÍSTICAS[/#9999FF]

[#7AFFFF]--Menú estadísticas--[/#7AFFFF]
              
1 - Servicios más prestados
2 - Clientes con más notas
3 - Promedio de los montos de las notas
4 - Volver al Menú Principal
              
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

class ServiciosMasPrestados:
    def __init__(self):
        self.definir_rango_fechas()
        self.obtener_ranking()

    def definir_rango_fechas(self):
        os.system('cls')
        while True:
            try:

                fecha_inicial = input("Ingesa la fecha inicial del periodo a reportar en formato(dd/mm/aaaa): ")
                self.fecha_inicial = datetime.datetime.strptime(fecha_inicial,"%d/%m/%Y").date()

                while True:
                    fecha_final = input("Ingresa la fecha final del periodo a reportar en formato(dd/mm/aaaa): ")
                    self.fecha_final = datetime.datetime.strptime(fecha_final,"%d/%m/%Y").date()

                    if self.fecha_final < self.fecha_inicial:
                        print('\n[red]La fecha final debe ser mayor o igual a la fecha inicial[/red]\n')
                    else:
                        break

            except ValueError:
                print('\n[red]Tipo de formato de fecha no válido[red]\n')
            except Exception as e:
                print(e)
            else:
                break 
        
    def obtener_ranking(self): 
            try: 
                with sqlite3.connect("taller_mecanico_DB.db") as conn: 
                    mi_cursor = conn.cursor() 
                    cantidad = int(input('Ingrese cantidad de servicios a identificar: '))

                    if cantidad <= 0: 
                        print('\n[red]No se puede solicitar un ranking de dicha cifra.[/red]')
                        input('\nPresione Enter para continuar\n')
                        return
                    
                    valores = {"fecha_inicial":self.fecha_inicial, "fecha_final":self.fecha_final,
                               "cantidad":cantidad}
                    
                    mi_cursor.execute("SELECT S.nombre, COUNT(D.clave_servicio)\
                                      FROM servicios AS S \
                                      JOIN detalles_nota AS D ON S.clave = D.clave_servicio \
                                      JOIN notas AS N ON N.folio = D.folio_nota \
                                      WHERE (N.fecha BETWEEN :fecha_inicial AND :fecha_final) \
                                      AND N.estado = 1 AND S.estado = 1 \
                                      GROUP BY clave_servicio \
                                      ORDER BY COUNT(clave_servicio) DESC LIMIT :cantidad", valores)
                    
                    registros = mi_cursor.fetchall()

                    if not registros:
                        print('\n[red]No existen registros dentro del periodo[/red]')
                        input('\nPresione Enter para continuar\n')
                        return

                    t_servicios_top = Table(title = f'[#7AFFFF]--Top {cantidad} de servicios más prestados--[/#7AFFFF]')

                    t_servicios_top.add_column("Nombre", justify="left", style="#9999FF")
                    t_servicios_top.add_column("Veces que se solicitó", justify="center", style="white")

                    for registro in registros:
                        t_servicios_top.add_row(registro[0], str(registro[1]))
                    
                    print(t_servicios_top)

                    df_registros = pd.DataFrame(registros)
                    df_registros.columns = ["Nombre", "Veces que se solicitó"]

                    print('''
[#9999FF]EXPORTACIÓN DE RESULTADO[/#9999FF]
        
[#7AFFFF]--Menú Exportación de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al Menú de Estadísticas
        
''')
                    while True:
                        tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                        if tipo_exportacion == "1":
                            df_registros.to_csv(f"ReporteServiciosMasPrestados_{self.fecha_inicial}_{self.fecha_final}.csv")
                            break
                        elif tipo_exportacion == "2":
                            df_registros.to_excel(f"ReporteServiciosMasPrestados_{self.fecha_inicial}_{self.fecha_final}.xlsx")
                            break
                        elif tipo_exportacion == '3':
                            break  
                                
                        else: 
                            print('Opción no existente.')
                            input('Presione Enter para continuar')
            
            except sqlite3.Error as e:
                print(f'[red]{e}[/red]')
                input('\nPresiona Enter para continuar\n')
            except Exception as e: 
                print(f'[red]{e}[/red]')
                input('\nPresiona Enter para continuar\n')

class ClientesConMasNotas:
    def __init__(self):
        self.definir_rango_fechas()
        self.obtener_ranking()

    def definir_rango_fechas(self):
        os.system('cls')
        while True:
            try:

                fecha_inicial = input("Ingesa la fecha inicial del periodo a reportar en formato(dd/mm/aaaa): ")
                self.fecha_inicial = datetime.datetime.strptime(fecha_inicial,"%d/%m/%Y").date()

                while True:
                    fecha_final = input("Ingresa la fecha final del periodo a reportar en formato(dd/mm/aaaa): ")
                    self.fecha_final = datetime.datetime.strptime(fecha_final,"%d/%m/%Y").date()

                    if self.fecha_final < self.fecha_inicial:
                        print('\n[red]La fecha final debe ser mayor a la fecha inicial[/red]\n')
                    else:
                        break

            except ValueError:
                print('\n[red]Tipo de formato de fecha no válido[red]\n')
            except Exception as e:
                print(e)
            else:
                break 
        
    def obtener_ranking(self): 
            try: 
                with sqlite3.connect("taller_mecanico_DB.db") as conn: 
                    mi_cursor = conn.cursor() 
                    cantidad = int(input('Ingrese cantidad de clientes a identificar: '))
                    if cantidad <= 0: 
                        print('\n[red]No se puede solicitar un ranking de dicha cifra.[/red]')
                        input('\nPresione Enter para continuar\n')
                        return
                         
                    valores = {"fecha_inicial":self.fecha_inicial, "fecha_final":self.fecha_final,
                               "cantidad":cantidad}
                    
                    mi_cursor.execute("SELECT C.NOMBRE, COUNT(C.clave) \
                                      FROM clientes AS C \
                                      JOIN notas AS N ON C.clave = N.cliente \
                                      WHERE (N.fecha BETWEEN :fecha_inicial AND :fecha_final) \
                                      AND N.estado = 1 AND C.estado = 1 \
                                      GROUP BY C.clave \
                                      ORDER BY COUNT(C.clave) DESC LIMIT :cantidad", valores)
                    
                    registros = mi_cursor.fetchall()

                    if not registros:
                        print('\n[red]No existen registros dentro del periodo[/red]')
                        input('\nPresione Enter para continuar\n')
                        return

                    t_servicios_top = Table(title = f'[#7AFFFF]--Top {cantidad} de clientes con más notas--[/#7AFFFF]')

                    t_servicios_top.add_column("Nombre", justify="left", style="#9999FF")
                    t_servicios_top.add_column("# notas registradas", justify="center", style="white")

                    for registro in registros:
                        t_servicios_top.add_row(registro[0], str(registro[1]))
                    
                    print(t_servicios_top)

                    df_registros = pd.DataFrame(registros)
                    df_registros.columns = ["Nombre", "# notas registradas"]

                    print('''
[#9999FF]EXPORTACIÓN DE RESULTADO[/#9999FF]
        
[#7AFFFF]--Menú Exportación de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al Menú de Estadísticas
        
''')
                    while True:
                        tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                        if tipo_exportacion == "1":
                            df_registros.to_csv(f"ReporteClientesConMasNotas_{self.fecha_inicial}_{self.fecha_final}.csv")
                            break
                        elif tipo_exportacion == "2":
                            df_registros.to_excel(f"ReporteClientesConMasNotas_{self.fecha_inicial}_{self.fecha_final}.xlsx")
                            break
                        elif tipo_exportacion == "3":
                            break  
                                
                        else: 
                            print('Opción no existente.')
                            input('Presione Enter para continuar')

            except Exception as e: 
                print(e)

class PromedioMontos:
    def __init__(self):
        self.definir_rango_fechas()
        self.obtener_promedio()
    
    def definir_rango_fechas(self):
        os.system('cls')
        while True:
            try:
                
                fecha_inicial = input("Ingesa la fecha inicial del periodo a reportar formato(dd/mm/aaaa): ")
                self.fecha_inicial = datetime.datetime.strptime(fecha_inicial,"%d/%m/%Y").date()

                while True:
                    fecha_final = input("Ingresa la fecha final del periodo a reportar formato(dd/mm/aaaa): ")
                    self.fecha_final = datetime.datetime.strptime(fecha_final,"%d/%m/%Y").date()

                    if self.fecha_final < self.fecha_inicial:
                        print('\n[red]La fecha final debe ser mayor a la fecha inicial[/red]\n')
                    else:
                        break


            except ValueError:
                print('\n[red]Tipo de formato de fecha no válido[red]\n')
            except Exception as e:
                print(e)
            else:
                break #
        
    def obtener_promedio(self):
        try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT AVG(monto) FROM notas WHERE \
                                  (fecha BETWEEN ? AND ?) AND estado = 1;", (self.fecha_inicial, self.fecha_final))
                
                resultado = mi_cursor.fetchone()

                if resultado[0]:
                    print(f"\nEl promedio de los montos de las notas en el período seleccionado es: {resultado[0]}")
                    input('\nPresiona Enter para continuar')
                else:
                    print("\n[red]No hay notas dentro del período seleccionado.[/red]")
                    input('\nPresiona Enter para continuar')

            
        except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input('Enter')
            return False
        except Exception as e:
            print(f'[red]{e}[/red]')
            input('Enter')
            return False
        finally:
            if conn:
                conn.close()