# PROJECT TICKETS

**Project:** Freelance Workflow Assistant Agent  
**Deadline:** 17 Mar 2026 @ 1:00 AM

---

## Infrastructure & Setup

### INFRA-001: Backend Project Setup
**Priority:** High  
**Status:** Pending  
**Description:** Set up FastAPI backend project structure with Python 3.11, including dependency management, project structure, and basic configuration.

**Acceptance Criteria:**
- FastAPI project initialized with proper structure
- `requirements.txt` or `pyproject.toml` with dependencies
- Environment configuration system (`.env` support)
- Basic health check endpoint
- Docker configuration (optional but recommended)

---

### INFRA-002: Database Setup
**Priority:** High  
**Status:** Pending  
**Description:** Set up PostgreSQL database schema with Alembic migrations. Configure AWS RDS connection.

**Acceptance Criteria:**
- PostgreSQL database configured (local dev + AWS RDS)
- Alembic initialized and configured
- Database connection pooling implemented
- Migration system working

---

### INFRA-003: Redis Setup
**Priority:** Medium  
**Status:** Pending  
**Description:** Configure Redis for caching and session management.

**Acceptance Criteria:**
- Redis connection configured
- Caching utilities implemented
- Session management using Redis

---

### INFRA-004: Next.js Dashboard Project Setup
**Priority:** High  
**Status:** Pending  
**Description:** Initialize Next.js project for user and admin dashboard, configured for Vercel deployment.

**Acceptance Criteria:**
- Next.js project initialized
- TypeScript configured
- Tailwind CSS or similar styling framework
- Vercel deployment configuration
- Environment variables setup

---

### INFRA-005: Chrome Extension Project Setup
**Priority:** High  
**Status:** Pending  
**Description:** Initialize Chrome extension project with manifest v3, content scripts, and background worker.

**Acceptance Criteria:**
- Chrome extension manifest.json configured
- Content script structure
- Background worker setup
- Build configuration

---

## Backend API - Authentication & User Management

### API-001: User Registration & Authentication
**Priority:** High  
**Status:** Pending  
**Description:** Implement user registration, login, and JWT token management.

**Acceptance Criteria:**
- User registration endpoint (`POST /api/auth/register`)
- User login endpoint (`POST /api/auth/login`)
- JWT token generation and validation
- Password hashing (bcrypt)
- Refresh token mechanism

---

### API-002: User Profile CRUD
**Priority:** High  
**Status:** Pending  
**Description:** Create endpoints for user profile management including skill inventory, experience, portfolio links, and rates.

**Acceptance Criteria:**
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- Profile includes: skills, experience summary, portfolio links, preferred rates
- Validation for all fields

---

### API-003: Past Proposals Upload
**Priority:** Medium  
**Status:** Pending  
**Description:** Allow users to upload past successful proposals for AI context.

**Acceptance Criteria:**
- `POST /api/users/me/proposals` - Upload past proposal
- `GET /api/users/me/proposals` - List past proposals
- `DELETE /api/users/me/proposals/{id}` - Delete proposal
- File storage (S3 or local)

---

## Backend API - Job Analysis

### API-004: Job Analysis Endpoint
**Priority:** High  
**Status:** Pending  
**Description:** Create endpoint that receives job posting data and returns relevance analysis using Nova 2 Lite.

**Acceptance Criteria:**
- `POST /api/jobs/analyze` - Analyze job posting
- Accepts: job title, description, budget, required skills
- Returns: relevance score (0-100), skill match explanation, gaps & positioning advice, suggested bid strategy
- Integrates with Nova 2 Lite

---

### API-005: Proposal Generation Endpoint
**Priority:** High  
**Status:** Pending  
**Description:** Generate structured proposal using Nova 2 Lite based on job analysis and user profile.

**Acceptance Criteria:**
- `POST /api/jobs/{job_id}/proposals/generate` - Generate proposal
- Returns structured JSON with: opening hook, problem understanding, relevant experience alignment, technical approach, timeline estimate, CTA, optional milestone structure
- Uses user profile and past proposals as context

---

## Backend API - Application Tracking

### API-006: Application CRUD
**Priority:** High  
**Status:** Pending  
**Description:** Create endpoints for managing application lifecycle (drafted, approved, submitted, interviewed, won, lost).

**Acceptance Criteria:**
- `POST /api/applications` - Create application record
- `GET /api/applications` - List user's applications with filters
- `GET /api/applications/{id}` - Get application details
- `PUT /api/applications/{id}` - Update application status
- `DELETE /api/applications/{id}` - Delete application

---

