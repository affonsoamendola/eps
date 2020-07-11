import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import w0wzCDM
from scipy.optimize import curve_fit
from scipy.stats import chisquare
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

#Loading Data
data = np.loadtxt(open('sn1a.txt', "r"))
z_data, md_data, err_data = data.T[0], data.T[1], data.T[2]

len_data = len(z_data)

#Constants
h_0 = 70.

#Confidence Ellipse code 
#(From https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html)
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def confidence_ellipse_cov(x, y, ax, covariance, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    Returns
    -------
    matplotlib.patches.Ellipse

    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    #cov = np.cov(x, y)
    cov = covariance

    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def chi_squared(obs, exp, sigma):
    chi_squared_sum = 0.

    for i in range(len(obs)):
        chi_squared_sum += ((obs[i] - exp[i])**2)/(sigma[i]**2)

    return chi_squared_sum


#Item A

def func(z, omega_ee):
    omega_m = 1. - omega_ee
    omega_k = 0.
    distance_modulus = 0.
    w = -1.0

    cosmo = w0wzCDM(h_0, omega_m, omega_ee, w0=w)

    #Get Luminosity distance from current parameters
    lum_distance = cosmo.luminosity_distance(z)
    lum_distance = np.array(lum_distance)

    #Get distance modulus from lum_distance
    if lum_distance.all() != 0:
        temp = lum_distance * (10**6)
        distance_modulus = 5 * np.log10(temp/10)

    return distance_modulus

x_data = z_data
y_data = md_data

parameters, cov = curve_fit(func, x_data, y_data, p0=0.7, sigma=err_data, bounds=(-1,1))

fit_omega_ee = parameters[0]

theoric_md = np.empty(len_data)

for i in range(0, len_data):
    theoric_md[i] = func(z_data[i], fit_omega_ee)

print(fit_omega_ee)
print(np.sqrt(np.diag(cov)))


#Plotting
#Chi Squared for Omega_EE

plot_omega = []
plot_chi_squared = []

for test_omega_ee in np.linspace(0.4, 1.0, 25):
    test_md = func(z_data, test_omega_ee)
    plot_omega.append(test_omega_ee)
    plot_chi_squared.append(chi_squared(md_data, test_md, err_data))

print(plot_chi_squared)
plt.plot(plot_omega, plot_chi_squared)

plt.show()

'''
#Chi Squared for Omega_EE, Probability
plot_omega = []
plot_chi_squared = []

for test_omega_ee in np.linspace(-1.0, 1.0, 1000):
    test_md = func(z_data, test_omega_ee)
    plot_omega.append(test_omega_ee)
    plot_chi_squared.append(np.exp(-chi_squared(md_data, test_md, err_data)))

plt.plot(plot_omega, plot_chi_squared)
plt.show()
'''
#End Item A

#Item B
'''
def func(z, omega_m, omega_ee):
    omega_k = 1.0 - omega_m - omega_ee
    distance_modulus = 0.
    w = -1.0

    cosmo = w0wzCDM(h_0, omega_m, omega_ee, w0=w)

    #Get Luminosity distance from current parameters
    lum_distance = cosmo.luminosity_distance(z)
    lum_distance = np.array(lum_distance)

    #Get distance modulus from lum_distance
    if lum_distance.all() != 0:
        temp = lum_distance * (10**6)
        distance_modulus = 5 * np.log10(temp/10)

    return distance_modulus

x_data = z_data
y_data = md_data

parameters, cov = curve_fit(func, x_data, y_data, sigma=err_data, bounds=([0,-1],[1,1]))

fit_omega_m = parameters[0]
fit_omega_ee = parameters[1]

theoric_md = np.empty(len_data)

for i in range(0, len_data):
    theoric_md[i] = func(z_data[i], fit_omega_m, fit_omega_ee)

print(fit_omega_m)
print(fit_omega_ee)
print(np.sqrt(np.diag(cov)))
'''
#Ellipses Plot
'''
x = fit_omega_m
y = fit_omega_ee

confidence_plot = plt.subplot()
value = plt.plot(x, y,'.')

confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=1, label=r'$1\sigma$', edgecolor='red', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=2, label=r'$2\sigma$', edgecolor='green', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=3, label=r'$3\sigma$', edgecolor='blue', linestyle='--')

confidence_plot.legend(loc=2)
plt.show()
'''
'''
#Item C
def func(z, omega_m, omega_ee):
    omega_k = 1.0 - omega_m - omega_ee
    distance_modulus = 0.
    w = -1.0

    cosmo = w0wzCDM(h_0, omega_m, omega_ee, w0=w)

    #Get Luminosity distance from current parameters
    lum_distance = cosmo.luminosity_distance(z)
    lum_distance = np.array(lum_distance)

    #Get distance modulus from lum_distance
    if lum_distance.all() != 0:
        temp = lum_distance * (10**6)
        distance_modulus = 5 * np.log10(temp/10)

    return distance_modulus + (((omega_k + 0.06)**2)/((0.05)**2)**2) #Adding the omega_k prior.

x_data = z_data
y_data = md_data

parameters, cov = curve_fit(func, x_data, y_data, sigma=err_data, bounds=([0,-1],[1,1]))

fit_omega_m = parameters[0]
fit_omega_ee = parameters[1]

theoric_md = np.empty(len_data)

for i in range(0, len_data):
    theoric_md[i] = func(z_data[i], fit_omega_m, fit_omega_ee)

#Ellipses Plot

x = fit_omega_m
y = fit_omega_ee

print(fit_omega_m)
print(fit_omega_ee)
print(np.sqrt(np.diag(cov)))

confidence_plot = plt.subplot()
value = plt.plot(x, y,'.')

confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=1, label=r'$1\sigma$', edgecolor='red', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=2, label=r'$2\sigma$', edgecolor='green', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=3, label=r'$3\sigma$', edgecolor='blue', linestyle='--')

confidence_plot.legend(loc=2)
plt.show()
'''
#Item D
'''
def func(z, omega_m, w):
    omega_k = 0.
    omega_ee = 1. - omega_m
    distance_modulus = 0.

    cosmo = w0wzCDM(h_0, omega_m, omega_ee, w0=w)

    #Get Luminosity distance from current parameters
    lum_distance = cosmo.luminosity_distance(z)
    lum_distance = np.array(lum_distance)

    #Get distance modulus from lum_distance
    if lum_distance.all() != 0:
        temp = lum_distance * (10**6)
        distance_modulus = 5 * np.log10(temp/10)

    return distance_modulus + ((((omega_k + 0.06)**2)/((0.05)**2))/len_data) #Adding the omega_k prior.

x_data = z_data
y_data = md_data

parameters, cov = curve_fit(func, x_data, y_data, sigma=err_data, bounds=([0,-1],[1,1]))

fit_omega_m = parameters[0]
fit_w = parameters[1]

theoric_md = np.empty(len_data)

for i in range(0, len_data):
    theoric_md[i] = func(z_data[i], fit_omega_m, fit_w)

print(fit_omega_m)
print(fit_w)
print(np.sqrt(np.diag(cov)))

#Ellipses Plot

x = fit_omega_m
y = fit_w

confidence_plot = plt.subplot()
value = plt.plot(x, y,'.')

confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=1, label=r'$1\sigma$', edgecolor='red', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=2, label=r'$2\sigma$', edgecolor='green', linestyle='--')
confidence_ellipse_cov(x, y, confidence_plot, covariance=cov, n_std=3, label=r'$3\sigma$', edgecolor='blue', linestyle='--')

confidence_plot.legend(loc=2)
plt.show()
'''
