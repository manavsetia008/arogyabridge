# ArogyaBridge — Bridge to Healthcare

**SIH 2026 | Problem Statement ID: 26133**
**Organization:** Government of Maharashtra
**Department:** Maharashtra State Innovation Society, Department of Skills, Employment, Entrepreneurship and Innovation
**Category:** Software · **Theme:** MedTech / BioTech / HealthTech

---

## Table of Contents
1. [The Problem We're Solving](#1-the-problem-were-solving)
2. [Why This Problem — The Real-World Connection](#2-why-this-problem--the-real-world-connection)
3. [Our Approach — What We're Building](#3-our-approach--what-were-building)
4. [Minimum Requirements](#4-minimum-requirements--what-the-problem-statement-and-basic-prototype-logic-demand)
5. [What We Currently Have — Minimum Met, Plus Key Features](#5-what-we-currently-have--minimum-met-plus-key-features)
6. [How This Differs From Existing Solutions](#6-how-this-differs-from-existing-solutions)
7. [What's Unique to ArogyaBridge](#7-whats-unique-to-arogyabridge)
8. [Current Prototype — Full Feature List](#8-current-prototype--full-feature-list)
9. [Planned Integrations — APIs We Are Not Connecting Yet](#9-planned-integrations--apis-we-are-not-connecting-yet)
10. [Known Issues — Queued for the Next Update](#10-known-issues--queued-for-the-next-update)
11. [Roadmap — What's Planned Next](#11-roadmap--whats-planned-next)

---

## 1. The Problem We're Solving

**Problem Statement Title:** *Accessibility and quality of public healthcare services, particularly in rural and underserved areas.*

In plain terms: people in rural and underserved parts of Maharashtra (and India broadly) don't get timely, continuous, or accountable healthcare — not because the public health system doesn't exist, but because it's **fragmented**. The official problem description names the pain points precisely:

- Long travel distances to reach a doctor or specialist
- Shortage of specialists at the facility level people can actually reach
- Irregular diagnostics — tests aren't always available or trackable
- Fragmented medical records — a patient's history doesn't travel with them between a Sub-Centre, a PHC, a rural hospital, and a district hospital
- Delayed referrals — a patient sent from one facility to another can simply get lost in the handoff
- Limited awareness of what services even exist and where
- Constrained staff and equipment at primary facilities
- Connectivity, language, health literacy, and affordability barriers on top of all of this

The problem statement is explicit that the goal is **not** to route around the public health system, but to **strengthen it** — the ASHA worker, the PHC doctor, and the district administrator all stay exactly who they are; the system just gives them a shared, connected way of working instead of paper registers and phone calls that don't survive a handoff between facilities.

---

## 2. Why This Problem — The Real-World Connection

This isn't an abstract case study. India's public health delivery for rural areas already runs on a real, functioning human network — ASHA (Accredited Social Health Activist) and ANM (Auxiliary Nurse Midwife) workers who are the first point of contact for most rural households, backed by a tiered facility structure (Sub-Centre → PHC → Rural/District Hospital). The problem isn't that this network doesn't work — it's that **it works on paper, phone calls, and word of mouth**, so:

- A referral from a Sub-Centre to a District Hospital has no guarantee the patient actually arrives, or that the receiving doctor sees the same history the ASHA worker recorded.
- A patient with a chronic or high-risk condition depends entirely on a human ASHA worker remembering to follow up, with nothing to prompt her if she doesn't.
- A patient traveling to a facility has no way to know if the medicine they need, or the specialist they want, is even available there that day.
- None of this is visible to a district administrator until it's already a crisis (an outbreak, a stockout, an unresolved emergency).

We chose this problem because it sits exactly at the intersection of **real infrastructure that already exists** (ASHA workers, PHCs, district hospitals) and **a genuinely solvable software gap** (continuity of information across that infrastructure) — which is a better fit for a hackathon-timeline software solution than trying to build new medical infrastructure from scratch.

---

## 3. Our Approach — What We're Building

**ArogyaBridge** is a single, role-based web platform (built with Python/Streamlit + SQLite, designed to scale to a proper backend/DB in production) that connects five kinds of users around one shared, longitudinal patient record:

| Role | What they do on the platform |
|---|---|
| **Patient** | Self-register with Aadhaar, book appointments, run a self symptom-check, trigger Emergency SOS, get a walk-in queue token, view their own health record |
| **ASHA / ANM Worker** | Register patients in the field, run AI-assisted triage, refer to a facility, track high-risk follow-ups |
| **Doctor** | See a priority-sorted queue at their facility, order diagnostics, write prescriptions, manage appointments, respond to SOS alerts |
| **Facility / Hospital** | Registers itself once, then issues verified login credentials to its own ASHA workers and doctors, manages medicine stock |
| **District Admin** | Sees facility-wise and village-wise analytics, active emergencies, quality scorecards, and system-wide alerts |

The core design principle: **every patient has exactly one identity (Aadhaar-linked), and every action taken on their behalf — triage, referral, prescription, diagnostic, SOS — writes to that one record**, regardless of which ASHA worker, which facility, or which doctor touched it. That's what turns a collection of separate transactions into actual continuity of care.

---

## 4. Minimum Requirements — What the Problem Statement (and Basic Prototype Logic) Demand

Reading the SIH "Expected Solution / Outcome" text closely, an integrated solution *must* combine:

1. Assisted teleconsultation
2. Appointment and queue management
3. Digital triage
4. Longitudinal patient records
5. Referral tracking
6. Diagnostic coordination
7. Medicine availability visibility
8. High-risk patient follow-up
9. Facility dashboards
10. Support for frontline health workers
11. Low-connectivity environment support
12. Multilingual interaction
13. Emergency escalation
14. Interoperable health records based on approved standards

On top of that, basic prototype logic demands the un-glamorous but non-negotiable plumbing: real authentication (not everyone editing everyone else's data), duplicate-registration prevention, role separation, and a persistent data layer — none of which are explicitly named in the problem statement but without which nothing above actually works safely.

---

## 5. What We Currently Have — Minimum Met, Plus Key Features

### The minimum, met:
- ✅ **Digital triage** — rule-based (with optional Groq/Llama 3.1 LLM) classification into RED / YELLOW / GREEN, plus automatic department suggestion and vitals-aware escalation (abnormal temperature/SpO₂/pulse flagged automatically)
- ✅ **Longitudinal patient records** — every triage, referral, prescription, and diagnostic is tied to one Aadhaar-linked patient ID for life
- ✅ **Referral tracking** — referrals move from creation to completion with the prescribing doctor and facility recorded
- ✅ **Diagnostic coordination** — doctors order tests from a facility's queue, track them as Ordered → Completed with result notes
- ✅ **Medicine availability** — public, searchable, facility-wise stock visibility with a full change log
- ✅ **High-risk patient follow-up** — RED/YELLOW triages get an automatic follow-up due date and an ASHA worklist
- ✅ **Facility dashboards** — a dedicated Facility/Hospital portal plus a District Admin dashboard
- ✅ **Frontline worker support** — the entire ASHA portal is built around field registration and triage
- ✅ **Multilingual interaction** — full UI in English, Hindi, Marathi, Tamil, Telugu, and Bengali
- ✅ **Emergency escalation** — Emergency SOS, both manual and auto-triggered from a RED self-triage
- ⚠️ **Appointment and queue management** — appointments and a walk-in token queue are implemented; a doctor/ASHA can only *Accept* or *Decline* an appointment today, not *postpone* it (queued next — see Roadmap §11.8)
- ⚠️ **Assisted teleconsultation** — the workflow and button exist; real video/audio (WebRTC) is not yet wired in
- ⚠️ **Low-connectivity support** — the design assumes lightweight, low-bandwidth interactions; true offline-first operation is not yet built
- ⚠️ **Interoperable records (approved standards)** — not yet implemented (see Roadmap — an ABDM/FHIR-style export is planned)

### Key features beyond the minimum:
- **Facility-issued staff credentials** — ASHA workers and doctors cannot self-register; a facility must register itself first and then issue each worker a generated ID and password, closing off fake/unverified accounts
- **Aadhaar-based identity with duplicate prevention** — one person, one record, always, with Aadhaar masked everywhere except the patient's own screen
- **5-second SOS cancel window with full dispatch reporting** — an SOS auto-arms, gives 5 seconds to cancel a false alarm, and on confirmation packages the patient's recent medical history and a routing log before notifying every doctor and ASHA worker
- **Walk-in queue / token system** — both patients (self-service) and facilities (for walk-ins) can issue numbered queue tokens, with a "Call Next" workflow for doctors
- **Facility Quality Scorecard** — an auto-computed score per facility from referral completion rate, average turnaround time, and low-stock penalty, meant to flag facilities needing support rather than to rank-and-shame
- **Village-level risk map with drill-down** — villages are automatically colour-coded (Critical/High/Moderate/Low) by RED/YELLOW case load, and an admin can select any single village to pull up every case recorded there
- **Health Awareness & Tips module** — in-app, multilingual health literacy content addressing the "limited awareness of available services" gap named directly in the problem statement
- **Notifications system** — role- and individual-targeted, so a doctor or ASHA worker sees exactly what's relevant to them

---

## 6. How This Differs From Existing Solutions

The rural/public-healthcare-access space in India is not empty — it is, in fact, crowded with tools that each solve **one slice** of the problem, which is itself the fragmentation the SIH problem statement complains about. We looked across government platforms, government-worker-only tools, rural hybrid startups, and mainstream private consumer apps (free and paid) rather than comparing against a single competitor.

### A. National government digital-health infrastructure
| Platform | What it does well | What it doesn't do |
|---|---|---|
| **eSanjeevani** (MoHFW/C-DAC) | The world's largest telemedicine implementation in primary care — over 490 million consultations, an AI-based Clinical Decision Support System, a hub-and-spoke model connecting HWCs/PHCs to specialist "hub" doctors, and full ABDM/ABHA integration | It is fundamentally a **consultation** platform (doctor-to-doctor or patient-to-doctor). It does not manage facility-level medicine stock, walk-in queues, village-wise outbreak risk, a facility quality scorecard, or an automated multi-responder emergency SOS |
| **ABDM / ABHA** (Ayushman Bharat Digital Mission) | The national interoperability *standard* — over 900 million ABHA health IDs and 1 billion+ linked health records, plus the Health Facility Registry (HFR) and Healthcare Professionals Registry (HPR) | It is infrastructure/plumbing, not an operational application — it doesn't itself run ASHA field registration, triage, referral routing, or facility dashboards; individual apps (like eSanjeevani) plug into it |
| **Aarogya Setu** (National Health App) | Lets citizens create an ABHA ID, view digital records/prescriptions, and book eSanjeevani OPD appointments from one consumer app | Purely patient-facing; there is no ASHA workflow, no facility-side stock/queue management, and no district-admin analytics layer behind it |
| **CoWIN** | Did one job — vaccination slot booking — at massive national scale during COVID | Single-purpose and event-specific; not designed as a general chronic-care or triage-referral platform |

### B. Government frontline-worker-only data tools
| Platform | What it does well | What it doesn't do |
|---|---|---|
| **ANMOL (ANM Online) / RCH Portal** | Tablet/Android app for ANMs to log Reproductive & Child Health data (pregnancies, immunizations) with offline-first sync, tied to the national RCH Portal | It is a **worker-only, single-programme** data-entry tool — patients have zero visibility into their own record, and independent field studies (e.g. a 2025 Chandigarh primary-care usability study) found ANMOL frequently **not implemented or poorly implemented** at the facility level due to technical/training gaps |
| **e-HMIS / Nikshay / MCTS** | National program-monitoring portals — Nikshay for TB, MCTS for mother-and-child tracking, HMIS for aggregate programme statistics | Each covers one disease/programme in isolation; none give a single ASHA or doctor a unified, general-purpose triage-to-referral-to-treatment workflow for *any* patient walking in |

### C. Rural hybrid "phygital" e-clinic startups
| Platform | What it does well | What it doesn't do |
|---|---|---|
| **CureBay** (Odisha/Chhattisgarh/Jharkhand) | Closest philosophically to ArogyaBridge — 150+ rural e-clinics staffed by community health workers ("Swasthya Mitras," an ASHA-like role) offering teleconsultation, diagnostics, medicine delivery, and hospital-admission concierge, with ~90,000 active preventive-care subscribers | It is a **private, subscription/franchise brand** running its own parallel clinics and doctor network — it does not digitize or plug into the *government's already-existing* Sub-Centre/PHC/District Hospital hierarchy or its ASHA workforce |
| **Neurosynaptic ReMeDi** | A proven telemedicine hardware+software kiosk (with a 40-test point-of-care diagnostic device) sold to rural clinics for screening and teleconsultation | Sold as a paid B2B/franchise product per clinic; no district-wide admin dashboard, no village risk map, no public medicine-availability search |
| **Karma Healthcare / iKure** | Similar "clinic-in-a-box" rural telehealth models combining local health workers with a digital backend | Also paid, closed B2B/B2B2C deployments tied to their own clinic network rather than a free, public, government-facility-agnostic system |

### D. Mainstream private consumer health apps (free-to-download, paid services)
| Platform | What it does well | What it doesn't do |
|---|---|---|
| **Practo** | Searchable doctor directory by name/speciality/rating, appointment booking, video consults, e-pharmacy, up to 60% consult discounts for members | Doctor listings are self-registered private practitioners, not linked to the public Sub-Centre/PHC/hospital hierarchy; no ASHA-mediated registration for patients without a smartphone or with low literacy |
| **Apollo 24\|7** | Hospital-backed (institutional trust), bundles teleconsult + pharmacy + diagnostics + doctor discovery under one app | Built around Apollo's own hospital/pharmacy network; a rural PHC patient with no Apollo facility nearby gets none of the "facility loop" benefit |
| **Tata 1mg** | Extensive verified medicine database, lab-test booking, a paid "Care Plan" subscription (~₹165/3 months) | Focused on medicine/diagnostics commerce, not on a shared, worker-mediated, longitudinal clinical record across public facilities |
| **PharmEasy / Netmeds** | Very wide pincode coverage including Tier-2/3 towns, membership plans (PharmEasy Plus, Netmeds First) for free delivery | Primarily e-pharmacy logistics businesses; no triage, no referral tracking, no facility/admin dashboards, no emergency SOS |
| **MediBuddy / mfine-style apps** | Corporate-insurance-linked teleconsultation bundles | Access is usually gated behind an employer's insurance policy, not free and open to a rural walk-in patient |

**Where ArogyaBridge sits:** every platform above is strong in exactly one lane — national-scale teleconsultation, a national ID standard, one worker's data entry, one private clinic chain, or one polished consumer app — and each is either *free but fragmented* (a citizen needs five different government apps to cover triage, records, medicine, and vaccination) or *unified but paid/private and disconnected from the public facility ladder*. ArogyaBridge's position is to put an Aadhaar-anchored patient identity, a closed digital triage-to-referral pipeline, facility-level accountability, and district-level visibility into **one connected system that runs through the ASHA worker and the public Sub-Centre/PHC/hospital ladder itself**, rather than building a parallel private network or asking a citizen to stitch five single-purpose apps together.

---

## 7. What's Unique to ArogyaBridge

Cross-checked against every category above (not just eSanjeevani) — here is what, as far as our research shows, no single existing platform combines:

1. **Runs through the existing public hierarchy, not around it.** Unlike CureBay/Neurosynaptic/Karma Healthcare/iKure (which build their own parallel private clinic networks) and unlike Practo/Apollo/1mg (private-practice-only), ArogyaBridge is designed for a Sub-Centre, PHC, or District Hospital to register itself directly and run its *own* ASHA workers and doctors through it.
2. **Facility-issued staff credentials, not self-signup.** Practo/Apollo doctors self-list; ANMOL requires only an ANM's registered mobile number. In ArogyaBridge, a facility must exist first and explicitly issue every ASHA/doctor account — a real accountability chain, not an honour system.
3. **One free, Aadhaar-anchored identity with duplicate prevention at registration time.** ABHA is a valuable but *voluntary* national ID; private apps each spin up their own siloed account. ArogyaBridge refuses a second record for the same Aadhaar number, whether the patient registers themselves or an ASHA registers them.
4. **Ownership-aware patient tracking.** The system distinguishes "patients I registered" from "all patients" for every ASHA worker — a traceability layer none of the tools above expose to the frontline worker herself.
5. **Village-level colour-coded outbreak/risk signal with drill-down.** HMIS/IDSP-style government dashboards report aggregated numbers upward to administrators; none of the platforms researched offer a live, clickable village-by-village Critical/High/Moderate/Low map that drills straight into the named case records behind the colour.
6. **A continuously auto-computed Facility Quality Scorecard.** The closest government analogue — schemes like Kayakalp or NQAS (National Quality Assurance Standards) — are valuable but rely on **manual, periodic (often annual) certification audits**. ArogyaBridge computes a live score from referral completion rate, turnaround time, and stock health automatically, every time the underlying data changes.
7. **Emergency SOS with a 5-second self-cancel and a full auto-generated multi-responder dispatch report.** eSanjeevani has no emergency-SOS concept at all; consumer apps have no location-aware worker dispatch; even CureBay routes emergencies to hospital-admission concierge manually. Nothing found in this research auto-packages a patient's recent medical history and pushes it simultaneously to every duty doctor *and* every ASHA worker within 5 seconds of confirmation.
8. **One integrated system spanning all five roles.** ANMOL is worker-only. Aarogya Setu/Practo/1mg are patient-only. eSanjeevani is provider-to-provider or patient-to-provider, but never facility-stock-plus-worker-issuance-plus-admin-analytics in the same app. ArogyaBridge is the only system in this comparison where Patient, ASHA, Doctor, Facility, and District Admin all read and write the *same* underlying record.
9. **Free and closed-loop at the same time.** Government tools are free but split across five single-purpose apps (ANMOL, Nikshay, HMIS, CoWIN, eSanjeevani). Private apps are unified but paid/subscription-gated and sit outside the public system entirely. ArogyaBridge is free, unified, and built specifically to strengthen — not replace — the public system the problem statement asks for.

---

## 8. Current Prototype — Full Feature List

### Patient Portal
- Aadhaar-based self-registration and login (PBKDF2-HMAC-SHA256 password hashing with a per-user salt)
- ASHA-assisted registration path, with an optional patient-login setup done on the spot
- Personal dashboard: ABHA ID, age, village, masked Aadhaar
- Multilingual Health Awareness & Tips module (4 categories)
- Book Appointment (facility, preferred date, time slot)
- Self Symptom Triage (Groq/Llama-3.1-assisted or rule-based fallback) with auto-RED SOS trigger and auto-YELLOW doctor/ASHA notification
- Emergency SOS button with a 5-second cancel window and full auto dispatch (all doctors + all ASHA workers notified, medical history packaged, routing log generated)
- Self-service Walk-in Queue Token generation with live "now serving" / waiting-count status
- Edit own details (age, gender, village, phone, language)
- My Health Record: full symptom/triage history with vitals, and referral/prescription history
- View own appointment list and status
- Visibility of any active SOS alert on their record

### ASHA / ANM Worker Portal
- Facility-issued Worker ID + password login (no self-signup)
- Register new patients with Aadhaar duplicate-check, with optional login setup for the patient
- "My Registered Patients" vs. "All Patients" views
- AI/rule-based triage with optional vitals capture (temperature, SpO₂, pulse) and abnormal-value warnings
- Automatic department suggestion and follow-up due-date scheduling (RED → 2 days, YELLOW → 7 days)
- Refer a patient to a chosen facility (RED/YELLOW cases)
- Follow-up worklist (overdue vs. due, mark done)
- Dedicated Emergency Cases view (all RED triages)
- Full triage history table (latest 50 records)
- Role-targeted notifications banner

### Doctor Dashboard
- Facility-issued Worker ID + password login
- At-a-glance metrics: patients completed, pending referrals, pending appointments
- Priority-sorted live patient queue (RED first) with a full patient history panel (past visits + past prescriptions)
- Teleconsultation launch button (workflow placeholder)
- Order diagnostic tests from a fixed test list; track Ordered → Completed with result notes
- Write prescription + doctor notes and complete the referral
- Search any patient in the system by name or Aadhaar ID
- Accept or Decline appointment requests (decline requires a stated reason)
- Personal completed-cases history
- Active SOS alert list, one-click "Accept" ownership, view the packaged medical summary
- Diagnostics tab to mark facility-wide ordered tests complete
- Walk-in queue management: issue tokens, "Call Next," mark served, live queue view

### Facility / Hospital Portal
- One-time facility self-registration (name, type, area served, phone + password)
- Create ASHA worker accounts (auto-generated ID + password) with duplicate-name guard
- Create doctor accounts (auto-generated ID + password, choose speciality) with duplicate guard
- Staff directories (My ASHA Workers / My Doctors)
- Medicine stock management: view stock with low-stock highlighting (<10 units), add/remove/set-exact updates with a full audit trail, add new medicines
- Facility-level metrics: staff counts, pending referrals, pending appointments

### District Admin Dashboard
- Active SOS alerts with one-click resolve
- System-wide metrics: patients, triages run, total referrals, completion rate, follow-ups due, appointments pending, doctors, ASHA workers, facilities, diagnostics pending, today's queue count, emergency case count
- Facility Analytics: triage-by-priority, referrals-by-facility, department case-load, and appointment-status charts
- Auto-computed, colour-coded Facility Quality Scorecard
- Village Risk Map with Critical/High/Moderate/Low colour coding, a comparison chart, and per-village drill-down into named case records
- Advanced Records Filter (village, facility, priority, department, symptom keyword, multiple sort orders)
- Symptom Outbreak Signal (latest 20 triages, for early cross-village pattern spotting)
- System-wide low-medicine-stock alert table

### Public / System-wide
- Public, login-free Medicine Availability search (by facility and/or medicine name)
- Full 6-language interface: English, Hindi, Marathi, Tamil, Telugu, Bengali
- Role- and individual-targeted notifications engine with read/unread state
- SQLite persistence with a self-migrating schema (safely adds missing columns on startup)
- Secure, salted password hashing for every role (patient, ASHA, doctor, facility)
- AI triage with graceful degradation: Groq Llama-3.1 when an API key is configured, otherwise a deterministic bilingual (Hindi/English) rule-based RED/YELLOW/GREEN classifier

---

## 9. Planned Integrations — APIs We Are Not Connecting Yet

These are realistic, named next-step integrations for a production version — none are wired in for the prototype, by design, to keep the current build fully runnable offline/without external credentials:

- **ABDM Sandbox APIs (HIP/HIU)** — to issue real ABHA numbers and push/pull records from the actual national Health Information Exchange, instead of an internally generated ABHA-style ID
- **UIDAI Aadhaar eKYC/OTP API** — real Aadhaar verification at registration, instead of today's format-only (12-digit) validation
- **SMS / WhatsApp Business API** (MSG91, Gupshup, or Twilio) — OTP-based login, appointment reminders, and SOS alerts delivered to a doctor's or ASHA's phone even when the app isn't open
- **WebRTC / Daily.co / Jitsi API** — real audio-video teleconsultation to replace today's placeholder "Start Teleconsultation" button
- **Google Maps / Distance Matrix API** — nearest-facility suggestions for patients and an ETA/route for SOS ambulance dispatch
- **108 / 102 Ambulance dispatch API** (state-specific, where available) — to make the SOS "ambulance requested" step a real dispatch call rather than a logged intent
- **Bhashini / cloud translation-and-speech API** — real-time voice-to-text symptom entry and translation beyond today's six hardcoded UI languages
- **Firebase Cloud Messaging (or similar push service)** — real device push notifications instead of in-app-only banners
- **Cloud object storage (S3/GCS)** — for diagnostic report PDFs, scanned prescriptions, and other attachments
- **Payment gateway (UPI/Razorpay)** — for any optional paid add-ons or PM-JAY co-payment handling, once scheme integration (Roadmap §11.5–6) is in place
- **A stronger LLM for triage** (e.g., a larger hosted model) — the current Groq Llama-3.1-8B integration is optional and already pluggable; a larger model could improve multi-symptom, multi-language reasoning

---

## 10. Known Issues — Queued for the Next Update

Bugs and gaps identified in the current build that are next in line to fix (not yet touched, by design, until this document was finalized):

- **Patient login by phone number** — the phone number is collected and stored at registration, but login currently only works with the Aadhaar ID; phone-based login needs to be wired up and tested.
- **Prescription visibility bug** — a prescription saved by a doctor does not always reliably surface on the patient's own "My Referrals" view; needs a fix pass and a regression check across the patient/doctor/ASHA views.
- **Appointment decline reason not shown to the patient** — a doctor's decline reason is already recorded in the database but is never rendered back on the patient's own Appointments view (see Roadmap §11.8).
- **No doctor search for patients yet** — patients can only pick a facility when booking, not search or filter by a specific doctor's name or speciality (see Roadmap §11.2).
- **No postpone action yet** — a doctor (and an ASHA booking on a patient's behalf) can currently only Accept or Decline an appointment, with no Postpone/reschedule option (see Roadmap §11.8).

---

## 11. Roadmap — What's Planned Next

> Items 2 and 8 below are the very next things being built.

1. **ABDM/FHIR-style interoperable record export.** Generate a standards-based (FHIR Bundle / ABDM HIP-compliant) export of a patient's full record so it can be shared with any ABDM-participating hospital or app outside ArogyaBridge, not just viewed inside it.

2. 🔜 **Searchable doctor/specialist directory for patients.** Today a patient can only pick a *facility* when booking an appointment. This adds the ability to search and filter available doctors directly — by name, by speciality, and by facility/village — with basic availability shown, before choosing who to book with.

3. **Recurring chronic-care follow-up schedules.** Today's follow-up is a single due-date set once at triage time and then marked "done" for good. For chronic conditions — hypertension, diabetes, TB — this becomes a *repeating* schedule (e.g., "every 30 days until the ASHA/doctor closes the case"), with the existing ASHA follow-up worklist automatically showing the next due date instead of the case disappearing after one visit. This is written out in enough operational detail here so any teammate — or a judge reading this file cold — can see exactly what changes without needing a live walkthrough.

4. **Maternal & Child Health mini-module.** A dedicated antenatal-care (ANC) visit schedule and child immunization due-list layered on top of the existing patient record — similar in spirit to the government's ANMOL/RCH tracking, but (unlike ANMOL) visible to the mother herself in the Patient Portal, not only to the ANM entering the data.

5. **PM-JAY / Ayushman Bharat scheme linkage.** Let a patient's profile record whether they hold a PM-JAY / Ayushman Bharat card, so a referring ASHA worker or doctor can see at a glance whether a case can be routed as a cashless scheme case.

6. **Affordability-aware referral routing.** Building on (5): use that scheme flag to actively surface scheme-eligible patients in the doctor's queue and the facility's referral list, so a PM-JAY beneficiary isn't inadvertently referred to a facility or test outside the scheme's cashless network. (Split out from a single combined "PM-JAY/affordability" item into two focused pieces of work: *recording* eligibility, and *acting* on it.)

7. **Facility SLA-breach flagging + patient feedback loop.** India's existing facility-quality frameworks — schemes like **Kayakalp** and the **National Quality Assurance Standards (NQAS)** — are valuable but run on **manual, periodic (typically annual) certification audits**, and they score a facility, not an individual case in flight. This item adds two things our current (backward-looking) Quality Scorecard doesn't yet do: (a) **live SLA-breach detection** — automatically flag any referral still `PENDING` past a defined threshold (e.g., 24 hours for a RED case, 72 hours for YELLOW) and surface it to the District Admin in real time, rather than only computing an aggregate score after the fact; and (b) a lightweight **patient feedback loop** — a 1–5 star rating with an optional comment after a completed referral, feeding directly back into that facility's Quality Score alongside completion rate, turnaround time, and stock health.

8. 🔜 **Appointment postponement + full status transparency.** Right now a doctor can only *Accept* or *Decline* (with a mandatory reason) an appointment request. This adds a **Postpone** action for the doctor — proposing a new date/time back to the patient — and gives the **ASHA worker the same Accept/Decline/Postpone authority** for appointments she books on behalf of a patient who doesn't operate the app herself (a common real-world case in rural households). Critically, every outcome — confirmed, declined-with-reason, or postponed-with-new-slot — must actually render on the **Patient Portal's own "My Appointments" view**, which today only shows a bare status column and silently drops the decline reason the doctor already records in the database (see Known Issues §10).

9. **Real WebRTC-based teleconsultation.** Replace today's placeholder "Start Teleconsultation" button with an actual audio/video session (Daily.co, Jitsi, or similar), so "assisted teleconsultation" — item #1 in the SIH problem statement's expected outcome — is a real, working feature rather than a workflow stub.

10. **True offline-first data capture.** Allow ASHA registration, triage, and vitals entry to be saved locally on the worker's device and synced to the server once connectivity returns — matching how ANMOL is *designed* to work in the field, and directly addressing the "low-connectivity environment support" requirement in the problem statement.

---

*This document reflects the current state of the ArogyaBridge prototype and is intended to be read alongside the working application and the SIH26133 problem statement.*
