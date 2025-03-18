# Calculadora Financiera API

Esta API ofrece herramientas para realizar cálculos financieros básicos, como la conversión de tasas de interés, el cálculo de interés compuesto y el costo nivelado de la energía (LCOE) para proyectos eléctricos. Utiliza una base de datos SQLite para almacenar y gestionar los cálculos de interés compuesto, permitiendo un historial persistente de las operaciones realizadas.

---

## Endpoint Ventana Principal

- **Ruta**: `/`
- **Método**: GET
- **Descripción**: Devuelve una página HTML de bienvenida que presenta la API y ofrece un enlace a la documentación detallada.
- **Respuesta**: Una página HTML con un título, una breve descripción y un enlace a `/docs`.

---

## Endpoint Conversor de Tasas de Interés

- **Ruta**: `/convertir-tasas`
- **Método**: POST
- **Descripción**: Convierte una tasa de interés dada (diaria, mensual o anual) en tasas equivalentes para los otros períodos.
- **Parámetros**:
  - `request: ConversionTasaRequest` - Objeto con:
    - `tasa: float` - Valor de la tasa de interés.
    - `tipo: TipoTasa` - Tipo de tasa (diaria, mensual o anual).
- **Respuesta**: Un objeto `ConversionTasaResponse` con:
  - `tasa_diaria: float` - Tasa diaria equivalente.
  - `tasa_mensual: float` - Tasa mensual equivalente.
  - `tasa_anual: float` - Tasa anual equivalente.
  - `mensaje: str` - Descripción del cálculo (ej. "Tasa mensual de 2% equivale a 24% anual").

---

## Endpoint Cálculo de Interés Compuesto

- **Ruta**: `/interes-compuesto`
- **Método**: POST
- **Descripción**: Calcula el monto final y las ganancias de una inversión con interés compuesto, según el capital inicial, la tasa, el plazo y el tipo de tasa. Guarda los resultados en la base de datos SQLite.
- **Parámetros**:
  - `request: InteresCompuestoRequest` - Objeto con:
    - `capital: float` - Capital inicial.
    - `tasa: float` - Tasa de interés.
    - `plazo: int` - Número de períodos.
    - `tipo_tasa: TipoTasa` - Tipo de tasa (diaria, mensual o anual).
  - `db: Session` - Sesión de la base de datos para almacenar el cálculo.
- **Respuesta**: Un diccionario con:
  - `capital_inicial: str` - Capital formateado como moneda.
  - `tasa_aplicada: str` - Tasa y tipo (ej. "5% mensual").
  - `tasa_anual_equivalente: str` - Tasa anual equivalente.
  - `plazo: str` - Duración del cálculo (ej. "12 periodos (mensual)").
  - `monto_final: str` - Monto final formateado.
  - `ganancias: str` - Ganancias formateadas.

---

## Endpoint Cálculo de LCOE

- **Ruta**: `/lcoe`
- **Método**: POST
- **Descripción**: Calcula el costo nivelado de la energía (LCOE) para un proyecto eléctrico basado en costos de capital, operación, producción anual, tasa de descuento y vida útil.
- **Parámetros**:
  - `request: LCOERequest` - Objeto con:
    - `capex: float` - Costo de capital.
    - `opex: float` - Costo de operación anual.
    - `produccion_anual: float` - Producción anual en MWh.
    - `tasa_descuento: float` - Tasa de descuento.
    - `vida_util: int` - Vida útil en años.
- **Respuesta**: Un diccionario con:
  - `lcoe: float` - Valor del LCOE redondeado.
  - `unidad: str` - Unidad del LCOE ("$/MWh").
  - `mensaje: str` - Descripción (ej. "El costo nivelado de la energía es 50.25 $/MWh").

---

## Endpoint Actualizar Cálculo de Interés Compuesto

- **Ruta**: `/interes-compuesto/{id}`
- **Método**: PUT
- **Descripción**: Actualiza un cálculo de interés compuesto existente en la base de datos SQLite.
- **Parámetros**:
  - `id: int` - Identificador del cálculo a actualizar.
  - `request: InteresCompuestoRequest` - Objeto con los nuevos valores (capital, tasa, plazo, tipo_tasa).
  - `db: Session` - Sesión de la base de datos para realizar la actualización.
- **Respuesta**: Un diccionario con:
  - `mensaje: str` - Confirmación de la actualización.
  - `datos: object` - Datos actualizados del cálculo.

---

## Endpoint Eliminar Cálculo de Interés Compuesto

- **Ruta**: `/interes-compuesto/{id}`
- **Método**: DELETE
- **Descripción**: Elimina un cálculo de interés compuesto de la base de datos SQLite.
- **Parámetros**:
  - `id: int` - Identificador del cálculo a eliminar.
  - `db: Session` - Sesión de la base de datos para realizar la eliminación.
- **Respuesta**: Un diccionario con:
  - `mensaje: str` - Confirmación de la eliminación (ej. "Cálculo con ID 1 eliminado correctamente").

---

## Endpoint Actualizar Cálculo del Costo Nivelado de la Energía (LCOE)

