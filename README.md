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

## Uso de la Base de Datos SQLite

La API utiliza una base de datos SQLite para almacenar los cálculos de interés compuesto. Cada vez que se realiza un cálculo mediante el endpoint `/interes-compuesto`, los datos (capital, tasa, plazo, monto final y ganancias) se guardan automáticamente en la base de datos. Esto permite mantener un historial de cálculos, que pueden ser actualizados o eliminados usando los endpoints `/interes-compuesto/{id}` con los métodos PUT y DELETE, respectivamente. La integración con SQLite se gestiona mediante SQLAlchemy, asegurando una conexión eficiente y persistente.
