# POO.py
from pathlib import Path
from typing import List, Dict
try:
    import yaml
except ImportError as e:
    raise RuntimeError("Falta pyyaml. Instálalo con: pip install pyyaml") from e

PROBLEMS_PATH = Path(__file__).parent / "problems.yaml"


class Pregunta:
    def __init__(self, title: str, prompt: str, hints: List[str] = None, tags: List[str] = None):
        self.title = title
        self.prompt = prompt
        self.hints = hints or []
        self.tags = tags or []

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "prompt": self.prompt,
            "hints": self.hints,
            "tags": self.tags
        }


# Lista por defecto (10 preguntas) — modificá/expandí según quieras
DEFAULT_PREGUNTAS = [
    Pregunta("Clase Mascota", "Crea una clase Mascota con atributos nombre y especie.",
             ["Usa __init__", "self.atributo"], ["poo", "mascotas"]),
    Pregunta("Método alimentar", "Agrega un método alimentar() que imprima '<nombre> está comiendo'.",
             ["Usa print", "Accede a self.nombre"], ["poo", "mascotas", "métodos"]),
    Pregunta("Herencia Perro", "Crea la clase Perro que herede de Mascota y agregue un método ladrar().",
             ["Usa super()", "Método específico de Perro"], ["poo", "mascotas", "herencia"]),
    Pregunta("Encapsular edad", "Haz privado el atributo edad y crea métodos get y set para accederlo.",
             ["Usa __edad", "Getters y setters"], ["poo", "mascotas", "encapsulamiento"]),
    Pregunta("Contador de Mascotas", "Agrega un atributo de clase que cuente cuántas mascotas se crean en total.",
             ["Usa variable de clase", "Incrementa en __init__"], ["poo", "mascotas", "atributos de clase"]),
    Pregunta("Método estático", "Agrega un método estático que muestre un mensaje genérico sobre mascotas.",
             ["Usa @staticmethod", "No requiere self"], ["poo", "métodos", "estáticos"]),
    Pregunta("Clase Gato", "Crea la clase Gato que herede de Mascota y tenga un método maullar().",
             ["Herencia", "Definir método específico"], ["poo", "mascotas", "herencia"]),
    Pregunta("Polimorfismo", "Haz que Perro y Gato sobrescriban un método sonido() con su propio comportamiento.",
             ["Usa override", "Mismo nombre, diferente implementación"], ["poo", "mascotas", "polimorfismo"]),
    Pregunta("Representación", "Agrega __str__ a Mascota para imprimir '<nombre> es un/a <especie>'.",
             ["Definir __str__", "Usa return con formato"], ["poo", "métodos especiales"]),
    Pregunta("Comparación de edad", "Agrega __lt__ para comparar mascotas por edad con '<'.",
             ["Definir __lt__", "Comparar self.__edad"], ["poo", "métodos especiales", "comparación"])
]


def _normalize_title(t: str) -> str:
    return (t or "").strip().lower()


def cargar_preguntas() -> int:
    """
    Lee problems.yaml (si existe) y agrega las preguntas por defecto que no estén ya.
    Devuelve la cantidad de preguntas agregadas.
    """
    # Cargar existentes
    if PROBLEMS_PATH.exists():
        with PROBLEMS_PATH.open("r", encoding="utf-8") as f:
            existing = yaml.safe_load(f) or []
            if not isinstance(existing, list):
                raise RuntimeError("Formato inválido en problems.yaml: se esperaba una lista")
    else:
        existing = []

    existing_titles = {_normalize_title(p.get("title", "")) for p in existing}

    to_add = []
    for preg in DEFAULT_PREGUNTAS:
        n = _normalize_title(preg.title)
        if n not in existing_titles:
            to_add.append(preg.to_dict())
            existing_titles.add(n)

    if to_add:
        existing.extend(to_add)
        # Guardar manteniendo el orden (sort_keys=False) y permitiendo unicode
        with PROBLEMS_PATH.open("w", encoding="utf-8") as f:
            yaml.safe_dump(existing, f, allow_unicode=True, sort_keys=False)

    print(f"[POO] Preguntas por defecto: {len(DEFAULT_PREGUNTAS)} — agregadas: {len(to_add)}")
    return len(to_add)


if __name__ == "__main__":
    cargar_preguntas()
