#!/usr/bin/env python
# Package for calculate light curves of stellar occultations events
# LIBRERIA PARA CALCULO DE CURVAS DE LUZ DE OCULTACIONES ESTELARES
## JOEL H.CASTRO JULIO 2019

import numpy as np
import pandas as pd

SUN_TEMPERATURE_KELVIN = 5780  # Temperatura del SOl en grados Kelvin
SUN_RADIUS_METERS = 6.96e8  # Radio del sol en mts
PARSEC_IN_METERS = 3.085e16
ASTRONOMICAL_UNIT_METERS = 1.496e11


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (phi, rho)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def calculate_image_grid(n_pixels, plane):
    centered_axis = np.linspace(-plane / 2, plane / 2, n_pixels)
    x, y = np.meshgrid(centered_axis, centered_axis)
    phi_grid, rho_grid = cart2pol(x, y)
    return phi_grid, rho_grid


def pupilCO(n_pixels, plane, object_diameter):
    """Genera obstruccion circular

    Keyword arguments:
    n_pixels -- matrix size in pixels
    plane -- size of matrix in meters
    object_diameter -- oscurecimiento central/diametro en metros
    """
    phi, rho = calculate_image_grid(n_pixels, plane)
    return np.double(rho >= object_diameter / 2)


def trasladar_px(object_matrix, dx, dy):
    """Trasladar una matriz en direcciones X, Y
    según el numero de pixeles en cada coordenada  Xpx, Ypx respectivamente.

    Si mx > 0 Se mueve hacia la derecha.
    Si my > 0 se mueve hacia arriba en las graficas"""
    object_array = np.array(object_matrix)
    P_rolled = np.roll(object_array, dx, axis=1)
    return np.roll(P_rolled, dy, axis=0)


def pupil_doble(
    n_pixels,
    plane,
    object_diameter,
):
    """Generar obstruccion tipo Binario de Contacto con la misma area de una obstruccion circular de diametro d.
    n_pixels -- matrix size in pixels
    plane -- size of matrix in meters
    object_diameter -- oscurecimiento central/diametro en metros como si fuese circular
    """

    Dx, Dy, r1, r2 = calculate_binary_parameters(object_diameter)
    sepX = calculate_separation(n_pixels, plane, Dx)
    sepY = calculate_separation(n_pixels, plane, Dy)
    th, r = calculate_image_grid(n_pixels, plane)
    # Generar Objetos
    P1 = np.double(r >= r1)  # Obstruccion grande
    P2 = np.double(r >= r2)  # Obstruccion pequena
    # separar objetos simetricamente Usar funcion trasladar
    P = trasladar_px(P1, -sepX, sepY) + trasladar_px(P2, sepX, sepY)
    # Binarizar
    P = P == 2
    return np.double(P)


def calculate_separation(n_pixels, plane, diameter):
    return int(np.floor(((diameter / 2) / plane) * n_pixels))


def calculate_binary_parameters(object_diameter):
    primary_radius = (object_diameter / 2) * 0.65
    secondary_radius = np.sqrt((object_diameter / 2) ** 2 - (primary_radius) ** 2)
    dx = 0.45 * 2 * primary_radius + 0.45 * 2 * secondary_radius
    dy = 0
    return dx, dy, primary_radius, secondary_radius


def pupilCA(M, D, d):
    """Generar apertura circular"""
    # M>> tamaño matriz en pixeles
    # D>> tamaño de matriz en metros
    # d>> oscurecimiento central en metros
    m = np.linspace(-D / 2, D / 2, M)
    a, b = np.meshgrid(m, m)
    th, r = cart2pol(a, b)
    P = np.double(r <= d / 2)
    return P


def pupilSO(M, D, d):
    """Generar obstruccion cuadrada"""
    # M>> tamaño matriz en pixeles
    # D>> tamaño de matriz en metros
    # d>> oscurecimiento central en metros
    t = M * d / D
    c = M / 2
    P = np.ones((M, M))
    P[-t / 2 + c : t / 2 + c, -t / 2 + c : t / 2 + c] = 0
    # & A>=m/(d/2))

    return P


def pupilSA(M, D, d):
    """Generar apertura cuadrada"""
    # M>> tamaño matriz en pixeles
    # D>> tamaño de matriz en metros
    # d>> oscurecimiento central en metros
    t = M * d / D
    c = M / 2
    P = np.zeros((M, M))
    P[-t / 2 + c : t / 2 + c, -t / 2 + c : t / 2 + c] = 1  # & A>=m/(d/2))

    return P


