import math

def qlrps(fmhz, zsys, en0, ipol, eps, sgm):
    """
    ???

    """
    gma = 157e-9
    wn  = fmhz / 47.7
    ens  = en0
    
    if zsys != 0:

        ens = ens * exp(-zsys / 9460)

    gme  = gma * (1 - 0.04665 * exp(ens / 179.3))

    zq   = complex(eps, 376.62 * sgm / wn)

    zgnd = math.sqrt(zq - 1)

    if ipol != 0:

        zgnd = zgnd / zq

    return wn, gme, ens, zgnd