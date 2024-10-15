from datetime import datetime
from queue import Queue, LifoQueue
import os

class Tareas:
    """
    Clase que representa una tarea.

    Atributos:
        id (int): Identificador único de la tarea.
        titulo (str): Título de la tarea.
        descripcion (str): Descripción de la tarea.
        prioridad (int): Prioridad de la tarea (1 alta, 3 baja).
        fecha_vencimiento (datetime): Fecha de vencimiento de la tarea.
    """
    def __init__(self, id: int, titulo: str, descripcion: str, prioridad: int, fecha_vencimiento: datetime):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_vencimiento = fecha_vencimiento

    def __str__(self):
        """Representación en string de la tarea."""
        return f'{self.titulo} - {self.descripcion} - Prioridad: {self.prioridad} - Vencimiento: {self.fecha_vencimiento.strftime("%d/%m/%Y")}'


class Categoria:
    """
    Clase que representa una categoría que puede contener subcategorías y tareas.

    Atributos:
        id (int): Identificador único de la categoría.
        nombre (str): Nombre de la categoría.
        subcategorias (list[Categoria]): Lista de subcategorías de esta categoría.
        tareasUrgentes (Queue[Tareas]): Cola de tareas urgentes de esta categoría.
        tareas (list[Tareas]): Lista de tareas asociadas a esta categoría.
    """
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre
        self.subcategorias: list[Categoria] = []
        self.tareasUrgentes: Queue[Tareas] = Queue()
        self.tareas: list[Tareas] = []

    def __str__(self):
        """Representación en string de la categoría."""
        return f'{self.nombre}'

    def agregarSubcategoria(self, id: int, nombre: str):
        """
        Agrega una nueva subcategoría a la categoría actual.
        
        Args:
            id (int): Identificador de la nueva subcategoría.
            nombre (str): Nombre de la nueva subcategoría.
        """
        categoria = Categoria(id, nombre)
        self.subcategorias.append(categoria)