def fresnel(U0, M, plano, z, lmda):
    """Calcular el patron de difraccion en Intensidad de un objeto a  una distancia z"""
    k = 2 * np.pi / lmda
    nx, ny = np.shape(U0)
    x = (plano / M) * nx  # ojo normalmente nx=M por lo tanto x=plano en metros
    y = (plano / M) * ny
    fx = 1 / x  # frecuencia espacial en m**-1
    fy = 1 / y

    u = np.ones((nx, 1)) * (np.arange(0, nx) - nx / 2) * fx
    v = np.transpose((np.arange(0, ny) - ny / 2) * np.ones((ny, 1)) * fy)

    O = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(U0)))
    # O=fft2(U0)
    H = np.exp(1j * k * z) * np.exp(-1j * np.pi * (lmda * z) * (u ** 2 + v ** 2))

    U = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(np.multiply(O, H))))
    # U=ifft2(O*H)
    I = np.abs(U) ** 2
    # import pdb; pdb.set_trace()
    return I


def spectra(U0, M, plano, z, spectral_type, nLmdas):
    star_parameters = select_data_by_spectraltype(spectral_type)
    file_path = "data/spectra/" + ["Spectra_filename"].iloc[0] # Direccion del archivo de datos de la convolucion FILTRO,ESTRELLA
    convolution_df = pd.read_csv(file_path, sep=",", header=None)  # datos en formato panda
    convolution_data_array = np.array(convolution_df)  # datos en formato numpy
    a, b = convolution_data_array.shape
    ind = np.round(np.linspace(0, a - 1, nLmdas))  # indices para lambda y peso
    acc = np.zeros((U0.shape))
    cont = 1

    for k in ind:
        lamda = convolution_data_array[int(k)][0] * 1e-10
        peso = convolution_data_array[int(k)][1]

        I = fresnel(U0, M, plano, z, lamda) * peso
        # print(lamda)
        acc = acc + I
        # print(np.min(np.min(I)))
        cont = cont + 1  # Correcciones para probar errores en original matlab
    # acc=acc/cont   #OJO NO SE DEBERIA DIVIDIR
    In = acc / acc[0][0]
    return In


def select_data_by_spectraltype(spectral_type):
    stars_data = pd.read_csv("data/estrellas.csv")
    return stars_data[stars_data["Spectral_type"] == spectral_type]


def calculate_star_radius(mV, spectral_type, object_distance_ua):
    """Funcion para calcular los radios aparentes de estrellas

    Keyword arguments:
    mV --> magnitud Aparente
    spectral_type --> tipo espectral de la estrella
    object_distance_ua --> Distancia al objeto ua

    Output:
    R_star --> radio aparente de estrella calculado"""

    object_distance = ua2meters(object_distance_ua)  # distancia en metros

    star_parameters = select_data_by_spectraltype(spectral_type)
    T0 = star_parameters["Temperature"].iloc[0]  # Temperature
    M0 = star_parameters["Absolute_magnitude"].iloc[0]  # Absolute Magnitude
    L0 = star_parameters["Luminosity_rel"].iloc[0]  # Luminosity relative to the Sun
    distance_pc = 10 ** ((mV - M0 + 5) / 5)
    distance_m = parsec2meters(distance_pc)  # Convirtiendo de parsecs PCs a mts (distancia)
    star_radius = (L0 ** 0.5) / (
        T0 / SUN_TEMPERATURE_KELVIN
    ) ** 2  # Radio de la estrella en SUN_RADIUS_METERS
    alfa = (
        SUN_RADIUS_METERS * star_radius
    ) / distance_m  # Tamano angular de la estrella en radianes
    aparent_radius_meters = (
        alfa * object_distance
    )  # Tam de la estrella en mts, RADIO...sobre el objeto
    return aparent_radius_meters


def parsec2meters(distance_pc):
    return PARSEC_IN_METERS * distance_pc


def ua2meters(distance_ua):
    return ASTRONOMICAL_UNIT_METERS * distance_ua


