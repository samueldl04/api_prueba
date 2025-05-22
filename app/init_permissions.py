import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Añadir directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.session import SessionLocal
from models.rbac import Permission, Role, RolePermissionRel

# Permisos básicos organizados por módulo
BASIC_PERMISSIONS = [
    # Empleados/Usuarios
    {"code": "user.create", "name": "Crear usuario", "resource": "user", "action": "create"},
    {"code": "user.read", "name": "Ver usuarios", "resource": "user", "action": "read"},
    {"code": "user.update", "name": "Modificar usuario", "resource": "user", "action": "update"},
    {"code": "user.delete", "name": "Eliminar usuario", "resource": "user", "action": "delete"},
    
    # Fichajes
    {"code": "clock_in.create", "name": "Crear fichaje", "resource": "clock_in", "action": "create"},
    {"code": "clock_in.read", "name": "Ver fichajes", "resource": "clock_in", "action": "read"},
    {"code": "clock_in.update", "name": "Modificar fichaje", "resource": "clock_in", "action": "update"},
    {"code": "clock_in.delete", "name": "Eliminar fichaje", "resource": "clock_in", "action": "delete"},
    {"code": "clock_in.admin", "name": "Administrar fichajes", "resource": "clock_in", "action": "admin"},
    
    # Informes
    {"code": "report.basic", "name": "Ver informes básicos", "resource": "report", "action": "basic"},
    {"code": "report.advanced", "name": "Ver informes avanzados", "resource": "report", "action": "advanced"},
    {"code": "report.export", "name": "Exportar informes", "resource": "report", "action": "export"},
    
    # Horarios
    {"code": "schedule.create", "name": "Crear horario", "resource": "schedule", "action": "create"},
    {"code": "schedule.read", "name": "Ver horarios", "resource": "schedule", "action": "read"},
    {"code": "schedule.update", "name": "Modificar horario", "resource": "schedule", "action": "update"},
    {"code": "schedule.delete", "name": "Eliminar horario", "resource": "schedule", "action": "delete"},
    
    # Ubicaciones
    {"code": "location.create", "name": "Crear ubicación", "resource": "location", "action": "create"},
    {"code": "location.read", "name": "Ver ubicaciones", "resource": "location", "action": "read"},
    {"code": "location.update", "name": "Modificar ubicación", "resource": "location", "action": "update"},
    {"code": "location.delete", "name": "Eliminar ubicación", "resource": "location", "action": "delete"},
    
    # Departamentos
    {"code": "department.create", "name": "Crear departamento", "resource": "department", "action": "create"},
    {"code": "department.read", "name": "Ver departamentos", "resource": "department", "action": "read"},
    {"code": "department.update", "name": "Modificar departamento", "resource": "department", "action": "update"},
    {"code": "department.delete", "name": "Eliminar departamento", "resource": "department", "action": "delete"},
    
    # Gestión de RBAC
    {"code": "rbac.role.list", "name": "Listar roles", "resource": "rbac", "action": "role.list"},
    {"code": "rbac.role.create", "name": "Crear rol", "resource": "rbac", "action": "role.create"},
    {"code": "rbac.role.view", "name": "Ver rol", "resource": "rbac", "action": "role.view"},
    {"code": "rbac.role.update", "name": "Actualizar rol", "resource": "rbac", "action": "role.update"},
    {"code": "rbac.permission.list", "name": "Listar permisos", "resource": "rbac", "action": "permission.list"},
    {"code": "rbac.permission.create", "name": "Crear permiso", "resource": "rbac", "action": "permission.create"},
    {"code": "rbac.user.assign", "name": "Asignar rol a usuario", "resource": "rbac", "action": "user.assign"},
    {"code": "rbac.user.unassign", "name": "Quitar rol a usuario", "resource": "rbac", "action": "user.unassign"},
    {"code": "rbac.user.view", "name": "Ver roles de usuario", "resource": "rbac", "action": "user.view"},
]

# Roles predefinidos con conjuntos de permisos
DEFAULT_ROLES = [
    {
        "name": "Administrador",
        "description": "Acceso completo a todas las funciones",
        "permissions": ["*"],  # Todos los permisos
        "is_admin": True
    },
    {
        "name": "Gerente",
        "description": "Gestión de usuarios y acceso a informes",
        "permissions": [
            "user.read", "user.create", "user.update",
            "clock_in.read", "clock_in.update", "clock_in.admin",
            "report.basic", "report.advanced", "report.export",
            "schedule.read", "schedule.create", "schedule.update",
            "location.read", "department.read"
        ],
        "parent": "Administrador"
    },
    {
        "name": "Supervisor",
        "description": "Supervisión de fichajes y reportes básicos",
        "permissions": [
            "user.read",
            "clock_in.read", "clock_in.update",
            "report.basic", "schedule.read",
            "location.read", "department.read"
        ],
        "parent": "Gerente"
    },
    {
        "name": "Empleado",
        "description": "Acceso básico para fichajes",
        "permissions": [
            "clock_in.create", "clock_in.read",
            "user.read", "schedule.read"
        ],
        "parent": "Supervisor"
    }
]

def init_permissions(db: Session, company_id: int = 10):
    """Inicializa los permisos y roles básicos para una empresa"""
    print(f"Inicializando permisos y roles para la empresa ID: {company_id}")
    
    # 1. Crear permisos básicos
    created_permissions = {}
    for perm_data in BASIC_PERMISSIONS:
        code = perm_data["code"]
        # Verificar si ya existe
        existing = db.query(Permission).filter(Permission.code == code).first()
        if existing:
            created_permissions[code] = existing
            print(f"Permiso existente: {code}")
            continue
        
        # Crear nuevo permiso
        permission = Permission(**perm_data)
        db.add(permission)
        db.flush()
        created_permissions[code] = permission
        print(f"Permiso creado: {code}")
    
    # 2. Crear roles predefinidos
    role_map = {}
    for role_data in DEFAULT_ROLES:
        # Verificar si ya existe
        existing = db.query(Role).filter(
            Role.name == role_data["name"],
            Role.company_id == company_id
        ).first()
        
        if existing:
            role_map[role_data["name"]] = existing
            print(f"Rol existente: {role_data['name']}")
            continue
        
        # Crear nuevo rol
        role = Role(
            name=role_data["name"],
            description=role_data.get("description", ""),
            company_id=company_id
        )
        
        # Asignar padre si aplica
        if "parent" in role_data and role_data["parent"] in role_map:
            role.parent_id = role_map[role_data["parent"]].id
        
        db.add(role)
        db.flush()
        role_map[role_data["name"]] = role
        print(f"Rol creado: {role_data['name']}")
        
        # Asignar permisos al rol
        for perm_code in role_data["permissions"]:
            # Si es '*', asignar todos los permisos
            if perm_code == "*":
                for p in created_permissions.values():
                    role_perm = RolePermissionRel(role_id=role.id, permission_id=p.id)
                    db.add(role_perm)
            elif perm_code in created_permissions:
                role_perm = RolePermissionRel(
                    role_id=role.id,
                    permission_id=created_permissions[perm_code].id
                )
                db.add(role_perm)
    
    db.commit()
    print("Inicialización completada con éxito.")

if __name__ == "__main__":
    # Ejemplo de uso: python init_permissions.py 1
    company_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    db = SessionLocal()
    try:
        init_permissions(db, company_id)
    finally:
        db.close()