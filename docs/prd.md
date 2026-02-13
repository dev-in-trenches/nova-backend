# PRODUCT REQUIREMENTS DOCUMENT

**Project Name:** Freelance Workflow Assistant Agent  
**Deadline:** 17 Mar 2026 @ 1:00 AM

## 1. Executive Summary

It is an AI-powered freelance proposal copilot that integrates directly into freelance platforms via a browser extension. It analyzes job postings in real time, matches them against a freelancer's skills, generates highly personalized proposals using Amazon Nova 2 Lite, and assists with application preparation, while keeping the user fully in control of submission.

This system reduces proposal drafting time, increases personalization quality at scale, and improves application success rates through intelligent reasoning.

## 2. Core Objectives

- Reduce proposal creation time by 70%
- Increase proposal relevance and personalization
- Keep human approval mandatory
- Demonstrate advanced agentic reasoning using Nova 2 Lite
- Deliver stable, compliant integration with freelance platforms

## 3. Confirmed Architecture

### Frontend
- **Next.js** (Dashboard) hosted on Vercel. For both user and admin
- **Chrome Extension** (Content script + background worker)

### Backend
- Python 3.11
- FastAPI
- PostgreSQL (AWS RDS)
- Redis
- Deployed on AWS EC2 or ECS

### AI Layer
- **Nova 2 Lite** → Core reasoning engine
- Optional: Nova Multimodal Embeddings (skill similarity & job clustering)
- Abstracted LLM interface for vendor flexibility so we can switch to other AI vendors afterwards

## 4. Feature List (MVP Scope)

### 4.1 User Profile Setup
- Skill inventory
- Experience summary
- Portfolio links
- Preferred rates
- Past successful proposals (optional upload)

### 4.2 Browser Extension (Assistive Layer)

When user opens a job post:
- Detect platform (Upwork / Freelancer)
- Extract:
  - Job title
  - Description
  - Budget
  - Required skills
- Send structured payload to backend
- Display "Generate Proposal" button
- Autofill proposal field after approval
- Never auto-submit

### 4.3 Job Analysis Engine (Nova 2 Lite)

System generates:
- Relevance score (0–100)
- Skill match explanation
- Gaps & positioning advice
- Suggested bid strategy

### 4.4 Proposal Generation Engine

Nova produces structured JSON:
- Opening hook
- Problem understanding
- Relevant experience alignment
- Technical approach
- Timeline estimate
- CTA
- Optional milestone structure

Output editable in dashboard or extension overlay.

### 4.5 Human-in-the-Loop Approval

User can:
- Edit proposal inline
- Regenerate specific sections
- Approve proposal
- Copy or autofill into platform
- Manually click submit

### 4.6 Application Tracking Dashboard

**Track:**
- Drafted
- Approved
- Submitted
- Interviewed
- Won
- Lost

**Metrics:**
- Win rate
- Avg proposal generation time
- Proposal edit percentage
- Revenue impact

## 5. User Flow

### Step 1: Account Setup

**User:**
- Creates account
- Fills skill profile
- Sets preferred rate

**System:**
- Stores structured profile
- Prepares AI context

### Step 2: Browsing Jobs

**User:**
- Opens Upwork or Freelancer job page

**Extension:**
- Detects job
- Extracts data
- Shows "Analyze Job" button

### Step 3: Job Analysis

User clicks Analyze.

**Backend:**
- Sends job + profile to Nova 2 Lite
- Returns:
  - Relevance score
  - Match reasoning
  - Strategy notes
- Displayed in overlay.

### Step 4: Proposal Generation

User clicks Generate Proposal.

**Backend:**
- Sends structured reasoning prompt to Nova
- Returns JSON proposal sections
- Displayed in editable UI.

### Step 5: Human Approval

**User:**
- Edits content
- Adjusts bid
- Clicks Approve

### Step 6: Autofill

**Extension:**
- Inserts proposal into platform form
- Inserts bid
- Inserts milestones if supported

User manually clicks Submit.

### Step 7: Tracking

- System logs application as Submitted.
- User updates status later.
- Dashboard updates analytics.

## 6. System Strengths

- Clean separation of reasoning and execution
- Vendor-agnostic LLM architecture
- Human-in-the-loop control
- Compliant assistive positioning
- Stable demo path (manual paste fallback possible)

## 7. Demo Flow

This is the flow we are aiming for. We will show this in the demo video.

## 8. Application Positioning

This system is:

> "An AI Workflow Assistant that augments freelancer intelligence, not an automation bot."

This framing:
- Reduces compliance risk
- Increases judge trust
- Emphasizes Nova reasoning depth
- Highlights real economic value
