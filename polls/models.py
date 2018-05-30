from django.db import models


class CandidatoDto:
    name = None
    veces_mencionado = None
    personas_hablando = None
    ratio = None
    promedio = None
    ultimas_menciones = None
    positivos = None
    positivos_porcentaje = None
    negativos = None
    negativos_porcentaje = None
    img_file = None


    def get_name(self):
        return self.name

    def __init__(self, name,
                 veces_mencionado,
                 personas_hablando,
                 ratio,
                 promedio,
                 ultimas_menciones,
                 positivos,
                 positivos_porcentaje,
                 negativos,
                 negativos_porcentaje,
                 img_file):
        self.name = name
        self.veces_mencionado = veces_mencionado
        self.personas_hablando = personas_hablando
        self.ratio = ratio
        self.promedio = promedio
        self.ultimas_menciones = ultimas_menciones
        self.positivos = positivos
        self.positivos_porcentaje = positivos_porcentaje
        self.negativos = negativos
        self.negativos_porcentaje = negativos_porcentaje
        self.img_file = img_file