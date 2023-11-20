import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TreeSimulationApp:
    def __init__(self, root):
        self.root = root  
        self.root.title("Simulación de Crecimiento de Árboles")
        self.root.resizable(False, False)
        # Variables de entrada
        self.tiempo_simulacion_var = tk.DoubleVar()
        self.nitrogeno_var = tk.DoubleVar()
        self.fosforo_var = tk.DoubleVar()
        self.potasio_var = tk.DoubleVar()
        # Configuración de la interfaz
        self.setup_ui()
#Initialize the application and configure the graphical interface.
#Create control variables (DoubleVar) for the input values: simulation 
#time, percentage of nitrogen, phosphorus and potassium in the soil.
#Call the setup_ui() method to configure the interface.

    def setup_ui(self):
        # Etiquetas y cajas de entrada
        ttk.Label(self.root, text="Ingrese los datos para la simulación").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.root, text="Tiempo de Simulación (años):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.tiempo_simulacion_var).grid(row=1, column=1, padx=5, pady=5)        
        ttk.Label(self.root, text="Porcentaje de nitrógeno en el terreno:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.nitrogeno_var).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Porcentaje de fósforo en el terreno:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.fosforo_var).grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Porcentaje de Potasio en el terreno:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.potasio_var).grid(row=4, column=1, padx=5, pady=5)
        # Botón de simulación
        ttk.Button(self.root, text="Simular", command=self.simulate).grid(row=5, column=1, columnspan=2, pady=10)
        # Crear una nueva figura y ejes para el gráfico
        self.fig = Figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot(111)
        # Crear el lienzo del gráfico para mostrar en la interfaz
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=6, column=0, columnspan=2, padx=10)
#setup_ui() method:
#Configure the graphical interface with labels, input boxes, and a simulation button.
#Create a new Matplotlib figure and canvas to display the plot in the interface.
   
    def simulate(self):
        # Obtener los valores ingresados
        self.ax.clear() 
        tiempo_simulacion =    int(self.tiempo_simulacion_var.get())
        porcentaje_nitrogeno = int(self.nitrogeno_var.get())/100
        porcentaje_fosforo =   int(self.fosforo_var.get())/100
        porcentaje_potasio =   int(self.potasio_var.get())/100

        #Parametros por arbol (11) 0-10
        #K1, K2, K3, tasa_transpiracion,  tasa_fotosintesis_co2, tasa_crecimiento_temperatura, 
        #tasa_competicion_luz, tasa_competicion_espacio, tasa_competicion_nutrientes, 
        #edad_maxima, altura_maxima
        parametros_roble =     self.datos_roble()
        parametros_pino =      self.datos_pino()
        parametros_eucalipto = self.datos_eucalipto()
        parametros_castano =   self.datos_castano()   

        nutrientes_roble =     [porcentaje_nitrogeno,porcentaje_fosforo,porcentaje_potasio]
        nutrientes_pino =      [porcentaje_nitrogeno,porcentaje_fosforo,porcentaje_potasio]     
        nutrientes_eucalipto = [porcentaje_nitrogeno,porcentaje_fosforo,porcentaje_potasio]
        nutrientes_castano =   [porcentaje_nitrogeno,porcentaje_fosforo,porcentaje_potasio] 
        
        crecimiento_roble     = self.crecimiento_arbol(tiempo_simulacion, parametros_roble,     nutrientes_roble)
        crecimiento_pino      = self.crecimiento_arbol(tiempo_simulacion, parametros_pino,      nutrientes_pino) 
        crecimiento_eucalipto = self.crecimiento_arbol(tiempo_simulacion, parametros_eucalipto, nutrientes_eucalipto)
        crecimiento_catano    = self.crecimiento_arbol(tiempo_simulacion, parametros_castano,   nutrientes_castano) 

        # Gráficos para cada árbol por separado
        self.ax.plot(np.arange(len(crecimiento_roble)), crecimiento_roble, label='Crecimiento Roble', color='blue')
        self.ax.plot(np.arange(len(crecimiento_pino)), crecimiento_pino, label='Crecimiento Pino', color='green')
        self.ax.plot(np.arange(len(crecimiento_eucalipto)), crecimiento_eucalipto, label='Crecimiento Eucalipto', color='red')
        self.ax.plot(np.arange(len(crecimiento_catano)), crecimiento_catano, label='Crecimiento Castaño', color='black')

        self.ax.set_xlabel('Tiempo (años)')
        self.ax.set_ylabel('Altura (metros)')
        self.ax.legend()
        self.ax.grid(True)        
        # Redibujar el gráfico
        self.canvas.draw()  
