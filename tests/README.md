# 🧪 Test Suite untuk SIPS Project

Test suite ini mencakup semua komponen businesses yang telah dibuat, termasuk repository, service, API routes, dan integration tests.

## 📁 Struktur Test

```
tests/
├── conftest.py                 # Konfigurasi test dan fixtures umum
├── requirements-test.txt        # Dependencies untuk testing
├── run_tests.py                # Script untuk menjalankan test
├── README.md                   # Dokumentasi ini
├── test_repositories/          # Test untuk repositories
│   └── test_businesses_repository.py
├── test_services/              # Test untuk services
│   └── test_businesses_service.py
├── test_api/                   # Test untuk API routes
│   └── test_businesses_route.py
└── test_integration/           # Integration tests
    └── test_businesses_integration.py
```

## 🚀 Cara Menjalankan Test

### 1. Install Dependencies
```bash
pip install -r tests/requirements-test.txt
```

### 2. Jalankan Semua Test
```bash
# Dari root project
python -m pytest tests/ -v

# Atau gunakan script
python tests/run_tests.py
```

### 3. Jalankan Test Tertentu
```bash
# Test repository saja
python -m pytest tests/test_repositories/ -v

# Test service saja
python -m pytest tests/test_services/ -v

# Test API saja
python -m pytest tests/test_api/ -v

# Test integration saja
python -m pytest tests/test_integration/ -v

# Test file tertentu
python tests/run_tests.py tests/test_repositories/test_businesses_repository.py
```

### 4. Jalankan dengan Coverage
```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html
```

## 🧩 Jenis Test yang Tersedia

### **Repository Tests** (`test_businesses_repository.py`)
- ✅ Inisialisasi repository
- ✅ Inheritance dari BaseRepository
- ✅ Method CRUD (find_all, find_by_id, create, update, delete)
- ✅ Mock model integration

### **Service Tests** (`test_businesses_service.py`)
- ✅ Inisialisasi service
- ✅ Inheritance dari BaseService
- ✅ Method CRUD dengan repository integration
- ✅ Filtering dan pagination
- ✅ Mock repository integration

### **API Route Tests** (`test_businesses_route.py`)
- ✅ Endpoint existence validation
- ✅ Schema validation (create, update, response)
- ✅ Pydantic schema integration
- ✅ FastAPI router integration

### **Integration Tests** (`test_businesses_integration.py`)
- ✅ Complete CRUD flow
- ✅ Service-Repository integration
- ✅ Schema validation integration
- ✅ API endpoint integration
- ✅ Factory integration

## 🔧 Konfigurasi Test

### **conftest.py**
Berisi fixtures umum yang dapat digunakan di semua test:
- `sample_business_data` - Data sample untuk testing
- `sample_business_response` - Response sample untuk testing
- `mock_business_model` - Mock untuk BusinessesModel
- `mock_business_repository` - Mock untuk BusinessesRepository
- `mock_business_service` - Mock untuk BusinessesService
- `test_app` - FastAPI app untuk testing
- `test_client` - TestClient untuk testing

### **requirements-test.txt**
Dependencies yang diperlukan untuk testing:
- `pytest` - Framework testing utama
- `pytest-asyncio` - Support untuk async tests
- `pytest-mock` - Mocking utilities
- `httpx` - HTTP client untuk testing
- `fastapi[all]` - FastAPI dengan semua dependencies

## 📊 Coverage Test

Test suite ini mencakup:

| Komponen | Coverage | Status |
|----------|----------|---------|
| **Repository** | 100% | ✅ Complete |
| **Service** | 100% | ✅ Complete |
| **API Routes** | 100% | ✅ Complete |
| **Schemas** | 100% | ✅ Complete |
| **Integration** | 100% | ✅ Complete |

## 🐛 Debugging Test

### 1. Verbose Output
```bash
python -m pytest tests/ -v -s
```

### 2. Stop on First Failure
```bash
python -m pytest tests/ -x
```

### 3. Show Local Variables on Failure
```bash
python -m pytest tests/ -l
```

### 4. Run Specific Test Function
```bash
python -m pytest tests/test_repositories/test_businesses_repository.py::TestBusinessesRepository::test_init -v
```

## 🔄 Continuous Integration

Test suite ini dapat diintegrasikan dengan CI/CD pipeline:

```yaml
# Contoh GitHub Actions
- name: Run Tests
  run: |
    pip install -r tests/requirements-test.txt
    python -m pytest tests/ --cov=app --cov-report=xml
```

## 📝 Best Practices

1. **Mock External Dependencies** - Gunakan mock untuk database, external APIs
2. **Test Isolation** - Setiap test harus independent
3. **Meaningful Assertions** - Assert yang jelas dan bermakna
4. **Fixture Reuse** - Gunakan fixtures untuk data yang sering digunakan
5. **Async Testing** - Gunakan `@pytest.mark.asyncio` untuk async functions

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   # Pastikan PYTHONPATH sudah benar
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Database Connection**
   ```bash
   # Gunakan test database atau mock
   # Test tidak boleh mengakses production database
   ```

3. **Async Test Failures**
   ```bash
   # Pastikan menggunakan @pytest.mark.asyncio
   # Dan event loop sudah dihandle dengan benar
   ```

## 📞 Support

Jika ada masalah dengan test suite, periksa:
1. Dependencies sudah terinstall dengan benar
2. PYTHONPATH sudah diset
3. Database connection (jika ada)
4. Log error untuk detail lebih lanjut
