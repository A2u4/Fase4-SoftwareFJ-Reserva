# Modulo 4: clase Reserva - Sistema Software FJ (Fase 4)
# Autor: Adrian David Uriel Vergara
# Usa los servicios del modulo 3 (Leidy Alvarez), archivo servicios.py

from servicios import ReservaSala  # traigo la sala del modulo de Leidy
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

# Ana: su reserva no esta confirmada, debe dar error
r = Reserva("Ana", sala, 3)
try:
    r.procesar()
except ReservaError as error:
    print("Error:", error)
    logging.error(error)  # el error tambien queda en el log

# Luis: su reserva esta confirmada, debe pagar
r2 = Reserva("Luis", sala, 2)
r2.confirmar()
print("Costo:", r2.procesar())

# Pedro: la sala B no esta disponible, debe dar error
r3 = Reserva("Pedro", sala_b, 2)
r3.confirmar()
try:
    r3.procesar()
except ReservaError as error:
    print("Error:", error, "Causa:", error.__cause__)  # muestro mi error y la causa original
    logging.error(error)  # el error tambien queda en el log

# si llega aqui, el programa nunca se detuvo
print("Finalizado")
