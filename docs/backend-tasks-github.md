# Backend Development Tasks - GitHub Issues

**Project:** Freelance Workflow Assistant Agent - Backend  
**Deadline:** 17 Mar 2026 @ 1:00 AM

This document contains all backend tasks formatted as GitHub issues, organized in implementation order.

---

## Phase 1: Foundation & Infrastructure

### Issue #1: Backend Project Setup
**Labels:** `priority:high` `type:infrastructure` `epic:foundation`

**Description:**
Set up FastAPI backend project structure with Python 3.11, including dependency management, project structure, and basic configuration.

**Tasks:**
- Initialize FastAPI project with proper directory structure
- Set up dependency management (`requirements.txt` or `pyproject.toml`)
- Configure environment variable management (`.env` support using `pydantic-settings`)
- Create basic project structure:
  ```
  app/
    ├── api/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    ├── services/
    └── main.py
  ```
- Implement basic health check endpoint (`GET /health`)
- Add Docker configuration (Dockerfile, docker-compose.yml)
- Set up logging configuration
- Configure CORS for frontend and extension

**Acceptance Criteria:**
- ✅ FastAPI project runs locally with `uvicorn app.main:app --reload`
- ✅ Health check endpoint returns 200 OK
- ✅ Environment variables loaded from `.env` file
- ✅ Docker container builds and runs successfully
- ✅ CORS configured for Next.js dashboard and Chrome extension origins

**Dependencies:** None

---

### Issue #2: Database Setup & Configuration
**Labels:** `priority:high` `type:infrastructure` `epic:foundation`

**Description:**
Set up PostgreSQL database with Alembic migrations. Configure database connection pooling and AWS RDS connection.

**Tasks:**
- Install and configure SQLAlchemy
- Set up Alembic for database migrations
- Configure database connection (local PostgreSQL + AWS RDS)
- Implement database connection pooling
- Create database session management
- Set up database initialization script
- Configure database URL from environment variables

**Acceptance Criteria:**
- ✅ Alembic initialized and configured
- ✅ Database connection works for local PostgreSQL
- ✅ Database connection configured for AWS RDS (via env vars)
- ✅ Connection pooling implemented
- ✅ Database session dependency injection working
- ✅ Can run migrations: `alembic upgrade head`

**Dependencies:** Issue #1

---

### Issue #3: Redis Setup & Configuration
**Labels:** `priority:medium` `type:infrastructure` `epic:foundation`

**Description:**
Configure Redis for caching and session management.

**Tasks:**
- Install Redis client library (`redis` or `aioredis`)
- Configure Redis connection
- Create Redis connection utility
- Implement caching utilities (get, set, delete with TTL)
- Set up session management using Redis
- Add Redis health check

**Acceptance Criteria:**
- ✅ Redis connection configured and working
- ✅ Caching utilities implemented and tested
- ✅ Session storage using Redis
- ✅ Redis connection error handling

**Dependencies:** Issue #1

---

## Phase 2: Database Models

### Issue #4: User Model & Migration
**Labels:** `priority:high` `type:database` `epic:models`

**Description:**
Create User database model with authentication fields and profile information.

**Tasks:**
- Create User model with fields:
  - `id` (UUID, primary key)
  - `email` (unique, indexed)
  - `password_hash` (hashed password)
  - `is_active` (boolean, default True)
  - `is_admin` (boolean, default False)
  - `skills` (JSON array)
  - `experience_summary` (text)
  - `portfolio_links` (JSON array)
  - `preferred_rate` (decimal)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Create Pydantic schemas for User (Create, Read, Update)
- Create Alembic migration
- Add proper indexes and constraints

**Acceptance Criteria:**
- ✅ User model created with all required fields
- ✅ Migration file created and tested
- ✅ Email uniqueness constraint enforced
- ✅ Proper indexes on email and created_at
- ✅ Pydantic schemas for request/response validation

**Dependencies:** Issue #2

---

### Issue #5: Job Posting Model & Migration
**Labels:** `priority:high` `type:database` `epic:models`

**Description:**
Create model for storing analyzed job postings from Upwork and Freelancer.

**Tasks:**
- Create JobPosting model with fields:
  - `id` (UUID, primary key)
  - `platform` (enum: upwork, freelancer)
  - `job_title` (string)
  - `description` (text)
  - `budget` (decimal, nullable)
  - `required_skills` (JSON array)
  - `url` (string, unique)
  - `extracted_at` (timestamp)
  - `created_at` (timestamp)
- Create Pydantic schemas
- Create Alembic migration
- Add indexes for search (job_title, platform, created_at)

**Acceptance Criteria:**
- ✅ JobPosting model created
- ✅ Platform enum defined
- ✅ URL uniqueness constraint
- ✅ Migration tested
- ✅ Pydantic schemas created

**Dependencies:** Issue #2

---

### Issue #6: Job Analysis Model & Migration
**Labels:** `priority:high` `type:database` `epic:models`

**Description:**
Create model for storing job analysis results from Nova 2 Lite.

**Tasks:**
- Create JobAnalysis model with fields:
  - `id` (UUID, primary key)
  - `user_id` (foreign key to User)
  - `job_posting_id` (foreign key to JobPosting)
  - `relevance_score` (integer, 0-100)
  - `skill_match_explanation` (text)
  - `gaps_advice` (text)
  - `bid_strategy` (text)
  - `created_at` (timestamp)
- Create Pydantic schemas
- Create Alembic migration
- Add foreign key constraints and indexes

**Acceptance Criteria:**
- ✅ JobAnalysis model created
- ✅ Foreign keys properly configured
- ✅ Relevance score validation (0-100)
- ✅ Migration tested
- ✅ Pydantic schemas created

**Dependencies:** Issue #2, Issue #4, Issue #5

---

### Issue #7: Application Model & Migration
**Labels:** `priority:high` `type:database` `epic:models`

**Description:**
Create model for tracking application lifecycle (drafted, approved, submitted, interviewed, won, lost).

**Tasks:**
- Create Application model with fields:
  - `id` (UUID, primary key)
  - `user_id` (foreign key to User)
  - `job_posting_id` (foreign key to JobPosting)
  - `status` (enum: drafted, approved, submitted, interviewed, won, lost)
  - `proposal_content` (text)
  - `bid_amount` (decimal, nullable)
  - `milestones` (JSON, nullable)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
  - `submitted_at` (timestamp, nullable)
- Create ApplicationStatus enum
- Create Pydantic schemas
- Create Alembic migration
- Add indexes for filtering by status and user

**Acceptance Criteria:**
- ✅ Application model created
- ✅ Status enum defined
- ✅ Foreign keys properly configured
- ✅ Migration tested
- ✅ Pydantic schemas created

**Dependencies:** Issue #2, Issue #4, Issue #5

---

### Issue #8: Past Proposal Model & Migration
**Labels:** `priority:medium` `type:database` `epic:models`

**Description:**
Create model for storing user's past successful proposals for AI context.

**Tasks:**
- Create PastProposal model with fields:
  - `id` (UUID, primary key)
  - `user_id` (foreign key to User)
  - `title` (string)
  - `content` (text)
  - `platform` (string, nullable)
  - `outcome` (string, nullable)
  - `created_at` (timestamp)
- Create Pydantic schemas
- Create Alembic migration
- Add foreign key constraint

**Acceptance Criteria:**
- ✅ PastProposal model created
- ✅ Foreign key to User configured
- ✅ Migration tested
- ✅ Pydantic schemas created

**Dependencies:** Issue #2, Issue #4

---

## Phase 3: Authentication & Security

### Issue #9: Authentication System (JWT)
**Labels:** `priority:high` `type:feature` `epic:auth`

**Description:**
Implement user registration, login, and JWT token management with password hashing.

**Tasks:**
- Install and configure JWT library (`python-jose`)
- Install password hashing library (`passlib[bcrypt]`)
- Create password hashing utilities
- Implement user registration endpoint (`POST /api/auth/register`)
- Implement user login endpoint (`POST /api/auth/login`)
- Implement JWT token generation (access token + refresh token)
- Create JWT token validation dependency
- Implement refresh token endpoint (`POST /api/auth/refresh`)
- Add password validation rules
- Create authentication middleware/dependency

**Acceptance Criteria:**
- ✅ User can register with email and password
- ✅ Passwords are hashed using bcrypt
- ✅ User can login and receive JWT tokens
- ✅ Access tokens expire after configured time (e.g., 30 minutes)
- ✅ Refresh tokens work for token renewal
- ✅ Protected endpoints require valid JWT token
- ✅ Password validation (min length, complexity)

