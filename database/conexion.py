import mysql.connector
from mysql.connector import Error


class ConexionBD:
    def __init__(self, host, usuario, contraseña, base_datos):
        self.host = host
        self.usuario = usuario
        self.contraseña = contraseña
        self.base_datos = base_datos
        self.conexion = None
    
    def conectar(self):
        """Establece conexión con MySQL"""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contraseña,
                database=self.base_datos
            )
            print("✓ Conexión exitosa a MySQL")
            return self.conexion
        except Error as e:
            print(f"✗ Error de conexión: {e}")
            return None
    
    def desconectar(self):
        """Cierra la conexión"""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("✓ Conexión cerrada")
    
    def ejecutar_consulta(self, sql, parametros=None):
        """
        Ejecuta una consulta SELECT
        
        Args:
            sql: Consulta SQL SELECT
            parametros: Tupla de parámetros para la consulta (opcional)
        
        Returns:
            Lista de resultados (diccionarios)
        """
        if not self.conexion:
            print("✗ No hay conexión a la base de datos")
            return None
        
        cursor = None
        try:
            cursor = self.conexion.cursor(dictionary=True)
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"✗ Error en consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def ejecutar_insertar(self, sql, parametros=None):
        """
        Ejecuta un INSERT
        
        Args:
            sql: Consulta SQL INSERT
            parametros: Tupla de parámetros para la consulta (opcional)
        
        Returns:
            ID del registro insertado
        """
        if not self.conexion:
            print("✗ No hay conexión a la base de datos")
            return 0
        
        cursor = None
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            id_insertado = cursor.lastrowid
            print(f"✓ Registro insertado con ID: {id_insertado}")
            return id_insertado
        except Error as e:
            print(f"✗ Error al insertar: {e}")
            self.conexion.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def ejecutar_actualizar(self, sql, parametros=None):
        """
        Ejecuta un UPDATE
        
        Args:
            sql: Consulta SQL UPDATE
            parametros: Tupla de parámetros para la consulta (opcional)
        
        Returns:
            Número de registros actualizados
        """
        if not self.conexion:
            print("✗ No hay conexión a la base de datos")
            return 0
        
        cursor = None
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            print(f"✓ Registros actualizados: {filas_afectadas}")
            return filas_afectadas
        except Error as e:
            print(f"✗ Error al actualizar: {e}")
            self.conexion.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def ejecutar_eliminar(self, sql, parametros=None):
        """
        Ejecuta un DELETE
        
        Args:
            sql: Consulta SQL DELETE
            parametros: Tupla de parámetros para la consulta (opcional)
        
        Returns:
            Número de registros eliminados
        """
        if not self.conexion:
            print("✗ No hay conexión a la base de datos")
            return 0
        
        cursor = None
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            print(f"✓ Registros eliminados: {filas_afectadas}")
            return filas_afectadas
        except Error as e:
            print(f"✗ Error al eliminar: {e}")
            self.conexion.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()