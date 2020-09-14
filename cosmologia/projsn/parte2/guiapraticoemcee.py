######### PACOTES #########

import emcee
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing

''' ITEM A '''

######### FUNÇÕES PARA O EMCEE #########

def lnlike(p, z, data, err):
    '''
    Função que calcula o ln da likelihood (verossimilhança)
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # no item a só omegaEE varia, então p é isso aí
    Omega_EE = p
    
    # k é o módulo de distância calculado pelo seu modelo a partir dos dados de redshift
    k = distanceModule(z, Omega_EE)
    
    # e aqui o cálculo do chi2 normal
    chi2 = np.sum(((k - data) ** 2)/(err**2))
    
    # esse return é o que ele pediu que fosse a likelihood lá no documento do projeto
    return -0.5 * chi2

def lnprior(p):
    '''
    Função que retorna o ln do prior, a informação que vc tem previamente sobre o seu problema
    A gente sabe que omegaEE nesse item tem que estar entre 0 e 1, então se estiver fora, ele
    vai retornar 0 (= ln[-infinito]) e se estiver dentro, retorna 1 (= ln[0])
    '''
    
    Omega_EE = p
    
    if 0 < Omega_EE < 1:
        return 0
    return -np.inf

def lnprob(p, z, data, err):
    '''
    Função que retorna o ln do posterior, que é o que a gente quer
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # se o ln do prior for -infinito, lnprob = -infinito (prob = 0)
    if not np.isfinite(lnprior(p)):
        return -np.inf
        
    # senão, retorna o cálculo: posterior = likelihood * prior
    return lnlike(p, z, data, err) + lnprior(p)
    
def get_p0(min, max):
    '''
    Função que retorna pontos aleatórios no intervalo dado
    '''
    
    return min + np.random.random()*(max-min)

# n lembro o que ele faz com isso aqui
def explnlike(p, z, data, err):
    
    Omega_EE= p
    k = distanceModule(z, Omega_EE)

    chi2 = np.sum(((k - data) ** 2)/(err**2))

    return np.exp(-0.5*chi2)
    
    
######### EMCEE #########

# número de dimensões e de walkers
ndim, nwalkers = 1, 64

# sei lá
pool = multiprocessing.Pool()

# fofinho que vai rodar o código de fato, args são os dados que vc tem do arquivo .txt do Cypriano
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(redshift, dm, err_dm), pool=pool)

# números aleatórios de onde os walkers começarão sua jornada pelo incrível espaço de parâmetros
p0 = [[get_p0(0, 1)] for i in range(nwalkers)]
        
# agora a magia acontece
print('\n Starting emcee')
sampler.run_mcmc(p0, 1000, progress=True)

# sei lá
tau = sampler.get_autocorr_time()

# pegando as correntes que os walkers percorreram e transformando em vetores
flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
samples = sampler.chain[:, 100:, :].reshape((-1, ndim)) #np.loadtxt('samples.txt').reshape((-1, 1)) # isso aqui comentado vc usa p
                                                                                                    # n ter q rodar o código d nvo
trace = sampler.chain[:, 100:, :].reshape((-1, ndim)).T

# os corner plot
fig1 = corner.corner(samples, labels=["$\Omega_{EE}$"], show_titles=True, plot_datapoints=True, \
                     quantiles=[0.0015, 0.023,0.16, 0.5, 0.84, 0.977,0.9985], truth_color='#4682b4')
fig1.suptitle("Intervalos de confiança para $\Omega_{EE}$")
plt.savefig('fit.png', dpi=900, quality = 85)

''' N tenho ideia do que ele ta fazendo, por isso to comentando

Omega_EE = np.linspace(0.5,1,200)
chi2 = Omega_EE*0   

for i in range(0,len(Omega_EE)):
    chi2[i] = np.exp(lnlike(Omega_EE[i], redshift, dm, err_dm))

plt.plot(Omega_EE, chi2, color='orangered')
# plt.xlim(0.5,1)
# plt.ylim(0, 1.5)
plt.title('Densidade de probabilidade P($\mathbf{\Omega_{EE}}$)', fontweight='bold')
plt.xlabel('$\mathbf{\Omega_{EE}}$', fontweight='bold')
plt.ylabel('$\mathbf{P(\Omega_{EE}) \propto \exp(-\chi^2)}$ ')
plt.savefig('prob.png', dpi=900, quality = 85)
plt.show()
'''


''' ITEM B '''

######### FUNÇÕES PARA O EMCEE #########

def lnlike(p, z, data, err):
    '''
    Função que calcula o ln da likelihood (verossimilhança)
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # no item b omegaM e omegaEE variam, então p é isso aí
    Omega_M, Omega_EE = p
    
    # k é o módulo de distância calculado pelo seu modelo a partir dos dados de redshift
    k = distanceModule(z, Omega_EE)
    
    # e aqui o cálculo do chi2 normal
    chi2 = np.sum(((k - data) ** 2)/(err**2))
    
    # esse return é o que ele pediu que fosse a likelihood lá no documento do projeto
    return -0.5 * chi2

def lnprior(p):
    '''
    Função que retorna o ln do prior, a informação que vc tem previamente sobre o seu problema
    Mesma coisa de antes, agora pros dois omegas
    '''
    
    Omega_M, Omega_EE = p
    
    if -1 < Omega_EE < 1 and 0 < Omega_M < 1:
        return 0
        
    return -np.inf

def lnprob(p, z, data, err):
    '''
    Função que retorna o ln do posterior, que é o que a gente quer
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # se o ln do prior for -infinito, lnprob = -infinito (prob = 0)
    if not np.isfinite(lnprior(p)):
        return -np.inf
        
    # senão, retorna o cálculo: posterior = likelihood * prior
    return lnlike(p, z, data, err) + lnprior(p)
    
