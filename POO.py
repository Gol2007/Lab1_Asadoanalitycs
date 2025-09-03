# --- Ejercicio 1: Clase Mascota ---
class Mascota:
    # atributo de clase para contar mascotas
    contador = 0  

    def __init__(self, nombre, especie, edad=0):
        self.nombre = nombre
        self.especie = especie
        self.__edad = edad  # atributo encapsulado (privado)
        Mascota.contador += 1  # se incrementa cada vez que se crea una mascota

    # --- Ejercicio 2: Método alimentar ---
    def alimentar(self):
        print(f"{self.nombre} está comiendo")

    # --- Ejercicio 4: Encapsulamiento (getter y setter) ---
    def get_edad(self):
        return self.__edad

    def set_edad(self, nueva_edad):
        if nueva_edad >= 0:
            self.__edad = nueva_edad
        else:
            print("La edad no puede ser negativa")


# --- Ejercicio 3: Herencia ---
class Perro(Mascota):
    def __init__(self, nombre, edad=0):
        super().__init__(nombre, "Perro", edad)

    def ladrar(self):
        print(f"{self.nombre} dice: ¡Guau guau!")


# --- Ejemplo de uso ---
if __name__ == "__main__":
    m1 = Mascota("Mishi", "Gato", 3)
    m2 = Perro("Firulais", 5)

    m1.alimentar()
    m2.alimentar()
    m2.ladrar()

    print("Edad de Mishi:", m1.get_edad())
    m1.set_edad(4)
    print("Edad nueva de Mishi:", m1.get_edad())

    print("Cantidad total de mascotas creadas:", Mascota.contador)
# Fin del código