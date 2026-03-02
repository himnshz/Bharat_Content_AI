# PostgreSQL Migration Checklist

Use this checklist to ensure a smooth migration from SQLite to PostgreSQL.

---

## 📋 Pre-Migration Checklist

### Backup & Safety
- [ ] Backup SQLite database file
  ```powershell
  cp bharat_content_ai.db bharat_content_ai.db.backup_$(date +%Y%m%d)
  ```
- [ ] Backup .env file
  ```powershell
  cp .env .env.backup
  ```
- [ ] Document current application state
- [ ] Test all API endpoints with SQLite (baseline)

### Environment Setup
- [ ] Install PostgreSQL
  - Windows: Download from https://www.postgresql.org/download/windows/
  - Or: `choco install postgresql`
- [ ] Verify PostgreSQL is running
  ```powershell
  Get-Service postgresql*
  ```
- [ ] Install PostgreSQL client tools (psql)
- [ ] Test PostgreSQL connection
  ```bash
  psql -U postgres
  ```

### Database Creation
- [ ] Create PostgreSQL database
  ```sql
  CREATE DATABASE bharat_content_ai;
  ```
- [ ] Create database user (optional)
  ```sql
  CREATE USER bharat_user WITH PASSWORD 'secure_password';
  GRANT ALL PRIVILEGES ON DATABASE bharat_content_ai TO bharat_user;
  ```
- [ ] Test database connection
  ```bash
  psql -U postgres -d bharat_content_ai
  ```

---

## 🔧 Migration Checklist

### Update Dependencies
- [ ] Install asyncpg
  ```powershell
  pip install asyncpg
  ```
- [ ] Verify all dependencies installed
  ```powershell
  pip install -r requirements.txt
  ```
- [ ] Check for dependency conflicts
  ```powershell
  pip check
  ```

### Update Configuration
- [ ] Update .env file with PostgreSQL URL
  ```env
  DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai
  ```
- [ ] Verify .env file syntax
- [ ] Test environment variable loading
  ```python
  from dotenv import load_dotenv
  import os
  load_dotenv()
  print(os.getenv("DATABASE_URL"))
  ```

### Initialize Alembic
- [ ] Review alembic.ini configuration
- [ ] Review alembic/env.py
- [ ] Create initial migration
  ```powershell
  alembic revision --autogenerate -m "Initial PostgreSQL migration"
  ```
- [ ] Review generated migration file
- [ ] Apply migration
  ```powershell
  alembic upgrade head
  ```

### Migrate Data (if needed)
- [ ] Review migration script
  ```powershell
  cat migrate_sqlite_to_postgres.py
  ```
- [ ] Run migration script
  ```powershell
  python migrate_sqlite_to_postgres.py
  ```
- [ ] Verify data migration
  ```sql
  SELECT COUNT(*) FROM users;
  SELECT COUNT(*) FROM contents;
  SELECT COUNT(*) FROM campaigns;
  -- ... check all tables
  ```
- [ ] Verify sequences reset
  ```sql
  SELECT last_value FROM users_id_seq;
  SELECT last_value FROM contents_id_seq;
  ```

---

## ✅ Testing Checklist

### Basic Functionality
- [ ] Start FastAPI server
  ```powershell
  uvicorn app.main:app --reload
  ```
- [ ] Access API documentation
  - Visit: http://localhost:8000/api/docs
- [ ] Test health endpoint
  - GET /api/health

### User Endpoints
- [ ] POST /api/users/register - Create user
- [ ] POST /api/users/login - Login user
- [ ] GET /api/users/me - Get current user
- [ ] PUT /api/users/me - Update user
- [ ] GET /api/users/{id} - Get user by ID

### Content Endpoints
- [ ] POST /api/content/generate - Generate content
- [ ] GET /api/content - List content
- [ ] GET /api/content/{id} - Get content by ID
- [ ] PUT /api/content/{id} - Update content
- [ ] DELETE /api/content/{id} - Delete content

