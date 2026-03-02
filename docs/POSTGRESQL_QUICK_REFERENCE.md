# PostgreSQL Migration - Quick Reference

## 🚀 Quick Start (5 Minutes)

### 1. Install PostgreSQL
```powershell
# Windows (download installer)
https://www.postgresql.org/download/windows/

# Or use package manager
choco install postgresql
```

### 2. Create Database
```bash
psql -U postgres
CREATE DATABASE bharat_content_ai;
\q
```

### 3. Update .env
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai
```

### 4. Install Dependencies
```powershell
cd backend
pip install asyncpg
```

### 5. Run Migration
```powershell
# Option A: Fresh start (no data)
alembic upgrade head

# Option B: Migrate from SQLite
python migrate_sqlite_to_postgres.py
```

### 6. Start Server
```powershell
uvicorn app.main:app --reload
```

## 📊 Key Changes

| Component | Before (SQLite) | After (PostgreSQL) |
|-----------|----------------|-------------------|
| Driver | sqlite3 | asyncpg |
| Sessions | Synchronous | Async |
| JSON Columns | JSON | JSONB (indexed) |
| Connections | Single | Pool (20+10) |
| Indexes | Basic | Composite + GIN |
| Foreign Keys | Basic | CASCADE/SET NULL |

## 🔧 Common Commands

### Alembic
```powershell
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Check status
alembic current
```

### PostgreSQL
```bash
# Connect
psql -U postgres -d bharat_content_ai

# List tables
\dt

# Describe table
\d users

# Backup
pg_dump -U postgres bharat_content_ai > backup.sql

# Restore
psql -U postgres bharat_content_ai < backup.sql
```

## 📈 Performance Gains

- **JSONB Indexes**: 10-100x faster JSON queries
- **Connection Pool**: Handle 30 concurrent requests
- **Composite Indexes**: 5-10x faster filtered queries
- **Async Operations**: Non-blocking I/O

## ⚠️ Important Notes

1. **Async Everywhere**: All database operations are now async
   ```python
   # Old (sync)
   db.query(User).all()
   
   # New (async)
   await db.execute(select(User))
   ```

2. **JSONB vs JSON**: Use JSONB for better performance
   ```python
   # Indexed JSONB queries
   .filter(Content.keywords.contains({"tag": "marketing"}))
   ```

3. **Connection Pool**: Configured for production
   - Pool size: 20
   - Max overflow: 10
   - Recycle: 1 hour

## 🐛 Troubleshooting

### Can't connect to PostgreSQL
```powershell
# Check if running
Get-Service postgresql*

# Start service
Start-Service postgresql-x64-14
```

### Migration fails
```powershell
# Reset database
psql -U postgres -d bharat_content_ai -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Rerun migration
alembic upgrade head
```

### Slow queries
```sql
-- Analyze tables
ANALYZE;

-- Check indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

## 📝 Production Checklist

- [ ] PostgreSQL installed and running
- [ ] Database created
- [ ] .env updated with connection string
- [ ] Dependencies installed (asyncpg)
- [ ] Migrations applied
- [ ] Application tested
- [ ] Backup strategy configured
- [ ] Monitoring setup
- [ ] AWS RDS configured (production)
- [ ] Security groups configured

## 🔗 Resources

- Full Guide: `POSTGRESQL_MIGRATION_GUIDE.md`
- Migration Script: `migrate_sqlite_to_postgres.py`
- Alembic Config: `alembic.ini`
- Database Config: `app/config/database.py`

## 💡 Pro Tips

1. **Always backup before migration**
   ```bash
   cp bharat_content_ai.db bharat_content_ai.db.backup
   ```

2. **Test locally before production**
   ```powershell
   # Use local PostgreSQL first
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
   ```

3. **Monitor connection pool**
   ```python
   print(f"Pool size: {engine.pool.size()}")
   ```

4. **Use transactions for data integrity**
   ```python
   async with session.begin():
       # Your operations here
   ```

## 🎯 Next Steps

1. ✅ Complete migration
2. ✅ Test all endpoints
3. ✅ Monitor performance
4. ✅ Setup AWS RDS for production
5. ✅ Configure automated backups
6. ✅ Setup monitoring (CloudWatch)
