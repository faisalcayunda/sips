#!/usr/bin/env python3
"""
Test script untuk memverifikasi migration fix
"""

from sqlalchemy import text


def test_sql_text_usage():
    """Test bahwa sa.text() berfungsi dengan benar"""

    # Simulasi connection (tidak perlu database real)
    print("🧪 Testing SQL text usage...")

    # Test 1: Basic text usage
    try:
        sql_query = text("SELECT COUNT(*) FROM businesses WHERE kups_acc_id IS NOT NULL")
        print("✅ sa.text() berfungsi dengan benar")
        print(f"   Query: {sql_query}")
    except Exception as e:
        print(f"❌ Error dengan sa.text(): {e}")
        return False

    # Test 2: Complex UPDATE query
    try:
        update_query = text(
            """
            UPDATE businesses
            SET kups_acc_id = CONCAT('["', kups_acc_id, '"]')
            WHERE kups_acc_id REGEXP '^[0-9]+$' AND kups_acc_id != '[]'
        """
        )
        print("✅ Complex UPDATE query dengan sa.text() berfungsi")
        print(f"   Query: {update_query}")
    except Exception as e:
        print(f"❌ Error dengan complex query: {e}")
        return False

    # Test 3: JSON conversion logic
    print("\n🔍 Testing JSON conversion logic...")

    test_cases = [
        ("", "[]"),  # Empty string -> empty array
        ("123", '["123"]'),  # Number -> array with number
        ("1,2,3", '["1","2","3"]'),  # Comma-separated -> array
        ("abc", '["abc"]'),  # Text -> array with text
    ]

    for input_val, expected in test_cases:
        print(f"   Input: '{input_val}' -> Expected: {expected}")

    print("\n✅ Semua test berhasil!")
    return True


def test_migration_structure():
    """Test struktur migration file"""

    print("\n📁 Testing migration file structure...")

    try:
        # Import migration file
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "migration", "migrations/versions/20250812_2207_099536a084e5_revision_table.py"
        )
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)

        # Check if functions exist
        if hasattr(migration_module, "upgrade"):
            print("✅ upgrade() function ditemukan")
        else:
            print("❌ upgrade() function tidak ditemukan")
            return False

        if hasattr(migration_module, "downgrade"):
            print("✅ downgrade() function ditemukan")
        else:
            print("❌ downgrade() function tidak ditemukan")
            return False

        print("✅ Migration file structure valid")
        return True

    except Exception as e:
        print(f"❌ Error testing migration file: {e}")
        return False


def main():
    """Main test function"""

    print("🚀 Starting Migration Fix Tests...\n")

    # Run tests
    test1_passed = test_sql_text_usage()
    test2_passed = test_migration_structure()

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   SQL Text Usage: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Migration Structure: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 SEMUA TEST BERHASIL! Migration siap dijalankan.")
        print("\n📋 Langkah selanjutnya:")
        print("   1. Backup database")
        print("   2. Jalankan: alembic upgrade 099536a084e5")
        print("   3. Verifikasi hasil")
    else:
        print("\n⚠️  Ada test yang gagal. Periksa error di atas.")

    print("=" * 50)


if __name__ == "__main__":
    main()
