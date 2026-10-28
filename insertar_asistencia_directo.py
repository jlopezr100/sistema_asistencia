import pymysql # O usa mysql.connector si lo tienes en tus requirements.txt
from datetime import date

# 1. Configura los datos exactos que usas en tu MySQL Workbench
DB_CONFIG = {
    'host': 'tu_host_de_://azure.com', # Reemplaza con tu host de Workbench
    'user': 'avnadmin',
    'password': 'tu_password_aqui', # Reemplaza con tu contraseña
    'database': 'defaultdb',
    'port': 3306 # Reemplaza si usas otro puerto
}

def ejecutar():
    hoy = "2026-10-28"
    dia_texto = "MIERCOLES"
    
    try:
        conexion = pymysql.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        # A. Obtener el ID del corte activo para hoy
        cursor.execute("""
            SELECT id FROM asistencia_corte 
            WHERE f_inicio <= %s AND f_final >= %s AND procesado = 0 
            LIMIT 1
        """, (hoy, hoy))
        corte = cursor.fetchone()
        corte_id = corte[0] if corte else "NULL"
        
        # B. Filtrar personal activo que NO descanse los miércoles
        cursor.execute("""
            SELECT id FROM asistencia_personal 
            WHERE condicion = 1 AND UPPER(dia_descanso) != %s
        """, (dia_texto,))
        empleados = cursor.fetchall()
        
        print(f"Personal activo calificado encontrado: {len(empleados)}")
        registros_creados = 0
        
        # C. Insertar plantillas de forma directa saltándose el ORM
        for (emp_id,) in empleados:
            # Validar si ya existe el registro para evitar duplicidad
            cursor.execute("""
                SELECT 1 FROM asistencia_asistencia 
                WHERE personal_id = %s AND fecha = %s
            """, (emp_id, hoy))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO asistencia_asistencia 
                    (fecha, h_entrada, h_salida, justificado, personal_id, corte_id) 
                    VALUES (%s, NULL, NULL, 0, %s, %s)
                """, (hoy, emp_id, corte_id if corte_id != "NULL" else None))
                registros_creados += 1
                
        conexion.commit()
        print(f"Éxito absoluto: Se inyectaron {registros_creados} nuevas plantillas de asistencia en Workbench.")
        
    except Exception as e:
        print(f"Error en la conexión directa: {str(e)}")
    finally:
        if 'conexion' in locals() and conexion.open:
            cursor.close()
            conexion.close()

if __name__ == '__main__':
    ejecutar()
