"""
SQLite to PostgreSQL Migration Script
Safely migrates data from SQLite database to PostgreSQL
"""
import asyncio
import sqlite3
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Database URLs
SQLITE_URL = "sqlite:///./bharat_content_ai.db"
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai")

# Table migration order (respecting foreign key dependencies)
MIGRATION_ORDER = [
    "users",
    "contents",
    "posts",
    "translations",
    "social_accounts",
    "analytics",
    "content_performance",
    "voice_inputs",
    "ai_model_configs",
    "model_usage_logs",
    "campaigns",
    "teams",
    "team_members",
    "team_invites",
    "comments",
    "approval_workflows",
    "activity_logs",
    "templates",
]


def get_sqlite_data(table_name):
    """Extract data from SQLite database"""
    try:
        conn = sqlite3.connect("bharat_content_ai.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        data = []
        for row in rows:
            data.append(dict(row))
        
        conn.close()
        return data
    except sqlite3.OperationalError as e:
        print(f"⚠️  Table {table_name} not found in SQLite: {e}")
        return []


async def insert_postgres_data(table_name, data, session):
    """Insert data into PostgreSQL database"""
    if not data:
        print(f"  ℹ️  No data to migrate for {table_name}")
        return 0
    
    try:
        # Get column names from first row
        columns = list(data[0].keys())
        placeholders = ", ".join([f":{col}" for col in columns])
        column_names = ", ".join(columns)
        
        # Build INSERT query
        query = text(f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders})
        """)
        
        # Insert each row
        count = 0
        for row in data:
            try:
                await session.execute(query, row)
                count += 1
            except Exception as e:
                print(f"    ⚠️  Error inserting row into {table_name}: {e}")
                print(f"    Row data: {row}")
                continue
        
        await session.commit()
        return count
    
    except Exception as e:
        print(f"  ❌ Error migrating {table_name}: {e}")
        await session.rollback()
        return 0


async def migrate_table(table_name, pg_session):
    """Migrate a single table from SQLite to PostgreSQL"""
    print(f"\n📦 Migrating table: {table_name}")
    
    # Extract from SQLite
    print(f"  📤 Extracting data from SQLite...")
    data = get_sqlite_data(table_name)
    print(f"  ✓ Found {len(data)} rows")
    
    if not data:
        return
    
    # Insert into PostgreSQL
    print(f"  📥 Inserting data into PostgreSQL...")
    count = await insert_postgres_data(table_name, data, pg_session)
    print(f"  ✓ Migrated {count}/{len(data)} rows successfully")


async def reset_sequences(pg_engine):
    """Reset PostgreSQL sequences to match the max ID in each table"""
    print("\n🔄 Resetting PostgreSQL sequences...")
    
    async with pg_engine.connect() as conn:
        for table in MIGRATION_ORDER:
            try:
                # Get max ID
                result = await conn.execute(text(f"SELECT MAX(id) FROM {table}"))
                max_id = result.scalar()
                
                if max_id:
                    # Reset sequence
                    await conn.execute(text(f"SELECT setval('{table}_id_seq', {max_id}, true)"))
                    print(f"  ✓ Reset {table}_id_seq to {max_id}")
            except Exception as e:
                print(f"  ⚠️  Could not reset sequence for {table}: {e}")
        
        await conn.commit()


async def verify_migration(pg_engine):
    """Verify data was migrated correctly"""
    print("\n✅ Verifying migration...")
    
    async with pg_engine.connect() as conn:
        for table in MIGRATION_ORDER:
            try:
                result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  ✓ {table}: {count} rows")
            except Exception as e:
                print(f"  ⚠️  Could not verify {table}: {e}")


async def main():
    """Main migration function"""
    print("=" * 60)
    print("🚀 SQLite to PostgreSQL Migration")
    print("=" * 60)
    
    # Check if SQLite database exists
    if not os.path.exists("bharat_content_ai.db"):
        print("❌ SQLite database not found: bharat_content_ai.db")
        print("   Please ensure the database file exists in the current directory.")
        sys.exit(1)
    
    print(f"\n📊 Source: SQLite (bharat_content_ai.db)")
    print(f"📊 Target: PostgreSQL ({POSTGRES_URL.split('@')[1] if '@' in POSTGRES_URL else POSTGRES_URL})")
    
    # Confirm migration
    print("\n⚠️  WARNING: This will overwrite existing data in PostgreSQL!")
    response = input("Do you want to continue? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Migration cancelled.")
        sys.exit(0)
    
    # Create PostgreSQL engine and session
    pg_engine = create_async_engine(POSTGRES_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)
    
    try:
        # Create tables in PostgreSQL
        print("\n🏗️  Creating PostgreSQL tables...")
        from app.config.database import Base, init_db
        await init_db()
        print("  ✓ Tables created successfully")
        
        # Migrate each table
        async with AsyncSessionLocal() as session:
            for table in MIGRATION_ORDER:
                await migrate_table(table, session)
        
        # Reset sequences
        await reset_sequences(pg_engine)
        
        # Verify migration
        await verify_migration(pg_engine)
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("  1. Update your .env file with PostgreSQL DATABASE_URL")
        print("  2. Test the application with PostgreSQL")
        print("  3. Backup the SQLite database for safety")
        print("  4. Run: alembic revision --autogenerate -m 'Initial migration'")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        await pg_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
