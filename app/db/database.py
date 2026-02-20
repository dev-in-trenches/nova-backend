"""Database connection and session management."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database (create tables and admin user)."""
    # Import models here to avoid circular import
    from app.db.models.user import User, UserRole

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create admin user if credentials are provided
    if settings.ADMIN_EMAIL and settings.ADMIN_USERNAME and settings.ADMIN_PASSWORD:
        # Import here to avoid circular import
        from app.core.security import get_password_hash

        async with AsyncSessionLocal() as session:
            try:
                # Check if admin user already exists
                result = await session.execute(
                    select(User).where(
                        (User.email == settings.ADMIN_EMAIL)
                        | (User.username == settings.ADMIN_USERNAME)
                        | (User.role == UserRole.ADMIN)
                    )
                )
                existing_admin = result.scalar_one_or_none()

                if not existing_admin:
                    # Create admin user
                    admin_user = User(
                        email=settings.ADMIN_EMAIL,
                        username=settings.ADMIN_USERNAME,
                        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                        full_name=settings.ADMIN_FULL_NAME,
                        role=UserRole.ADMIN,
                        is_active=True,
                        is_superuser=True,
                    )

                    session.add(admin_user)
                    await session.commit()
                    logger.info(f"Admin user created: {settings.ADMIN_USERNAME}")
                else:
                    # Update existing admin if needed
                    if existing_admin.role != UserRole.ADMIN:
                        existing_admin.role = UserRole.ADMIN
                        existing_admin.is_superuser = True
                        await session.commit()
                        logger.info(
                            f"Existing user promoted to admin: {existing_admin.username}"
                        )
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
                await session.rollback()
