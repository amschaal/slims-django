from django.db import migrations, models
from django.db.backends.mysql.schema import DatabaseSchemaEditor

def change_charset(apps, schema_editor: DatabaseSchemaEditor):
    database_name = schema_editor.connection.settings_dict['NAME']

    # Step 0: Disable foreign key checks
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    with schema_editor.connection.cursor() as cursor:
        cursor.execute("UPDATE run SET run_date='1900-01-01' WHERE run_date LIKE '0000-00-00';")

    # Step 1: Change the character set for the database
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"ALTER DATABASE `{database_name}` CHARACTER SET = utf8 COLLATE = utf8_general_ci;")

    # Step 2: Change the character set for each table
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = %s
            AND TABLE_TYPE = 'BASE TABLE';  -- Excludes views
        """, [database_name])
        
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"""
                ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
            """)

    # Step 3: Change the character set for each column
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND CHARACTER_SET_NAME IS NOT NULL;
        """, [database_name])
        
        columns = cursor.fetchall()
        
        for table_name, column_name, column_type in columns:
            cursor.execute(f"""
                ALTER TABLE `{table_name}`
                CHANGE `{column_name}` `{column_name}` {column_type} CHARACTER SET utf8 COLLATE utf8_general_ci;
            """)
    
    # Step 4: Re-enable foreign key checks
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

class Migration(migrations.Migration):
    dependencies = [
        ('slims', '0001_initial')
    ]

    operations = [
        migrations.RunPython(change_charset),
    ]