simulate() method:

#It is activated when the "Simulate" button is clicked.
#Gets the values ​​entered by the user.
#Call the tree_growth() function to simulate the growth of four types of trees (oak, pine, eucalyptus, and chestnut) over time.
#Plot the growth of each type of tree on a single graph.
    
    def crecimiento_arbol(self, tiempo_simulacion, parametros_arbol, nutrientes):   
        crecimiento_arbol = [0]            
        tasa_crecimiento_estacional = np.sin(np.linspace(0, tiempo_simulacion, tiempo_simulacion) * 2 * np.pi / 365)

        for t in range(tiempo_simulacion):
            # Variables climáticas
            luz_solar = np.random.uniform(0.0, 1.0)
            agua = np.random.uniform(0.0, 1.0)
            temperatura = np.random.uniform(0, 27.0)
            co2 = np.random.uniform(0.00, 0.10)       

            tasa_fotosintesis = parametros_arbol[0] * luz_solar * nutrientes[0] * (1 - np.exp(-crecimiento_arbol[-1]))
            tasa_crecimiento_raices = parametros_arbol[1] * agua * nutrientes[1] * (1 - np.exp(-crecimiento_arbol[-1]))
            tasa_nutrientes = parametros_arbol[2] * sum(nutrientes) * np.exp(-crecimiento_arbol[-1])
            tasa_absorcion_agua = parametros_arbol[8] * agua * np.exp(-crecimiento_arbol[-1])
            tasa_transpiracion_agua = parametros_arbol[3] * crecimiento_arbol[-1]
            tasa_fotosintesis_co2_actual = parametros_arbol[4] * co2
            tasa_crecimiento_temperatura_actual = parametros_arbol[5] * temperatura
            tasa_competicion_luz_actual = parametros_arbol[6] * luz_solar * np.exp(-crecimiento_arbol[-1])
            tasa_competicion_espacio_actual = parametros_arbol[7] * np.exp(-crecimiento_arbol[-1])
            tasa_crecimiento_estacional_actual = tasa_crecimiento_estacional[t % tiempo_simulacion]

            crecimiento_anual = (tasa_fotosintesis + tasa_crecimiento_raices
                                - tasa_nutrientes - tasa_absorcion_agua - tasa_transpiracion_agua
                                + tasa_fotosintesis_co2_actual + tasa_crecimiento_temperatura_actual
                                - tasa_competicion_luz_actual - tasa_competicion_espacio_actual + tasa_crecimiento_estacional_actual)
                
            if crecimiento_arbol[-1] >= parametros_arbol[10] or t >= parametros_arbol[9] or crecimiento_anual < 0:
                crecimiento_anual = 0
            print(crecimiento_anual)    
            crecimiento_arbol.append(crecimiento_arbol[-1] + crecimiento_anual)         
        return crecimiento_arbol
    #################################################################################
    #Datos de los arboles
Tree_growth method (simulation_time, tree_parameters, nutrients):

