# Sistema Software FJ - Módulo 4: Reserva

Curso Programación 213023 - UNAD - Fase 4 (Prácticas simuladas)
Autor del módulo 4: Adrian David Uriel Vergara

## Qué hace
La clase `Reserva` une un cliente, un servicio, las horas y el estado de la reserva.
Permite confirmar, cancelar y procesar una reserva. Al procesarla calcula el costo con el servicio del módulo 3.

## Manejo de excepciones
- Excepción personalizada `ReservaError`.
- Validaciones: la reserva debe estar confirmada, el cliente debe ser texto, las horas deben ser un número mayor a 0.
- `try/except/else/finally` en `procesar()`.
- Encadenamiento: si el servicio lanza `ValueError` (sala no disponible), se lanza `ReservaError ... from error`.
- Archivo de log `reserva.log` con los eventos (INFO) y los errores (ERROR).

## Archivos
- `reserva.py`: módulo 4 (clase Reserva y pruebas).
- `servicios.py`: módulo 3, servicios (autora: Leidy Alvarez). Se usa `ReservaSala`.
- `reserva.log`: log generado al ejecutar.

## Cómo ejecutar
```
python reserva.py
```
