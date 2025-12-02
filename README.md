# Proyecto Final - Programación Orientada a Objetos (POO) - Gestión de Ventas

## Requisitos
- Python 3.8+
- MySQL
- Instalar dependencias: `pip install -r requirements.txt`

## Crear base de datos
1. Ejecutar `database/script_creacion.sql` en tu servidor MySQL:
   - `mysql -u root -p < database/script_creacion.sql`
2. Ajustar credenciales si es necesario en `src/config/db_config.py` o mediante variables de entorno `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`.

## Estructura
- `src/` código fuente (models, controllers, views)
- `database/` script SQL
- `requirements.txt`

## Ejecutar
Desde la carpeta principal:
```bash
python -m src.main