### API-007: Application Analytics Endpoint
**Priority:** Medium  
**Status:** Pending  
**Description:** Provide analytics metrics for user's applications.

**Acceptance Criteria:**
- `GET /api/applications/analytics` - Get analytics
- Returns: win rate, avg proposal generation time, proposal edit percentage, revenue impact
- Time range filtering support

---

## Database Models

### DB-001: User Model
**Priority:** High  
**Status:** Pending  
**Description:** Create User model with authentication fields and profile information.

**Acceptance Criteria:**
- User table with: id, email, password_hash, created_at, updated_at
- Profile fields: skills (JSON/array), experience_summary, portfolio_links (JSON), preferred_rate
- Proper indexes and constraints

---

### DB-002: Past Proposal Model
**Priority:** Medium  
**Status:** Pending  
**Description:** Create model for storing user's past successful proposals.

**Acceptance Criteria:**
- PastProposal table with: id, user_id, title, content, platform, outcome, created_at
- Foreign key to User
- File storage reference if applicable

---

### DB-003: Job Posting Model
**Priority:** High  
**Status:** Pending  
**Description:** Create model for storing analyzed job postings.

**Acceptance Criteria:**
- JobPosting table with: id, platform, job_title, description, budget, required_skills (JSON), url, extracted_at
- Indexes for search

---

### DB-004: Application Model
**Priority:** High  
**Status:** Pending  
**Description:** Create model for tracking application lifecycle.

**Acceptance Criteria:**
- Application table with: id, user_id, job_posting_id, status (enum), proposal_content, bid_amount, milestones (JSON), created_at, updated_at, submitted_at
- Status enum: drafted, approved, submitted, interviewed, won, lost
- Foreign keys to User and JobPosting

---

### DB-005: Job Analysis Model
**Priority:** High  
**Status:** Pending  
**Description:** Create model for storing job analysis results.

**Acceptance Criteria:**
- JobAnalysis table with: id, user_id, job_posting_id, relevance_score, skill_match_explanation, gaps_advice, bid_strategy, created_at
- Foreign keys to User and JobPosting

---

## AI/LLM Integration

### AI-001: LLM Abstraction Layer
**Priority:** High  
**Status:** Pending  
**Description:** Create vendor-agnostic LLM interface that can switch between Nova 2 Lite and other providers.

**Acceptance Criteria:**
- Abstract LLM interface/class
- Nova 2 Lite implementation
- Configuration for switching providers
- Error handling and retry logic

---

### AI-002: Job Analysis Prompt Engineering
**Priority:** High  
**Status:** Pending  
**Description:** Design and implement prompts for job analysis using Nova 2 Lite.

**Acceptance Criteria:**
- Prompt template for job analysis
- Returns structured JSON: relevance score, skill match, gaps, bid strategy
- Handles edge cases (missing data, unclear requirements)

---

### AI-003: Proposal Generation Prompt Engineering
**Priority:** High  
**Status:** Pending  
**Description:** Design and implement prompts for proposal generation using Nova 2 Lite.

**Acceptance Criteria:**
- Prompt template incorporating user profile, job analysis, past proposals
- Returns structured JSON with all required sections
- Consistent formatting and quality

---

### AI-004: Nova 2 Lite API Integration
**Priority:** High  
**Status:** Pending  
**Description:** Integrate with Amazon Nova 2 Lite API for reasoning tasks.

**Acceptance Criteria:**
- API client for Nova 2 Lite
- Authentication configured
- Error handling
- Rate limiting consideration
- Response parsing

---

### AI-005: Nova Multimodal Embeddings (Optional)
**Priority:** Low  
**Status:** Pending  
**Description:** Implement skill similarity and job clustering using Nova Multimodal Embeddings.

**Acceptance Criteria:**
- Embedding generation for skills and jobs
- Similarity calculation
- Job clustering functionality
- Integration with job matching

---

## Chrome Extension

### EXT-001: Platform Detection
**Priority:** High  
**Status:** Pending  
**Description:** Detect when user is on Upwork or Freelancer job posting pages.

**Acceptance Criteria:**
- Content script runs on Upwork job pages
- Content script runs on Freelancer job pages
- Platform identification logic

---

### EXT-002: Job Data Extraction
**Priority:** High  
**Status:** Pending  
**Description:** Extract job title, description, budget, and required skills from job posting pages.

**Acceptance Criteria:**
- Extract job title
- Extract job description
- Extract budget/rate information
- Extract required skills
- Handle different page layouts
- Error handling for missing data

---

