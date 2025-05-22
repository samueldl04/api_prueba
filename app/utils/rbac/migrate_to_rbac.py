import sys
import os
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

def migrate_data(db: Session):
    """Migra los datos del antiguo sistema de permisos al nuevo RBAC usando SQL directo"""
    
    print("Iniciando migración de datos a RBAC...")
    
    # 1. Migrar allowances a permissions
    print("\n[1/5] Migrando allowances a permissions...")
    
    # Usar SQL directo para consultar allowances
    allowances = db.execute(text("SELECT id, name FROM allowances")).fetchall()
    permissions_created = 0
    
    for a_id, a_name in allowances:
        # Crear código y nombre para el nuevo permiso
        code = f"legacy.allowance.{a_id}"
        name = f"Legacy: {a_name}"
        
        # Verificar si ya existe
        existing = db.execute(
            text("SELECT id FROM permissions WHERE code = :code"),
            {"code": code}
        ).fetchone()
        
        if existing:
            print(f"  - Ya existe el permiso '{code}'")
            continue
        
        # Insertar nuevo permiso con SQL directo
        db.execute(
            text("""
                INSERT INTO permissions (code, name, description, resource, action, created_at)
                VALUES (:code, :name, :description, :resource, :action, NOW())
            """),
            {
                "code": code,
                "name": name,
                "description": f"Migrado desde allowance.id={a_id}",
                "resource": "legacy",
                "action": f"allowance.{a_id}"
            }
        )
        permissions_created += 1
        print(f"  - Creado permiso '{code}' desde allowance.id={a_id}")
    
    db.commit()
    print(f"  Se crearon {permissions_created} permisos")
    
    # 2. Migrar roles de role_company_rel a roles
    print("\n[2/5] Migrando roles...")
    roles_created = 0
    
    roles = db.execute(text("""
        SELECT role_id, name, company_id 
        FROM role_company_rel
    """)).fetchall()
    
    for r_id, r_name, c_id in roles:
        # Verificar si ya existe
        existing = db.execute(
            text("SELECT id FROM roles WHERE name = :name AND company_id = :company_id"),
            {"name": r_name, "company_id": c_id}
        ).fetchone()
        
        if existing:
            print(f"  - Ya existe el rol '{r_name}' para company_id={c_id}")
            continue
        
        # Insertar nuevo rol con SQL directo
        db.execute(
            text("""
                INSERT INTO roles (name, description, company_id, created_at, updated_at)
                VALUES (:name, :description, :company_id, NOW(), NOW())
            """),
            {
                "name": r_name,
                "description": f"Migrado desde role_company_rel.role_id={r_id}",
                "company_id": c_id
            }
        )
        roles_created += 1
        
        print(f"  - Creado rol '{r_name}' desde role_id={r_id}, company_id={c_id}")
    
    db.commit()
    print(f"  Se crearon {roles_created} roles")
    
    # 3. Crear mapeo entre old_role_id y new_role_id
    print("\n[3/5] Creando mapeo de roles antiguos a nuevos...")
    
    # Crear tabla temporal de mapeo si no existe
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS temp_role_mapping (
            old_role_id INT NOT NULL,
            company_id INT NOT NULL,
            new_role_id INT NOT NULL,
            PRIMARY KEY (old_role_id, company_id)
        )
    """))
    
    # Limpiar tabla temporal
    db.execute(text("TRUNCATE TABLE temp_role_mapping"))
    
    # Insertar mapeos
    db.execute(text("""
        INSERT INTO temp_role_mapping (old_role_id, company_id, new_role_id)
        SELECT rcr.role_id, rcr.company_id, r.id
        FROM role_company_rel rcr
        JOIN roles r ON r.name = rcr.name AND r.company_id = rcr.company_id
    """))
    
    db.commit()
    
    mapping_count = db.execute(text("SELECT COUNT(*) FROM temp_role_mapping")).scalar()
    print(f"  Se crearon {mapping_count} mapeos de roles")
    
    # 4. Migrar role_allowance_rel a role_permission_rel
    print("\n[4/5] Migrando asignaciones de permisos...")
    permissions_assigned = 0
    
    # Obtener todas las asignaciones
    role_allowances = db.execute(text("""
        SELECT ra.role_id, ra.allowance_id, rcr.company_id
        FROM role_allowance_rel ra
        JOIN role_company_rel rcr ON ra.role_id = rcr.role_id
    """)).fetchall()
    
    for role_id, allowance_id, company_id in role_allowances:
        # Obtener nuevos IDs
        new_role = db.execute(
            text("SELECT new_role_id FROM temp_role_mapping WHERE old_role_id = :role_id AND company_id = :company_id"),
            {"role_id": role_id, "company_id": company_id}
        ).fetchone()
        
        new_permission = db.execute(
            text("SELECT id FROM permissions WHERE code = :code"),
            {"code": f"legacy.allowance.{allowance_id}"}
        ).fetchone()
        
        if not new_role or not new_permission:
            print(f"  - No se encontró mapeo para role_id={role_id}, allowance_id={allowance_id}")
            continue
        
        new_role_id = new_role[0]
        new_permission_id = new_permission[0]
        
        # Verificar si ya existe la asignación
        existing = db.execute(
            text("""
                SELECT 1 FROM role_permission_rel
                WHERE role_id = :role_id AND permission_id = :permission_id
            """),
            {"role_id": new_role_id, "permission_id": new_permission_id}
        ).fetchone()
        
        if existing:
            print(f"  - Ya existe asignación para role_id={new_role_id}, permission_id={new_permission_id}")
            continue
        
        # Insertar nueva asignación
        db.execute(
            text("""
                INSERT INTO role_permission_rel (role_id, permission_id)
                VALUES (:role_id, :permission_id)
            """),
            {"role_id": new_role_id, "permission_id": new_permission_id}
        )
        permissions_assigned += 1
        
        print(f"  - Asignado permiso ID={new_permission_id} a rol ID={new_role_id}")
    
    db.commit()
    print(f"  Se asignaron {permissions_assigned} permisos a roles")
    
    # 5. Migrar user_company_role_rel a user_role
    print("\n[5/5] Migrando asignaciones de roles a usuarios...")
    user_roles_created = 0
    
    # Obtener todas las asignaciones de usuarios
    user_roles = db.execute(text("""
        SELECT user_id, company_id, role_id
        FROM user_company_role_rel
    """)).fetchall()
    
    for u_id, c_id, r_id in user_roles:
        # Buscar rol mapeado
        new_role = db.execute(
            text("SELECT new_role_id FROM temp_role_mapping WHERE old_role_id = :role_id AND company_id = :company_id"),
            {"role_id": r_id, "company_id": c_id}
        ).fetchone()
        
        if not new_role:
            print(f"  - No se encontró mapeo para role_id={r_id}, company_id={c_id}")
            continue
        
        new_role_id = new_role[0]
        
        # Verificar si ya existe la asignación
        existing = db.execute(
            text("""
                SELECT 1 FROM user_role
                WHERE user_id = :user_id AND role_id = :role_id AND company_id = :company_id
            """),
            {"user_id": u_id, "role_id": new_role_id, "company_id": c_id}
        ).fetchone()
        
        if existing:
            print(f"  - Ya existe asignación para user_id={u_id}, role_id={new_role_id}")
            continue
        
        # Insertar nueva asignación
        db.execute(
            text("""
                INSERT INTO user_role (user_id, role_id, company_id, assigned_at, valid_from)
                VALUES (:user_id, :role_id, :company_id, NOW(), NOW())
            """),
            {"user_id": u_id, "role_id": new_role_id, "company_id": c_id}
        )
        user_roles_created += 1
        
        print(f"  - Asignado rol ID={new_role_id} a usuario ID={u_id}")
    
    db.commit()
    print(f"  Se crearon {user_roles_created} asignaciones de roles a usuarios")
    
    print("\nMigración completada con éxito!")
