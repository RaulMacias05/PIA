import os
from rich import print
from time import sleep
import notas
import clientes
import servicios
import estadisticas

class Menu_principal:
    def __init__(self) -> None:

        while True:
            self.mostrar_menu()

            match self.eleccion_del_menu:
                case 1:
                    self.notas()
                case 2:
                    self.clientes()
                case 3:
                    self.servicios()
                case 4:
                    self.estadisticas()
                case 5:
                    if self.salir_del_sistema():
                        break

    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]REGISTRO Y MANIPULACIÓN DE DATOS[/#9999FF]

[#7AFFFF]--Menú Principal--[/#7AFFFF]
              
1 - Notas
2 - Clientes
3 - Servicios
4 - Estadisticas
5 - Salir del Sistema
              
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

    def notas(self):
        notas.Menu()

    def clientes(self):
        clientes.Menu()

    def servicios(self):
        servicios.Menu()

    def estadisticas(self):
        estadisticas.Menu()


    def salir_del_sistema(self):
        while True:
            os.system('cls')
            salir = input("\n¿Desea salir definitivamente del programa?\n\n| s - Sí | n - No |\n\n")

            if salir.upper() in ('S', 'SI', 'SÍ'):
                os.system('cls')
                print("\n[#9999FF]Gracias por su visita, vuelva pronto[/#9999FF]")
                return True
            
            elif salir.upper() in ('N', 'NO'):
                print("\n[#9999FF]Volviendo al Menú Principal[/#9999FF]")
                for i in range(3):
                    print('[#9999FF].[/#9999FF]', end=' ')
                    sleep(.3)
                sleep(.3)
                return False
                
            else:
                print('Opción no válida. Intente de nuevo\n')
                sleep(.7)

Menu_principal() 