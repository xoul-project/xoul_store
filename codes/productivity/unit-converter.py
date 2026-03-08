def run(value: str = "100", from_unit: str = "kg", to_unit: str = "lb"):
    """
    value: Value (default: 100)
    from_unit: From unit (default: kg)
    to_unit: To unit (default: lb)
    """
    v=float(value)
    conversions={'km_mi':0.621371,'mi_km':1.60934,'m_ft':3.28084,'ft_m':0.3048,'cm_in':0.393701,'in_cm':2.54,'kg_lb':2.20462,'lb_kg':0.453592,'g_oz':0.035274,'oz_g':28.3495,'l_gal':0.264172,'gal_l':3.78541}
    key=f"{from_unit}_{to_unit}"
    if key in conversions:
        r=v*conversions[key]
        print(f"\U0001f4d0 {v} {from_unit} = {r:.4f} {to_unit}")
    elif from_unit=='c' and to_unit=='f':print(f"\U0001f4d0 {v}°C = {v*9/5+32:.1f}°F")
    elif from_unit=='f' and to_unit=='c':print(f"\U0001f4d0 {v}°F = {(v-32)*5/9:.1f}°C")
    else:print(f"\u274c Unknown: {from_unit} \u2192 {to_unit}\n  Supported: km/mi, m/ft, cm/in, kg/lb, g/oz, l/gal, c/f")