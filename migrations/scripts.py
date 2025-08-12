import asyncio
import os
import subprocess
import sys

from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.db_manager import DatabaseManager

load_dotenv()


async def execute_sql_file(db_manager: DatabaseManager, sql_file_path: str):
    """Execute SQL file content"""
    try:
        if not os.path.exists(sql_file_path):
            print(f"Warning: SQL file {sql_file_path} not found")
            return False

        with open(sql_file_path, encoding="utf-8") as file:
            sql_content = file.read()

        # Split SQL content by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

        for statement in statements:
            if statement and not statement.startswith("--") and not statement.startswith("/*"):
                try:
                    await db_manager.execute_query(statement)
                    print(f"Executed SQL statement: {statement[:50]}...")
                except Exception as e:
                    print(f"Warning: Failed to execute statement: {e}")
                    # Continue with other statements

        print(f"Successfully executed SQL file: {sql_file_path}")
        return True

    except Exception as e:
        print(f"Error executing SQL file {sql_file_path}: {e}")
        return False


async def main():
    """Main async function to execute pre-test, Alembic migration, SQL files, and post-check"""
    try:
        print("🚦 Running pre-migration test (pre_test.py)...")
        pre_test_result = subprocess.run(
            [sys.executable, os.path.join("migrations", "pre_test.py")], capture_output=True, text=True
        )
        print(pre_test_result.stdout)
        if pre_test_result.returncode != 0:
            print("❌ pre_test.py failed:")
            print(pre_test_result.stderr)
            sys.exit(1)
        else:
            print("✅ pre_test.py succeeded.")

        print("Starting migration and SQL execution process...")

        # Step 1: Jalankan migration script Alembic sebelum eksekusi SQL files
        print("Running Alembic migration: upgrade 099536a08 ...")

        # Jalankan perintah Alembic upgrade
        result = subprocess.run(["alembic", "upgrade", "099536a08"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Alembic migration failed:")
            print(result.stderr)
            sys.exit(1)
        else:
            print("✅ Alembic migration succeeded.")
            print(result.stdout)

        # Step 2: Execute SQL files directly
        print("Executing SQL files...")
        db_manager = DatabaseManager()

        # Execute forestry_area.sql
        forestry_area_sql = os.path.join("migrations", "forestry_area.sql")
        await execute_sql_file(db_manager, forestry_area_sql)

        # Execute role_users.sql
        role_users_sql = os.path.join("migrations", "role_users.sql")
        await execute_sql_file(db_manager, role_users_sql)

        # Cleanup database connections
        await db_manager.dispose()

        print("SQL execution completed successfully")

    except Exception as e:
        print(f"Error during migration or SQL execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
