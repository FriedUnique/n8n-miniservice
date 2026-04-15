from section import Section

def percent(value: float):
    return str(round(value-100, Section.ACCURACY)) + " %"