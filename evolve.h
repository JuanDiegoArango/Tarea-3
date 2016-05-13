double calcula_tiempo_total(int n);
double calcula_time_step(int n, double epsilon);
void calcula_aceleracion(double *p, double *v, double *a, int n, double epsilon);
void calcula_RCM(double *p, int n, double *RCM);
int comp (const void * elem1, const void * elem2);
void calcula_aceleracion_esfera(double *p, double *v, double *a, int n, double epsilon, double *RCM, double *R);
void  kick(double *p, double *v, double *a, int n, double delta_t);
void  drift(double *p, double *v, double *a, int n, double delta_t);
void calcula_energia(double *p, double *v, double *U, double *K, int n);

