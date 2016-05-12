import numpy as np
import matplotlib.pyplot as plt



coordenadas=np.loadtxt("coordenadas.dat", delimiter=',')
numero_de_particulas=len((coordenadas))



#costantes
G=4.492e-3
m=1



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



n=1000 #iteraciones
indices=range(0,numero_de_particulas)
potenciales=[]
loglike=[]



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
        
    else:
        parametro1.append(parametro1[i])
        parametro2.append(parametro2[i])
        parametro3.append(parametro3[i])
        parametro4.append(parametro4[i])
        parametro=[parametro1[i],parametro2[i],parametro3[i],parametro4[i]]
        likehood.append(likehood_viejo)



    i=i+1

y_final=densidad(distancias, parametro[0], parametro[1],parametro[2],parametro[3])
print "Parametros finales:"
print  "Alfa= "+str(parametro[0])+" "
print  "Beta= "+ str(parametro[1]) +" "
print  "R0= "+str(np.exp(parametro[2]))+" "
print  "Rho= "+str(np.exp(parametro[3]))+" "
 
plt.plot(np.log(distancias),np.log(y_final_1),label="Modelo")
plt.plot(np.log(distancias),np.log(y_obs),label="Observaciones")     
       
plt.xlabel("log(distancia)")
plt.ylabel("log(densidad)")    
plt.savefig("modelo.pdf")