**Dependencies:** Issue #4

---

### Issue #10: Protected Route Decorator/Dependency
**Labels:** `priority:high` `type:feature` `epic:auth`

**Description:**
Create reusable dependency for protecting API routes that require authentication.

**Tasks:**
- Create `get_current_user` dependency
- Extract JWT token from Authorization header
- Validate token and extract user info
- Load user from database
- Handle token expiration errors
- Handle invalid token errors
- Create admin-only dependency (optional)

**Acceptance Criteria:**
- ✅ `get_current_user` dependency works
- ✅ Returns current authenticated user
- ✅ Raises 401 for invalid/expired tokens
- ✅ Can be used in route dependencies
- ✅ Admin-only routes protected

**Dependencies:** Issue #9

---

## Phase 4: LLM Integration

### Issue #11: LLM Abstraction Layer
**Labels:** `priority:high` `type:feature` `epic:ai`

**Description:**
Create vendor-agnostic LLM interface that can switch between Nova 2 Lite and other providers.

**Tasks:**
- Create abstract base class/interface for LLM providers
- Define common methods: `generate()`, `chat()`, `analyze()`
- Implement Nova 2 Lite provider class
- Create LLM configuration system (from env vars)
- Implement error handling and retry logic
- Add rate limiting consideration
- Create LLM service/factory pattern
- Add logging for LLM calls

**Acceptance Criteria:**
- ✅ Abstract LLM interface defined
- ✅ Nova 2 Lite implementation working
- ✅ Can switch providers via configuration
- ✅ Error handling and retries implemented
- ✅ Rate limiting handled gracefully
- ✅ All LLM calls logged

**Dependencies:** Issue #1

---

### Issue #12: Nova 2 Lite API Client
**Labels:** `priority:high` `type:feature` `epic:ai`

**Description:**
Integrate with Amazon Nova 2 Lite API for reasoning tasks.

**Tasks:**
- Research Nova 2 Lite API documentation
- Install required SDK/library
- Configure API authentication (API keys, region)
- Create Nova 2 Lite client class
- Implement API request/response handling
- Add error handling for API failures
- Implement response parsing
- Add timeout handling
- Test API connectivity

**Acceptance Criteria:**
- ✅ Nova 2 Lite API client implemented
- ✅ Authentication configured correctly
- ✅ Can make successful API calls
- ✅ Error handling for API failures
- ✅ Response parsing works correctly
- ✅ Timeout handling implemented

**Dependencies:** Issue #11

---

### Issue #13: Job Analysis Prompt Engineering
**Labels:** `priority:high` `type:feature` `epic:ai`

**Description:**
Design and implement prompts for job analysis using Nova 2 Lite.

**Tasks:**
- Design prompt template for job analysis
- Include user profile context in prompt
- Structure prompt to return JSON:
  - relevance_score (0-100)
  - skill_match_explanation
  - gaps_advice
  - bid_strategy
- Create prompt builder utility
- Handle edge cases (missing data, unclear requirements)
- Test with various job postings
- Iterate on prompt quality

**Acceptance Criteria:**
- ✅ Prompt template created
- ✅ Returns structured JSON response
- ✅ Handles missing job data gracefully
- ✅ Relevance scores are reasonable (0-100)
- ✅ Explanations are clear and actionable
- ✅ Tested with multiple job types

**Dependencies:** Issue #12

---

### Issue #14: Proposal Generation Prompt Engineering
**Labels:** `priority:high` `type:feature` `epic:ai`

**Description:**
Design and implement prompts for proposal generation using Nova 2 Lite.

**Tasks:**
- Design prompt template for proposal generation
- Incorporate user profile, job analysis, and past proposals
- Structure prompt to return JSON with sections:
  - opening_hook
  - problem_understanding
  - relevant_experience_alignment
  - technical_approach
  - timeline_estimate
  - cta
  - milestones (optional)
- Create prompt builder utility
- Test proposal quality and consistency
- Iterate on prompt to improve output

**Acceptance Criteria:**
- ✅ Prompt template created
- ✅ Returns structured JSON with all sections
- ✅ Proposals are personalized to user profile
- ✅ Proposals reference job requirements
- ✅ Quality is consistent across generations
- ✅ Tested with various job types

