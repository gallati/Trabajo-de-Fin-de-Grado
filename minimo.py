import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from model import Model

# def grafica_errores(n, Mtot=5.0, Rtot=11.5, Ltot=70.0, Tc=2.0, dR=0.5, dL=5.0):
#     """
#     Genera una gráfica que muestra el error relativo total para variaciones de L y R.

#     ## Parámetros:
#         * n: Tamaño del máximo incremento. Se calculan incrementos como [Xtot - n*dX, ..., Xtot + 0*dX, ..., Xtot + n*dX]
#         * Mtot: Masa total del modelo (default 5.0)
#         * Rtot: Radio total del modelo (default 11.5)
#         * Ltot: Luminosidad total del modelo (default 70.0)
#         * Tc: Temperatura central del modelo (default 2.0)
#         * dR: Variación del radio (default 0.5)
#         * dL: Variación de la luminosidad (default 5.0)
#     """

#     # Dimensiones de la tabla e inicialización de la matriz de errores
#     d = 2*n+1
#     matriz_error = np.zeros((d, d), dtype=float)

#     # Creamos la figura
#     plt.rcParams['font.family'] = 'serif'   # Cambiamos la fuente utilizada
#     figSize = (10, 7)
#     fig, ax = plt.subplots(figsize=figSize)

#     # Calculamos la matriz de errores
#     for i in range(d):
#         for j in range(d):
#             matriz_error[i, j] = Model(Mtot=Mtot, Rtot=Rtot + (j-n)*dR, Ltot=Ltot+(i-n)*dL, Tc=Tc).error()
#             ax.text(j, i, f'{matriz_error[i, j]:.2f} %', ha='center', va='center')

#     # Generamos el imshow y lo representamos
#     imshow = ax.imshow(matriz_error, cmap='coolwarm', vmax=100.0)
#     ax.set_title(f"M$_{{Tot}}$={Mtot}   R$_{{Tot}}$={Rtot}   L$_{{Tot}}$={Ltot}   T$_{{c}}$={Tc}   $\\delta$R={dR}   $\\delta$L={dL}")
#     ax.set_xticks(range(d))
#     ax.set_xticklabels([f"{j-n}·$\\delta$R" for j in range(d)])
#     ax.set_yticks(range(d))
#     ax.set_yticklabels([f"{i-n}·$\\delta$L" for i in range(d)])

#     plt.colorbar(imshow)
#     plt.show()


# grafica_errores(2, Mtot=5.0, Rtot=11.06, Ltot=76.01, Tc=1.956, dR=0.1, dL=1.0)



# def minimo_error_modelo(x):
#     return Modelo(Mtot=5.0, Rtot=x[0], Ltot=x[1], Tc=x[2]).error()

# initial_guess = [11.06, 76.01, 1.956]

# result = minimize(minimo_error_modelo, initial_guess)

# print(result)

# print(Modelo(Mtot=5.0, Rtot=10.93, Ltot=73.52, Tc=1.95).error())



# Limitations of stellar structure models
#   Spherical Symmetry Assumption ignores rotation and magnetic fields
#       May not accurately represent rapidly rotating stars (Betelgeuse)
#   Local Thermodynamic Equilibrium (LTE) assumes energy transport is local
#       Can break down in stellar atmospheres where radiation becomes non-local
#   Mixing Length Theory provides simplified model of convection
#       Introduces free parameters that may not fully capture complex convective processes
#   Time-Independence assumes instantaneous adjustment of stellar structure
#       May not accurately represent rapid evolutionary phases (supernova explosions)
#   Neglect of Mass Loss overlooks important processes in massive stars and late evolutionary stages
#       Significant for Wolf-Rayet stars and red giants
#   One-Dimensional Modeling ignores 3D effects like turbulence and convective overshooting
#       Limits accuracy in regions with complex fluid dynamics (stellar cores)
#   Nuclear Reaction Rate Uncertainties affect energy generation predictions
#       Can impact estimates of stellar lifetimes and nucleosynthesis
#   Opacity Approximations influence radiative transfer calculations
#       May not fully capture complex atomic and molecular interactions in stellar interiors
#   Equation of State Limitations may not accurately describe all stellar conditions
#       Particularly challenging for extreme environments (white dwarf interiors, neutron star crusts)

# modelo = Model(Rtot=11.06, Ltot=76.01, Tc=1.956)
# print(modelo)
# print(modelo.error())


def gradient_descent(f, r0, eps):
    """
    Gradient descent algorithm to find minimum values for two variables functions.

    ## How it works
        * Given a function f(x, y) and a starting point r0 = (x0, y0)
        it calculates its gradient grad(f(r0)) using central derivatives. Golden-section 
        search method is used to find for which value of the coefficient alpha does the
        function f(alpha) = f(r0 + alpha*grad(f(r0))) have a minimum. Once calculated, a
        new iteration is performed using the minimum point. The algorithm stops when the
        function minimum is found with the desired precision.

    ## Parameters
        * f (function): \\
        babababa
        * r0 (array-like): \\
        babababa
        * eps (float): \\
        bababab
    """

    # Defining the norm
    def norm(r):
        return (r[0]**2 + r[1]**2)**0.5

    # Defining function gradient
    def gf(f, r):
        """
        Given a two variables functions and a point it calculates its gradient.
        """
        x, y = r                                # x and y values
        h = 1e-5                                # Step for central derivatives
        gx = (f([x+h/2, y])-f([x-h/2, y]))/h    # Central x derivarive
        gy = (f([x, y+h/2])-f([x, y-h/2]))/h    # Central y derivarive
        
        return np.array([gx, gy], dtype=float)

    # Defining golden-section search method
    def golden_section(f, x1, x4, eps):
        """
        Given a single variable function, two points which in between have a minimum
        and a desired precision it calculates the minimum of the function.
        """

        # Defining golden ratio
        z = (1+5**(1/2))/2

        # Defining internal points
        x2 = x4 - (x4 - x1)/z
        x3 = x1 + (x4 - x1)/z

        # Defining the value of the function in the given points
        f1, f2, f3, f4 = f(x1), f(x2), f(x3), f(x4)

        # Performing the calculation
        while abs(x4 - x1) > eps:

            if f2 < f3:
                x4, f4 = x3, f3 
                x3, f3 = x2, f2 
                x2 = x4 - (x4 - x1)/z 
                f2 = f(x2)
            else: 
                x1, f1 = x2, f2
                x2, f2 = x3, f3 
                x3 = x1 + (x4 - x1)/z 
                f3 = f(x3)

        return (x1 + x4)/2

    # Performing the gradient descent algorithm
    error = 1
    while error > eps:
        
        # Defining the direction to optimize
        def s(alpha):
            return f(r0 + alpha*gf(f, r0)/norm(gf(f, r0)))
        
        # Calculating for which alpha does the direction have a minimum
        alpha1, alpha4 = -1, 1
        alpha_min = golden_section(s, alpha1, alpha4, 1e-6)    
        r1 = r0 + alpha_min*gf(f, r0)/norm(gf(f, r0))
        
        # Calculating the error
        error = norm(r1 - r0)
        
        # Redefining the initial point
        r0 = r1

        print(r1)
    return r1


def f(r):
    return Model(Mtot=5.0, Rtot=r[0], Ltot=r[1], Tc=1.95).error()

print(gradient_descent(f, np.array([11.5, 70.0], dtype=float), 1e-5))
