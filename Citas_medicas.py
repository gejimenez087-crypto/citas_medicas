### 1. Clase Controladora: `AdministradorClinica`
import json

# 1. Clase Controladora
class AdministradorClinica:
    def __init__(self, medicos, pacientes, agenda_citas):
        self.medicos = medicos  # Lista de objetos Medico
        self.pacientes = pacientes  # Lista de objetos Paciente
        self.agenda_citas = agenda_citas  # Lista de objetos Cita

    def crear_cita(self, id_medico, id_paciente, folio, fecha_hora, motivo_consulta):
        nueva_cita = Cita(id_medico, id_paciente, folio, fecha_hora, motivo_consulta)
        self.agenda_citas.append(nueva_cita)
        print("Cita creada exitosamente.")
        
        for cita in self.agenda_citas:
            if cita. id_medico == id_medico and cita.fecha_hora == fecha_hora:
                print(f"El médico {id_medico} ya tiene una cita en {fecha_hora}.")
                return 

    def cancelar_cita(self, folio):
        self.agenda_citas = [cita for cita in self.agenda_citas if cita.folio != folio]

    def buscar_paciente(self, id_paciente):
        for paciente in self.pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None

    def ver_agenda_medico(self, cedula_medico):
        citas_medico = [cita for cita in self.agenda_citas if cita.id_medico == cedula_medico]
        return citas_medico

    def guardar_sistema(self):
        datos = {
            "medicos": [{"cedula": m.cedula, "nombre": m.nombre, "especialidad": m.especialidad}
                        for m in self.medicos],
            "pacientes": [{"id_paciente": p.id_paciente, "nombre": p.nombre,
                           "historial_clinico": p.historial_clinico}
                          for p in self.pacientes],
            "agenda_citas": [{"folio": c.folio, "id_medico": c.id_medico,
                              "id_paciente": c.id_paciente,
                              "fecha_hora": c.fecha_hora,
                              "motivo_consulta": c.motivo_consulta}
                             for c in self.agenda_citas]
        }
        with open("sistema_clinica.json", "w") as fp:
            json.dump(datos, fp, indent=4)

# 2. Clase Entidad: Medico
class Medico:
    def __init__(self, cedula, nombre, especialidad):
        self.cedula = cedula
        self.nombre = nombre
        self.especialidad = especialidad
        self.activo = True

    def esta_disponible(self, fecha_hora, agenda_citas):
        for cita in agenda_citas:
            if cita.id_medico == self.cedula and cita.fecha_hora == fecha_hora:
                return False
        return True

    def mostrar_perfil(self):
        return {"Cédula": self.cedula, "Nombre": self.nombre, "Especialidad": self.especialidad}

    def cambiar_estado(self, activo_inactivo):
        self.activo = bool(activo_inactivo)
        return self.activo

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
            paciente = administrador.buscar_paciente(input("Ingrese el ID del paciente: "))
            if paciente:
                print(f"Paciente encontrado: {paciente.nombre}")
            else:
                print("Paciente no encontrado.")

        elif opcion == "4":
            citas = administrador.ver_agenda_medico(input("Ingrese la cédula o ID del médico: "))
            for cita in citas:
                print(f"Cita Folio: {cita.folio}, Fecha y Hora: {cita.fecha_hora}, Motivo: {cita.motivo_consulta}")

        elif opcion == "5":
            administrador.guardar_sistema()
            print("Sistema guardado en 'sistema_clinica.json'.")

        elif opcion == "6":
            print("Hasta luego.")
            break
