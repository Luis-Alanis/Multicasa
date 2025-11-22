from models.locacion_model import Locacion
from models.admin_model import Admin
from models.usuario_model import Usuario
from models.casa_model import Casa

# Instancias ORM
loc = Locacion()
admin = Admin()
usuario = Usuario()
casa = Casa()

print("\n===== TABLA: LOCACIONES =====")
print(loc.obtener_todas())

print("\n===== TABLA: USUARIOS =====")
print(usuario.obtener_todos())

print("\n===== TABLA: CASAS =====")
print(casa.obtener_todas())

print("\n===== TABLA: ADMINS (ANTES) =====")
print(admin.obtener_todos())

print("\n>>> CONSULTANDO ADMIN CON ID = 2...")
admin_pedro = admin.obtener_por_id(2)
print(admin_pedro)

print("\n>>> ELIMINANDO ADMIN CON ID = 2...")
admin.eliminar(2)
print("Admin eliminado.")

print("\n===== TABLA: ADMINS (DESPUÉS DE ELIMINAR) =====")
print(admin.obtener_todos())

print("\n>>> TEST FINALIZADO CON ÉXITO")