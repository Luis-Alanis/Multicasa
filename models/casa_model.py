from models.BaseModel import BaseModel
import math

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
              recamaras, baños, estatus_venta, fotos=None):

        sql = f"""
            INSERT INTO casas
            (id_locacion, latitud, longitud, codigo_postal, costo,
             recamaras, baños, estatus_venta, fotos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (id_locacion, latitud, longitud, codigo_postal, costo,
                  recamaras, baños, estatus_venta, fotos)

        self.query(sql, params)
        return True

    # ---- UPDATE ----

    def actualizar(self, id_casa, id_locacion, latitud, longitud, codigo_postal,
                   costo, recamaras, baños, estatus_venta, fotos):

        sql = f"""
            UPDATE casas
            SET id_locacion=%s, latitud=%s, longitud=%s, codigo_postal=%s,
                costo=%s, recamaras=%s, baños=%s, estatus_venta=%s, fotos=%s
            WHERE id_casa=%s
        """

        params = (id_locacion, latitud, longitud, codigo_postal,
                  costo, recamaras, baños, estatus_venta, fotos, id_casa)

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
                         recamaras=None, baños=None, id_locacion=None):

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

        if baños:
            sql += " AND c.baños >= %s"
            params.append(baños)

        if min_precio:
            sql += " AND c.costo >= %s"
            params.append(min_precio)

        if max_precio:
            sql += " AND c.costo <= %s"
            params.append(max_precio)

        return self.query(sql, params)
    
    def buscar_completo(self, ubicacion=None, precio_min=None, precio_max=None,
                    recamaras=None, baños=None, user_lat=None, user_lon=None,
                    rango_km=None, incluir_vendidas=False):
    
        sql = """
            SELECT c.*, l.nombre AS locacion, l.id_locacion
            FROM casas c
            INNER JOIN catalogo_locacion l
            ON c.id_locacion = l.id_locacion
            WHERE 1 = 1
        """
        params = []

        if not incluir_vendidas:
            sql += " AND c.estatus_venta = 'En Venta'"

        if ubicacion:
            sql += """
                AND (l.nombre LIKE %s OR CAST(c.codigo_postal AS CHAR) LIKE %s)"""
            like = f"%{ubicacion}%"
            params.extend([like, like])
            
        if precio_min:
            sql += " AND c.costo >= %s"
            params.append(precio_min)

        if precio_max:
            sql += " AND c.costo <= %s"
            params.append(precio_max)

        if recamaras:
            if recamaras == "4+":
                sql += " AND c.recamaras >= 4"
            else:
                sql += " AND c.recamaras = %s"
                params.append(recamaras)

        if baños:
            if baños == "3+":
                sql += " AND c.baños >= 3"
            else:
                sql += " AND c.baños = %s"
                params.append(baños)

        casas = self.query(sql, params)

        if rango_km and user_lat and user_lon:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            rango_km = float(rango_km)

            def haversine(lat1, lon1, lat2, lon2):
                R = 6371
                d_lat = math.radians(lat2 - lat1)
                d_lon = math.radians(lon2 - lon1)
                a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * \
                    math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c

            filtradas = []
            for casa in casas:
                if 'latitud' not in casa or 'longitud' not in casa:
                    continue

                dist = haversine(
                    user_lat,
                    user_lon,
                    float(casa["latitud"]),
                    float(casa["longitud"])
                )

                if dist <= rango_km:
                    casa["distancia_km"] = dist
                    filtradas.append(casa)

            return filtradas

        return casas
    
    def obtener_para_mapa(self, solo_en_venta=True):
        sql = """
            SELECT c.id_casa, c.latitud, c.longitud, c.costo, c.recamaras, c.baños, c.estatus_venta,
                l.nombre AS locacion
            FROM casas c
            INNER JOIN catalogo_locacion l ON c.id_locacion = l.id_locacion
            WHERE c.latitud IS NOT NULL AND c.longitud IS NOT NULL
        """
        params = []

        if solo_en_venta:
            sql += " AND c.estatus_venta = %s"
            params.append("En Venta")

        return self.query(sql, params)