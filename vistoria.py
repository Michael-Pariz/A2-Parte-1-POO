#classe Vistoria
class Vistoria:
    def __init__(self, pneus, freios, correntes):
        self._pneus = pneus
        self._freios = freios
        self._correntes = correntes

    #função para verificar se o equipamento está danificado ou não
    def esta_danificada(self):
        return not(
            self._pneus and self._freios and self._correntes
        )
    #informa se o equipamennto esta danificado ou não e qual parte
    def __str__(self):
        return (
            f"Pneus: {'OK' if self._pneus else 'DANIFICADO'} | " 
            f"Freios: {'OK' if self._freios else 'DANIFICADO'} | "
            f"Correntes: {'OK' if self._correntes else 'DANIFICADO'}"
        )
