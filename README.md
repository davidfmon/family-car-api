# Family Car API

## 📊 Diagrama de Tablas

```
┌──────────────────────────┐           ┌─────────────────────────────┐
│        families          │           │           cars              │
├──────────────────────────┤           ├─────────────────────────────┤
│ id (PK)  INTEGER         │◄──────────┤ id_family (FK) INTEGER      │
│ name     VARCHAR(100)    │           │ id (PK)        INTEGER      │
└──────────────────────────┘           │ name           VARCHAR(100) │
                                       └─────────────────────────────┘
```

---

## 📁 Descripción de las Tablas

### 🏷️ Tabla: **families**

| Campo  | Tipo                                   | Descripción                             |
| ------ | -------------------------------------- | --------------------------------------- |
| `id`   | `INTEGER GENERATED ALWAYS AS IDENTITY` | Identificador único de la familia (PK). |
| `name` | `VARCHAR(100)`                         | Nombre de la familia.                   |

---

### 🚗 Tabla: **cars**

| Campo       | Tipo                                   | Descripción                         |
| ----------- | -------------------------------------- | ----------------------------------- |
| `id`        | `INTEGER GENERATED ALWAYS AS IDENTITY` | Identificador único del coche (PK). |
| `id_family` | `INTEGER`                              | Referencia a `familias.id` (FK).    |
| `name`      | `VARCHAR(100)`                         | Nombre del coche.                   |

---

## 🔗 Relación entre tablas

* Una **familia** puede tener **muchos coches**.
* Un **coche** pertenece a **una única familia**.

Relación: **1 → N (uno a muchos)**

---

## 📝 Notas

* La relación está definida mediante una clave foránea `id_family` en la tabla `cars`.
* Se utiliza SQLAlchemy para mapear estas tablas a modelos dentro de FastAPI.


