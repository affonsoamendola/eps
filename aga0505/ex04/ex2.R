QUALIDADE_BOA = 0
QUALIDADE_MEDIA = 1
QUALIDADE_RUIM = 2

simular <- function(n_noites)
{
  n_noites_boas <- 0
  qualidade_ultima_noite <- QUALIDADE_MEDIA
 
  for(i in 1:n_noites)
  {
    qualidade_noite = -1
    rnd = runif(1)
    
    if(qualidade_ultima_noite == QUALIDADE_BOA)
    {
      if(rnd <= 0.6) qualidade_noite <- QUALIDADE_BOA
      else if(rnd <= 0.6 + 0.3) qualidade_noite <- QUALIDADE_MEDIA
      else qualidade_noite <- QUALIDADE_RUIM
    }
    
    if(qualidade_ultima_noite == QUALIDADE_MEDIA)
    {
      if(rnd <= 0.5) qualidade_noite <- QUALIDADE_BOA
      else if(rnd <= 0.5 + 0.25) qualidade_noite <- QUALIDADE_MEDIA
      else qualidade_noite <- QUALIDADE_RUIM
    }
    
    if(qualidade_ultima_noite == QUALIDADE_RUIM)
    {
      if(rnd <= 0.2) qualidade_noite <- QUALIDADE_BOA
      else if(rnd <= 0.2 + 0.4) qualidade_noite <- QUALIDADE_MEDIA
      else qualidade_noite <- QUALIDADE_RUIM
    }
    
    if(qualidade_noite == QUALIDADE_BOA)
    {
      n_noites_boas <- n_noites_boas + 1
    }
    qualidade_ultima_noite <- qualidade_noite
  }
  
  return(n_noites_boas)
}

N = 100000
print(simular(N)/N)