def promedio_PD(I, R_star, plano, M, d):
    """    
    Keyword arguments:
    I --> es la imagen del patron de difraccion en intensidad
    R_star --> es el radio aparente de la estrella mts--> Calcular con: calc_rstar()
    plano --> tamano de la pantalla blanca diametro mts
    M --> tamano de la matriz en pixeles
    d -->  diametro del objeto en mts"""
    star_px = ((R_star) / plano) * M
    obj_px = ((d / 4) / plano) * M
    div = np.ceil(star_px / obj_px)
    rr = star_px / div
    reso = np.arange(rr, star_px + 0.0001, rr)  # arange(start,stop,step) Resolucion de paso

    kin = len(reso)
    # print(star_px)
    # print(rr)
    mu2 = np.zeros((I.shape))
    co = 1
    for k1 in range(kin):
        # calculo de desplazamiento en teta
        perim = 2 * np.pi * reso[k1]  # perimetro en pixeles
        paso = np.ceil(perim / obj_px)  # Num de veces que cabe el objeto en el perimetro
        resot = (2 * np.pi) / paso  # Paso en radianes
        # print(resot)
        k2 = np.arange(resot, 2 * np.pi + 0.0001, resot)  # ***OJO ESTO COMIENZA EN 0
        for teta in k2:
            mu2 = trasladar_px(I, reso[k1] * np.cos(teta), reso[k1] * np.sin(teta)) + mu2
            co += 1
            # print(np.min(np.min(mu2)))

    Ix = mu2 + I
    # print(np.min(np.min(I)))
    Ix = Ix / Ix[0][0]
    # Ix=(mu2+I)/co #normalizar
    # Ix=Ix/(Ix[M-np.int(M*0.1),M-np.int(M*0.1)]) #Normalizar
    return Ix


def extraer_perfil(I0, M, D, T, b):
    """Funcion que extrae el perfil de difraccion de un patron I0
    I0--> Patron de difraccion, matriz MxM
    M--> Num de pixeles en una dimension de la matriz del patron de difraccion
    D--> Tamanio en metros del plano donde se encuantra el objeto y el patron de difraccion
    T--> Angulo Tetha al cual sera extraido el perfil
    b--> parametro de impacto en metros
    OUT --> x,y vectores con los valores de x en metros y de las intensidades del patron"""
    # Funcion para extraer perfil de difraccion
    # T=0
    # b=1000
    m2p = M / D
    x = np.linspace(-D / 2, D / 2, M)
    # calcular los arreglos de coordenada X a extraer
    x1 = x * np.cos(T * np.pi / 180) - b * np.sin(T * np.pi / 180)
    x2 = x * np.sin(T * np.pi / 180) + b * np.cos(T * np.pi / 180)
    # Convertir a numero de pixeles
    hp = np.array(m2p * x1) + M / 2  # ojo el +M/2 es para iniciar en positivos
    vp = np.array(m2p * x2) + M / 2
    hp = hp.astype(int)
    vp = vp.astype(int)
    y = np.ones(x.shape)
    for k in range(M - 1):
        y[k] = I0[vp[k], hp[k]]  # Ojo Numpy invierte los ejes
    return (x, y)


def calculate_fresnel_scale(λ, z):
    return np.sqrt(λ * z / 2)


def calculate_plane(object_diameter, λ, object_distance_ua):
    """Funcion para calcular el tamanio del plano (objeto y de difraccion) optimo para objetos pequenos (<10km)
    evitando el problema de escalamiento de la FFT
    object_diameter --> tam de objeto en metros diametro
    λ --> long de onda en metros
    object_distance_ua --> dist del objeto en UA
    OUT --> plane: tamanio del plano en metros (una dimension)"""
    object_distance_meters = ua2meters(object_distance_ua)
    fresnel_scale = calculate_fresnel_scale(λ, object_distance_meters)  # escala de fresnel
    Rho = object_diameter / (2 * fresnel_scale)
    plane = (50 * object_diameter) / Rho
    return plane


def add_ruido(I, mV):
    """Anadir ruido de Poisson a una imagen
    I--> matriz de la imagen
    mV--> magnitud aparente de la estrella
    OUT--> In: matriz con ruido anadido, asumiendo RUIDO=1/SNR calculada de TAOS-II"""
    ruido = 1 / SNR_TAOS2(mV)
    n_mask = np.random.poisson(I)
    n_mask = (
        n_mask / np.mean(n_mask)
    ) * ruido - ruido  # pesando el ruido de acuerdo con TAOS-II y normalizando
    In = I + n_mask
    return In


def SNR_TAOS2(mV):
    """Ajuste polinomial para la curva de  SNR de TAOS-II
    mV-->Magnitud aparente de la estrella
    OUT--> SNR: valor de senal a ruido de TAOS-II"""
    x = mV
    p1 = 1.5792
    p2 = -57.045
    p3 = 515.04
    SNR = p1 * x ** 2 + p2 * x + p3
    return SNR


