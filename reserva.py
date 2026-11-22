# Modulo 4: clase Reserva - Sistema Software FJ (Fase 4)
# Autor: Adrian David Uriel Vergara
# Usa los servicios del modulo 3 (Leidy Alvarez), archivo servicios.py

from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # traigo los servicios del modulo de Leidy
import logging  # herramienta de Python para escribir en un archivo de log

# todo lo que pase se guarda en el archivo reserva.log
logging.basicConfig(filename="reserva.log", level=logging.INFO)

# mi propio error para los problemas de las reservas
class ReservaError(Exception):
    pass

class Reserva:
    def __init__(self, cliente, servicio, horas):
        self.cliente = cliente  # quien hace la reserva
        self.servicio = servicio  # el servicio que reserva (por ejemplo una sala)
        self.horas = horas  # cuantas horas
        self.estado = "pendiente"  # toda reserva empieza pendiente

    def confirmar(self):
        self.estado = "confirmada"  # la empresa acepta la reserva

    def cancelar(self):
        self.estado = "cancelada"  # el cliente ya no quiere la reserva

    def procesar(self):
        # solo se puede procesar una reserva confirmada
        if self.estado != "confirmada":
            raise ReservaError("La reserva no esta confirmada")
        # el cliente debe ser un texto (su nombre)
        if not isinstance(self.cliente, str):
            raise ReservaError("El cliente debe ser un texto")
        # las horas deben ser un numero
        if not isinstance(self.horas, (int, float)):
            raise ReservaError("Las horas deben ser un numero")
        # no se puede reservar 0 horas o horas negativas
        if self.horas <= 0:
            raise ReservaError("Las horas deben ser mayores a 0")
        try:
            # le pido el precio al servicio de Leidy
            costo = self.servicio.calcular_costo(self.horas)
        except ValueError as error:
            # si el servicio falla, lo convierto en mi error y guardo la causa (encadenamiento)
            raise ReservaError("No se pudo procesar la reserva") from error
        else:
            # solo si no hubo error, la reserva queda procesada
            self.estado = "procesada"
        finally:
            # esto pasa siempre, con error o sin error
            logging.info("Proceso terminado para " + self.cliente)
        return costo  # devuelvo el precio

# Pruebas
sala = ReservaSala("S01", "Sala A", 50000, 10)  # sala disponible
sala_b = ReservaSala("S02", "Sala B", 40000, 5, False)  # sala NO disponible

print(sala.describir())
print(sala_b.describir())

# Simulacion 1 - Ana: su reserva no esta confirmada, debe dar error
r = Reserva("Ana", sala, 3)
try:
    r.procesar()
except ReservaError as error:
    print("Error:", error)
    logging.error(error)  # el error tambien queda en el log

# Simulacion 2 - Luis: su reserva esta confirmada, debe pagar
r2 = Reserva("Luis", sala, 2)
r2.confirmar()
print("Costo:", r2.procesar())

# Simulacion 3 - Pedro: la sala B no esta disponible, debe dar error
r3 = Reserva("Pedro", sala_b, 2)
r3.confirmar()
try:
    r3.procesar()
except ReservaError as error:
    print("Error:", error, "Causa:", error.__cause__)  # muestro mi error y la causa original
    logging.error(error)  # el error tambien queda en el log


# Simulaciones 4 a 9 usan la misma forma, por eso la pongo en una funcion
def simular(numero, reserva):
    print("Simulacion", numero, "-", reserva.cliente)  # que simulacion es
    try:
        costo = reserva.procesar()  # intento procesar la reserva
        print("  Costo:", costo)  # si salio bien, muestro el precio
    except ReservaError as error:
        print("  Error:", error)  # si salio mal, muestro el error
        logging.error(error)  # y lo guardo en el log


asesoria = AsesoriaEspecializada("A01", "Asesoria Python", 80000, "Programacion")  # asesoria disponible
equipo = AlquilerEquipo("E01", "Portatil", 30000, 3)  # 3 portatiles disponibles

# Simulacion 4 - Maria: asesoria confirmada de 2 horas, debe pagar
r4 = Reserva("Maria", asesoria, 2)
r4.confirmar()
simular(4, r4)

# Simulacion 5 - Jose: alquila un portatil 1 dia, debe pagar
r5 = Reserva("Jose", equipo, 1)
r5.confirmar()
simular(5, r5)

# Simulacion 6 - Carla: cancela su reserva y luego intenta procesarla, debe dar error
r6 = Reserva("Carla", sala, 2)
r6.cancelar()
simular(6, r6)

# Simulacion 7 - Sofia: reserva 0 horas, debe dar error
r7 = Reserva("Sofia", sala, 0)
r7.confirmar()
simular(7, r7)

# Simulacion 8 - el cliente es un numero, debe dar error
r8 = Reserva(123, sala, 2)
r8.confirmar()
simular(8, r8)

# Simulacion 9 - Diego: escribe las horas en texto, debe dar error
r9 = Reserva("Diego", sala, "tres")
r9.confirmar()
simular(9, r9)

# Simulacion 10 - crear un servicio con tarifa negativa, el modulo de Leidy debe dar error
print("Simulacion 10 - servicio con datos incorrectos")
try:
    sala_mala = ReservaSala("S03", "Sala C", -5000, 10)  # tarifa negativa
except ValueError as error:
    print("  Error:", error)  # muestro el error del servicio
    logging.error(error)  # y lo guardo en el log

# si llega aqui, el programa nunca se detuvo
print("Finalizado")
