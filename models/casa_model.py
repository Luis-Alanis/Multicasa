from models.BaseModel import BaseModel

class Casa(BaseModel):
    table_name = "casas"

    # ---- SELECTS ----

    def obtener_todas(self):
        sql = """
            SELECT c.*, l.nombre AS locacion
            FROM casas c
            INNER JOIN catalogo_locacion l ON c.id_locacion = l.id_locacion
        """
        return self.query(sql)

    def obtener_por_id(self, id_casa):
        sql = """
            SELECT c.*, l.nombre AS locacion
            FROM casas c
            INNER JOIN catalogo_locacion l ON c.id_locacion = l.id_locacion
            WHERE id_casa = %s
        """
        return self.query(sql, (id_casa,), fetchone=True)

    # ---- CREATE ----

    def crear(self, id_locacion, latitud, longitud, codigo_postal, costo,
              recamaras, banos, estatus_venta, fotos=None):

        sql = f"""
            INSERT INTO casas
            (id_locacion, latitud, longitud, codigo_postal, costo,
             recamaras, baños, estatus_venta, fotos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (id_locacion, latitud, longitud, codigo_postal, costo,
                  recamaras, banos, estatus_venta, fotos)

        self.query(sql, params)
        return True

    # ---- UPDATE ----

    def actualizar(self, id_casa, id_locacion, latitud, longitud, codigo_postal,
                   costo, recamaras, banos, estatus_venta, fotos):

        sql = f"""
            UPDATE casas
            SET id_locacion=%s, latitud=%s, longitud=%s, codigo_postal=%s,
                costo=%s, recamaras=%s, baños=%s, estatus_venta=%s, fotos=%s
            WHERE id_casa=%s
        """

        params = (id_locacion, latitud, longitud, codigo_postal,
                  costo, recamaras, banos, estatus_venta, fotos, id_casa)

        self.query(sql, params)
        return True

    # ---- DELETE ----

    def eliminar(self, id_casa):
        sql = "DELETE FROM casas WHERE id_casa = %s"
        self.query(sql, (id_casa,))
        return True

    # ---- BÚSQUEDAS ----

    def buscar(self, texto):
        sql = """
            SELECT c.*, l.nombre AS locacion
            FROM casas c
            INNER JOIN catalogo_locacion l ON c.id_locacion = l.id_locacion
            WHERE l.nombre LIKE %s
               OR c.codigo_postal LIKE %s
        """
        like = f"%{texto}%"
        return self.query(sql, (like, like))

    def buscar_avanzado(self, min_precio=None, max_precio=None,
                         recamaras=None, banos=None, id_locacion=None):

        sql = """
            SELECT c.*, l.nombre AS locacion
            FROM casas c
            INNER JOIN catalogo_locacion l ON c.id_locacion = l.id_locacion
            WHERE 1 = 1
        """
        params = []

        if id_locacion:
            sql += " AND c.id_locacion = %s"
            params.append(id_locacion)

        if recamaras:
            sql += " AND c.recamaras >= %s"
            params.append(recamaras)

        if banos:
            sql += " AND c.baños >= %s"
            params.append(banos)

        if min_precio:
            sql += " AND c.costo >= %s"
            params.append(min_precio)

        if max_precio:
            sql += " AND c.costo <= %s"
            params.append(max_precio)

        return self.query(sql, params)
