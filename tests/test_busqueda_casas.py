from models.casa_model import Casa

def test_busqueda():
    casa = Casa()

    print("\n--- PRUEBA 1: Buscar por ubicación ---")
    print(casa.buscar_completo(
        ubicacion="Coahuila"
    ))

    print("\n--- PRUEBA 2: Precio mínimo ---")
    print(casa.buscar_completo(
        precio_min=500000
    ))

    print("\n--- PRUEBA 3: Recámaras >= 3 ---")
    print(casa.buscar_completo(
        recamaras=3
    ))

    print("\n--- PRUEBA 4: Combinado (locación + precio + recámaras) ---")
    print(casa.buscar_completo(
        ubicacion="Coahuila",
        precio_min=500000,
        recamaras=3
    ))

    print("\n--- PRUEBA 5: Código Postal ---")
    print(casa.buscar_completo(
        ubicacion="25000"  # aquí prueba buscar por CP
    ))

    print("\n--- PRUEBA 6: Búsqueda con distancia (Haversine) ---")
    print(casa.buscar_completo(
        user_lat=25.4387,
        user_lon=-101.0000,
        rango_km=10
    ))


if __name__ == "__main__":
    test_busqueda()
