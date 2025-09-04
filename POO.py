import yaml
from pathlib import Path

class Pregunta:
    def __init__(self, title, prompt, hints, tags):
        self.title = title
        self.prompt = prompt
        self.hints = hints
        self.tags = tags

    def to_dict(self):
        return {
            "title": self.title,
            "prompt": self.prompt,
            "hints": self.hints,
            "tags": self.tags
        }

def cargar_preguntas_poo():
    preguntas = [
        Pregunta(
            title="Clase Destino",
            prompt="Crea una clase Destino con atributos ciudad y país.",
            hints=["Usa __init__", "self.atributo"],
            tags=["poo", "viajes"]
        ),
        Pregunta(
            title="Método describir",
            prompt="Agrega un método que imprima 'Visitar {ciudad}, {país}'.",
            hints=["Usa f-string", "Accede a self"],
            tags=["poo", "viajes", "métodos"]
        ),
        Pregunta(
            title="Herencia destino playa",
            prompt="Crea DestinoPlaya que herede de Destino y agregue el atributo temperatura.",
            hints=["Usa super()", "Agrega atributo extra"],
            tags=["poo", "viajes", "herencia"]
        ),
        Pregunta(
            title="Contador de destinos",
            prompt="Agrega un atributo de clase que cuente cuántos destinos se crean.",
            hints=["Usa variable de clase", "Incrementa en el constructor"],
            tags=["poo", "viajes", "atributos de clase"]
        ),
        # Agrega 6 preguntas más aquí...
    ]

    archivo_yaml = Path("problems.yaml")
    
    # Leer datos existentes o inicializar lista vacía
    if archivo_yaml.exists():
        with open(archivo_yaml, 'r', encoding='utf-8') as f:
            datos_existentes = yaml.safe_load(f) or []
    else:
        datos_existentes = []

    # Convertir nuevas preguntas a diccionarios
    nuevas_preguntas = [p.to_dict() for p in preguntas]
    # Evitar duplicados basados en el título (opcional)
    titulos_existentes = {p['title'] for p in datos_existentes}
    preguntas_a_agregar = [p for p in nuevas_preguntas if p['title'] not in titulos_existentes]
    
    todos_los_datos = datos_existentes + preguntas_a_agregar

    # Escribir en el YAML con encoding UTF-8
    with open(archivo_yaml, 'w', encoding='utf-8') as f:
        yaml.dump(todos_los_datos, f, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    cargar_preguntas_poo()