def get_p0(min, max):
    '''
    Função que retorna pontos aleatórios no intervalo dado
    '''
    
    return min + np.random.random()*(max-min)
    

######### EMCEE #########

# número de dimensões e de walkers
ndim, nwalkers = 2, 64

# sei lá
pool = multiprocessing.Pool()

# fofinho que vai rodar o código de fato, args são os dados que vc tem do arquivo .txt do Cypriano
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(redshift, dm, err_dm), pool=pool)

# números aleatórios de onde os walkers começarão sua jornada pelo incrível espaço de parâmetros
p0 = [[get_p0(0, 1), get_p0(-1, 1)] for i in range(nwalkers)]
        
# agora a magia acontece
print('\n Starting emcee')
sampler.run_mcmc(p0, 4000, progress=True)

# pegando as correntes que os walkers percorreram e transformando em uma matriz com 2 vetores
flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
samples = sampler.chain[:, 750:, :].reshape((-1, ndim)) #np.loadtxt('samples.txt').reshape((-1, 1)) # isso aqui comentado vc usa p
                                                                                                    # n ter q rodar o código d nvo
trace = sampler.chain[:, 750:, :].reshape((-1, ndim)).T

# os corner plot
fig1 = corner.corner(samples, labels=["$\Omega_{M}$","$\Omega_{EE}$"], show_titles=True, plot_datapoints=True, \
                     quantiles=[0.0015, 0.023,0.16, 0.5, 0.84, 0.977,0.9985], levels=(0.68, 0.95,0.99))
# fig1.suptitle("Intervalos de confiança para $\Omega_{EE}$")
plt.savefig('corner_c_c.png', dpi=900, quality = 85)


''' ITEM C '''

# fazer a mesma coisa para o item b, mas agora na função lnlike tem um termo a mais:
#
#   chi2 = np.sum(((k - data) ** 2)/(err**2)) + ( ((1 - Omega_M - Omega_EE) + 0.06)**2)/0.05**2


''' ITEM D '''

######### FUNÇÕES PARA O EMCEE #########

def lnlike(p, z, data, err):
    '''
    Função que calcula o ln da likelihood (verossimilhança)
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # no item b omegaM e w variam, então p é isso aí
    Omega_M, w = p
    
    # k é o módulo de distância calculado pelo seu modelo a partir dos dados de redshift
    k = distanceModule(z, Omega_EE)
    
    # e aqui o cálculo do chi2 normal
    chi2 = np.sum(((k - data) ** 2)/(err**2))
    
    # esse return é o que ele pediu que fosse a likelihood lá no documento do projeto
    return -0.5 * chi2

def lnprior(p):
    '''
    Função que retorna o ln do prior, a informação que vc tem previamente sobre o seu problema
    Mesma coisa de antes, agora pra omegaM e w
    '''
    
    Omega_M, w = p
    
    if -2 < w < 2 and 0 < Omega_M < 2:
        return 0
        
    return -np.inf

def lnprob(p, z, data, err):
    '''
    Função que retorna o ln do posterior, que é o que a gente quer
    p é um argumento simples ou vetor com os parâmetros que vão variar
    z são os dados de redshift
    data são os dados do módulo de distância
    err é a incerteza de data
    '''
    
    # se o ln do prior for -infinito, lnprob = -infinito (prob = 0)
    if not np.isfinite(lnprior(p)):
        return -np.inf
        
    # senão, retorna o cálculo: posterior = likelihood * prior
    return lnlike(p, z, data, err) + lnprior(p)
    
def get_p0(min, max):
    '''
    Função que retorna pontos aleatórios no intervalo dado
    '''
    
    return min + np.random.random()*(max-min)


######### EMCEE #########

# número de dimensões e de walkers
ndim, nwalkers = 2, 64

# sei lá
pool = multiprocessing.Pool()

# fofinho que vai rodar o código de fato, args são os dados que vc tem do arquivo .txt do Cypriano
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(redshift, dm, err_dm), pool=pool)

# números aleatórios de onde os walkers começarão sua jornada pelo incrível espaço de parâmetros
p0 = [[get_p0(0, 0.4), get_p0(-1, 1)] for i in range(nwalkers)]
        
# agora a magia acontece
print('\n Starting emcee')
sampler.run_mcmc(p0, 4000, progress=True)

# pegando as correntes que os walkers percorreram e transformando em uma matriz com 2 vetores
flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
samples = sampler.chain[:, 100:, :].reshape((-1, ndim)) #np.loadtxt('samples.txt').reshape((-1, 1)) # isso aqui comentado vc usa p
                                                                                                    # n ter q rodar o código d nvo
trace = sampler.chain[:, 100:, :].reshape((-1, ndim)).T

# os corner plot
fig1 = corner.corner(samples, labels=["$\Omega_{M}$","w"], show_titles=True, plot_datapoints=True, \
                     quantiles=[0.0015, 0.023,0.16, 0.5, 0.84, 0.977,0.9985], levels=(0.68, 0.95,0.99))
# fig1.suptitle("Intervalos de confiança para $\Omega_{EE}$")
plt.savefig('corner_d_d.png', dpi=900, quality = 85)












