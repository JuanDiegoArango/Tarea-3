
# coding: utf-8

# In[149]:

import numpy as np
import matplotlib as plt


# In[150]:

coordenadas=np.loadtxt("coordenadas.dat", delimiter=',')
numero_de_particulas=len((coordenadas))


# In[ ]:

#costantes
G=4.492e-3
m=


# In[2]:

def potencial_gravitacional(r):
    return -G*m*m/r
def volumen(r):
    return 4.0/3.0*np.pi*(r)**3
def densidad(r, a, b,log_r0,log_rho):
    return np.exp(log_rho)*((r*np.exp(-log_r0))**-a)*((1+r*np.exp(-log_r0)))**-b
def loglikelihood(y_obs,y_model):
    loglike = 0.5*sum((y_obs-y_model)**2.0)
    return -loglike
def nuevo_valor(x,sigma):
    return np.random.normal(x, sigma)


# In[ ]:

n=1000 #iteraciones
indices=range(0,numero_de_particulas)
potenciales=[]
loglike=[]


# In[ ]:

for i in indices:
    suma=0
    for j in indices.remove(i):
        r=norm(coordenadas[i]-coordenadas[j])
        suma=suma+potencial_gravitacional(r)
    potenciales.append(suma)
potenciales=array(potenciales)
centro=potenciales.index(min(potenciales))
print"la particula numero "
print centro
print "tiene el mayor potencial entonces es la que se encuentra mas central a todas las demas particulas"     


# In[ ]:

coordenadas=coordenadas-coordenadas[centro]
#particula mas lejana
normas=np.linalg.norm(coordenadas, axis=1)
norma_maxima=potenciales.index(max(normas))
dr=norma_maxima/5000
y_obs=[]
distancias=[]
for i,j in enumerate  (0,5000):
    a=len(normas[normas>dr*i & normas<=dr*j])/(volumen(dr*j)-volumen(dr*i))
    y_obs.append(a)
    distancias.append(dr*j)
y_obs=array(y_obs)
distancias=array(distancias)      

    


# In[3]:

a=0.001 #exponente alfa
b=15.0 #exponente beta
logr0=10.0
logrho=50.0
distancias=np.exp(np.linspace(-20.0,60,20000))
y_obs=densidad(distancias, a, b,logr0,logrho)


# In[9]:

parametro1=[]#exponente alfa
parametro2=[]#exponente beta
parametro3=[]#exponente log(r0)
parametro4=[]#exponente log(rho)
likehood=[]

parametro1.append(a+0.80)
parametro2.append(b+0.90)
parametro3.append(logr0-10)
parametro4.append(np.log(max(y_obs)))
parametro_prueba=np.zeros(4)

print parametro1
print parametro2
print parametro3
print parametro4
i=0
n=30000
while(i<n):
        
    alfa=(nuevo_valor(parametro1[i],1.0))
    if(alfa>0):
            parametro_prueba[0]=(alfa)
    else:        
        while(alfa<0):
            alfa=(nuevo_valor(parametro1[i],1.0))
            if(alfa>0):
                parametro_prueba[0]=(alfa)
           
    beta=(nuevo_valor(parametro2[i],1.0))
    if(beta>0):
            parametro_prueba[1]=(beta)
    else:        
        while(beta<0):
            beta=(nuevo_valor(parametro2[i],1.0))
            if(beta>0):
                parametro_prueba[1]=(beta)
                       
    rc=(nuevo_valor(parametro3[i],1.0))
    parametro_prueba[2]=(rc)           
    rho=(nuevo_valor(parametro4[i],1.0))
    parametro_prueba[3]=(rho)
    
    
    y_modelo_nuevo = densidad(distancias,parametro_prueba[0],parametro_prueba[1],parametro_prueba[2],parametro_prueba[3])
    y_modelo_viejo = densidad(distancias,parametro1[i],parametro2[i],parametro3[i],parametro4[i])

    likehood_nuevo=loglikelihood(y_obs,y_modelo_nuevo)
    likehood_viejo=loglikelihood(y_obs,y_modelo_viejo)    
    delta=min(1,np.exp(-likehood_viejo+likehood_nuevo)) 

    
    if(np.random.uniform()<=delta):
        parametro1.append(parametro_prueba[0])
        parametro2.append(parametro_prueba[1])
        parametro3.append(parametro_prueba[2])
        parametro4.append(parametro_prueba[3])
        parametro=[parametro_prueba[0],parametro_prueba[1],parametro_prueba[2],parametro_prueba[3]]
        likehood.append(likehood_nuevo)
        print i
        
        
    else:
        parametro1.append(parametro1[i])
        parametro2.append(parametro2[i])
        parametro3.append(parametro3[i])
        parametro4.append(parametro4[i])
        parametro=[parametro1[i],parametro2[i],parametro3[i],parametro4[i]]
        likehood.append(likehood_viejo)



    i=i+1


# In[ ]:

#se ha visto que hay problemas en hacer un ajuste para el parametro beta que es el responsable de como de cae la densidad
#entonces se hace otra cadena de marvok con solo beta para ajustar mejor el parametro
#tomando los otros parametros como fijos
parametro_beta=[]#exponente beta
likehood=[]
parametro_beta.append(parametro[1])
parametro_prueba=0
nuevo_b=0

i=0
n=10000

while(i<n):      
    beta=(nuevo_valor(parametro_beta[i],10.0))
    if(beta>0):
            parametro_prueba=(beta)
    else:        
        while(beta<0):
            beta=(nuevo_valor(parametro_beta[i],10.0))
            if(beta>0):
                parametro_prueba=(beta)
                           
    y_modelo_nuevo = densidad(distancias,parametro[0],parametro_prueba,parametro[2],parametro[3])
    y_modelo_viejo = densidad(distancias,parametro[0],parametro_beta[i],parametro[2],parametro[3])

    likehood_nuevo=loglikelihood(y_obs,y_modelo_nuevo)
    likehood_viejo=loglikelihood(y_obs,y_modelo_viejo)    
    delta=min(1,np.exp(-likehood_viejo+likehood_nuevo)) 
    
    if(np.random.uniform()<=delta):
        parametro_beta.append(parametro_prueba)
        likehood.append(likehood_nuevo)  
        nuevo_b=parametro_prueba     
        print i
    else:
        parametro_beta.append(parametro_beta[i])
        likehood.append(likehood_viejo)
        nuevo_b=parametro_prueba
    i=i+1


# In[7]:

plt.figure()

y_final_1=densidad(distancias, parametro[0], parametro[1],parametro[2],parametro[3])
y_final_2=densidad(distancias, parametro[0], nuevo_b,parametro[2],parametro[3])
diferencia=loglikelihood(y_obs,y_final_1)-loglikelihood(y_obs,y_final_2)

if (diferencia>0):
    parametro[1]=nuevo_b

print "Parametros finales:"
print  "Alfa= "+str(parametro[0])+" "
print  "Beta= "+ str(parametro[1]) +" "
print  "R0= "+str(np.exp(parametro[2]))+" "
print  "Rho= "+str(np.exp(parametro[3]))+" "
 
y_final=densidad(distancias, parametro[0], parametro[1],parametro[2],parametro[3])       
plt.plot(np.log(distancias),np.log(y_final),label="Modelo")
plt.scatter(np.log(distancias),np.log(y_obs),label="Observaciones") 
    
plt.xlabel("log(distancia)")
plt.ylabel("log(densidad)")
        
plt.savefig("modelo.pdf")


# In[ ]:




# In[ ]:




# In[ ]:



