# Seed Scripts

This folder contains database seeding scripts to populate the database with initial data.

## Usage

### Seed Users

To seed the database with initial users (1 admin + 4 normal users):

```bash
python seeds/seed_users.py
```

Or from the project root:

```bash
python -m seeds.seed_users
```

## Default Credentials

**Admin User:**
- Email: `admin@example.com`
- Username: `admin`
- Password: `admin123`

**Normal Users:**
- All users have password: `user123`
- Users:
  1. `johndoe` - john.doe@example.com
  2. `janesmith` - jane.smith@example.com
  3. `bobjohnson` - bob.johnson@example.com
  4. `alicewilliams` - alice.williams@example.com

⚠️ **WARNING:** These are default passwords for development only. Change them in production!

## Notes

- The script checks for existing users and won't create duplicates
- If a user already exists, it will be skipped
- The script uses the same repository pattern as the main application
- Passwords are properly hashed using bcrypt