**Dependencies:** Issue #12, Issue #13

---

## Phase 5: User Profile APIs

### Issue #15: User Profile CRUD Endpoints
**Labels:** `priority:high` `type:feature` `epic:user-profile`

**Description:**
Create endpoints for user profile management including skill inventory, experience, portfolio links, and rates.

**Tasks:**
- Create `GET /api/users/me` endpoint
  - Returns current user's profile
  - Requires authentication
- Create `PUT /api/users/me` endpoint
  - Updates user profile
  - Validates all fields
  - Updates skills, experience_summary, portfolio_links, preferred_rate
- Create Pydantic schemas for request/response
- Add validation for:
  - Skills (array of strings)
  - Portfolio links (array of valid URLs)
  - Preferred rate (positive number)
- Update user model on save

**Acceptance Criteria:**
- ✅ `GET /api/users/me` returns user profile
- ✅ `PUT /api/users/me` updates profile successfully
- ✅ All fields validated properly
- ✅ Requires authentication
- ✅ Returns 404 if user not found
- ✅ Returns 400 for invalid data

**Dependencies:** Issue #9, Issue #10, Issue #4

---

### Issue #16: Past Proposals Management Endpoints
**Labels:** `priority:medium` `type:feature` `epic:user-profile`

**Description:**
Allow users to upload and manage past successful proposals for AI context.

**Tasks:**
- Create `POST /api/users/me/proposals` endpoint
  - Upload past proposal (text content)
  - Store title, content, platform, outcome
- Create `GET /api/users/me/proposals` endpoint
  - List all past proposals for user
  - Support pagination
- Create `GET /api/users/me/proposals/{id}` endpoint
  - Get specific past proposal
- Create `PUT /api/users/me/proposals/{id}` endpoint
  - Update past proposal
- Create `DELETE /api/users/me/proposals/{id}` endpoint
  - Delete past proposal
- Add file upload support (optional, for future)
- Create Pydantic schemas

**Acceptance Criteria:**
- ✅ All CRUD operations work
- ✅ Requires authentication
- ✅ Users can only access their own proposals
- ✅ Pagination works for list endpoint
- ✅ Validation for proposal content

**Dependencies:** Issue #9, Issue #10, Issue #8

---

## Phase 6: Job Analysis APIs

### Issue #17: Job Posting Storage Endpoint
**Labels:** `priority:high` `type:feature` `epic:job-analysis`

**Description:**
Create endpoint to receive and store job posting data from Chrome extension.

**Tasks:**
- Create `POST /api/jobs` endpoint
  - Accepts: platform, job_title, description, budget, required_skills, url
  - Validates all required fields
  - Checks if job already exists (by URL)
  - Creates or updates JobPosting record
  - Returns job posting ID
- Create Pydantic schemas for request/response
- Add validation for platform enum
- Handle duplicate URLs gracefully

**Acceptance Criteria:**
- ✅ Endpoint accepts job posting data
- ✅ Validates all fields
- ✅ Prevents duplicate URLs
- ✅ Returns job posting ID
- ✅ Stores extracted_at timestamp

**Dependencies:** Issue #5, Issue #10

---

### Issue #18: Job Analysis Endpoint
**Labels:** `priority:high` `type:feature` `epic:job-analysis`

**Description:**
Create endpoint that analyzes job posting and returns relevance analysis using Nova 2 Lite.

**Tasks:**
- Create `POST /api/jobs/{job_id}/analyze` endpoint
  - Accepts job_id
  - Loads job posting and current user profile
  - Calls LLM service with job analysis prompt
  - Stores analysis result in JobAnalysis table
  - Returns: relevance_score, skill_match_explanation, gaps_advice, bid_strategy
- Handle errors from LLM service
- Cache analysis results (optional, using Redis)
- Create Pydantic schemas

**Acceptance Criteria:**
- ✅ Endpoint analyzes job posting
- ✅ Returns structured analysis response
- ✅ Stores analysis in database
- ✅ Requires authentication
- ✅ Handles LLM errors gracefully
- ✅ Returns 404 if job not found

**Dependencies:** Issue #6, Issue #13, Issue #15, Issue #17

---

## Phase 7: Proposal Generation APIs

