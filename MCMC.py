
import numpy as np
import matplotlib.pyplot as plt
import sys

argumento = sys.argv[1]



def densidad(r, a, b,log_r0,log_rho):
    return np.exp(log_rho)*((r*np.exp(-log_r0))**-a)*((1+r*np.exp(-log_r0)))**-b
def volumen(r):
    return 4.0/3.0*np.pi*(r)**3
def loglikelihood(y_obs,y_model):
    loglike = 0.5*sum((y_obs-y_model)**2.0)
    return -loglike
def nuevo_valor(x,sigma):
    return np.random.normal(x, sigma)



archivo=np.loadtxt(argumento, delimiter=' ')



numero_de_particulas =len(archivo)
energias=(np.transpose(archivo)[6:8])
coordenadas=np.transpose(np.transpose(archivo)[0:3])
energia_potencial=energias[0]-energias[1]
centro=np.where(energia_potencial==min(energia_potencial))



coordenadas=coordenadas-coordenadas[centro]
#particula mas lejana
normas=[]
for i in range (0,numero_de_particulas):
    normas.append(np.linalg.norm(coordenadas[i]))   
normas =np.array(normas)
dr=max(normas)/2000.0
y_obs=[]
distancias=[]
for i in range(1,2001):
    a=((dr*(i-1)  < normas) & (normas<=dr*i)).sum()/(volumen(dr*i)-volumen(dr*(i-1)))
    if(a!=0):
        y_obs.append(a)
        distancias.append(dr*(i-0.5))

y_obs=np.array(y_obs)
distancias=np.array(distancias)



parametro1=[]#exponente alfa
parametro2=[]#exponente beta
parametro3=[]#exponente log(r0)
parametro4=[]#exponente log(rho)
likehood=[]

parametro1.append(1.0) #adivinanza inicial de exponente alfa
parametro2.append(2.0) #adivinanza inicial de exponente beta
parametro3.append(0.0) #adivinanza inicial de radio de densidad uniforme
parametro4.append(np.log(max(y_obs))) #adivinanza de densidad maxima.
parametro_prueba=np.zeros(4)

i=0
n=30000
while(i<n):
    alfa=(nuevo_valor(parametro1[i],2.0)) #no puede ser negativo la potencia
    if(alfa>0):
            parametro_prueba[0]=(alfa)
    else:        
        while(alfa<0):
            alfa=(nuevo_valor(parametro1[i],2.0))
            if(alfa>0):
                parametro_prueba[0]=(alfa)
           
    beta=(nuevo_valor(parametro2[i],1.0))#no puede ser negativo la potencia
    if(beta>0):
            parametro_prueba[1]=(beta)
    else:        
        while(beta<0):
            beta=(nuevo_valor(parametro2[i],1.0))
            if(beta>0):
                parametro_prueba[1]=(beta)
                
                       
    
    r0=(nuevo_valor(parametro3[i],2.0))
    parametro_prueba[2]=(r0)
   
    
    rho=(nuevo_valor(parametro4[i],0.007))
    if((rho<=np.log(max(y_obs))) & (rho>0)):
            parametro_prueba[3]=(rho)
    else:        
        while((rho>np.log(max(y_obs))) | (rho<0)):
            rho=(nuevo_valor(parametro4[i],0.007))
            if((rho<=np.log(max(y_obs))) & (rho>0)):
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



a,b=np.histogram(parametro1,bins=15)
maximo=np.where(a==max(a))[0]
parametro_final_1=(b[maximo+1]-b[maximo])/2+b[maximo]
error1=(np.std(b))



a,b=np.histogram(parametro2,bins=15)
maximo=np.where(a==max(a))[0]
parametro_final_2=(b[maximo+1]-b[maximo])/2+b[maximo]
error2=(np.std(b))



a,b=np.histogram(parametro3,bins=15)
maximo=np.where(a==max(a))[0]
parametro_final_3=(b[maximo+1]-b[maximo])/2+b[maximo]
error3=(np.std(b))



a,b=np.histogram(parametro4,bins=15)
maximo=np.where(a==max(a))[0]
parametro_final_4=(b[maximo+1]-b[maximo])/2+b[maximo]
error4=(np.std(b))



y_final=densidad(distancias, parametro_final_1, parametro_final_2,parametro_final_3,parametro_final_4)
print "Parametros finales:"
print  "Alfa= "+str(parametro_final_1)+" error "+str(error1)+" "
print  "Beta= "+str(parametro_final_2)+" error "+str(error2)+" "
print  "R0= "+str(parametro_final_3)+" error "+str(error3)+" "
print  "Rho= "+str(parametro_final_4)+" error "+str(error4)+" "
 
plt.figure()
plt.plot(np.log(distancias),np.log(y_final),label="Modelo")
plt.scatter(np.log(distancias),np.log(y_obs),label="Observaciones")     
       
plt.xlabel("log(distancia)")
plt.ylabel("log(densidad)")    
plt.savefig("modelo.pdf")

