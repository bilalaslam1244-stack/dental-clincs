# Handoff: Smile Arts free trial + 4Skales ads

Read this first. It is the full context from the first (cloud) session, so a new session can continue without re-asking.

## Who we are

- **Fourskales Sdn. Bhd. ("4Skales")**, Kuala Lumpur and Johor Bahru. Sells clinic websites with WhatsApp booking, plus patient lead generation (Meta ads, later Google).
- Offer to clinics: **2 weeks of patient enquiries, free. 4Skales pays the ad spend too.** No card, no contract. Like it: continue on the monthly plan. Not for you: walk away.
- Pricing after the trial: **RM 3,000/month** for ads on both branches (campaign management, new creatives monthly in EN/BM/中文, WhatsApp tracking, monthly report and call). Ad spend separate, paid by the clinic to Meta (suggest RM 1,000–1,500 per branch per month to start). Google search ads come with the paid plan, not the trial. Month to month, cancel anytime.
- Website redesign: not priced in the pitch. Internal guide ~RM 3,000 if taken with the ads plan (min 3 months). Public list price in `docs/copy-deck.md` is RM 6,800.

## The client: Smile Arts Dental Clinic

- **Dr. Daren Ang**, founder and director. DDS (Universiti Sains Malaysia, 2008). Invisalign provider since 2016. Digital Smile Design trained. Focus: veneers, implants, orthodontics.
- **Status: agreed to the free 2-week trial.** The user has his Meta account access.
- Website: https://smilearts.com.my (WordPress/Elementor). Brand: font **Tajawal**, colour **#A89379** (taupe), logo https://smilearts.com.my/wp-content/uploads/2024/10/Group1.png (white version: .../Site-Logo-White.png).
- Branches (three exist; the trial covers two):

| Branch | In trial | WhatsApp (from his site, confirm) | Instagram | Enquiries/week now | Ad languages |
|---|---|---|---|---|---|
| Kepong | Yes | 011-6427 5645 | @smileartsdental_kepong | about 10 | English + Chinese |
| Subang Perdana | Yes | 010-361 7347 | @smileartsdental_subangperdana | not given yet, ask | English + Bahasa Malaysia |
| Kota Damansara | No (later) | 014-365 0270 | @smileartsdental_kd | | |

- Treatments to promote: **braces (incl. Invisalign), implants, veneers.**
- The receptionist replies on WhatsApp within 15 minutes.
- His goal: more enquiries and appointments, more social media exposure.
- Website problems we noted: bot-check page before the homepage, one generic contact form, empty reviews section, broken "Read More", branches listed twice, no meta descriptions.

## Trial campaign plan

- **One Click-to-WhatsApp campaign** (objective: Engagement → messaging conversations), **two ad sets**: Kepong and Subang Perdana, each about **5 km radius**, adults ~25–55, each sending to **its own branch WhatsApp**, shown as that branch's Page/Instagram identity.
- Creatives per ad set: braces, implants and veneers, in that branch's languages, 9:16 (Stories/Reels) and 4:5 (Feed).
- **Pre-filled WhatsApp messages name the branch and treatment** so the receptionist can tell ad enquiries apart, e.g. "Hi Smile Arts Kepong, I'd like to ask about braces".
- Budget: **4Skales pays.** Suggested RM 25–30/day per branch for 14 days (~RM 700–840 total). **The user has not confirmed the exact daily budget: ask.**
- Timeline: set-up (access, WhatsApp linking, ad approval) → Day 1 launch → Day 3 pause weak ads, move budget → Day 7 update to Dr. Daren on WhatsApp → Day 14 report + 20-minute call, then propose the monthly plan.
- Tracking: receptionist keeps a one-line log per ad enquiry (date, branch, treatment, booked yes/no). Day-14 report: enquiries, cost per enquiry, appointments booked, strongest treatment per branch.

## Compliance (Malaysian Dental Council) — hard rules for every ad

- **No** before-and-after photos, **no** patient testimonials or reviews, **no** discounts, promos or "free" treatment, **no** "best"/"cheapest" claims.
- **Yes**: his factual qualifications, real photos of the team and clinics, clear facts (treatments, branch, hours), an invitation to book a consultation.
- If he wants a promo featured: only if he confirms it is within MDC rules (his call).
- **KKLIU**: private clinic ads may need Medicine Advertisements Board (Ministry of Health) approval, shown as a KKLIU number. Ask whether his current ads carry one; if so, our ads need approval before launch.
- **Dr. Daren approves every ad before it runs.**

## Meta access and safety

- Use **partner access through 4Skales' Business Manager** (his Facebook Page + both branch Instagram accounts shared to 4Skales with ad access). Avoid using his personal login or password; it breaks Meta's terms and can get his account locked.
- Click-to-WhatsApp needs each branch's WhatsApp number linked to its Page/Instagram; Meta texts a one-time code to that phone (the receptionist forwards it). Check whether each branch has its own Facebook Page.
- **4Skales' own ad account bills in ₹ (Indian rupees).** Currency can't be changed on an existing ad account; create a new ad account in MYR inside the same Business Manager.

## Rules for the agent (non-negotiable)

1. **Never spend money without the user's explicit OK.** Create campaigns, ad sets and ads **PAUSED**, show a summary (objective, audience, budget, placements, creatives, destination numbers), and only publish when the user says so.
2. Never change a live budget, bid or targeting without asking.
3. Every Smile Arts creative goes to the user for Dr. Daren's approval before upload.
4. Treat client phone numbers and access as private; never paste tokens into files or commits.
5. Commit and push work to branch `claude/eager-davinci-a69h55` with clear messages.

## What already exists

- **Repo** (`bilalaslam1244-stack/dental-clincs`, branch `claude/eager-davinci-a69h55`): see `README.md`.
  - `video/statics/statics.html` + `video/tools/render-statics.mjs`: static ad system (light luxury style, 9:16 + 4:5). `video/tools/build-statics-i18n.py`: BM and Chinese versions (Chinese font subsets). `video/tools/build-motion.py` + `compose-music-motion.py`: 7.5 s motion versions (HyperFrames; render with `npx hyperframes render -c <file> --quality high -o <out>`; then the static PNG is overlaid on frame 0 as poster).
  - `video/renders/statics/` and `video/renders/motion/`: **4Skales' own ads aimed at clinic owners** (8 concepts × EN/BM/ZH × 9:16/4:5). These are for 4Skales' lead generation, **not** for Smile Arts patients.
  - `video/share-copy.txt`: Meta primary text/headlines for those ads (EN/BM/ZH) and pre-filled messages that filter out non-owners.
  - `demo-clinic/index.html`: Lumen Dental demo site (fictional).
- **Google Drive**: folder "4Skales Dentist Ads (Oct 2026)" (https://drive.google.com/drive/folders/1ohE-H1UP3RseSH5dbAVKxGkWDD25wgRt) with language/format subfolders and the ad copy doc. The media files are sent there by the uploader page https://claude.ai/artifact/HcjWyDfSj627vVrYT2fStQ (the user presses Upload; not confirmed done).
- **Pitch deck** for Dr. Daren (16 slides, Smile Arts branding): https://claude.ai/artifact/CbqgzNLzNXbkWpshRR1NiF. **Meeting checklist**: https://claude.ai/code/artifact/e8b7dc17-53ee-4f7b-8623-47fc4f2e6adf.
- 4Skales' own Meta results so far: Dentists campaign, Stories/Reels only, 3 messaging conversations at about ₹506 each. Countertop campaign shut down (low-quality leads).

## To do, in order

1. **Check the setup**: confirm the Meta connector/plugins work, list the accessible ad accounts, Pages and Instagram accounts, and confirm Smile Arts' Page and both branch Instagrams are reachable through 4Skales. Report what is and isn't connected.
2. **Ask the user for the open items**: daily budget per branch; Subang Perdana's weekly enquiries; whether both WhatsApp numbers are linked; the KKLIU answer; extra photos/videos from Dr. Daren (otherwise use content from his Instagram pages, with his OK).
3. **Make Smile Arts' patient-facing creatives**: braces, implants, veneers × Kepong (EN, 中文) and Subang Perdana (EN, BM), statics and short videos in 9:16 and 4:5, in Smile Arts' brand (Tajawal, #A89379, his logo), MDC-compliant, ending in "Book a consultation on WhatsApp". Reuse the `video/` tooling. Write matching primary text/headlines.
4. **Send the creatives to the user for Dr. Daren's approval.**
5. **Build the campaign PAUSED** (one campaign, two ad sets as above, pre-filled messages per branch/treatment), show the summary, publish only on the user's go-ahead.
6. **Tracking**: a simple Google Sheet for the receptionist's log, and WhatsApp quick replies for the front desk (EN/BM/中文).
7. **Day 3 / Day 7 / Day 14**: pull results, recommend changes, draft the updates to Dr. Daren, build the Day-14 report and the monthly-plan proposal.
8. **4Skales' own campaign**: upload the creatives in `video/renders/` to 4Skales' ad account (MYR), Stories/Reels and Feed ad sets per language, using `video/share-copy.txt`.