#Simulates the growth of a tree over time.
#It uses a series of equations and specific parameters for each type of tree.
#Calculate factors such as photosynthesis, nutrient absorption, competition for light, space and nutrients, etc.
#Returns a list representing the height of the tree in each year.
    
    def datos_roble(self):
        # Parámetros específicos del Roble, 23 cm por año
        K1_1 = 0.02
        K2_1 = 0.03
        K3_1 = 0.005
        tasa_transpiracion_1 = 0.001
        tasa_fotosintesis_co2_1 = 0.001
        tasa_crecimiento_temperatura_1 = 0.005
        tasa_competicion_luz_1 = 0.001
        tasa_competicion_espacio_1 = 0.001
        tasa_competicion_nutrientes_1 = 0.002
        edad_maxima_1 = 500
        altura_maxima_1 = 30.0
        parametros_roble = [K1_1 , K2_1 , K3_1 , tasa_transpiracion_1,  tasa_fotosintesis_co2_1, tasa_crecimiento_temperatura_1, 
                            tasa_competicion_luz_1, tasa_competicion_espacio_1, tasa_competicion_nutrientes_1, 
                            edad_maxima_1, altura_maxima_1]
        return parametros_roble
    
    def datos_pino(self):
        # Parámetros específicos del Pino, 50 cm por año
        K1_2 = 0.02
        K2_2 = 0.03
        K3_2 = 0.005        
        tasa_transpiracion_2 = 0.002
        tasa_fotosintesis_co2_2 = 0.002
        tasa_crecimiento_temperatura_2 = 0.007
        tasa_competicion_luz_2 = 0.002
        tasa_competicion_espacio_2 = 0.002
        tasa_competicion_nutrientes_2 = 0.003
        edad_maxima_2 = 500
        altura_maxima_2 = 30.0        
        parametros_pino = [K1_2 , K2_2 , K3_2 , tasa_transpiracion_2,  tasa_fotosintesis_co2_2, tasa_crecimiento_temperatura_2, 
                            tasa_competicion_luz_2, tasa_competicion_espacio_2, tasa_competicion_nutrientes_2, 
                            edad_maxima_2, altura_maxima_2]
        return parametros_pino        

    def datos_eucalipto(self):
        # Parámetros específicos del Eucalipto, 100 cm por año
        K1_3 = 0.02
        K2_3 = 0.03
        K3_3 = 0.005        
        tasa_transpiracion_3 = 0.003
        tasa_fotosintesis_co2_3 = 0.003
        tasa_crecimiento_temperatura_3 = 0.01
        tasa_competicion_luz_3 = 0.003
        tasa_competicion_espacio_3 = 0.003
        tasa_competicion_nutrientes_3 = 0.005
        edad_maxima_3 = 400
        altura_maxima_3 = 24.0        
        parametros_eucalipto = [K1_3 , K2_3 , K3_3 , tasa_transpiracion_3,  tasa_fotosintesis_co2_3, tasa_crecimiento_temperatura_3, 
                            tasa_competicion_luz_3, tasa_competicion_espacio_3, tasa_competicion_nutrientes_3, 
                            edad_maxima_3, altura_maxima_3]
        return parametros_eucalipto   

    def datos_castano(self):
        # Parámetros específicos del Castaño, 150 cm por año
        K1_4 = 0.02
        K2_4 = 0.03
        K3_4 = 0.005      
        tasa_transpiracion_4 = 0.004
        tasa_fotosintesis_co2_4 = 0.004
        tasa_crecimiento_temperatura_4 = 0.015
        tasa_competicion_luz_4 = 0.004
        tasa_competicion_espacio_4 = 0.004
        tasa_competicion_nutrientes_4 = 0.006
        edad_maxima_4 = 1000
        altura_maxima_4 = 30.0        
        parametros_castaño = [K1_4 , K2_4 , K3_4 , tasa_transpiracion_4,  tasa_fotosintesis_co2_4, tasa_crecimiento_temperatura_4, 
                            tasa_competicion_luz_4, tasa_competicion_espacio_4, tasa_competicion_nutrientes_4, 
                            edad_maxima_4, altura_maxima_4]
        return parametros_castaño   

#Methods oak_data(), pine_data(), eucalyptus_data(), and chestnut_data() methods:
#They define the specific parameters for each type of tree. These parameters include 
#growth rates, competition, maximum age, and maximum height.

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeSimulationApp(root)
    root.mainloop()
