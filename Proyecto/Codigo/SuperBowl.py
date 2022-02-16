import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def hist(dfs, variable, nombres, colores):
    plt.figure(figsize=(10, 5))
    
    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.title("{} {}".format(variable, nombres[i]))
        dfs[i][variable].value_counts().plot.bar(rot=0, color=colores[i])
        
        plt.ylim(0, len(dfs[i][variable]))
        
    plt.suptitle(variable)
    plt.savefig("{}.png".format(variable))
    plt.close()
    return None

def bootstrapping(dfs, variable):
    n = 10000
    rta_boot = []
    
    for i in range(len(dfs)):        
        lista_var = np.array(dfs[i][variable])
        partidos = len(lista_var)
        boot_lista_var = np.zeros(n)
        
        for j in range(n):
            sim_partido = np.zeros(partidos)
            
            for k in range(partidos):
                np.random.shuffle(lista_var)
                sim_partido[k] = lista_var[0]
            
            boot_lista_var[j] = np.mean(sim_partido)
        
        rta_boot.append(boot_lista_var)        
    return rta_boot

def hist_boot(rta_boot, variable, nombres, colores):
    plt.figure(figsize=(10, 5))
    for i in range(len(rta_boot)):
        plt.subplot(1, 2, i + 1)
        plt.title("{} {}".format(variable, nombres[i]))
        lab = "$\mu = {:.2f}$ \n$\sigma = {:.2f}$".format(np.mean(rta_boot[i]), np.std(rta_boot[i]))
        plt.hist(rta_boot[i], bins=20, density=True, color=colores[i], label=lab)
        plt.legend()
    
    plt.savefig("{}.png".format(variable))
    plt.close()
    return None

def P_val(info_P_val, variable, nombres):
    diffs = info_P_val[0] - info_P_val[1]
    hipotesis = 0
    mu = np.mean(diffs)
    
    diffs -= mu
    hipotesis = np.abs(hipotesis - mu)
    frac_altos = np.count_nonzero(diffs > hipotesis)/len(diffs)
    
    plt.figure()

    ms = "$\mu = {:.2f}$\n".format(mu)
    ms += "Pvalue = {:.2f}".format(frac_altos)
    
    plt.hist(diffs, bins=20, density=True, label=ms)
    plt.axvline(hipotesis, c="red")
    
    plt.title("Diferencia {} - {} de {}".format(nombres[0], nombres[1], variable))
    plt.legend()
    plt.savefig("Pval {}.png".format(variable))
    plt.close()
    return None

df_b = pd.read_csv("Bengals.csv")
df_r = pd.read_csv("Rams.csv")

dfs = [df_b, df_r]
keys = df_b.keys()

nombres = ["Bengals", "Rams"]
colores = ["darkorange", "royalblue"]

labels_h = [keys[2]]
labels_boot = np.array(keys[13:])
info_P_val = []

hist(dfs, labels_h[0], nombres, colores)

for i in range(len(labels_boot)):
    rta_boot = bootstrapping(dfs, labels_boot[i])
    hist_boot(rta_boot, labels_boot[i], nombres, colores)
        
    ii = labels_boot == labels_boot[i]
    
    if(np.count_nonzero(ii) > 0):
        info_P_val.append(rta_boot)


for i in range(len(labels_boot)):
    P_val(info_P_val[i], labels_boot[i], nombres)
