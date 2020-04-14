funcao_a_integrar <- function(x)
{
  return (x^3)
}

monte_carlo <- function(npt)
{
  x <- runif(npt)
  y <- runif(npt)
  d <- funcao_a_integrar(x) - y
  
  n_ac <- which(d > 0)
  
  return (length(n_ac)/npt)
}

estimate <- function(N, npt)
{
  arr = array(dim=N)
  for (i in 1:N)
  {
    arr[i] = monte_carlo(npt)
  }
  
  return(arr)
}

print(estimate(1, 10000))
#g_N = 10000

#x = rep(0,4)
#y = rep(0,4)

#for(i in 1:4)
#{
#  x[i] = 10^i
#  y[i] = var(estimate(g_N, x[i]))
#}

#plot(x,y,xlab="N",ylab="Variância do valor da função por Monte-Carlo",, main="Mostrando que a variância cai com 1/N",log = "xy")

#a=10^mean(log10(x)+log10(y))
#xl=seq(x[1],x[4],1)
#yl=a/xl
#lines(xl,yl, col = 'red')