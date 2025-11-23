from models.BaseModel import BaseModel

class Admin(BaseModel):
    table_name = "admins"

    def obtener_todos(self):
        sql = f"SELECT * FROM {self.table_name}"
        return self.query(sql)

    def obtener_por_id(self, id_admin):
        sql = f"SELECT * FROM {self.table_name} WHERE id_admin = %s"
        return self.query(sql, (id_admin,), fetchone=True)

    def obtener_por_correo(self, correo):
        sql = f"SELECT * FROM {self.table_name} WHERE correo = %s"
        return self.query(sql, (correo,), fetchone=True)

    def crear(self, nombre, correo, contraseña):
        sql = f"""
            INSERT INTO {self.table_name} (nombre, correo, contraseña)
            VALUES (%s, %s, %s)
        """
        self.query(sql, (nombre, correo, contraseña))
        return True

    def actualizar(self, id_admin, nombre, correo, contraseña):
        sql = f"""
            UPDATE {self.table_name}
            SET nombre = %s, correo = %s, contraseña = %s
            WHERE id_admin = %s
        """
        self.query(sql, (nombre, correo, contraseña, id_admin))
        return True

    def eliminar(self, id_admin):
        sql = f"DELETE FROM {self.table_name} WHERE id_admin = %s"
        self.query(sql, (id_admin,))
        return True