### Campaign Endpoints
- [ ] POST /api/campaigns - Create campaign
- [ ] GET /api/campaigns - List campaigns
- [ ] GET /api/campaigns/{id} - Get campaign
- [ ] PUT /api/campaigns/{id} - Update campaign
- [ ] DELETE /api/campaigns/{id} - Delete campaign

### Team Endpoints
- [ ] POST /api/teams - Create team
- [ ] GET /api/teams - List teams
- [ ] POST /api/teams/{id}/members - Add member
- [ ] POST /api/teams/{id}/invites - Send invite
- [ ] GET /api/teams/{id}/activity - Get activity

### Template Endpoints
- [ ] POST /api/templates - Create template
- [ ] GET /api/templates - List templates
- [ ] GET /api/templates/{id} - Get template
- [ ] PUT /api/templates/{id} - Update template
- [ ] DELETE /api/templates/{id} - Delete template

### Performance Testing
- [ ] Test concurrent requests (10 users)
  ```python
  # Use locust or similar tool
  ```
- [ ] Test JSONB queries
  ```sql
  SELECT * FROM contents WHERE keywords @> '{"tag": "marketing"}';
  ```
- [ ] Test composite index queries
  ```sql
  SELECT * FROM contents WHERE user_id = 1 AND status = 'published';
  ```
- [ ] Monitor connection pool
  ```python
  from app.config.database import engine
  print(f"Pool size: {engine.pool.size()}")
  print(f"Checked out: {engine.pool.checkedout()}")
  ```

---

## 🔍 Verification Checklist

### Data Integrity
- [ ] Verify row counts match
  ```sql
  -- Compare SQLite vs PostgreSQL
  SELECT 'users' as table_name, COUNT(*) FROM users
  UNION ALL
  SELECT 'contents', COUNT(*) FROM contents
  UNION ALL
  SELECT 'campaigns', COUNT(*) FROM campaigns;
  ```
- [ ] Verify foreign key relationships
  ```sql
  SELECT * FROM contents WHERE user_id NOT IN (SELECT id FROM users);
  -- Should return 0 rows
  ```
- [ ] Verify enum values
  ```sql
  SELECT DISTINCT role FROM users;
  SELECT DISTINCT status FROM campaigns;
  ```
- [ ] Verify JSON/JSONB data
  ```sql
  SELECT keywords, hashtags FROM contents LIMIT 5;
  ```

### Index Verification
- [ ] Check all indexes created
  ```sql
  SELECT tablename, indexname, indexdef 
  FROM pg_indexes 
  WHERE schemaname = 'public'
  ORDER BY tablename, indexname;
  ```
- [ ] Verify GIN indexes
  ```sql
  SELECT indexname FROM pg_indexes 
  WHERE indexdef LIKE '%gin%';
  ```
- [ ] Verify composite indexes
  ```sql
  SELECT indexname FROM pg_indexes 
  WHERE indexdef LIKE '%,%';
  ```

### Performance Verification
- [ ] Run EXPLAIN ANALYZE on key queries
  ```sql
  EXPLAIN ANALYZE 
  SELECT * FROM contents 
  WHERE user_id = 1 AND status = 'published';
  ```
- [ ] Check index usage
  ```sql
  SELECT schemaname, tablename, indexname, idx_scan
  FROM pg_stat_user_indexes
  ORDER BY idx_scan DESC;
  ```
- [ ] Monitor query performance
  ```sql
  SELECT query, mean_exec_time, calls
  FROM pg_stat_statements
  ORDER BY mean_exec_time DESC
  LIMIT 10;
  ```

---

## 🚀 Production Deployment Checklist

### AWS RDS Setup
- [ ] Create RDS PostgreSQL instance
  - Instance class: db.t3.micro (or larger)
  - Storage: 20GB (or more)
  - Multi-AZ: Yes (for production)
  - Backup retention: 7 days
- [ ] Configure security group
  - Allow port 5432 from application servers
  - Restrict to specific IP ranges
- [ ] Configure parameter group
  - max_connections: 100+
  - shared_buffers: 25% of RAM
  - effective_cache_size: 75% of RAM
