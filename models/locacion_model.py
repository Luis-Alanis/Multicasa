from models.BaseModel import BaseModel

class Locacion(BaseModel):
    table_name = "catalogo_locacion"

    def obtener_todas(self):
        sql = f"SELECT * FROM {self.table_name}"
        return self.query(sql)

    def obtener_por_id(self, id_locacion):
        sql = f"SELECT * FROM {self.table_name} WHERE id_locacion = %s"
        return self.query(sql, (id_locacion,), fetchone=True)

    def crear(self, nombre):
        sql = f"INSERT INTO {self.table_name} (nombre) VALUES (%s)"
        self.query(sql, (nombre,))
        return True

    def actualizar(self, id_locacion, nombre):
        sql = f"""
            UPDATE {self.table_name}
            SET nombre = %s
            WHERE id_locacion = %s
        """
        self.query(sql, (nombre, id_locacion))
        return True

    def eliminar(self, id_locacion):
        sql = f"DELETE FROM {self.table_name} WHERE id_locacion = %s"
        self.query(sql, (id_locacion,))
        return True

    def buscar(self, texto):
        sql = f"SELECT * FROM {self.table_name} WHERE nombre LIKE %s"
        like = f"%{texto}%"
        return self.query(sql, (like,))