def muestreos(lc, D, vr, fps, toff, vE, opangle, ua):
    """Funcion para muestrear el perfil de difraccion obteniendo el punto promedio
    lc--> perfil de difraccion o curva de luz
    D--> tamaño del plano en metros
    vr--> velocidad del objeto ~5000 m/s (positiva si va en contra de la vel de la tierra)
    fps--> frames pos segundo de la camara, 20 para TAOS-2
    toff--> Tiempo de desfase dentro del periodo de muestreo
    vE--> velocidad traslacional de la tierra ==29800 m/s
    opangle--> angulo desde oposicion del objeto: O,S,E
    ua--> Distancia en Unidadades Astronomicas del objeto
        OUT--> s_lin,lc_lin,s_pun,lc_pun: vetores de tiempo para lineas, muestra en lineas, tiempo en puntos y muestra en puntos RESPECTIVAMENTE"""
    tam = lc.size
    T = 1 / fps  # Tiempo de exposicion
    OA = opangle * np.pi / 180  # Angulo desde oposicion en radianes
    Vt = (
        vE * (np.cos(OA) - np.sqrt((1 / ua) * (1 - (1 / ua ** 2) * np.sin(OA) ** 2))) + vr
    )  # Velocidad tangencial del obj. rel a tierra
    t = D / Vt  # visibilidad del plano en segundos
    Nm = t / T  # numero de muestras totales en el plano de observacion
    dpix = np.int(tam / Nm)
    pixoffset = np.int(toff)
    Xpx = tam
    curv = lc

    # partir en 2 la curva para comenzar a muestrear desde el centro, por eso uso fliplr
    curv1 = np.flip(curv[: np.int(Xpx / 2) + pixoffset])
    curv2 = curv[np.int(Xpx / 2) + pixoffset : Xpx]
    mcurv1 = np.ones(np.size(curv1))  # vector de muestras lineas
    mcurv2 = np.ones(np.size(curv2))  # vector de muestras lineas
    cmuestras1 = np.ones(
        (np.int(np.floor((Xpx / 2) / dpix + pixoffset / dpix)))
    )  # vector de muestras puntos
    cmuestras2 = np.ones(
        (np.int(np.floor((Xpx / 2) / dpix - pixoffset / dpix)))
    )  # vector de muestras puntos

    n = 0  # Muestrear curva 1
    for cu in range(cmuestras1.size):
        mcurv1[(cu) * dpix : (cu + 1) * dpix] = np.mean(curv1[(cu) * dpix : (cu + 1) * dpix])
        cmuestras1[n] = np.mean(curv1[(cu) * dpix : (cu + 1) * dpix])
        n = n + 1

    n = 0  # Muestrear curva 2
    for cu in range(cmuestras2.size):
        mcurv2[(cu) * dpix : (cu + 1) * dpix] = np.mean(curv2[(cu) * dpix : (cu + 1) * dpix])
        cmuestras2[n] = np.mean(curv2[(cu) * dpix : (cu + 1) * dpix])
        n = n + 1

    lc_lin = np.append(np.flip(mcurv1), mcurv2)  # Juntando curvas con lineas constantes
    lc_pun = np.append(np.flip(cmuestras1), cmuestras2)  # extraccion de puntos
    # Calculo de tiempos
    s_lin = np.linspace(-t / 2, t / 2, lc_lin.size)
    #  vector de tiempo para lineas
    s_pun = np.linspace(-t / 2, t / 2, lc_pun.size)
    #  vector de tiempo para puntos
    return (s_lin, lc_lin, s_pun, lc_pun)


def buscar_picos(x, y, D, fil=0.005):
    """Funcion para buscar picos con la derivada de la ocultacion
    IN...
    x,y--> vectores con los datos de la ocultacion,distancia y amplitud
    D--> diametro del objeto [mts]
    fil--> valor de umbral para identificar los picos, DEFAULT=0.005
    OUT--> indices para ubicar los PICOS EN y,  también los valores.
    """
    yp = np.diff(y)  # derivada de la ocultacion
    cyp = abs(yp) < fil  # convertir 0s en 1s de la derivada, buscar valores cercanos a 0
    xin = np.where(abs(x) < (D / 2))  # seleccionar solo la region de la ocultacion
    xin2 = np.array(xin)  # convertir los indices (tuple) en arreglo de numpy
    indx = np.where(cyp[xin] == 1)  # buscar los 1s en el rango establecido (xin)
    inpks = (
        xin2[0, 0] + indx
    )  # estos son los indices donde están los picos en la curva de luz original

    Y = np.array(y[inpks])  # valores pico
    ban = 0
    inew = []
    pY = []
    for k in range(Y.size - 1):  # Eliminar Repetidos
        I = Y[0, k]
        J = Y[0, k + 1]
        if np.abs(I - J) > fil or ban == 0:  # si NO esta repetido
            inew.append(inpks[0, k + 1])  # Indice del pico en la curva de luz
            pY.append(J)  # Valor del pico en la curva de luz
            ban = 1
    pY = np.array(pY)

    return (inew, pY)