class ManejadorTareas:
    """
    Clase que administra categorías, subcategorías, tareas y permite la gestión de un historial de acciones.

    Atributos:
        categorias (list[Categoria]): Lista de todas las categorías.
        idCategoria (int): Contador para el ID de la próxima categoría.
        idTarea (int): Contador para el ID de la próxima tarea.
        historial_acciones (list): Historial de acciones realizadas.
        historial_deshacer (list): Historial de acciones para deshacer.
    """
    def __init__(self) -> None:
        self.categorias: list[Categoria] = []
        self.idCategoria = 1
        self.idTarea = 1
        self.historial_acciones = LifoQueue()
        self.historial_deshacer = LifoQueue()
  
    def encontrarCategoria(self, id: int = None, nombre: str = None) -> Categoria:
        """
        Encuentra una categoría por ID o nombre.

        Args:
            id (int, optional): ID de la categoría.
            nombre (str, optional): Nombre de la categoría.

        Returns:
            Categoria: La categoría encontrada, o None si no se encuentra.
        """
        # Buscar en las categorías principales
        for categoria in self.categorias:
            # Si se encuentra la categoría, retornarla
            if categoria.id == id or categoria.nombre == nombre:
                return categoria
            # Buscar en las subcategorías
            for subcategoria in categoria.subcategorias:
                resultado = self.encontrarCategoriaEnSubcategorias(subcategoria, id, nombre)
                if resultado:
                    return resultado
        return None

    def encontrarCategoriaEnSubcategorias(self, categoria: Categoria, id: int = None, nombre: str = None) -> Categoria:
        """
        Busca una categoría en las subcategorías recursivamente.

        Args:
            categoria (Categoria): Categoría inicial donde empezar la búsqueda.
            id (int, optional): ID de la categoría.
            nombre (str, optional): Nombre de la categoría.

        Returns:
            Categoria: La categoría encontrada, o None si no se encuentra.
        """
        # Si se encuentra la categoría, retornarla
        if categoria.id == id or categoria.nombre == nombre:
            return categoria
        # Buscar en las subcategorías
        for subcategoria in categoria.subcategorias:
            resultado = self.encontrarCategoriaEnSubcategorias(subcategoria, id, nombre)
            if resultado:
                return resultado
        return None

    def agregarCategoria(self, nombre: str):
        """
        Agrega una nueva categoría.

        Args:
            nombre (str): Nombre de la nueva categoría.
        """
        # Verificar si la categoría ya existe
        categoria = self.encontrarCategoria(nombre=nombre)
        if categoria:
            print('Error: La categoría ya existe.')
        else:
            # Agregar la nueva categoría
            self.categorias.append(Categoria(self.idCategoria, nombre))
            # Incrementar el contador de categorías
            self.idCategoria += 1
            # Mostrar mensaje de éxito
            print(f"Categoría '{nombre}' agregada correctamente.")

    def agregarSubcategoria(self, nombre: str, nombreCategoria: str):
        """
        Agrega una nueva subcategoría a una categoría existente.

        Args:
            nombre (str): Nombre de la subcategoría.
            nombreCategoria (str): Nombre de la categoría padre.
        """
        # Encontrar la categoría padre
        categoria = self.encontrarCategoria(nombre=nombreCategoria)
        if categoria:
            # Agregar la subcategoría
            categoria.agregarSubcategoria(self.idCategoria, nombre)
            # Incrementar el contador de categorías
            self.idCategoria += 1
            # Mostrar mensaje de éxito
            print(f"Subcategoría '{nombre}' agregada a '{nombreCategoria}'.")
        else:
            # Mostrar mensaje de error si la categoría padre no existe
            print('Error: La categoría no existe.')

    def mostrarCategorias(self):
        """
        Muestra todas las categorías y sus subcategorías, incluyendo las tareas.
        """
        # Verificar si hay categorías
        if not self.categorias:
            # Mostrar mensaje si no hay categorías
            print("No hay categorías disponibles.")
        else:
            # Mostrar cada categoría
            for categoria in self.categorias:
                print(f"Categoría: {categoria}")
                self.mostrarTareas(categoria)
                self.mostrarSubcategorias(categoria, nivel=1)

    def mostrarSubcategorias(self, categoria: Categoria, nivel: int):
        """
        Muestra recursivamente todas las subcategorías de una categoría específica.

        Args:
            categoria (Categoria): Categoría para mostrar sus subcategorías.
            nivel (int): Nivel de profundidad (para fines de visualización).
        """
        # Mostrar cada subcategoría
        for subcategoria in categoria.subcategorias:
            print(' ' * nivel * 2 + f'- Subcategoría: {subcategoria}')
            # Mostrar tareas de la subcategoría
            self.mostrarTareas(subcategoria, nivel + 1)
            # Mostrar subcategorías de la subcategoría
            self.mostrarSubcategorias(subcategoria, nivel + 1)

    def mostrarTareas(self, categoria: Categoria, nivel: int = 0):
        """
        Muestra las tareas asociadas a una categoría.

        Args:
            categoria (Categoria): Categoría para mostrar sus tareas.
            nivel (int, optional): Nivel de profundidad (para fines de visualización).
        """
        # Mostrar tareas de la categoría
        if categoria.tareas:
            print(' ' * nivel * 2 + f'Tareas en {categoria.nombre}:')
            # Mostrar cada tarea
            for tarea in categoria.tareas:
                # Mostrar información de la tarea
                print(' ' * (nivel + 2) * 2 + f'* ID: {tarea.id} - {tarea}')
        else:
            # Mostrar mensaje si no hay tareas
            print(' ' * nivel * 2 + f'No hay tareas en {categoria.nombre}.')

    def agregarTarea(self, titulo: str, descripcion: str, prioridad: int, fecha_vencimiento: datetime, categoria_nombre: str):
        """
        Agrega una tarea a una categoría específica.

        Args:
            titulo (str): Título de la tarea.
            descripcion (str): Descripción de la tarea.
            prioridad (int): Prioridad de la tarea (1 alta, 3 baja).
            fecha_vencimiento (datetime): Fecha de vencimiento de la tarea.
            categoria_nombre (str): Nombre de la categoría donde agregar la tarea.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        if categoria:
            # Crear la tarea y agregarla a la categoría
            tarea = Tareas(self.idTarea, titulo, descripcion, prioridad, fecha_vencimiento)
            categoria.tareas.append(tarea)
            # Incrementar el contador de tareas
            self.idTarea += 1
            # Agregar la acción al historial
            self.historial_acciones.put(('agregar', tarea, categoria))
            print(f"Tarea '{titulo}' agregada correctamente a la categoría '{categoria_nombre}'.")
        else:
            # Mostrar mensaje de error si la categoría no existe
            print('Error: La categoría no existe.')

    def eliminarTarea(self, idTarea: int, categoria_nombre: str):
        """
        Elimina una tarea de una categoría específica.

        Args:
            idTarea (int): ID de la tarea a eliminar.
            categoria_nombre (str): Nombre de la categoría donde está la tarea.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        if categoria:
            # Encontrar la tarea
            tarea = next((tarea for tarea in categoria.tareas if tarea.id == idTarea), None)
            if tarea:
                # Eliminar la tarea
                categoria.tareas.remove(tarea)
                # Agregar la acción al historial
                self.historial_acciones.put(('eliminar', tarea, categoria))
                # Mostrar mensaje de éxito
                print(f"Tarea con ID '{idTarea}' eliminada correctamente.")
            else:
                print('Error: La tarea no existe.')
        else:
            print('Error: La categoría no existe.')

    def modificarTarea(self, idTarea: int, nuevo_titulo: str, nueva_descripcion: str, nueva_prioridad: int, nueva_fecha_vencimiento: datetime, categoria_nombre: str):
        """
        Modifica una tarea existente.

        Args:
            idTarea (int): ID de la tarea a modificar.
            nuevo_titulo (str): Nuevo título de la tarea.
            nueva_descripcion (str): Nueva descripción de la tarea.
            nueva_prioridad (int): Nueva prioridad de la tarea (1 alta, 3 baja).
            nueva_fecha_vencimiento (datetime): Nueva fecha de vencimiento de la tarea.
            categoria_nombre (str): Nombre de la categoría donde está la tarea.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        if categoria:
            # Encontrar la tarea
            tarea = next((tarea for tarea in categoria.tareas if tarea.id == idTarea), None)
            # Si la tarea existe, modificarla
            if tarea:
                tarea_anterior = Tareas(tarea.id, tarea.titulo, tarea.descripcion, tarea.prioridad, tarea.fecha_vencimiento)
                tarea.titulo = nuevo_titulo
                tarea.descripcion = nueva_descripcion
                tarea.prioridad = nueva_prioridad
                tarea.fecha_vencimiento = nueva_fecha_vencimiento
                # Agregar la acción al historial
                self.historial_acciones.put(('modificar', tarea_anterior, tarea, categoria))
                # Mostrar mensaje de éxito
                print(f"Tarea '{nuevo_titulo}' modificada correctamente.")
            else:
                print('Error: La tarea no existe.')
        else:
            print('Error: La categoría no existe.')

    def mostrarTareasOrdenadas(self, categoria_nombre: str):
        """
        Muestra las tareas de una categoría específica ordenadas por prioridad y fecha de vencimiento.

        Args:
            categoria_nombre (str): Nombre de la categoría.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        if categoria:
            # Ordenar las tareas por prioridad y fecha de vencimiento
            if categoria.tareas:
                tareas_ordenadas = sorted(categoria.tareas, key=lambda t: (t.prioridad, t.fecha_vencimiento))
                for tarea in tareas_ordenadas:
                    print(tarea)
            else:
                print("No hay tareas en esta categoría.")
        else:
            print('Error: La categoría no existe.')

    def deshacer(self):
        """
        Deshace la última acción realizada (agregar, eliminar o modificar tarea).
        """
        # Verificar si hay acciones para deshacer
        if not self.historial_acciones.empty():
            # Obtener la última acción
            ultima_accion = self.historial_acciones.get()
            # Deshacer la acción
            accion = ultima_accion[0]
            # Dependiendo del tipo de acción, revertir los cambios
            if accion == 'agregar':
                tarea, categoria = ultima_accion[1], ultima_accion[2]
                categoria.tareas.remove(tarea)
            elif accion == 'eliminar':
                tarea, categoria = ultima_accion[1], ultima_accion[2]
                categoria.tareas.append(tarea)
            elif accion == 'modificar':
                tarea_anterior, tarea_modificada, categoria = ultima_accion[1], ultima_accion[2], ultima_accion[3]
                # Revertimos los cambios
                tarea_modificada.titulo = tarea_anterior.titulo
                tarea_modificada.descripcion = tarea_anterior.descripcion
                tarea_modificada.prioridad = tarea_anterior.prioridad
                tarea_modificada.fecha_vencimiento = tarea_anterior.fecha_vencimiento
            # Agregar la acción al historial de deshacer
            self.historial_deshacer.put(ultima_accion)
            print("Acción deshecha correctamente.")
        else:
            print("No hay acciones para deshacer.")

    def rehacer(self):
        """
        Rehace la última acción deshecha.
        """
        # Verificar si hay acciones para rehacer
        if not self.historial_deshacer.empty():
            # Obtener la última acción deshecha
            accion_deshacer = self.historial_deshacer.get()
            # Rehacer la acción
            accion = accion_deshacer[0]
            # Dependiendo del tipo de acción, aplicar los cambios nuevamente
            if accion == 'agregar':
                tarea, categoria = accion_deshacer[1], accion_deshacer[2]
                categoria.tareas.append(tarea)
            elif accion == 'eliminar':
                tarea, categoria = accion_deshacer[1], accion_deshacer[2]
                categoria.tareas.remove(tarea)
            elif accion == 'modificar':
                tarea_anterior, tarea_modificada, categoria = accion_deshacer[1], accion_deshacer[2], accion_deshacer[3]
                # Aplicamos nuevamente los cambios
                tarea_modificada.titulo = tarea_anterior.titulo
                tarea_modificada.descripcion = tarea_anterior.descripcion
                tarea_modificada.prioridad = tarea_anterior.prioridad
                tarea_modificada.fecha_vencimiento = tarea_anterior.fecha_vencimiento
            # Agregar la acción al historial de acciones
            self.historial_acciones.put(accion_deshacer)
            print("Acción rehecha correctamente.")
        else:
            print("No hay acciones para rehacer.")

    def agregarTareaUrgente(self, titulo: str, descripcion: str, prioridad: int, fecha_vencimiento: datetime, categoria_nombre: str):
        """
        Agrega una tarea urgente a una categoría específica.

        Args:
            titulo (str): Título de la tarea urgente.
            descripcion (str): Descripción de la tarea urgente.
            prioridad (int): Prioridad de la tarea.
            fecha_vencimiento (datetime): Fecha de vencimiento de la tarea.
            categoria_nombre (str): Nombre de la categoría.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        # Si la categoría existe
        if categoria:
            # Crear la tarea urgente y agregarla a la cola de tareas urgentes
            tarea = Tareas(self.idTarea, titulo, descripcion, prioridad, fecha_vencimiento)
            # Agregar la tarea urgente a la cola de tareas urgentes
            categoria.tareasUrgentes.put(tarea)
            # Incrementar el contador de tareas
            self.idTarea += 1
            print(f'Tarea urgente añadida: {tarea}')
        else:
            print('Error: La categoría no existe.')

    def procesarTareaUrgente(self, categoria_nombre: str):
        """
        Procesa la siguiente tarea urgente de la categoría (FIFO).

        Args:
            categoria_nombre (str): Nombre de la categoría.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        # Si la categoría existe
        if categoria:
            # Verificar si hay tareas urgentes
            if not categoria.tareasUrgentes.empty():
                # Obtener la siguiente tarea urgente
                tarea = categoria.tareasUrgentes.get()
                # Mostrar la tarea urgente
                print(f'Procesando tarea urgente: {tarea}')
            else:
                print('No hay tareas urgentes en esta categoría.')
        else:
            print('Error: La categoría no existe.')

    def mostrarTareasUrgentes(self, categoria_nombre: str):
        """
        Muestra todas las tareas urgentes de una categoría.

        Args:
            categoria_nombre (str): Nombre de la categoría.
        """
        # Encontrar la categoría
        categoria = self.encontrarCategoria(nombre=categoria_nombre)
        # Si la categoría existe
        if categoria:
            # Verificar si hay tareas urgentes
            if not categoria.tareasUrgentes.empty():
                # Mostrar las tareas urgentes
                print(f'Tareas urgentes en {categoria_nombre}:')
                for tarea in list(categoria.tareasUrgentes.queue):
                    print(f'* ID: {tarea.id} - {tarea.titulo} - {tarea.descripcion} - Prioridad: {tarea.prioridad} - Vencimiento: {tarea.fecha_vencimiento.strftime("%d/%m/%Y")}')
            else:
                print('No hay tareas urgentes en esta categoría.')
        else:
            print(f'Error: La categoría "{categoria_nombre}" no existe.')


