from models.BaseModel import BaseModel

class Usuario(BaseModel):
    table_name = "usuarios"

    # Obtener todos los tickets
    def obtener_todos(self):
        sql = f"SELECT * FROM {self.table_name}"
        return self.query(sql)

    # Obtener un ticket por ID
    def obtener_por_id(self, id_usuario):
        sql = f"SELECT * FROM {self.table_name} WHERE id_usuario = %s"
        return self.query(sql, (id_usuario,), fetchone=True)

    # Crear un nuevo ticket
    def crear(self, nombre, correo, telefono, asunto, mensaje, estado="pendiente"):
        sql = f"""
            INSERT INTO {self.table_name} 
            (nombre, correo, telefono, asunto, mensaje, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.query(sql, (nombre, correo, telefono, asunto, mensaje, estado))
        return True

    # Actualizar un ticket
    def actualizar(self, id_usuario, nombre=None, correo=None, telefono=None,
                   asunto=None, mensaje=None, estado=None):
        # Creamos partes dinámicas para actualizar solo los campos enviados
        campos = []
        params = []

        if nombre is not None:
            campos.append("nombre=%s")
            params.append(nombre)
        if correo is not None:
            campos.append("correo=%s")
            params.append(correo)
        if telefono is not None:
            campos.append("telefono=%s")
            params.append(telefono)
        if asunto is not None:
            campos.append("asunto=%s")
            params.append(asunto)
        if mensaje is not None:
            campos.append("mensaje=%s")
            params.append(mensaje)
        if estado is not None:
            campos.append("estado=%s")
            params.append(estado)

        if not campos:
            return False  # No hay nada para actualizar

        sql = f"""
            UPDATE {self.table_name}
            SET {', '.join(campos)}
            WHERE id_usuario=%s
        """
        params.append(id_usuario)
        self.query(sql, tuple(params))
        return True

    # Eliminar un ticket
    def eliminar(self, id_usuario):
        sql = f"DELETE FROM {self.table_name} WHERE id_usuario = %s"
        self.query(sql, (id_usuario,))
        return True

    # Buscar tickets por texto en varios campos
    def buscar(self, texto):
        sql = f"""
            SELECT * FROM {self.table_name}
            WHERE nombre LIKE %s
               OR correo LIKE %s
               OR telefono LIKE %s
               OR asunto LIKE %s
               OR mensaje LIKE %s
        """
        like = f"%{texto}%"
        return self.query(sql, (like, like, like, like, like))