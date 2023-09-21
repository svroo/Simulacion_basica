import os
import numpy as np
import collections

nu = dict()


class Reencuento:
    def __init__(self, size: int, semilla: int, parameters=[48271, 0, 2147483647]):
        self.size = size
        self.semilla = semilla
        self.numeros = list()
        self.parameters = parameters

    def random_number_self(self):
        """Funcion creada de manera propia en la que

        Returns:
            _type_: _description_
        """
        if self.size > 0:
            nums = list()
            for i in range(1, self.size + 1):
                nums.append((((self.size**i) // i) + (self.size - i)) // i)
            return nums
        else:
            return []

    def minimos_cuadrados(self):
        """Funcion que retorna numeros aleatorios del tamaño que se indica en la función, utilizando el algoritmo de cuadrados medios

        Args:
            size (int): Cantidad de numeros aleatorios a generar
            semilla (int, optional): Semilla que se requiere para generar los números aleatorios, tiene que ser de más de 3 digitos. Defaults to 333.

        Returns:
            list[int,]: Lista con la cantidad de numeros pseudoaleatorios que se indican.
        """
        t = len(str(self.semilla))
        assert t >= 3, "El tamaño de la semilla es incorrecto"
        nums = [self.semilla]

        for i in range(self.size):
            num = str(nums[i] ** 2)
            dif = (len(num) - t) // 2

            n = num[dif : t + dif]

            if len(n) % 2 == 1:
                n = "0" + n
            n = int(n)

            nums.append(n)
        return nums[1:]

    def congruenciaLineal(self, normalizar=False):
        """Función para generar numeros aleatorios usando el algoritmo de congruencia lineal. Este método genera una secuancia de números pseudoaletorios a partir de una semilla inicial, utilizando la fórmula:
        xn+1 = (a * xn + c) mod m

        Args:
            size (int): Cantidad de números aleatorios a generar
            parameters (list, optional): Argumentos que se pueden modificar para generar los numeros aleatorios. Defaults to [1103515245, 12345, 32768].
            xn (_type_, optional): Semilla que se va a usar para generar los números aleatorios. Defaults to int(time.time()). Con el valor default se utiliza la hora del sistema

        Returns:
            list[int,]: Lista con la cantidad de números aleatorios generados.
        """
        xn = self.semilla

        a, c, m = self.parameters

        nums = [xn]

        if not normalizar:
            for i in range(self.size):
                xn1 = (a * nums[i] + c) % m
                nums.append(xn1)
        else:
            for i in range(self.size):
                xn1 = (a * nums[i] + c) % m
                nums.append(xn1)

        return nums[1:]

    def Randu(self, normalizar=False):
        """Randu Generador de número aleatorios utiilzado en los 60's y 70's se define como:
        Xn+1 = (2**16 + 3) Xn mod (2**31)

        Args:
            normalizar (bool, optional): Al activar esta funcion los valores que se van a devolver son en un rango de (0 a 1), si quiere valores fuera de ese rango deje el valor como esta. Defaults to False.

        Returns:
            list: Lista con los valores generados de forma aleatoria
        """
        assert self.size > 0, "El número ingresado no es valido"
        assert self.semilla > 0, "El número ingresado no es valido"

        nums = [self.semilla]
        m = 2**31

        if not normalizar:
            for i in range(self.size):
                x_ni = ((2**16) + 3) * nums[i] % m
                nums.append(x_ni)
        else:
            for i in range(self.size):
                x_ni = ((2**16) + 3) * nums[i] % m
                x_ni /= m
                nums.append(x_ni)

        return nums[1:]

    def Rand(self, normalizar=False):
        """Rand Por muchos años (antes de 1995) el generador de la función rand en matlab fue el generador congruencial:
        xn+1 = (7**5) * xn mod(2**31 -1)

        Args:
            size (int): _description_
            x_n (int): _description_
            normalizar (bool, optional): _description_. Defaults to False.

        Returns:
            list[int,]: _description_
        """
        assert self.size > 0, "El numero ingresado no es valido"
        assert self.semilla > 0, "El número ingresado no es valido"

        nums = [self.semilla]

        m = (2**31) - 1

        if not normalizar:
            for i in range(self.size):
                n = (7**5) * nums[i] % m
                nums.append(n)
        else:
            for i in range(self.size):
                n = ((7**5) * nums[i]) % m
                n = n / m
                nums.append(n)

        return nums[1:]

    def guardar_numeros(self, nombre: str, numeros=list, ubi="./Numeros generados/"):
        """Guardar Numeros

        Args:
            ubi (str, optional): Ubicación para guardar los números generados. Defaults to './Numeros generados/'.
            nombre (str) : Nombre que se le va a dar al archivo generado
        """

        # for i,j in numeros.items():
        with open(
            file=ubi + nombre + "_" + str(self.parameters) + ".txt", mode="w"
        ) as f:
            for element in numeros:
                f.write(str(element))
                f.write("\n")

    def generar_numeros(self, propio=False, normalizar=False):
        mini_cua = self.minimos_cuadrados()

        prop = []

        if propio:
            prop = self.random_number_self()

        congruencia = self.congruenciaLineal(normalizar=normalizar)
        randu = self.Randu(normalizar=normalizar)
        rand = self.Rand(normalizar=normalizar)

        numeros = {
            "Algoritmo_minimos_cuadrados": mini_cua,
            "Algoritmo_propio": prop,
            "Algoritmo_congruencia_lineal": congruencia,
            "Algoritmo_randu": randu,
            "Algoritmo_rand": rand,
        }

        for i, j in numeros.items():
            self.guardar_numeros(nombre=i, numeros=j)

    def comprobar_numeros(self, ubi="./Numeros generados/"):
        """Comprueba en que indice se encuentran los números y almacena los resultados en un archivo txt en la ubicación que se pasa

        Args:
            ubi (str, optional): Carpeta donde se va a guardar los resultados anteriormente generados, si no existen se generan automaticamente. Defaults to './Numeros generados/'.
        """
        files = os.listdir(ubi)
        # numeros = list()

        # cheek if the files exist
        if not bool(files):
            self.generar_numeros()
            files = os.listdir(ubi)

        for file in files:
            if file != "resultados.txt":
                with open(file=ubi + file, mode="r") as f:
                    for element in f:
                        n = float(element)
                        if n % 1 == 0.0:
                            n = int(element)
                            self.numeros.append(n)
                        else:
                            self.numeros.append(n)

        nums = np.array(self.numeros)
        unique, count = np.unique(nums, return_counts=True)
        res = dict(zip(unique, count))

        indices = dict()

        for i in range(unique.shape[0]):
            aux = list()
            for j in range(nums.shape[0]):
                if nums[j] == unique[i]:
                    aux.append(j)
            indices[unique[i]] = aux

        for numero in unique:
            nu[
                numero
            ] = f"El número {numero} aparece un total de : {res[numero]} veces, en los indices: {indices[numero]}"

        with open(file=ubi + "resultados.txt", mode="w", encoding="utf-8") as file:
            for i, j in nu.items():
                file.write(j)
                file.write("\n")

        print("Terminado")

    def comprobar_numeros_dos(self, ubi="./Numeros generados/"):
        # Comprobar si los archivos ya existen
        if not os.path.exists(ubi):
            os.makedirs(ubi)
            self.generar_numeros()

        numeros_unicos = set()
        indices = {}

        # Leer los archivos y realizar el seguimiento de los índices
        for file in os.listdir(ubi):
            if not file.startswith("resultados_dos"):  # or file != 'resultados.txt':
                with open(os.path.join(ubi, file), "r") as f:
                    for index, element in enumerate(f):
                        n = float(element)
                        if n.is_integer():
                            n = int(n)
                        else:
                            n = round(n)  # Redondear números no enteros
                        numeros_unicos.add(n)
                        indices.setdefault(n, []).append(index)

        # Calcular las frecuencias
        frecuencias = {numero: indices[numero] for numero in numeros_unicos}

        # Escribir los resultados en un archivo
        with open(
            os.path.join(ubi, "resultados_dos_" + str(self.parameters) + ".txt"),
            "w",
            encoding="utf-8",
        ) as file:
            for numero, index_list in frecuencias.items():
                file.write(
                    f"El número {numero} aparece un total de {len(index_list)} veces, en los índices: {index_list}\n"
                )

        print("Terminado")
