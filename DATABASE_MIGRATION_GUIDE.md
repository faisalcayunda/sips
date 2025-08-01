# Database Migration Guide

## Overview

This guide covers the improved database migration system that resolves async connection issues and provides robust database management utilities.

## Problem Solved

The original migration script was experiencing `RuntimeError: Event loop is closed` errors due to improper async connection handling. This has been resolved by implementing:

1. **Proper Engine Disposal**: All async engines are now properly disposed of using `await engine.dispose()`
2. **Context Managers**: Using `@asynccontextmanager` for safe connection handling
3. **Error Handling**: Comprehensive error handling with proper cleanup
4. **Connection Pooling**: Optimized connection pool settings for migrations

## Key Improvements

### 1. Database Manager (`app/utils/db_manager.py`)

The `DatabaseManager` class provides:

- **Async Context Management**: Safe connection and transaction handling
- **Proper Disposal**: Automatic engine cleanup to prevent connection leaks
- **Health Checks**: Database connectivity verification
- **Migration Utilities**: Complete migration process management

```python
# Example usage
from app.utils.db_manager import db_manager

async with db_manager.get_connection() as conn:
    result = await conn.execute(text("SELECT * FROM users"))
```

### 2. Improved Migration Script (`migrations/scripts.py`)

The migration script now:

- Uses the `DatabaseManager` for robust connection handling
- Provides detailed logging and error reporting
- Ensures proper cleanup in all scenarios
- Handles async operations correctly

### 3. Enhanced Alembic Configuration (`migrations/env.py`)

The Alembic environment now:

- Uses `NullPool` for migration operations
- Implements proper async context management
- Ensures engine disposal after migrations
- Provides better error handling

## Usage

### Running Migrations

```bash
# Run the complete migration process
source venv/bin/activate && PYTHONPATH=. python migrations/scripts.py
```

### Testing Database Connection

```bash
# Test database connectivity
source venv/bin/activate && PYTHONPATH=. python app/utils/test_db.py
```

### Manual Migration Commands

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check migration status
alembic current
```

## Best Practices

### 1. Connection Management

- Always use context managers for database connections
- Ensure proper engine disposal after operations
- Use `NullPool` for migration operations to avoid connection pooling issues

### 2. Error Handling

- Implement comprehensive try-catch blocks
- Always cleanup resources in finally blocks
- Log errors with sufficient detail for debugging

### 3. Async Operations

- Use `asyncio.run()` for top-level async operations
- Avoid mixing sync and async code inappropriately
- Ensure proper event loop handling

### 4. Database Configuration

```python
# Recommended engine configuration for migrations
engine = create_async_engine(
    database_url,
    poolclass=NullPool,  # No connection pooling for migrations
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections every hour
    echo=False,          # Disable SQL logging for production
    future=True          # Use SQLAlchemy 2.0 style
)
```

## Performance Optimizations

### 1. Connection Pooling

- **Development**: Use `NullPool` for migrations to avoid connection issues
- **Production**: Use `QueuePool` with appropriate settings for application connections

### 2. Query Optimization

- Use parameterized queries to prevent SQL injection
- Implement proper indexing strategies
- Consider query caching for frequently accessed data

### 3. Migration Performance

- Use `--autogenerate` sparingly in production
- Review generated migrations before applying
- Test migrations in staging environments first

## Troubleshooting

### Common Issues

1. **Event Loop Closed Error**
   - Ensure proper engine disposal
   - Use context managers for connections
   - Avoid mixing sync/async code

2. **Connection Timeout**
   - Check database server status
   - Verify connection string
   - Review network connectivity

3. **Migration Failures**
   - Check database permissions
   - Verify schema compatibility
   - Review migration dependencies

### Debug Commands

```bash
# Check database connection
python app/utils/test_db.py

# View migration history
alembic history

# Check current migration state
alembic current

# Downgrade to specific migration
alembic downgrade <revision>
```

## Security Considerations

1. **Connection Strings**: Store database URLs in environment variables
2. **Permissions**: Use dedicated database users with minimal required permissions
3. **SQL Injection**: Always use parameterized queries
4. **Logging**: Avoid logging sensitive data in production

## Monitoring and Logging

The improved system includes comprehensive logging:

- Connection status and health checks
- Migration progress and results
- Error details for debugging
- Performance metrics for optimization

## Future Enhancements

1. **Migration Rollback**: Implement automatic rollback on failure
2. **Parallel Migrations**: Support for concurrent migration operations
3. **Migration Testing**: Automated testing of migration scripts
4. **Performance Monitoring**: Real-time migration performance tracking

## Conclusion

The improved database migration system provides:

- **Reliability**: Robust error handling and resource cleanup
- **Performance**: Optimized connection management and query execution
- **Maintainability**: Clean, well-documented code structure
- **Scalability**: Support for complex migration scenarios

This system follows modern Python async best practices and provides a solid foundation for database operations in your application.
