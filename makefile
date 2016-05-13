modelo.pdf : output_4999.dat MCMC.py 
	python MCMC.py output_4999.dat

output_4999.dat : ncuerpos_esfera.x
	./ncuerpos_esfera.x 1000 0.1

ncuerpos_esfera.x : main.c evolve.c inicial.c 
	gcc main.c evolve.c inicial.c  -o ncuerpos_esfera.x -lm -fopenmp
