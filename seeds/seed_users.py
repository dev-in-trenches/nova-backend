"""Seed script to create initial users."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal, engine
from app.db.models.user import User, UserRole
from app.db.repositories.user_repository import UserRepository
from sqlalchemy import select


def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly."""
    # Encode password to bytes
    password_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string (bcrypt format that passlib can verify)
    return hashed.decode('utf-8')


async def seed_users():
    """Seed initial users into the database."""
    async with AsyncSessionLocal() as session:
        try:
            user_repository = UserRepository(session)

            # Admin user
            admin_email = "admin@example.com"
            admin_username = "admin"
            admin_password = "admin123"  # Change this in production!

            # Check if admin already exists
            existing_admin = await user_repository.get_by_email(admin_email)
            if not existing_admin:
                # Create User instance directly to properly handle enum
                admin_user = User(
                    email=admin_email,
                    username=admin_username,
                    password_hash=hash_password(admin_password),
                    full_name="Administrator",
                    role=UserRole.ADMIN,
                    is_active=True,
                    is_admin=True,
                )
                session.add(admin_user)
                await session.flush()
                await session.refresh(admin_user)
                await session.commit()
                print(f"✓ Created admin user: {admin_username} ({admin_email})")
                print(f"  Password: {admin_password}")
            else:
                print(f"⊘ Admin user already exists: {admin_username}")

            # Normal users
            normal_users = [
                {
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "password": "user123",
                    "full_name": "John Doe",
                },
                {
                    "email": "jane.smith@example.com",
                    "username": "janesmith",
                    "password": "user123",
                    "full_name": "Jane Smith",
                },
                {
                    "email": "bob.johnson@example.com",
                    "username": "bobjohnson",
                    "password": "user123",
                    "full_name": "Bob Johnson",
                },
                {
                    "email": "alice.williams@example.com",
                    "username": "alicewilliams",
                    "password": "user123",
                    "full_name": "Alice Williams",
                },
            ]

            created_count = 0
            skipped_count = 0

            for user_data in normal_users:
                # Check if user already exists
                existing_user = await user_repository.get_by_email(user_data["email"])
                if not existing_user:
                    # Create User instance directly to properly handle enum
                    new_user = User(
                        email=user_data["email"],
                        username=user_data["username"],
                        password_hash=hash_password(user_data["password"]),
                        full_name=user_data["full_name"],
                        role=UserRole.USER,
                        is_active=True,
                        is_admin=False,
                    )
                    session.add(new_user)
                    await session.flush()
                    await session.refresh(new_user)
                    await session.commit()
                    print(
                        f"✓ Created user: {user_data['username']} ({user_data['email']})"
                    )
                    created_count += 1
                else:
                    print(f"⊘ User already exists: {user_data['username']}")
                    skipped_count += 1

            print("\n" + "=" * 50)
            print("Seeding Summary:")
            print(f"  Admin users: 1 (checked)")
            print(f"  Normal users created: {created_count}")
            print(f"  Normal users skipped: {skipped_count}")
            print("=" * 50)
            print("\nDefault passwords:")
            print("  Admin: admin123")
            print("  Users: user123")
            print("\n⚠️  WARNING: Change these passwords in production!")

        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding users: {e}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_users())