### EXT-003: Extension UI Overlay
**Priority:** High  
**Status:** Pending  
**Description:** Create overlay UI that displays "Analyze Job" and "Generate Proposal" buttons.

**Acceptance Criteria:**
- Overlay appears on job pages
- "Analyze Job" button
- "Generate Proposal" button (after analysis)
- Styling matches platform aesthetics
- Non-intrusive positioning

---

### EXT-004: Job Analysis Display
**Priority:** High  
**Status:** Pending  
**Description:** Display job analysis results (relevance score, match explanation, advice) in extension overlay.

**Acceptance Criteria:**
- Display relevance score (0-100)
- Display skill match explanation
- Display gaps & positioning advice
- Display suggested bid strategy
- Clean, readable UI

---

### EXT-005: Proposal Display & Editing
**Priority:** High  
**Status:** Pending  
**Description:** Display generated proposal in editable format within extension overlay.

**Acceptance Criteria:**
- Display proposal sections (hook, understanding, experience, approach, timeline, CTA)
- Inline editing capability
- Section-by-section regeneration
- Save draft functionality

---

### EXT-006: Proposal Autofill
**Priority:** High  
**Status:** Pending  
**Description:** Autofill proposal content, bid, and milestones into platform form fields after user approval.

**Acceptance Criteria:**
- Insert proposal text into platform proposal field
- Insert bid amount into bid field
- Insert milestones if platform supports
- Never auto-submit (user must click submit manually)
- Works on both Upwork and Freelancer

---

### EXT-007: Extension-Backend Communication
**Priority:** High  
**Status:** Pending  
**Description:** Implement secure communication between extension and backend API.

**Acceptance Criteria:**
- API client in extension
- Authentication token management
- Error handling and retry logic
- Secure API endpoints

---

### EXT-008: Extension State Management
**Priority:** Medium  
**Status:** Pending  
**Description:** Manage extension state (current job, analysis results, proposal drafts) using Chrome storage.

**Acceptance Criteria:**
- Store current job data
- Store analysis results
- Store proposal drafts
- Sync with backend when online

---

## Next.js Dashboard - User Features

### DASH-001: User Authentication Pages
**Priority:** High  
**Status:** Pending  
**Description:** Create login and registration pages for users.

**Acceptance Criteria:**
- Login page (`/login`)
- Registration page (`/register`)
- Form validation
- Error handling
- Redirect after authentication

---

### DASH-002: User Profile Setup Page
**Priority:** High  
**Status:** Pending  
**Description:** Create profile setup/editing page for skills, experience, portfolio, and rates.

**Acceptance Criteria:**
- Profile form with all fields
- Skill inventory (add/remove skills)
- Experience summary (textarea)
- Portfolio links (multiple URLs)
- Preferred rates input
- Save functionality
- Validation

---

### DASH-003: Past Proposals Management
**Priority:** Medium  
**Status:** Pending  
**Description:** Allow users to upload and manage past successful proposals.

**Acceptance Criteria:**
- Upload past proposal (text or file)
- List past proposals
- Edit/delete past proposals
- Display in table/list view

---

### DASH-004: Application Tracking Dashboard
**Priority:** High  
**Status:** Pending  
**Description:** Display all applications with status tracking and filtering.

**Acceptance Criteria:**
- List all applications
- Filter by status (drafted, approved, submitted, interviewed, won, lost)
- Sort by date, status
- View application details
- Update application status
- Delete applications

---

### DASH-005: Application Analytics Dashboard
**Priority:** Medium  
**Status:** Pending  
**Description:** Display analytics metrics (win rate, avg time, edit percentage, revenue).

**Acceptance Criteria:**
- Win rate visualization (chart/gauge)
- Average proposal generation time
- Proposal edit percentage
- Revenue impact calculation
- Time range selector
- Visual charts/graphs

---

### DASH-006: Proposal Editor (Dashboard)
**Priority:** Medium  
**Status:** Pending  
**Description:** Allow users to view and edit proposals in the dashboard.

**Acceptance Criteria:**
- Display proposal sections
- Edit proposal content
- Regenerate specific sections
- Save as draft
- Approve proposal
- Copy to clipboard

---

## Next.js Dashboard - Admin Features

### ADMIN-001: Admin Authentication
**Priority:** Medium  
**Status:** Pending  
**Description:** Implement admin authentication and role-based access control.

**Acceptance Criteria:**
- Admin login
- Role-based access (admin vs user)
- Protected admin routes
- Admin dashboard access

---

### ADMIN-002: Admin Dashboard
**Priority:** Low  
**Status:** Pending  
**Description:** Create admin dashboard for system monitoring and user management.

