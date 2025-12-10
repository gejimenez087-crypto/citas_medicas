import json
import os

# 1. Clase Controladora
class AdministradorClinica:
    def __init__(self, medicos, pacientes, agenda_citas):
        self.medicos = medicos  # Lista de objetos Medico
        self.pacientes = pacientes  # Lista de objetos Paciente
        self.agenda_citas = agenda_citas  # Lista de objetos Cita

    def crear_cita(self, id_medico, id_paciente, folio, fecha_hora, motivo_consulta):
        # Validar disponibilidad
        for cita in self.agenda_citas:
            if cita.id_medico == id_medico and cita.fecha_hora == fecha_hora:
                print(f"El médico {id_medico} ya tiene una cita en {fecha_hora}.")
                return

        # Buscar médico y paciente
        medico = self.buscar_medico(id_medico)
        paciente = self.buscar_paciente(id_paciente)

        if not medico or not paciente:
            print("No se encontró médico o paciente.")
            return

        # Crear cita con IDs
        nueva_cita = Cita(id_medico, id_paciente, folio, fecha_hora, motivo_consulta)
        self.agenda_citas.append(nueva_cita)

        # Mostrar confirmación con datos
        print("Cita creada exitosamente.")
        print(f"Médico: {medico.nombre}, Especialidad: {medico.especialidad}")
        print(f"Paciente: {paciente.nombre}, Tel: {paciente.telefono if paciente.telefono else 'No registrado'}")

    def cancelar_cita(self, folio):
        self.agenda_citas = [cita for cita in self.agenda_citas if cita.folio != folio]

    def buscar_paciente(self, id_paciente):
        for paciente in self.pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None
    
    def ver_agenda_medico(self, id_medico):
        citas_medico = [cita for cita in self.agenda_citas if cita.id_medico == id_medico]
        return citas_medico

    def guardar_sistema(self):
        datos = {
            "medicos": [
            {"id_medico": "123", "nombre": "Dr. Pérez", "especialidad": "Cardiología"},
            {"id_medico": "456", "nombre": "Dra. López", "especialidad": "Pediatría"}
        ],
        "pacientes": [],
        "agenda_citas": []
        }
        with open("sistema_clinica.json", "w") as fp:
            json.dump(datos, fp, indent=4)
    
    def cargar_sistema(self): 
        if os.path.exists("sistema_clinica.json"):  # Verifica si el archivo existe
            with open("sistema_clinica.json", "r") as fp:
                datos = json.load(fp)

            self.medicos = []
            for m in datos["medicos"]:
                medico = Medico(m["id_medico"], m["nombre"], m["especialidad"])
                self.medicos.append(medico)

            # Reconstruir objetos Paciente
            self.pacientes = []
            for p in datos["pacientes"]:
                paciente = Paciente(p["id_paciente"], p["nombre"], p.get("historial_clinico", []))
                self.pacientes.append(paciente)

            # Reconstruir objetos Cita
            self.agenda_citas = []
            for c in datos["agenda_citas"]:
                cita = Cita(c["id_medico"], c["id_paciente"], c["folio"], c["fecha_hora"], c["motivo_consulta"])
                self.agenda_citas.append(cita)

            print("Sistema cargado correctamente.")
        else:
            print("No se encontró el archivo del sistema. Se iniciará vacío.")


class Medico:
    def __init__(self, cedula, id_medico, nombre, especialidad):
        self.id_medico = id_medico
        self.cedula = cedula
        self.nombre = nombre
        self.especialidad = especialidad
        self.activo = True

    def esta_disponible(self, fecha_hora, agenda_citas):
        for cita in agenda_citas:
            if cita.id_medico == self.id_medico and cita.fecha_hora == fecha_hora:
                return False
        return True

    def mostrar_perfil(self):
        return {"ID Médico": self.id_medico, "Nombre": self.nombre, "Especialidad": self.especialidad}
    
# 3. Clase Entidad: Paciente
class Paciente:
    def __init__(self, id_paciente, nombre, historial_clinico=None, telefono=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.historial_clinico = historial_clinico if historial_clinico else []
        self.telefono = telefono

    def agregar_nota_historial(self, nota):
        self.historial_clinico.append(nota)

    def ver_historial(self):
        return self.historial_clinico

    def actualizar_telefono(self, nuevo_telefono):
        self.telefono = nuevo_telefono
        return self.telefono

# 4. Clase Entidad: Cita
class Cita:
    def __init__(self, id_medico, id_paciente, folio, fecha_hora, motivo_consulta):
        self.folio = folio
        self.id_medico = id_medico
        self.id_paciente = id_paciente
        self.fecha_hora = fecha_hora
        self.motivo_consulta = motivo_consulta
        self.confirmada = False

    def confirmar_asistencia(self):
        self.confirmada = True

    def reprogramar(self, nueva_fecha):
        self.fecha_hora = nueva_fecha

    def formato_notificacion(self, paciente_nombre):
        return f"Estimado/a {paciente_nombre}, su cita (folio {self.folio}) está programada para {self.fecha_hora}. Motivo: {self.motivo_consulta}"

# Menú interactivo
if __name__ == "__main__":
    administrador = AdministradorClinica([], [], [])
    administrador.cargar_sistema()

    while True:
        print("Hola bienvenido al sistema de gestión de citas médicas")
        print("1. Crear cita")
        print("2. Cancelar cita")
        print("3. Buscar paciente")
        print("4. Ver agenda del médico")
        print("5. Guardar sistema")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            administrador.crear_cita(
                input("ID médico: "),
                input("ID paciente: "),
                input("Folio: "),
                input("Fecha y hora: "),
                input("Motivo de consulta: ")
            )
            
        elif opcion == "2":
            administrador.cancelar_cita(input("Folio de la cita a cancelar: "))

        elif opcion == "3":
            id_paciente = input("Ingrese el ID del paciente: ")
            paciente = administrador.buscar_paciente(id_paciente)
            if paciente:
                print("Paciente encontrado:")
                print(f"ID: {paciente.id_paciente}")
                print(f"Nombre: {paciente.nombre}")
                print(f"Teléfono: {paciente.telefono if paciente.telefono else 'No registrado'}")
                
                print("Historial clínico:")
                if paciente.historial_clinico:
                    for nota in paciente.ver_historial():
                        print(f"- {nota}")
                else:
                    print("No hay notas en el historial clínico.")
            else:
                print("Paciente no encontrado.")

        elif opcion == "4":
            cedula = input("Ingrese la cédula o ID del médico: ")
            citas = administrador.ver_agenda_medico(cedula)

            for cita in citas:
                medico = administrador.buscar_medico(cita.id_medico)
                paciente = administrador.buscar_paciente(cita.id_paciente)

                print(f"Cita Folio: {cita.folio}, Fecha y Hora: {cita.fecha_hora}, Motivo: {cita.motivo_consulta}")
                if medico:
                    print(f"Médico: {medico.nombre}, Especialidad: {medico.especialidad}")
                if paciente:
                    print(f"Paciente: {paciente.nombre}, Tel: {paciente.telefono}")

        elif opcion == "5":
            administrador.guardar_sistema()
            print("Sistema guardado correctamente")

        elif opcion == "6":
            print("Hasta luego.")
            break