def limpiar_consola():
    """
    Limpia la consola dependiendo del sistema operativo.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def consola_interactiva():
    """
    Proporciona una consola interactiva para gestionar categorías, subcategorías, y tareas.
    """
    # Crear un manejador de tareas
    manejador = ManejadorTareas()
    
    # Bucle principal
    while True:
        # Limpiar la consola
        limpiar_consola()
        # Listar las opciones del menú
        print("\n--- Menú Principal ---")
        print("1. Agregar categoría")
        print("2. Agregar subcategoría")
        print("3. Agregar tarea")
        print("4. Modificar tarea")
        print("5. Eliminar tarea")
        print("6. Mostrar tareas ordenadas por categoría")
        print("7. Deshacer última acción")
        print("8. Rehacer última acción")
        print("9. Agregar tarea urgente")
        print("10. Procesar tarea urgente")
        print("11. Mostrar tareas urgentes")
        print("12. Mostrar todas las categorías y subcategorías")
        print("13. Salir")
        
        # Leer la opción seleccionada
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            limpiar_consola()
            # Agregar una nueva categoría
            nombre_categoria = input("Introduce el nombre de la nueva categoría: ")
            # Verificar si se ingresó un nombre válido de lo contrario mostrar un mensaje de error
            if nombre_categoria:
                manejador.agregarCategoria(nombre_categoria)
            else:
                print("Error: Debes ingresar un nombre válido para la categoría.")
        
        elif opcion == '2':
            limpiar_consola()
            # Agregar una nueva subcategoría
            nombre_categoria_padre = input("Introduce el nombre de la categoría padre: ")
            nombre_subcategoria = input("Introduce el nombre de la nueva subcategoría: ")
            # Verificar si se ingresó un nombre válido de lo contrario mostrar un mensaje de error
            if nombre_categoria_padre and nombre_subcategoria:
                manejador.agregarSubcategoria(nombre_subcategoria, nombre_categoria_padre)
            else:
                print("Error: Debes ingresar un nombre válido para la categoría y la subcategoría.")
        
        elif opcion == '3':
            limpiar_consola()
            # Agregar una nueva tarea
            nombre_categoria = input("Introduce la categoría de la tarea: ")
            titulo = input("Introduce el título de la tarea: ")
            descripcion = input("Introduce la descripción de la tarea: ")
            # Solicitar la prioridad de la tarea
            try:
                prioridad = int(input("Introduce la prioridad de la tarea (1 alta, 3 baja): "))
                # Verificar si la prioridad es válida
                if prioridad < 1 or prioridad > 3:
                    raise ValueError
            except ValueError:
                print("Error: Debes ingresar una prioridad válida (1, 2 o 3).")
                continue
            # Solicitar la fecha de vencimiento de la tarea
            fecha_vencimiento_str = input("Introduce la fecha de vencimiento (DD/MM/YYYY): ")
            try:
                # Convertir la cadena de fecha a un objeto datetime
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%d/%m/%Y")
                # Agregar la tarea
                manejador.agregarTarea(titulo, descripcion, prioridad, fecha_vencimiento, nombre_categoria)
            except ValueError:
                print("Error: Formato de fecha incorrecto. Usa el formato DD/MM/YYYY.")

        elif opcion == '4':
            limpiar_consola()
            # Modificar una tarea existente
            nombre_categoria = input("Introduce la categoría de la tarea: ")
            try:
                id_tarea = int(input("Introduce el ID de la tarea a modificar: "))
            except ValueError:
                print("Error: El ID debe ser un número.")
                continue
            nuevo_titulo = input("Introduce el nuevo título de la tarea: ")
            nueva_descripcion = input("Introduce la nueva descripción de la tarea: ")
            try:
                nueva_prioridad = int(input("Introduce la nueva prioridad de la tarea (1 alta, 3 baja): "))
                if nueva_prioridad < 1 or nueva_prioridad > 3:
                    raise ValueError
            except ValueError:
                print("Error: Debes ingresar una prioridad válida (1, 2 o 3).")
                continue
            nueva_fecha_str = input("Introduce la nueva fecha de vencimiento (DD/MM/YYYY): ")
            try:
                nueva_fecha = datetime.strptime(nueva_fecha_str, "%d/%m/%Y")
                manejador.modificarTarea(id_tarea, nuevo_titulo, nueva_descripcion, nueva_prioridad, nueva_fecha, nombre_categoria)
            except ValueError:
                print("Error: Formato de fecha incorrecto. Usa el formato DD/MM/YYYY.")

        elif opcion == '5':
            limpiar_consola()
            # Eliminar una tarea
            nombre_categoria = input("Introduce la categoría de la tarea: ")
            try:
                # Solicitar el ID de la tarea a eliminar
                id_tarea = int(input("Introduce el ID de la tarea a eliminar: "))
                # Eliminar la tarea
                manejador.eliminarTarea(id_tarea, nombre_categoria)
            except ValueError:
                print("Error: El ID debe ser un número.")

        elif opcion == '6':
            limpiar_consola()
            # Mostrar tareas ordenadas por prioridad y fecha de vencimiento
            nombre_categoria = input("Introduce la categoría para mostrar tareas ordenadas: ")
            manejador.mostrarTareasOrdenadas(nombre_categoria)

        elif opcion == '7':
            limpiar_consola()
            # Deshacer la última acción
            manejador.deshacer()

        elif opcion == '8':
            limpiar_consola()
            # Rehacer la última acción deshecha
            manejador.rehacer()

        elif opcion == '9':
            limpiar_consola()
            # Agregar una tarea urgente
            nombre_categoria = input("Introduce la categoría de la tarea urgente: ")
            titulo = input("Introduce el título de la tarea urgente: ")
            descripcion = input("Introduce la descripción de la tarea urgente: ")
            try:
                prioridad = int(input("Introduce la prioridad de la tarea urgente (1 alta, 3 baja): "))
                if prioridad < 1 or prioridad > 3:
                    raise ValueError
            except ValueError:
                print("Error: Debes ingresar una prioridad válida (1, 2 o 3).")
                continue
            fecha_vencimiento_str = input("Introduce la fecha de vencimiento (DD/MM/YYYY): ")
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%d/%m/%Y")
                # Agregar la tarea urgente
                manejador.agregarTareaUrgente(titulo, descripcion, prioridad, fecha_vencimiento, nombre_categoria)
            except ValueError:
                print("Error: Formato de fecha incorrecto. Usa el formato DD/MM/YYYY.")

        elif opcion == '10':
            limpiar_consola()
            # Procesar la siguiente tarea urgente
            nombre_categoria = input("Introduce la categoría para procesar tareas urgentes: ")
            manejador.procesarTareaUrgente(nombre_categoria)
        
        elif opcion == '11':
            limpiar_consola()
            # Mostrar tareas urgentes de una categoría
            nombre_categoria = input("Introduce la categoría para mostrar las tareas urgentes: ")
            manejador.mostrarTareasUrgentes(nombre_categoria)

        elif opcion == '12':
            limpiar_consola()
            # Mostrar todas las categorías y subcategorías
            manejador.mostrarCategorias()

        elif opcion == '13':
            limpiar_consola()
            # Salir del programa
            print("Saliendo del programa...")
            break

        else:
            # Mostrar mensaje de error si la opción no es válida
            print("Opción no válida. Por favor, selecciona una opción válida.")
        # Esperar a que el usuario presione Enter para continuar
        input("\nPresiona Enter para continuar...")

# Ejecutar la consola interactiva
if __name__ == '__main__':
    # Iniciar la consola interactiva
    consola_interactiva()
