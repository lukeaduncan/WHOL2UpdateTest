Absolutely—thanks for sending ***HIV recs to test\_v1.xlsx***. I reviewed each 2025 recommendation and mapped the concrete DAK updates you’ll need across the three HIV DAK workbooks:

*   **Annex A – Data Dictionary** → `WHO-UCN-HHS-SIA-2023.27-eng.xlsx` [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
*   **Annex B – Decision‑Support Logic & Schedules** → `WHO-UCN-HHS-SIA-2023.28-eng.xlsx` [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **Annex C – Indicators** → `WHO-UCN-HHS-SIA-2023.29-eng.xlsx` [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

Below is a **change plan** that tells you precisely **which file(s) to touch** and **what to change** for each new/updated recommendation from your spreadsheet. (I include the relevant Decision IDs, Schedule IDs, and indicator IDs wherever they already exist in the DAK structure for clean traceability.)

***

## A. TESTING & PrEP

### A1) **Allow RDTs for initiation/continuation/discontinuation of long‑acting PrEP**

**Rec:** *“Rapid diagnostic tests may be used for HIV testing for initiation, continuation and discontinuation of long acting injectable PrEP.”* (HIV.TST.2025.001.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Update in Annex A (Data Dictionary)** — `2023.27`

*   **HTS (HIV.B) & PrEP (HIV.C) tabs**
    1.  Add **“HIV test type”** (select‑one; Coding) with options including **“Rapid diagnostic test (RDT)”**; validation that a test result accompanies the test type. Link to HTS decision logic and PrEP workflows. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    2.  Ensure existing **“HIV test result”**, **“HIV test date”**, and **“Date HIV test results returned”** fields are referenced by PrEP workflows; they already exist for indicators and logic—expand linkages to PrEP activities so they’re available at LA‑PrEP dosing encounters. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    3.  In **PrEP**: extend **“PrEP product prescribed”** to include **“Lenacapavir long‑acting injectable”** (see A2 below). [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Update in Annex B (Decision Support & Schedules)** — `2023.28`

*   **New/updated schedule** under **HIV.S.1** (Recommended post‑test services) or **new PrEP dosing schedule**:
    *   Add a row: **“HIV test prior to LA‑PrEP injection”** → Triggered by **PrEP injection due**; **Create condition:** “PrEP product = long‑acting injectable”; **Due date:** same day as dosing; **Completion:** valid negative **RDT** recorded. This reuses schedule patterns already present for post‑test actions and visit‑bound services. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **Decision tables**: In **PrEP suitability (HIV.C7.DT)** and **Determine PrEP/PEP regimen (HIV.C23.DT)**, add input expressions to accept **RDT‑based negative** results at initiation and continuation (IF “HIV test type = RDT” AND “HIV test result = negative” within allowed window THEN proceed with LA‑PrEP injection). [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Update in Annex C (Indicators)** — `2023.29`

*   No new indicator required; **HTS.2 / HTS.3** already measure HTS volume/positivity by **testing entry point**, and PrEP indicators already support **product/formulation** disaggregation. Confirm that “test type” (RDT) is available for analysis in your local pipeline, though it is not a core SI disaggregation. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### A2) **Add long‑acting injectable lenacapavir as a PrEP option**

**Rec:** *“Long‑acting injectable lenacapavir should be offered as an additional prevention choice…”* (HIV.PRV.2025.001.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Update in Annex A** — `2023.27`

*   **PrEP (HIV.C) and Prevention tabs**:
    1.  **Add drug concept:** **Lenacapavir (LA)** to **“Medications prescribed”** and **“PrEP product prescribed”** lists.
    2.  **Add dosing/administration** fields if you need: **“PrEP administration route”** (Injectable; select‑one), and **“PrEP injection date”** (DateTime).
    3.  **Contraindications / interactions** (placeholder fields) so decision logic can check them as evidence accumulates. Link to HIV.C7.DT / HIV.C23.DT. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Update in Annex B** — `2023.28`

*   **HIV.C7.DT (PrEP suitability)**: add rows to include **lenacapavir LA** as an **eligible option** when risk criteria are met and HIV‑negative test is documented. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **HIV.C23.DT (Determine PEP/PrEP regimen)**: add output actions to **recommend lenacapavir LA**; include guidance text and any initial dosing scheduling in the **Action/Guidance** columns. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **Schedules**: add/adjust visit cadence to match lenacapavir’s dosing cycle (e.g., injection due reminders under **HIV.S.1** as noted above). [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Update in Annex C** — `2023.29`

*   **HIV.IND.2 (Total PrEP recipients), HIV.IND.3 (PrEP coverage), HIV.IND.4 (Volume of PrEP prescribed)** already allow **“PrEP product and formulation”** including **long‑acting injectable**—add a **value for “lenacapavir (LA)”** in your product list and ensure **days of protection** conversion is documented under “Method of measurement” for Volume. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## B. PREVENTION OF VERTICAL TRANSMISSION (PMTCT)

> The following require edits to infant prophylaxis logic and breastfeeding follow‑up.

### B1) **Maintain 2021 feeding choice rec (affirmation)**

**Rec:** HIV.VER.2021.001.02 (unchanged)   
No structural DAK change; confirm references remain in E/F logic text. **No file edits required.** [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

### B2) **Enhanced community/facility breastfeeding support**

**Rec:** HIV.VER.2025.002.02 (updated) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   **PMTCT (HIV.E–F) & Follow‑up (HIV.H)**:
    *   Add checklist fields for **“Enhanced BF support provided”** (counselling, peer support, adherence plan, home visit scheduled), and **“Mother–infant pair retained in care”** status elements to support scheduling and monitoring. Link to schedules. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   **Schedules**: Under PMTCT workflows, add schedule lines for **follow‑up contacts** (facility/community) during breastfeeding with **actions** for adherence support and visit reminders. Use **HIV.S.1** pattern for post‑test services and add PMTCT‑specific rows. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   No new SI indicator is required; integrate with existing **linkage/retention** and **HTS linkage to prevention** frameworks if you locally track PMTCT support as a programme metric. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### B3) **Infant prophylaxis—NOT high risk: 6 weeks single‑drug NVP (preferred)**

**Rec:** HIV.VER.2025.003.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add/ensure **Infant risk classification** (select‑one: *high risk / not high risk*), **Infant prophylaxis regimen** (list includes **NVP single‑drug**), **Prophylaxis start date**, **Planned prophylaxis duration** (= 6 weeks for not‑high‑risk). Link these to PMTCT decision tables. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   **PMTCT decision logic** (HIV.E/F infant management): add rule: *IF risk = not high THEN recommend **NVP x 6 weeks***; output type **MedicationRequest** with guidance. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   If you report infant prophylaxis coverage, add a **programme‑level indicator** (local extension) referencing these data elements; core WHO SI 2022 does not include a standard global indicator for neonatal prophylaxis coverage. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### B4) **Infant prophylaxis—HIGH risk: 3‑drug ABC + 3TC + DTG (preferred)**

**Rec:** HIV.VER.2025.004.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Extend **Infant prophylaxis regimen** options to include **ABC + 3TC + DTG (3‑drug)** and dosing fields as needed (weight/age bands). [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   PMTCT logic: *IF risk = high THEN recommend **3‑drug ABC+3TC+DTG** regimen* with appropriate dosing guidance. Consider a **hit policy R** with explicit prioritization over any legacy rules. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

***

### B5) **Step‑down prophylaxis during breastfeeding after initial 3‑drug**

**Rec:** HIV.VER.2025.005.02 (continue single‑drug NVP until end of breastfeeding or maternal viral suppression) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add **Maternal viral suppression status** (Boolean or lab‑driven via VL result threshold) and **Date maternal suppression achieved**; add **Breastfeeding status** (already present in HTS/PMTCT; confirm linkages). [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   Add rule: *IF infant completed 3‑drug AND (breastfeeding = TRUE AND maternal suppression ≠ TRUE) THEN continue **single‑drug NVP** until suppression or BF ends.*
*   Add schedule to **check maternal VL** at recommended intervals during breastfeeding to automatically evaluate the stop condition. You can reuse patterns from **HIV.S.2** viral‑load schedules. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

***

## C. TREATMENT (ART)

### C1) **PI preference hierarchy**

**Recs:**

*   Preferred boosted PI when needed: **DRV/r** (HIV.TRT.2025.001.02)
*   Alternatives: **ATV/r** or **LPV/r** (HIV.TRT.2025.002.02) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex B** — `2023.28`

*   **HIV.D21.1.DT (Determine ART regimen)**:
    *   Update first‑/second‑line rule sets to **rank DRV/r as preferred PI** option, with **ATV/r or LPV/r** as alternatives when a PI is required. Ensure consistency with pediatric/adult branches. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Ensure **ART regimen** option lists and **Medications prescribed** include these PI options for decision‑support outputs. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex C** — `2023.29`

*   No indicator change—the **ART coverage and regimen** are covered in ART indicators; regimen granularity is typically analysed locally. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### C2) **NRTI backbone preferences**

**Recs:**

*   **Adults/adolescents/children ≥30 kg**: **TDF (or TAF) + 3TC/FTC** as **preferred** backbone, including prior exposure cases (HIV.TRT.2025.003.02)
*   **Children <30 kg**: **ABC + 3TC or TAF + 3TC/FTC** suggested for **subsequent ART** (HIV.TRT.2025.004.02) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex B** — `2023.28`

*   **HIV.D21.1.DT**: refine age/weight cut‑points and **backbone selection** logic per the above (be explicit on “previously treated or exposed” inputs). [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add/confirm **“Weight / Weight band”** and **“Prior ARV exposure”** data elements are available and linked to regimen decisions. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

***

### C3) **Dual‑drug simplification (DTG + 3TC)**

**Rec:** *Use DTG+3TC for simplification in virologically suppressed adults/adolescents without active HBV* (HIV.TRT.2025.005.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex B** — `2023.28`

*   **HIV.D21.1.DT**: add branch: *IF VL undetectable AND no active HBV → recommend **DTG+3TC** for simplification*; include **Guidance** on contraindication with HBV coinfection. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Ensure **HBsAg/anti‑HBc/anti‑HBs** fields and **HBV infection status** exist (Diagnostics tab) and are linked to regimen decisions. These elements already appear under S.1 services; ensure clinical decision linkages are present. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx), [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   No new global SI indicator; consider a local quality metric for **proportion simplified to DTG+3TC** among eligible. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### C4) **Long‑acting CAB + RPV as alternative switch**

**Rec:** *LA CAB+RPV may be used as an alternative switch for suppressed adults/adolescents without active HBV* (HIV\_HEP.TRT.2025.006.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add **CAB+RPV LA** under **Medications prescribed** (treatment) and add **“ART administration route”** (Injectable) and **injection schedule** fields if not yet present. Include **HBV status** linkage as above. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   **HIV.D21.1.DT**: add switch logic mirroring C3 with **VL undetectable + HBV negative** precondition; add **Schedule** entries (e.g., injection visits) similar to viral‑load review schedules. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   Add a **local disaggregation** to **ART.1 (People on ART)** for **“regimen category: LA CAB+RPV”** if you want visibility; not required in WHO SI 2022. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### C5) **AHD identification: CD4 preferred; staging if CD4 unavailable**

**Recs:** HIV.TRT.2025.007.02 & .008.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex B** — `2023.28`

*   **New/updated rule** (could be part of **HIV.D12.DT Determine screenings** or a dedicated **“Identify AHD”** decision):
    *   *IF CD4 available THEN use CD4 threshold to identify AHD; ELSE use WHO clinical staging.* Add pop‑ups to steer immediate AHD package if AHD identified. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **HIV.S.2** (Monitoring): ensure **baseline CD4 test at diagnosis/initiation** is scheduled (if not already), and **6‑monthly** until established on ART (already present). Add text that CD4 is **preferred for AHD identification**. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Confirm **CD4 count** and **WHO clinical stage** elements exist and are linked to the new rule; they do exist in current DAK but ensure the **linkages** column references the new decision ID. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

***

### C6) **Kaposi’s Sarcoma chemotherapy options**

**Rec:** *Suggest paclitaxel or pegylated liposomal doxorubicin for KS* (HIV.TRT.2025.009.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add diagnosis flag **“Kaposi’s Sarcoma (KS) diagnosed”** and **“Planned KS chemo regimen”** (options: *Paclitaxel*, *Pegylated liposomal doxorubicin*). [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   Add **Decision**: *IF KS diagnosed THEN create **ServiceRequest/MedicationRequest** for paclitaxel or PLD per availability; provide **Guidance** for referral/oncology coordination.* Hit policy can be **F** to present a single routed pathway when both match. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   No change to core indicators.

***

## D. TB/HIV

### D1) **TB Preventive Therapy (TPT) regimen preferences**

**Rec:** *Prefer **3HP (Rifapentine + INH, 3 months)**; alternatives include 6H/9H; in special cases 3HR, 1HP, 4R, 6Lfx* (HIV.TBH.2025.001.01) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add **TPT eligibility** flag; **Chosen TPT regimen** options: *3HP (preferred)*, *6H*, *9H*, *3HR*, *1HP*, *4R*, *6Lfx*; add **Contraindications** (e.g., DR‑TB exposure, drug interactions) and **TPT start/completion dates**. Link to decision & indicators as applicable. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   Add **Decision** under **HIV.D4.DT (Screen for TB)**/**HIV.D12.DT (Determine screenings to perform)** or a dedicated **“Select TPT regimen”** table:
    *   Priority rule choosing **3HP** when eligible/available; fall‑back to **6H/9H** when **3HP** not feasible; special‑circumstance branches for 3HR/1HP/4R/6Lfx. Provide **Guidance** on regimen‑specific counselling and monitoring. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **Schedules**: add **TPT follow‑up visits** (initiation, monthly as required, completion) under Schedules section. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   WHO SI 2022 includes TB/HIV items elsewhere; your current Indicators tab doesn’t show a dedicated TPT coverage indicator excerpt. If you want to track TPT coverage, add a **programme indicator** (local) using the new TPT data elements; align to national reporting. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## E. SERVICE DELIVERY

### E1) **Hospital‑to‑outpatient transitional support**

**Rec:** HIV.SRV.2025.001.02 (supports for linkage/engagement, reduce readmissions) [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add service‑delivery fields: **“Pre‑discharge goal set”**, **“Medication review completed”**, **“Transitional care plan”**, **“Phone follow‑up scheduled”**, **“Home visit scheduled”**, **“Peer support assigned”**. Link to schedules. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   **New schedule set** under **HIV.S.1**: trigger = **inpatient discharge** for **HIV+** clients; due dates for phone follow‑up, home visits, and clinic appointment; completion = documented contact. Use existing **S.1** schedule structure. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

***

### E2) **Adherence support interventions (counselling, reminders, lay support, education)**

**Rec:** HIV.SRV.2025.002.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add **“Adherence support provided”** (multi‑select: counselling, SMS reminder, peer/lay support, education), and **“Adherence plan agreed”**. These link neatly with existing **S.2** monitoring rules that reference adherence counselling. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx), [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex B** — `2023.28`

*   In **HIV.S.2 Monitoring the response to ART**, ensure adherence support is a **completion criterion** (already used in VL monitoring lines) and add a **proactive schedule** to deliver/record the interventions at ART initiation and at elevated VL follow‑up. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

***

### E3) **Integrate diabetes & hypertension care with HIV services**

**Rec:** HIV\_DIA\_HTN.SRV.2025.003.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Under **HIV.D** (Care‑Treatment): add data elements for **BP**, **diabetes screening result/HbA1c or FBG**, **hypertension/diabetes diagnosis** flags, **referral/management** status. (You already have an “other clinical services” structure in S.1; now make them first‑class clinical elements in the Care‑Treatment tab.) [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   Extend **HIV.D12.DT (Determine screenings to perform)** to include **BP & diabetes screening** per periodicity; add **Schedule** rows under **HIV.S.1** for referral/management follow‑ups. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   No change to core HIV SI indicators; these are typically reported via NCD programmes. Consider local programme indicators for **co‑management** coverage. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

### E4) **Integrate mental health care (depression, anxiety, alcohol use) with HIV services**

**Rec:** HIV\_MNH.SRV.2025.004.02 [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex A** — `2023.27`

*   Add screening elements (e.g., **PHQ‑9 score**, **GAD‑7 score**, **AUDIT‑C score** if used), **diagnosis flags**, **referral provided**, **treatment started**. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

**Annex B** — `2023.28`

*   Add mental‑health screening/management to **HIV.D12.DT**; add **HIV.S.1** schedule lines for **referral and follow‑up**. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

**Annex C** — `2023.29`

*   No changes to core HIV SI indicators. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## F. WHAT I WILL DELIVER (if you’d like me to implement)

1.  **ChangeLog tabs** in each workbook listing: Sheet, Row/ID, Current text, New text, Rationale, Source (your 2025 rec ID), Cross‑links. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx), [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx), [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)
2.  **Revised decision tables & schedules** (HIV.C7.DT, HIV.C23.DT, HIV.D21.1.DT, HIV.D12.DT, HIV.S.1, HIV.S.2, PMTCT infant prophylaxis tables, TPT selection) with **hit policy** notes and **pop‑up guidance** copy. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
3.  **Data Dictionary** updates (new data elements, option lists, validation/conditionality, linkages to decisions & indicators). I’ll annotate terminology columns and mark **TBD codes** for drugs (lenacapavir, CAB+RPV LA, PLD) for your terminology team to map. [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
4.  **Indicator notes**: confirm that **PrEP product** includes **lenacapavir LA**, and add **local** (optional) indicators for infant prophylaxis, LA CAB+RPV uptake, and TPT coverage if you want programme tracking beyond core WHO SI. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## G. Sequencing & QA I propose

*   **Phase 1:** Annex A additions first (so decisions & indicators can reference stable element IDs). [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
*   **Phase 2:** Annex B rules/schedules (unit tests to confirm triggers, hit policy behavior, and stop conditions—e.g., maternal suppression ending infant NVP). [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)
*   **Phase 3:** Annex C—confirm disaggregations (PrEP product list includes **lenacapavir LA**) and add any **local** indicators you want to track. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)
*   **Cross‑walk audit:** verify every rule/indicator references **existing** Data Element Labels and that **UCUM** units and **CQL operators** in decision tables are valid. [\[HIV recs to test_v1 | Excel\]](WHO-UCN-HHS-SIA-2023.28-eng.xlsx)

***

### Want me to start implementing now?

If you give me the go‑ahead, I can begin by:

*   Adding the **new data elements** and option values in **Annex A**,
*   Updating the **key decision tables** (**C7, C23, D21.1, D12**) and **schedules** (**S.1, S.2, PMTCT, TPT**) in **Annex B**,
*   Updating **Annex C** product lists and drafting **optional programme indicators** for your internal dashboards.

If you prefer, I can also produce a **diff report** first for your review before I touch the files.

