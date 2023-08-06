def qerf(z):
    """
    The standard normal complementary probability - see function in 
    C. Hastings, Jr. (1955). The maximum error should be 7.5x10^-8.

    Parameters
    ----------
    z : TODO: Type
        TODO: Description
    
    Output
    ------
    qerf1 : float
        TODO:

    """
    
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255987
    b5 = 1.330274429
    rp = 4.317008

    rrt2pi = 0.398942280

    x = z[0]
    t = abs(x)

    if t >= 10:
    
        qerf1 = 0
    
    else:
    
        t = rp / (t + rp)

        qerf1 = (
            exp(-0.5 * x**2) * rrt2pi * 
            ((((b5 * t + b4) * t + b3) * t + b2) * t + b1) * t
            )

    # if (x<0.) qerf1=1.-qerf1  TODO:

    return qerf1