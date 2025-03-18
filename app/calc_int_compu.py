def format_currency(amount):

    """
    Formatea un valor numérico como moneda con símbolo de dólar.
    
    Args:
        amount (float): Cantidad a formatear.
        
    Returns:
        str: Cadena formateada con el símbolo de dólar, separador de miles y dos decimales.
    """

    return '${:,.2f}'.format(amount)


def calc_por_inter(P, p, n):
    """
    Calcula la tasa de interés periódica a partir del monto inicial, monto final y número de períodos.
    
    Args:
        P (float): Monto inicial o principal.
        p (float): Monto final o valor futuro.
        n (float): Número de períodos.
        
    Returns:
        float: Tasa de interés periódica en porcentaje.
    """
    return ((p/P)**(1/n)-1)*100


def ted_tea(tasa_diaria):
    """
    Convierte una Tasa Efectiva Diaria (TED) a Tasa Efectiva Anual (TEA).
    
    Args:
        tasa_diaria (float): Tasa efectiva diaria en porcentaje.
        
    Returns:
        float: Tasa efectiva anual en porcentaje.
    """
    # Conversor de tasa efectiva diaria a tasa efectiva anual
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**days - 1)*100


def tea_ted(tasa_anual):
    """
    Convierte una Tasa Efectiva Anual (TEA) a Tasa Efectiva Diaria (TED).
    
    Args:
        tasa_anual (float): Tasa efectiva anual en porcentaje.
        
    Returns:
        float: Tasa efectiva diaria en porcentaje.
    """
    
    days = 365 # * Año de 365 días *
    return ((1 + tasa_anual/100)**(1/days) - 1)*100


def tem_tea(tasa_mensual):
    """
    Convierte una Tasa Efectiva Mensual (TEM) a Tasa Efectiva Anual (TEA).
    
    Args:
        tasa_mensual (float): Tasa efectiva mensual en porcentaje.
        
    Returns:
        float: Tasa efectiva anual en porcentaje.
    """
    
    return ((1 + tasa_mensual/100)**12 - 1)*100


def tea_tem(tasa_anual):
    """
    Convierte una Tasa Efectiva Anual (TEA) a Tasa Efectiva Mensual (TEM).
    
    Args:
        tasa_anual (float): Tasa efectiva anual en porcentaje.
        
    Returns:
        float: Tasa efectiva mensual en porcentaje.
    """
    
    return ((1 + tasa_anual/100)**(1/12) - 1)*100


def tem_ted(tasa_mensual):
    """
    Convierte una Tasa Efectiva Mensual (TEM) a Tasa Efectiva Diaria (TED).
    
    Args:
        tasa_mensual (float): Tasa efectiva mensual en porcentaje.
        
    Returns:
        float: Tasa efectiva diaria en porcentaje.
    """

    days = 365 # * Año de 365 días *
    return ((1 + tasa_mensual/100)**(12/days) - 1)*100


def ted_tem(tasa_diaria):
    """
    Convierte una Tasa Efectiva Diaria (TED) a Tasa Efectiva Mensual (TEM).
    
    Args:
        tasa_diaria (float): Tasa efectiva diaria en porcentaje.
        
    Returns:
        float: Tasa efectiva mensual en porcentaje.
    """
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**(days/12) - 1)*100


def calc_interes(P, r, n):
    """
    Calcula el monto final de una inversión o préstamo con interés compuesto.
    
    Args:
        P (float): Monto inicial o principal.
        r (float): Tasa de interés periódica en porcentaje.
        n (float): Número de períodos.
        
    Returns:
        float: Monto final después de n períodos.
    """

    return P*(1 + r/100)**n

# Capex: cap
# Opex: opex
# Producción: energy
# r: tasa de descuento
# n: años de vida útil del proyecto