### Issue #19: Proposal Generation Endpoint
**Labels:** `priority:high` `type:feature` `epic:proposal`

**Description:**
Generate structured proposal using Nova 2 Lite based on job analysis and user profile.

**Tasks:**
- Create `POST /api/jobs/{job_id}/proposals/generate` endpoint
  - Accepts job_id
  - Loads job posting, user profile, job analysis, past proposals
  - Calls LLM service with proposal generation prompt
  - Returns structured JSON with all proposal sections
  - Does NOT save proposal (user must approve first)
- Create Pydantic schemas for proposal structure
- Handle errors from LLM service
- Add logging for proposal generation

**Acceptance Criteria:**
- ✅ Endpoint generates proposal
- ✅ Returns all required sections (hook, understanding, experience, approach, timeline, CTA)
- ✅ Proposal is personalized to user
- ✅ Requires authentication
- ✅ Handles errors gracefully
- ✅ Returns 404 if job not found

**Dependencies:** Issue #14, Issue #18

---

### Issue #20: Proposal Regeneration Endpoint
**Labels:** `priority:medium` `type:feature` `epic:proposal`

**Description:**
Allow users to regenerate specific sections of a proposal.

**Tasks:**
- Create `POST /api/jobs/{job_id}/proposals/regenerate-section` endpoint
  - Accepts job_id and section_name
  - Regenerates only the specified section
  - Returns updated section content
- Support sections: opening_hook, problem_understanding, relevant_experience, technical_approach, timeline_estimate, cta
- Maintain context from other sections

**Acceptance Criteria:**
- ✅ Can regenerate individual sections
- ✅ Maintains context from other sections
- ✅ Returns updated section only
- ✅ Requires authentication

**Dependencies:** Issue #19

---

## Phase 8: Application Tracking APIs

### Issue #21: Application CRUD Endpoints
**Labels:** `priority:high` `type:feature` `epic:tracking`

**Description:**
Create endpoints for managing application lifecycle (drafted, approved, submitted, interviewed, won, lost).

**Tasks:**
- Create `POST /api/applications` endpoint
  - Creates new application record
  - Accepts: job_posting_id, proposal_content, bid_amount, milestones, status
  - Sets status to "drafted" by default
- Create `GET /api/applications` endpoint
  - Lists user's applications
  - Supports filtering by status
  - Supports pagination
  - Supports sorting by date
- Create `GET /api/applications/{id}` endpoint
  - Returns application details
- Create `PUT /api/applications/{id}` endpoint
  - Updates application (status, proposal_content, bid_amount, etc.)
  - Updates submitted_at when status changes to "submitted"
- Create `DELETE /api/applications/{id}` endpoint
  - Deletes application
- Create Pydantic schemas
- Ensure users can only access their own applications

**Acceptance Criteria:**
- ✅ All CRUD operations work
- ✅ Filtering by status works
- ✅ Pagination works
- ✅ Users can only access their own applications
- ✅ Status updates tracked with timestamps
- ✅ Requires authentication

**Dependencies:** Issue #7, Issue #10

---

### Issue #22: Application Analytics Endpoint
**Labels:** `priority:medium` `type:feature` `epic:tracking`

**Description:**
Provide analytics metrics for user's applications.

**Tasks:**
- Create `GET /api/applications/analytics` endpoint
  - Calculates win rate (won / (won + lost))
  - Calculates average proposal generation time
  - Calculates proposal edit percentage
  - Calculates revenue impact (sum of bid_amount for won applications)
  - Supports time range filtering (start_date, end_date)
- Create Pydantic schema for analytics response
- Optimize queries for performance

**Acceptance Criteria:**
- ✅ Returns all required metrics
- ✅ Time range filtering works
- ✅ Calculations are accurate
- ✅ Performance is acceptable (< 1 second)
- ✅ Requires authentication
- ✅ Returns 0 values when no data

**Dependencies:** Issue #21

---

## Phase 9: API Documentation

### Issue #23: OpenAPI/Swagger Documentation
**Labels:** `priority:medium` `type:documentation` `epic:docs`

**Description:**
Generate comprehensive API documentation using FastAPI's built-in OpenAPI/Swagger.

**Tasks:**
- Ensure all endpoints have proper docstrings
- Add response models to all endpoints
- Add example requests/responses
- Configure Swagger UI
- Add authentication documentation
- Test all endpoints appear in docs
- Add error response documentation

