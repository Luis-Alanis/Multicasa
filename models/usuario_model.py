from models.BaseModel import BaseModel

class Usuario(BaseModel):
    table_name = "usuarios"

    def obtener_todos(self):
        sql = f"SELECT * FROM {self.table_name}"
        return self.query(sql)

    def obtener_por_id(self, id_usuario):
        sql = f"SELECT * FROM {self.table_name} WHERE id_usuario = %s"
        return self.query(sql, (id_usuario,), fetchone=True)

    def crear(self, nombre, correo, telefono):
        sql = f"""
            INSERT INTO {self.table_name} (nombre, correo, telefono)
            VALUES (%s, %s, %s)
        """
        self.query(sql, (nombre, correo, telefono))
        return True

    def actualizar(self, id_usuario, nombre, correo, telefono):
        sql = f"""
            UPDATE {self.table_name}
            SET nombre = %s, correo = %s, telefono = %s
            WHERE id_usuario = %s
        """
        self.query(sql, (nombre, correo, telefono, id_usuario))
        return True

    def eliminar(self, id_usuario):
        sql = f"DELETE FROM {self.table_name} WHERE id_usuario = %s"
        self.query(sql, (id_usuario,))
        return True

    def buscar(self, texto):
        sql = f"""
            SELECT * FROM {self.table_name}
            WHERE nombre LIKE %s
               OR correo LIKE %s
               OR telefono LIKE %s
        """
        like = f"%{texto}%"
        return self.query(sql, (like, like, like))