**Acceptance Criteria:**
- User management (view, disable users)
- System metrics
- Usage statistics
- Error logs view

---

## Testing

### TEST-001: Backend Unit Tests
**Priority:** Medium  
**Status:** Pending  
**Description:** Write unit tests for backend API endpoints and business logic.

**Acceptance Criteria:**
- Test coverage for all API endpoints
- Test authentication logic
- Test job analysis logic
- Test proposal generation logic
- Minimum 70% coverage

---

### TEST-002: Database Model Tests
**Priority:** Medium  
**Status:** Pending  
**Description:** Write tests for database models and relationships.

**Acceptance Criteria:**
- Test all models
- Test relationships
- Test constraints
- Test migrations

---

### TEST-003: Extension Integration Tests
**Priority:** Medium  
**Status:** Pending  
**Description:** Test extension functionality on Upwork and Freelancer pages.

**Acceptance Criteria:**
- Test platform detection
- Test data extraction
- Test UI overlay
- Test autofill functionality
- Test on both platforms

---

### TEST-004: End-to-End Tests
**Priority:** Low  
**Status:** Pending  
**Description:** Create end-to-end tests for complete user flows.

**Acceptance Criteria:**
- Test complete job analysis flow
- Test proposal generation flow
- Test application tracking flow
- Automated E2E tests

---

## Deployment & DevOps

### DEPLOY-001: Backend Deployment Configuration
**Priority:** High  
**Status:** Pending  
**Description:** Configure backend deployment on AWS EC2 or ECS.

**Acceptance Criteria:**
- Docker containerization
- AWS deployment configuration
- Environment variables setup
- Health check endpoints
- Logging configuration

---

### DEPLOY-002: Database Migration Strategy
**Priority:** High  
**Status:** Pending  
**Description:** Set up automated database migrations for production.

**Acceptance Criteria:**
- Alembic migration scripts
- Migration strategy for production
- Rollback procedures
- Database backup strategy

---

### DEPLOY-003: Frontend Deployment
**Priority:** High  
**Status:** Pending  
**Description:** Deploy Next.js dashboard to Vercel.

**Acceptance Criteria:**
- Vercel project configured
- Environment variables set
- Custom domain (if needed)
- CI/CD pipeline

---

### DEPLOY-004: Extension Distribution
**Priority:** Medium  
**Status:** Pending  
**Description:** Prepare Chrome extension for distribution (Chrome Web Store or manual distribution).

**Acceptance Criteria:**
- Extension packaged
- Manifest validated
- Store listing prepared (if applicable)
- Distribution instructions

---

## Documentation

### DOC-001: API Documentation
**Priority:** Medium  
**Status:** Pending  
**Description:** Generate comprehensive API documentation.

**Acceptance Criteria:**
- OpenAPI/Swagger documentation
- All endpoints documented
- Request/response examples
- Authentication guide

---

### DOC-002: User Guide
**Priority:** Low  
**Status:** Pending  
**Description:** Create user guide for dashboard and extension usage.

**Acceptance Criteria:**
- Setup instructions
- Feature walkthrough
- Troubleshooting guide
- FAQ section

---

### DOC-003: Developer Setup Guide
**Priority:** Medium  
**Status:** Pending  
**Description:** Create developer setup and contribution guide.

**Acceptance Criteria:**
- Local development setup
- Environment configuration
- Database setup
- Running tests
- Contribution guidelines

---

## Demo Preparation

### DEMO-001: Demo Script & Flow
**Priority:** High  
**Status:** Pending  
**Description:** Prepare demo script showcasing complete user flow for hackathon presentation.

**Acceptance Criteria:**
- Demo script written
- All demo features working
- Smooth flow from job browsing to proposal submission
- Highlight Nova 2 Lite reasoning capabilities
- Backup plan for any failures

---

### DEMO-002: Demo Video Recording
**Priority:** High  
**Status:** Pending  
**Description:** Record demo video showing the complete workflow.

**Acceptance Criteria:**
- High-quality video recording
- Clear narration
- Shows all key features
- Under 5 minutes
- Professional presentation

---

## Summary

**Total Tickets:** 50  
**High Priority:** 28  
**Medium Priority:** 17  
**Low Priority:** 5

**Key Milestones:**
1. Infrastructure setup (INFRA-001 to INFRA-005)
2. Core backend APIs (API-001 to API-007)
3. Database models (DB-001 to DB-005)
4. AI integration (AI-001 to AI-004)
5. Chrome extension (EXT-001 to EXT-008)
6. Dashboard development (DASH-001 to DASH-006)
7. Testing and deployment
8. Demo preparation
