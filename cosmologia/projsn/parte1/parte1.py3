import random as rand

def monte_carlo(n, x_lim, y_lim, function):
  inside_points = 0
  
  for i in range(n):  #for every point, get new random values

    x = rand.random() * x_lim 
    y = rand.random() * y_lim

    func_y = function(x)

    if(func_y > y_lim):
      print("ERROR, Y_LIM IS SMALLER THAN FUNCTION MAX")

    if(y < func_y):
      inside_points = inside_points + 1 #if random value is under function add it to the under function count.

  return (inside_points/n)*(x_lim * y_lim) #returns area under function

#INPUTS:
h_0 = 70 # in (km/s) / Mpc
redshift = 1.0
omega_m = 1.0
omega_k = 0
omega_lambda = 0.0
light_speed = 299792.458 #in km/s
monte_carlo_n = 100000

def d_h():
  return light_speed/h_0

def E_function(redshift_prime):
  return (omega_m*((1.+redshift_prime)**3) +\
          omega_k*((1.+redshift_prime)**2) +
          omega_lambda)**(1./2.)

def integration_function(redshift_prime):
  return 1.0 / E_function(redshift_prime)
 
def d_c():
  print("Calculating D_C")
  return d_h() * monte_carlo(monte_carlo_n, redshift, 1.0, integration_function)

def d_m():
  print("Calculating D_M")
  if omega_k > 0:
    return d_h() * (1.0 / ((omega_k)**(1./2.))) * sinh(((omega_k)**(1./2.)) * (d_c() / d_h()))
  elif omega_k < 0:
    return d_h() * (1.0 / ((abs(omega_k))**(1./2.))) * sin(((abs(omega_k))**(1./2.)) * (d_c() / d_h()))
  else:
    return d_c()

def lum_distance():
  print("Calculating D_L")
  return (1+redshift)*d_m()

rand.seed(1234)

print(lum_distance())