- [ ] Enable automated backups
- [ ] Enable encryption at rest
- [ ] Configure monitoring (CloudWatch)

### Application Deployment
- [ ] Update production .env
  ```env
  DATABASE_URL=postgresql+asyncpg://admin:password@rds-endpoint.amazonaws.com:5432/bharat_content_ai
  ```
- [ ] Deploy application to EC2/ECS
- [ ] Run Alembic migrations
  ```powershell
  alembic upgrade head
  ```
- [ ] Verify application starts
- [ ] Test all endpoints in production

### Monitoring Setup
- [ ] Configure CloudWatch alarms
  - CPU utilization > 80%
  - Database connections > 80%
  - Disk space < 20%
  - Slow queries > 1s
- [ ] Setup log aggregation
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Setup uptime monitoring

### Backup Strategy
- [ ] Configure automated backups (RDS)
- [ ] Test backup restoration
- [ ] Document backup procedures
- [ ] Setup backup monitoring
- [ ] Configure backup retention policy

---

## 📊 Post-Migration Checklist

### Performance Monitoring
- [ ] Monitor query performance (first 24 hours)
- [ ] Monitor connection pool usage
- [ ] Monitor database CPU/memory
- [ ] Monitor application response times
- [ ] Identify slow queries
- [ ] Optimize indexes if needed

### Documentation
- [ ] Update README with PostgreSQL setup
- [ ] Document migration process
- [ ] Document rollback procedures
- [ ] Update deployment guide
- [ ] Update troubleshooting guide

### Team Communication
- [ ] Notify team of migration completion
- [ ] Share migration documentation
- [ ] Conduct knowledge transfer session
- [ ] Document lessons learned
- [ ] Update runbooks

---

## 🔄 Rollback Checklist (if needed)

### Emergency Rollback
- [ ] Stop application
- [ ] Restore .env.backup
  ```powershell
  cp .env.backup .env
  ```
- [ ] Restore SQLite database
  ```powershell
  cp bharat_content_ai.db.backup bharat_content_ai.db
  ```
- [ ] Restart application
- [ ] Verify functionality
- [ ] Document rollback reason

### Planned Rollback
- [ ] Export PostgreSQL data
  ```bash
  pg_dump -U postgres bharat_content_ai > postgres_backup.sql
  ```
- [ ] Stop application
- [ ] Switch to SQLite configuration
- [ ] Restart application
- [ ] Verify functionality
- [ ] Analyze rollback reason
- [ ] Plan re-migration

---

## 📝 Notes & Observations

### Migration Date: _______________

### Team Members Involved:
- [ ] _______________
- [ ] _______________
- [ ] _______________

### Issues Encountered:
1. _______________
2. _______________
3. _______________

### Resolutions:
1. _______________
2. _______________
3. _______________

### Performance Improvements Observed:
- Query speed: _______________
- Concurrent users: _______________
- Response time: _______________

### Lessons Learned:
1. _______________
2. _______________
3. _______________

---

## ✅ Sign-off

### Development Team
- [ ] Database migration verified
- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Signed: _______________ Date: _______________

### QA Team
- [ ] Functional testing complete
- [ ] Performance testing complete
- [ ] Security testing complete
- [ ] Signed: _______________ Date: _______________

### DevOps Team
- [ ] Infrastructure configured
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Signed: _______________ Date: _______________

### Product Owner
- [ ] Migration approved
- [ ] Documentation reviewed
- [ ] Ready for production
- [ ] Signed: _______________ Date: _______________

---

## 🎉 Migration Complete!

Congratulations! Your application is now running on PostgreSQL with:
- ✅ Async database operations
- ✅ Connection pooling (30 concurrent requests)
- ✅ Optimized indexes (40+)
- ✅ JSONB support with GIN indexes
- ✅ Production-ready configuration

**Next Steps:**
1. Monitor performance for 24-48 hours
2. Optimize queries based on real usage
3. Scale resources as needed
4. Celebrate! 🎊
