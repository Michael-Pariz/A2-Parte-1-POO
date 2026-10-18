FORMATO_DATA = "%d/%m/%Y"

def formatar_data(data):
    return data.strftime(FORMATO_DATA)


def formatar_data_hora(data_hora):
    return data_hora.strftime(FORMATO_DATA + " %H:%M")