def calc_lcoe(cap, ope, energy, r, n):
    """
    Cálculo del Costo Nivelado de la Energía (LCOE), que es el costo promedio por unidad-
    de energía producida durante la vida útil de un proyecto de energía.
    Este dato se usa para comparar el costo de producir electricidad con diferentes tecnologías.

    Args:
        cap (float): Costo de inversión (Capex) en millones de dólares.
        ope (float): Costos operativos (Opex) anuales en millones de dólares.
        energy (float): Producción anual de energía en MWh.
        r (float): Tasa de descuento anual (ejemplo 0.05 para 5%).
        n (int): Años de vida útil del proyecto.

    Returns:
        float: Costo Nivelado de la Energía (LCOE) en dólares por MWh.
    """

    # Inicializando acumuladores
    costos_descontados = 0
    produccion_descontada = 0

    for t in range(0, n+1):

        f_desc = (1 + r)**t
        # Sumar CAPEX solo en el primer año, OPEX en todos los años
        costos_anuales = (cap if t == 0 else 0) + (ope if t != 0 else 0)
        # Costos descontados
        costos_descontados += costos_anuales/f_desc
        # Sumar la producción de cada año 
        if t != 0:
            produccion_descontada += energy/f_desc

    lcoe = costos_descontados/produccion_descontada
    return lcoe


if __name__ == '__main__' :

        ###################### Formateo de numeros a moneda ######################

    monto = 1234.56
    print(format_currency(monto))  # Resultado: "$1,234.56"

    ######################################################################################

        ###################### Tasa de interes porcentual ######################

    capital_inicial = 1000 
    capital_final = 1210
    tiempo_en_años = 2

    tasa_de_interes = calc_por_inter(capital_inicial, capital_final, tiempo_en_años)
    print(f"Tasa de interés: {tasa_de_interes:.2f}%")  # Output: 10.00%

    #####################################################################################

    ###################### Tasa efectiva diaria a tasa efectiva anual ######################

    tasa_diaria = 0.03  # 0.03% diario
    tasa_anual = ted_tea(tasa_diaria)
    print(f"TEA: {tasa_anual:.2f}%")  # Resultado: "TEA: 11.57%"

    #####################################################################################

    ###################### Tasa efectiva anual a tasa efectiva diaria ######################

    tasa_anual = 10  # 10% anual
    tasa_diaria = tea_ted(tasa_anual)
    print(f"TED: {tasa_diaria:.4f}%")  # Resultado: "TED: 0.0261%"

    #####################################################################################

    ###################### Tasa efectiva mesual a tasa efectiva anual ######################

    tasa_mensual = 1  # 1% mensual
    tasa_anual = tem_tea(tasa_mensual)
    print(f"TEA: {tasa_anual:.2f}%")  # Resultado: "TEA: 12.68%"

    #####################################################################################

    ###################### Tasa efectiva anual a tasa efectiva mesual ######################

    tasa_anual = 12  # 12% anual
    tasa_mensual = tea_tem(tasa_anual)
    print(f"TEM: {tasa_mensual:.2f}%")  # Resultado: "TEM: 0.95%"

    #####################################################################################

    ###################### Tasa efectiva mensual a tasa efectiva diaria ######################

    tasa_mensual = 1  # 1% mensual
    tasa_diaria = tem_ted(tasa_mensual)
    print(f"TED: {tasa_diaria:.4f}%")  # Resultado: "TED: 0.0329%"

    #####################################################################################

    ###################### Tasa efectiva diaria a tasa efectiva mesual ######################

    tasa_diaria = 0.03  # 0.03% diario
    tasa_mensual = ted_tem(tasa_diaria)
    print(f"TEM: {tasa_mensual:.2f}%")  # Resultado: "TEM: 0.92%"

    #####################################################################################

    ###################### Calculo del interes compuesto ######################

    capital = 1000
    tasa = 5  # 5% 
    periodos = 3  # años
    monto_final = calc_interes(capital, tasa, periodos)
    print(format_currency(monto_final))  # Resultado: "$1,157.63"

    #####################################################################################

    ########## LCOE (Levelized Cost of Energy) o Costo Nivelado de Energía ##########

    # Ejemplo: proyecto solar
    capex = 1000 # $1k de inversión inicial
    opex = 100    # $100 de costos operativos anuales
    energia_anual = 500  # 500 Wh generados por año
    tasa_descuento = 0.1   # 10% de tasa de descuento
    vida_util = 3          # 3 años de vida útil

    lcoe = calc_lcoe(capex, opex, energia_anual, tasa_descuento, vida_util)
    print(f"El LCOE del proyecto es: ${lcoe:.4f} por MWh") # Resultado: "El LCOE del proyecto es: $1.004 por MWh