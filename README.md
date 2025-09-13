# 🎓 Scholarship Tracker

A Django-based web application for tracking scholarships, automating description summarization, monitoring emails, and forwarding updates to WhatsApp.  
This project is designed to be built in **phases**, with each phase delivering a working milestone.

---

## 🚀 Phased Implementation Roadmap

### **Phase 1 – Core Scholarship Tracker (MVP)**
**🎯 Goal:** Build the foundation for manual scholarship entry and management.  
**Features:**
- User authentication (login/signup).
- Each user can manage their own scholarships.
- Add, edit, delete, and view scholarships.
- Custom fields (key/value) for each scholarship.
- SQLite as the default database.

✅ **Checkpoint:**  
You can add, edit, delete, and view scholarships with custom fields.

---

### **Phase 2 – AI Summarization**
**🎯 Goal:** Automatically summarize scholarship descriptions.  
**Features:**
- Integrate AI API (Groq and LangChain).
- Summarize long descriptions into bullet points.
- Show summaries under scholarship details.

✅ **Checkpoint:**  
Paste a long scholarship description → AI generates a bullet-point summary.

---

### **Phase 3 – Email Monitoring & Notifications**
**🎯 Goal:** Detect and log scholarship-related emails.  
**Features:**
- Integrate with Gmail API (OAuth).
- Email listener service with **Celery + Django beat**.
- Store emails in database (`EmailLog`).
- Show notifications in the app.

✅ **Checkpoint:**  
Scholarship-related emails appear in the app’s **notifications tab**.

---

### **Phase 4 – WhatsApp Forwarding**
**🎯 Goal:** Forward scholarship notifications to WhatsApp.  
**Features:**
- Twilio WhatsApp API integration.
- Forward detected scholarship emails as clean WhatsApp messages.
- User profile settings: add WhatsApp number & toggle forwarding.

✅ **Checkpoint:**  
Scholarship emails → forwarded directly to user’s WhatsApp.

---

### **Phase 5 – Polish & Extensions (Optional)**
**Ideas:**
- Dashboard (track applied, pending, accepted, rejected scholarships).
- File uploads (attach visa documents, receipts, etc.).
- Scraping module to auto-fetch scholarships from websites.
- Analytics: applications submitted, success rate, etc.

---

## 📊 Tracking & Testing Strategy
- **Task Management:** Trello / Jira (phases broken into tasks).
- **Milestones:** End of each phase = working demo.
- **Unit Tests:**
  - Phase 1 → Models & forms.
  - Phase 2 → AI summary function.
  - Phase 3 → Email parsing.
  - Phase 4 → WhatsApp API call.
- **Manual Testing:** Verify each feature from the UI.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Database:** SQLite (default), Mysql (production-ready)
- **AI:** Groq API / LangChain
- **Async Tasks:** Celery + Redis
- **Email Integration:** Gmail API
- **Messaging:** Twilio WhatsApp API

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/scholarship-tracker.git
cd scholarship-tracker