- **Ruta**: `/lcoe/{id}`
- **Método**: PUT
- **Descripción**: Actualiza un cálculo de LCOE existente en la base de datos SQLite.
- **Parámetros**:
  - `id: int` - Identificador del cálculo a actualizar.
  - `request: LCOERequest` - Objeto con los nuevos valores (capex, opex, produccion_anual, tasa_descuento, vida_util).
  - `db: Session` - Sesión de la base de datos para realizar la actualización.
- **Respuesta**: Un diccionario con:
  - `mensaje: str` - Confirmación de la actualización.
  - `datos: object` - Datos actualizados del cálculo.

---

## Endpoint Eliminar Cálculo de Interés Compuesto

- **Ruta**: `/lcoe/{id}`
- **Método**: DELETE
- **Descripción**: Elimina un cálculo de LCOE de la base de datos SQLite.
- **Parámetros**:
  - `id: int` - Identificador del cálculo a eliminar.
  - `db: Session` - Sesión de la base de datos para realizar la eliminación.
- **Respuesta**: Un diccionario con:
  - `mensaje: str` - Confirmación de la eliminación (ej. "Cálculo con ID 1 eliminado correctamente").

---

## Uso de la Base de Datos SQLite

La API utiliza una base de datos SQLite para almacenar los cálculos de interés compuesto. Cada vez que se realiza un cálculo mediante el endpoint `/interes-compuesto`, los datos (capital, tasa, plazo, monto final y ganancias) se guardan automáticamente en la base de datos. Esto permite mantener un historial de cálculos, que pueden ser actualizados o eliminados usando los endpoints `/interes-compuesto/{id}` con los métodos PUT y DELETE, respectivamente. La integración con SQLite se gestiona mediante SQLAlchemy, asegurando una conexión eficiente y persistente.


# Ejemplos de uso de endpoints FastAPI

## 1. Endpoint Principal (`/`)
Este es un simple endpoint GET que muestra una página HTML con información sobre la calculadora financiera.

```
GET http://localhost:8000/
```

Este endpoint devuelve una página HTML simple con un título, una descripción y un enlace a la documentación.

## 2. Convertir Tasas de Interés (`/convertir-tasas`)
```
POST http://localhost:8000/convertir-tasas
Content-Type: application/json

{
  "tasa": 2.5,
  "tipo": "MENSUAL"
}
```

Respuesta esperada:
```json
{
  "tasa_diaria": 0.000833,
  "tasa_mensual": 2.5,
  "tasa_anual": 34.49,
  "mensaje": "Tasa mensual de 2.5% equivale a 34.49% anual"
}
```

## 3. Cálculo de Interés Compuesto (`/interes-compuesto`)
```
POST http://localhost:8000/interes-compuesto
Content-Type: application/json

{
  "capital": 10000,
  "tasa": 2.5,
  "plazo": 12,
  "tipo_tasa": "MENSUAL"
}
```

Respuesta esperada:
```json
{
  "capital_inicial": "$10,000.00",
  "tasa_aplicada": "2.5% mensual",
  "tasa_anual_equivalente": "34.49%",
  "plazo": "12 periodos (mensual)",
  "monto_final": "$13,448.52",
  "ganancias": "$3,448.52"
}
```

## 4. Cálculo del Costo Nivelado de Energía (LCOE) (`/lcoe`)
```
POST http://localhost:8000/lcoe
Content-Type: application/json

{
  "capex": 1000000,
  "opex": 50000,
  "produccion_anual": 5000,
  "tasa_descuento": 0.08,
  "vida_util": 25
}
```

Respuesta esperada:
```json
{
  "lcoe": 42.47,
  "unidad": "$/MWh",
  "mensaje": "El costo nivelado de la energía es 42.47 $/MWh"
}
```

## 5. Actualizar Cálculo de Interés Compuesto (`/interes-compuesto/{id}`)
```
PUT http://localhost:8000/interes-compuesto/1
Content-Type: application/json

{
  "capital": 15000,
  "tasa": 2.0,
  "plazo": 24,
  "tipo_tasa": "MENSUAL"
}
```

Respuesta esperada:
```json
{
  "mensaje": "Cálculo actualizado",
  "datos": {
    "id": 1,
    "capital": 15000,
    "tasa": 2.0,
    "plazo": 24,
    "monto_final": 23246.52,
    "ganancias": 8246.52
  }
}
```

## 6. Eliminar Cálculo de Interés Compuesto (`/interes-compuesto/{id}`)
```
DELETE http://localhost:8000/interes-compuesto/1
```

Respuesta esperada:
```json
{
  "mensaje": "Cálculo con ID 1 eliminado correctamente"
}
```

## 7. Actualizar calculo del Costo Nivelado de Energía (LCOE) (`/lcoe/{id}`)

```
PUT http://localhost:8000/lcoe/1
```
Respuesta esperada:
```json
{
    "mensaje": "LCOE actualizado", 
    "datos": {
        "id": 1,
        "capex": 0.12,
        "opex": 1000,
        "produccion_anual": 120,
        "tasa_total": 0.12,
        "vida_util": 25 
        }
}
```

## 8. Eliminar cálculo del Costo Nivelado de Energía (LCOE) (`/lcoe/{id}`)

```
DELETE http://localhost:8000/lcoe/1

Respuesta esperada:
```json
{
    "mensaje": "LCOE con ID 1 eliminado correctamente"
}
```
