import json
import os

# 1. Clase Controladora
class AdministradorClinica:
    def __init__(self, medicos, pacientes, agenda_citas):
        self.medicos = medicos  # Lista de objetos Medico
        self.pacientes = pacientes  # Lista de objetos Paciente
        self.agenda_citas = agenda_citas  # Lista de objetos Cita

    def crear_cita(self, id_medico, id_paciente, folio, fecha_hora, motivo_consulta):
    # Validar que no exista cita con el mismo folio
        for cita in self.agenda_citas:
            if cita.folio == folio:
                print("Error: Ya existe una cita con ese folio.")
                return

            # Validar que el médico no tenga otra cita en la misma fecha/hora
            if cita.id_medico == id_medico and cita.fecha_hora == fecha_hora:
                print("Error: El médico ya tiene una cita en esa fecha y hora.")
                return

        # Si pasa las validaciones, se crea la cita
        nueva_cita = Cita(id_medico, id_paciente, folio, fecha_hora, motivo_consulta)
        self.agenda_citas.append(nueva_cita)
        print("Cita creada exitosamente.")
       
    def cancelar_cita(self, folio):
        self.agenda_citas = [cita for cita in self.agenda_citas if cita.folio != folio]

    def buscar_paciente(self, id_paciente):
        for paciente in self.pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None
    
    def ver_agenda_medico(self, id_medico):
        return [cita for cita in self.agenda_citas if cita.id_medico == id_medico]
    
    def guardar_sistema(self):
        datos = {
            "agenda_citas": [
                {
                    "folio": cita.folio,
                    "id_medico": cita.id_medico,
                    "id_paciente": cita.id_paciente,
                    "fecha_hora": cita.fecha_hora,
                    "motivo_consulta": cita.motivo_consulta,
                    "confirmada": cita.confirmada
                } for cita in self.agenda_citas
            ]
        }
        with open("sistema_clinica.json", "w") as fp:
            json.dump(datos, fp, indent=4)

    def cargar_sistema(self): 
        if os.path.exists("sistema_clinica.json"):  # Verifica si el archivo existe
            with open("sistema_clinica.json", "r") as fp:
                datos = json.load(fp)

            # Reconstruir objetos Cita
            self.agenda_citas = []
            for c in datos["agenda_citas"]:
                cita = Cita(
                    c["id_medico"],
                    c["id_paciente"],
                    c["folio"],
                    c["fecha_hora"],
                    c["motivo_consulta"]
                )
                cita.confirmada = c["confirmada"]  # recuperar estado de confirmación
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
            id_medico = input("Ingrese el ID del médico: ")
            id_paciente = input("Ingrese el ID del paciente: ")
            folio = input("Ingrese el folio de la cita: ")
            fecha_hora = input("Ingrese la fecha y hora de la cita: ")
            motivo = input("Ingrese el motivo de la consulta: ")

            administrador.crear_cita(id_medico, id_paciente, folio, fecha_hora, motivo)
            
        elif opcion == "2":
            administrador.cancelar_cita(input("Folio de la cita a cancelar: "))

        elif opcion == "3":
            id_paciente = input("Ingrese el ID del paciente: ")
            citas_paciente = [cita for cita in administrador.agenda_citas if cita.id_paciente == id_paciente]

            if citas_paciente:
                print(f"Paciente encontrado: ID {id_paciente}")
                for cita in citas_paciente:
                    print(f"Folio: {cita.folio}, Motivo: {cita.motivo_consulta}")
            else:
                print("Paciente no encontrado o sin citas.")

        elif opcion == "4":
            id_medico = input("Ingrese el ID del médico: ")
            citas = administrador.ver_agenda_medico(id_medico)
            if citas:
                print(f"Citas del médico {id_medico}:")
                for cita in citas:
                    print(f"Folio: {cita.folio}, Paciente ID: {cita.id_paciente}, Fecha/Hora: {cita.fecha_hora}, Motivo: {cita.motivo_consulta}")
            else:
                print("No hay citas para este médico.")
                
        elif opcion == "5":
            administrador.guardar_sistema()
            print("Sistema guardado correctamente")

        elif opcion == "6":
            print("Hasta luego.")
            break
