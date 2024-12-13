from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la base del modelo
Base = declarative_base()

# Definir el modelo ORM para la tabla 'recetas'
class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    ingredientes = Column(String, nullable=False)
    pasos = Column(String, nullable=False)

# Configuración de la conexión a MariaDB
# Reemplaza estos valores con los de tu servidor MariaDB
DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost:3306/libro_de_recetas"

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Función para agregar una receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos: ")
    
    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta():
    ver_recetas()
    receta_id = input("ID de la receta a actualizar: ")
    receta = session.query(Receta).get(receta_id)

    if receta:
        nombre = input(f"Nuevo nombre de la receta (actual: {receta.nombre}): ")
        ingredientes = input(f"Nuevos ingredientes (actual: {receta.ingredientes}): ")
        pasos = input(f"Nuevos pasos (actual: {receta.pasos}): ")

        if nombre:
            receta.nombre = nombre
        if ingredientes:
            receta.ingredientes = ingredientes
        if pasos:
            receta.pasos = pasos

        session.commit()
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta():
    ver_recetas()
    receta_id = input("ID de la receta a eliminar: ")
    receta = session.query(Receta).get(receta_id)

    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver el listado de recetas
def ver_recetas():
    recetas = session.query(Receta).all()
    print("\nListado de recetas:")
    for receta in recetas:
        print(f"ID: {receta.id}, Nombre: {receta.nombre}")
    print()

# Función para buscar ingredientes y pasos de una receta
def buscar_receta():
    nombre = input("Nombre de la receta a buscar: ")
    receta = session.query(Receta).filter_by(nombre=nombre).first()

    if receta:
        print("\nIngredientes:", receta.ingredientes)
        print("Pasos:", receta.pasos)
    else:
        print("Receta no encontrada.")

# Menú principal
def menu():
    while True:
        print("\n--- Libro de Recetas ---")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_receta()
        elif opcion == '2':
            actualizar_receta()
        elif opcion == '3':
            eliminar_receta()
        elif opcion == '4':
            ver_recetas()
        elif opcion == '5':
            buscar_receta()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecución del programa
if __name__ == "__main__":
    menu()