**Acceptance Criteria:**
- ✅ Swagger UI accessible at `/docs`
- ✅ All endpoints documented
- ✅ Request/response examples shown
- ✅ Authentication flow documented
- ✅ Error responses documented

**Dependencies:** All API issues

---

## Phase 10: Testing

### Issue #24: Backend Unit Tests
**Labels:** `priority:medium` `type:testing` `epic:testing`

**Description:**
Write unit tests for backend API endpoints and business logic.

**Tasks:**
- Set up pytest and test configuration
- Create test fixtures (database, test client, test user)
- Write tests for authentication endpoints
- Write tests for user profile endpoints
- Write tests for job analysis endpoints
- Write tests for proposal generation endpoints
- Write tests for application tracking endpoints
- Achieve minimum 70% code coverage

**Acceptance Criteria:**
- ✅ Test suite runs successfully
- ✅ All API endpoints have tests
- ✅ Minimum 70% code coverage
- ✅ Tests use test database
- ✅ Tests are isolated and independent

**Dependencies:** All feature issues

---

### Issue #25: Database Model Tests
**Labels:** `priority:medium` `type:testing` `epic:testing`

**Description:**
Write tests for database models and relationships.

**Tasks:**
- Write tests for User model
- Write tests for JobPosting model
- Write tests for JobAnalysis model
- Write tests for Application model
- Write tests for PastProposal model
- Test foreign key relationships
- Test constraints and validations
- Test migrations

**Acceptance Criteria:**
- ✅ All models have tests
- ✅ Relationships tested
- ✅ Constraints tested
- ✅ Migrations tested

**Dependencies:** All model issues

---

## Phase 11: Deployment

### Issue #26: Backend Deployment Configuration
**Labels:** `priority:high` `type:deployment` `epic:deployment`

**Description:**
Configure backend deployment on AWS EC2 or ECS.

**Tasks:**
- Create production Dockerfile
- Configure environment variables for production
- Set up AWS deployment (EC2 or ECS)
- Configure health check endpoints
- Set up logging (CloudWatch or similar)
- Configure SSL/TLS
- Set up monitoring and alerts
- Create deployment documentation

**Acceptance Criteria:**
- ✅ Backend deployed on AWS
- ✅ Health checks working
- ✅ Logging configured
- ✅ SSL/TLS enabled
- ✅ Environment variables secure
- ✅ Monitoring in place

**Dependencies:** All backend issues

---

### Issue #27: Database Migration Strategy
**Labels:** `priority:high` `type:deployment` `epic:deployment`

**Description:**
Set up automated database migrations for production.

**Tasks:**
- Create migration scripts for production
- Set up migration automation
- Document rollback procedures
- Set up database backup strategy
- Test migrations on staging environment
- Create migration runbook

**Acceptance Criteria:**
- ✅ Migrations can run automatically
- ✅ Rollback procedures documented
- ✅ Backups configured
- ✅ Tested on staging

**Dependencies:** Issue #26

---

## Summary

**Total Backend Issues:** 27  
**High Priority:** 18  
**Medium Priority:** 9

**Implementation Order:**
1. **Foundation (Issues #1-3):** Project setup, database, Redis
2. **Models (Issues #4-8):** All database models
3. **Authentication (Issues #9-10):** JWT auth system
4. **LLM Integration (Issues #11-14):** AI/LLM abstraction and prompts
5. **User APIs (Issues #15-16):** Profile management
6. **Job Analysis (Issues #17-18):** Job posting and analysis
7. **Proposal Generation (Issues #19-20):** Proposal creation
8. **Application Tracking (Issues #21-22):** CRUD and analytics
9. **Documentation (Issue #23):** API docs
10. **Testing (Issues #24-25):** Unit tests
11. **Deployment (Issues #26-27):** Production deployment

**Critical Path:**
Issues #1 → #2 → #4 → #9 → #11 → #12 → #13 → #18 → #19 → #21

**Estimated Timeline:**
- Phase 1-2 (Foundation & Models): 3-4 days
- Phase 3-4 (Auth & LLM): 4-5 days
- Phase 5-8 (APIs): 5-6 days
- Phase 9-11 (Docs, Testing, Deployment): 3-4 days
- **Total: ~15-19 days**
