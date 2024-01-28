import random 
import pandas as pd

# Inicializa df como None fuera de la función
df = None

# Inicializa el dataset como lista vacía fuera de la función
dataset = []



def set_hostnames(number_of_hosts) -> None:
    sistemas_operativos = ['L'] * 40 + ['S'] * 30 + ['A'] * 20 + ['H'] * 10
    entornos = ['D'] * 10 + ['I'] * 10 + ['T'] * 25 + ['S'] * 25 + ['P'] * 30
    paises = ['NOR'] * 6 + ['FRA'] * 9 + ['ITA'] * 16 + ['ESP'] * 16 + ['DEU'] * 23 + ['IRL'] * 30
    
    hosts = []
    for i in range(number_of_hosts):
        sistema_operativo = random.choice(sistemas_operativos)
        entorno = random.choice(entornos)
        pais = random.choice(paises)
        
        # Genera número de nodo
        numero_nodo = str(random.randint(1, 999)).zfill(3) # concateno a str y zfill asegura que tenga 3 digitos, agrega ceros a la izq si es necesario
        
        hostname = sistema_operativo + entorno + pais + numero_nodo
        hosts.append(hostname)
    
    return hosts



def get_os(hostname) -> str:
    first_letter = hostname[0]
    
    if first_letter == 'L':
        return 'Linux'
    elif first_letter == 'S':
        return 'Solaris'
    elif first_letter == 'A':
        return 'AIX'
    elif first_letter == 'H':
        return 'HP-UX'
    else:
        return 'Unknown'

    

def get_environment(hostname) -> str:
    second_letter = hostname[1]
    
    if second_letter == 'D':
        return 'Development'
    elif second_letter == 'I':
        return 'Integration'
    elif second_letter == 'T':
        return 'Testing'
    elif second_letter == 'S':
        return 'Staging'
    elif second_letter == 'P':
        return 'Production'
    else:
        return 'Unknown'

    

def get_country(hostname) -> str:
    country_code = hostname[2:5]

    country_mapping = {
        'NOR': 'Norway',
        'FRA': 'France',
        'ITA': 'Italy',
        'ESP': 'Spain',
        'DEU': 'Germany',
        'IRL': 'Ireland',
    }

    return country_mapping.get(country_code, 'Unknown')



def set_dataframe(count) -> None: # crea un dataset de hostnames 
    # Accedo a las variables globales df y dataset
    global df # variable global que esta ya inicializada como df y le damos el valor 
    global dataset
    
    # Llamo a la función set_hostnames
    hostnames = set_hostnames(count)
    
    # Itero sobre los hostnames para construir el dataset
    for hostname in hostnames: # genera dicc y lo agrega a dataset
        data = { # dicc clave-valor
            'hostname': hostname,
            'os': get_os(hostname),
            'environment': get_environment(hostname),
            'country': get_country(hostname),
            'node': int(hostname[5:]) 
        }
        dataset.append(data)
    
    # Creo el DataFrame en Pandas con los datos de dataset
    df = pd.DataFrame(dataset)

# Uso de la función set_dataframe
count_of_records = 100
set_dataframe(count_of_records)

# Invoco la función set_dataframe con el argumento 1500
set_dataframe(1500)

# Guardo el DataFrame en un archivo CSV
df.to_csv('hostsnames.csv', header=True, index=False) # to_csv de Pandas para guardar el DataFrame


# Lee el archivo CSV 
hosts_df = pd.read_csv(r'hostsnames.csv')
                    


# Visualiza el DataFrame leído
hosts_df



# Visualización de gráficos 


import pandas as pd
import matplotlib.pyplot as plt

# Carga el DataFrame desde el archivo CSV
df = pd.read_csv('hostsnames.csv')

# Pivote del DataFrame para agrupar por país y contar la cantidad de cada entorno
pivot_df = df.groupby(['country', 'environment']).size().unstack()

# Genera un gráfico de barras agrupadas
pivot_df.plot(kind='bar', figsize=(10, 6), width=0.6)
plt.title('Distribution of environments by country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.legend(title='Environment', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()



# Crea la figura y los ejes
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Gráfico 1: Type of OS grouped by country
pivot_os_country = df.groupby(['country', 'os']).size().unstack()
pivot_os_country.plot(kind='barh', figsize=(10, 8), ax=axs[0, 0])
axs[0, 0].set_title('Type of OS grouped by country')
axs[0, 0].set_xlabel('Count')
axs[0, 0].set_ylabel('Country')

# Gráfico 2: Total Operating Systems
total_os = df['os'].value_counts()
axs[0, 1].pie(total_os,labels=total_os, startangle=100) 
axs[0, 1].set_title('Total Operating Systems')

# Ajusta el diseño para que el gráfico de tarta no ocupe espacio innecesario
axs[0, 1].axis('equal') 

# Agrega leyenda en la esquina superior derecha
axs[0, 1].legend([f"{os} ({percentage:.1f}%)" 
                  for os, percentage in zip(total_os.index, total_os / total_os.sum() * 100)],
                title='OS', loc='upper right')



# Gráfico 3: Total hosts by country

import seaborn as sns

total_hosts_by_country = df['country'].value_counts()
colors = sns.color_palette("crest", len(total_hosts_by_country))

axs[1, 0].barh(total_hosts_by_country.index, total_hosts_by_country, color=colors)
axs[1, 0].set_title('Total hosts by country')
axs[1, 0].set_xlabel('Number of hosts')
axs[1, 0].set_ylabel('Country')

# Muestra el número total de hosts a la derecha de cada barra
for index, value in enumerate(total_hosts_by_country):
    axs[1, 0].text(value + 5, index, str(value), va='center')

# Establece el valor máximo del eje x
axs[1, 0].set_xlim(0, max(total_hosts_by_country) + 100)



# Gráfico 4: Host by country grouped by environment 
host_by_country_env = df.groupby(['country', 'environment']).size().unstack(0)
host_by_country_env.plot(kind='bar', figsize=(10, 8), ax=axs[1, 1])
axs[1, 1].set_title('Host by country grouped by environment')
axs[1, 1].set_xlabel('Environment')
axs[1, 1].set_ylabel('Number of hosts')



# Ajustar el diseño y mostrar la figura
plt.tight_layout()