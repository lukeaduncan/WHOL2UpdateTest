Great—here’s a **structured, line‑by‑line diff report** (proposed changes only; no files altered yet). I’ve grouped diffs by workbook and tab, showing **Add / Modify / Remove**, precise **targets** (Decision IDs, Schedule IDs, Data Element IDs), and the **before → after** text where relevant. Each block cites the current DAK content I reviewed and the 2025 recommendation source you provided.

***

## 1) `WHO-UCN-HHS-SIA-2023.27-eng.xlsx` — **Web Annex A (Data Dictionary)** [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

### HIV.B — HTS visit (Testing)

**Add**

*   **New data element:**
    *   **Label:** *HIV test type*
    *   **Type:** *Coding (select one)*
    *   **Options:** *Rapid diagnostic test (RDT); Laboratory assay; Self‑test (reported)*
    *   **Required:** *C* (Required if *HIV test conducted* = True)
    *   **Linkages:** *HIV.C7.DT, HIV.C23.DT, HTS.2/HTS.3 indicators*
    *   **Rationale:** Allow RDT use at **initiation/continuation/discontinuation** of long‑acting PrEP. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Modify**

*   **Existing elements linkage updates:**
    *   *HIV test result*, *HIV test date*, *Date HIV test results returned* → **Add linkages** to **HIV.C (PrEP) activities** so these fields are consumable at LA‑PrEP dosing encounters. (No label change; linkage/annotation only.) [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

### HIV.C — PrEP/PEP visit

**Add**

*   **Option list extension (Medications prescribed / PrEP product prescribed):**
    *   **+ Lenacapavir (long‑acting injectable)** (new value)
    *   **+ Administration route:** *Injectable* (new supporting field if absent)
    *   **+ PrEP injection date:** *DateTime* (new field)
    *   **Rationale:** Introduce **LA lenacapavir** as prevention choice. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Linkage updates**

*   *PrEP product prescribed* → **Link to** *HIV.C7.DT* (suitability) and *HIV.C23.DT* (regimen determination). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### HIV.D — Care & Treatment (general)

**Add / Modify (for ART recommendations)**

*   **New/confirmed elements:**
    *   *Prior ARV exposure* (Boolean / categorical) → needed for backbone selection logic.
    *   *Weight* / *Weight band* (Quantity) → explicit linkage to regimen choice (≥30 kg vs <30 kg).
    *   *HBV infection status* (derived from HBsAg/anti‑HBc/anti‑HBs) → **Link to** ART simplification and LA CAB+RPV branching.
    *   *Regimen category* options: **DRV/r (preferred PI), ATV/r (alternative), LPV/r (alternative)** (ensure presence).
    *   *Switch regimen to DTG+3TC* (Action logging element) and *Switch regimen to CAB+RPV LA* (Action logging element) for traceability.  
        **Rationale:** Implement ART preference hierarchy, dual‑drug simplification, and LA CAB+RPV switching logic. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### HIV.E–F — PMTCT (pregnancy/post‑partum & infant)

**Add**

*   *Infant risk classification* (select one: **High risk / Not high risk**)
*   *Infant prophylaxis regimen* (options include **NVP single‑drug**, **ABC+3TC+DTG 3‑drug**)
*   *Prophylaxis start date* (Date) and *Planned prophylaxis duration* (Duration)
*   *Maternal viral suppression status* (Boolean) and *Date maternal suppression achieved* (Date)
*   *Enhanced breastfeeding (BF) support provided* (multi‑select: counselling, peer support, adherence plan, home visit, etc.)  
    **Rationale:** Align infant prophylaxis rules (6 weeks NVP for non‑high‑risk; 3‑drug ABC+3TC+DTG for high‑risk; step‑down NVP during BF until maternal suppression). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### HIV.D — TB/HIV (TPT)

**Add**

*   *Eligible for TPT* (Boolean)
*   *Chosen TPT regimen* (options: **3HP (preferred)**, 6H, 9H, 3HR, 1HP, 4R, 6Lfx)
*   *TPT start date*, *TPT completion date*, *TPT contraindications present* (Boolean/list)  
    **Rationale:** Implement 3HP preference with alternatives. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### HIV.D — Integrated comorbid care

**Add**

*   **Diabetes/Hypertension integration:**
    *   *Blood pressure* fields; *Diabetes screening result* (FBG/HbA1c), *HTN diagnosis*, *DM diagnosis*, *Referral provided*, *Treatment started*.  
        **Rationale:** Integrate NCD care per service‑delivery recommendations. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### HIV.D — Mental health integration

**Add**

*   *PHQ‑9 score*, *GAD‑7 score*, *AUDIT‑C score* (if adopted); *MH diagnosis flags*; *MH referral provided*; *MH treatment started*.  
    **Rationale:** Integrate mental health care within HIV services. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

***

## 2) `WHO-UCN-HHS-SIA-2023.28-eng.xlsx` — **Web Annex B (Decision‑Support logic & Schedules)** [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### PrEP decisions

**Modify — HIV.C7.DT (PrEP suitability)**

*   **Before:** LA options not including **lenacapavir**; HIV test acceptance agnostic to test type. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
*   **After:**
    *   **New input expression(s):** `"HIV test type"`, `"HIV test result"`, `"PrEP product prescribed"`
    *   **Rules:**
        *   IF `"HIV test type" = RDT` AND `"HIV test result" = Negative` AND risk criteria met → **Output:** *Recommend PrEP; include lenacapavir LA option*.
    *   **Guidance:** Clarify that RDT is acceptable for **initiation/continuation/discontinuation** of LA PrEP. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Modify — HIV.C23.DT (Determine PEP or PrEP regimen)**

*   **Add** new **Output Type** rows to **recommend lenacapavir (LA)** where eligible/available, with **scheduling hint** to S.1 for injection visits. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### ART regimen decisions

**Modify — HIV.D21.1.DT (Determine ART regimen)**

*   **Before:** First/second‑line preferences do not prioritize **DRV/r** explicitly and do not include **DTG+3TC simplification** or **LA CAB+RPV** as switch option. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
*   **After:**
    *   **PI hierarchy:** IF PI needed → **Preferred = DRV/r**, ELSE alternatives **ATV/r or LPV/r**.
    *   **Backbone selection:**
        *   IF `Age/weight ≥ 30 kg` → **Preferred backbone = TDF (or TAF) + 3TC/FTC** (even with prior TDF/AZT exposure).
        *   IF `< 30 kg` and on subsequent ART → **Suggested backbone = ABC + 3TC** or **TAF + 3TC/FTC**.
    *   **Simplification branch:** IF `VL undetectable` AND `No active HBV` → **Recommend DTG+3TC**.
    *   **Alternative switch:** IF `VL undetectable` AND `No active HBV` → **Recommend CAB+RPV LA** (where available).
    *   **Guidance text:** add clinical notes & cautions (HBV). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### AHD identification & monitoring

**Add/Modify — New “Identify AHD” or extend HIV.D12.DT**

*   **After:**
    *   **Preferred:** IF `CD4 available` THEN use **CD4** to classify AHD; **Else** use **WHO clinical staging**.
    *   **Actions:** trigger AHD package components as per local configuration.
    *   **HIV.S.2 schedules:** reinforce baseline CD4 and 6‑monthly until established on ART (already present)—**add note** that CD4 is **preferred** for AHD identification. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### PMTCT — infant prophylaxis & breastfeeding support

**Add/Modify — PMTCT infant management decision(s)**

*   **Rules:**
    *   IF `Infant risk = Not high` → **Recommend NVP single‑drug x 6 weeks**.
    *   IF `Infant risk = High` → **Recommend ABC + 3TC + DTG (3‑drug)**.
    *   IF `Completed 3‑drug` AND (`Breastfeeding = True` AND `Maternal suppression ≠ True`) → **Continue NVP single‑drug** until suppression or BF ends.
    *   **Hit policy:** *R* (Rule order) to execute applicable counseling + medication actions in sequence.
    *   **Guidance:** dosing/monitoring notes. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Add — Schedules (S.1 family)**

*   **Enhanced BF support** during breastfeeding for WLHIV: add visits/actions for counselling, peer support, adherence plan, home visit; **trigger** at delivery and periodic BF contacts; **completion** when documented. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### TB/HIV — TPT selection

**Add — New decision table or extend HIV.D12.DT**

*   **Rules:**
    *   **Preferred:** IF eligible AND no contraindications AND rifapentine available → **3HP**.
    *   **Alternative:** ELSE **6H/9H**.
    *   **Special circumstances:** **3HR, 1HP, 4R, 6Lfx** branches with appropriate annotations.
    *   **Schedules:** initiation, monthly checks (as needed), completion. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

### Service delivery

**Add — Transitional care after hospitalization**

*   **Schedules:** Trigger = *Inpatient discharge for PLHIV*; Actions: *phone follow‑up, home visit, peer support assignment, clinic appointment*. Completion when contact occurs/documented. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Modify — Adherence support integration in S.2**

*   Ensure adherence support interventions (counselling, reminders, lay support, education) are **scheduled and recorded** at ART initiation and during **elevated VL** follow‑up (some already reflected as completion criteria; add proactive entries). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

**Add — NCD & MH screening/management under D12 + S.1**

*   Add **BP/DM screening** and **MH screening (PHQ‑9, GAD‑7, AUDIT‑C)** with appropriate **referral/treatment** actions and follow‑up schedules. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

***

## 3) `WHO-UCN-HHS-SIA-2023.29-eng.xlsx` — **Web Annex C (Indicators)** [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

**Modify (value sets / disaggregation notes)**

*   **HIV.IND.2 / .3 / .4 (PrEP):**
    *   **Add value** under *PrEP product & formulation* = **“Lenacapavir (long‑acting injectable)”** (note: already supports “long‑acting injectable” as a category; we’re clarifying product value for country analytics).
    *   **Method of measurement (IND.4):** add local conversion for **person‑time of protection** specific to lenacapavir dosing, if you plan to use derived measures. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

**No core SI indicator changes required** for: PI preference updates, DTG+3TC simplification, LA CAB+RPV, AHD (CD4 preferred), PMTCT infant prophylaxis, TPT, transitional care, adherence support, NCD/MH integration. (These are mainly operational/clinical; you may add **local programme indicators** if desired.) [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## Representative “Before → After” snippets

> **Example 1 — ART decision (PI hierarchy)**  
> **Before (HIV.D21.1.DT excerpt):** PI choice not explicitly prioritizing **DRV/r**.   
> **After:** [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
>
> *   IF *PI indicated* AND *adult/adolescent* → **Output:** *MedicationRequest: DRV/r‑based regimen (Preferred)*; **Guidance:** “If DRV/r unavailable/contraindicated, consider **ATV/r** or **LPV/r**.” [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

> **Example 2 — PrEP suitability (RDT acceptance + LA lenacapavir)**  
> **Before (HIV.C7.DT):** Test type not used; LA lenacapavir not listed.   
> **After:** [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
>
> *   Rule: IF `"HIV test type" = RDT` AND `"HIV test result" = Negative` AND risk criteria met → **Action:** “Offer PrEP options including **lenacapavir (LA)**.” **Guidance:** “RDT result acceptable for LA‑PrEP initiation/continuation/discontinuation.” [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

> **Example 3 — PMTCT infant prophylaxis**  
> **Before:** No explicit 3‑drug **ABC+3TC+DTG** preference for **high‑risk** infants; step‑down during BF not encoded.   
> **After:** [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
>
> *   IF `Infant risk = High` → **Action:** “Start **ABC+3TC+DTG** (3‑drug) prophylaxis.”
> *   IF `Completed 3‑drug` AND (`BF = True` AND `Maternal suppression ≠ True`) → **Action:** “Continue **NVP single‑drug** until BF ends or maternal suppression achieved.” [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)

***

## Cross‑walk summary (Annex ↔ Annex)

*   **New/extended Data Elements (Annex A)** are referenced by updated **Decision Tables / Schedules (Annex B)**:
    *   *HIV test type* → **HIV.C7.DT / HIV.C23.DT** (RDT acceptance). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    *   *PrEP product = lenacapavir LA* → **HIV.C7.DT / HIV.C23.DT** (offer & dosing schedules). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    *   *Weight/Weight band, Prior ARV exposure, HBV status* → **HIV.D21.1.DT** (backbone selection, DTG+3TC, CAB+RPV LA switch). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    *   *Infant risk class, prophylaxis regimen, maternal suppression* → **PMTCT infant management rules** (NVP 6w; ABC+3TC+DTG; step‑down). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    *   *TPT eligibility/regimen* → **TPT decision & schedules**. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)
    *   *Adherence/Transitional care/NCD/MH fields* → **S.1/S.2 schedules and D12 screenings**. [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx), [\[WHO-UCN-HH...023.29-eng | Excel\]](WHO-UCN-HHS-SIA-2023.27-eng.xlsx)

*   **Indicators (Annex C)** remain **structurally unchanged**, except we **extend product value lists** for PrEP to explicitly include **lenacapavir LA** for country analytics. [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

***

## Next steps (my proposal)

1.  **You review this diff** and call out any additions you want removed or any missing items.
2.  I’ll produce **redlined workbooks** with:
    *   *CHANGELOG* tab documenting each inserted/edited row (sheet, row/ID, before, after, rationale, source).
    *   Validated **hit policies**, **UCUM units**, and **linkage checks** (no orphaned data elements or rule references). [\[HIV recs to test_v1 | Excel\]](HIV recs to test_v1.xlsx)
3.  Optional: add **local programme indicators** (infant prophylaxis coverage, LA CAB+RPV uptake, TPT coverage) to a **local Indicators** sheet for your dashboards (kept separate from core SI). [\[WHO-UCN-HH...023.28-eng | Excel\]](WHO-UCN-HHS-SIA-2023.29-eng.xlsx)

Would you like me to proceed to **apply these diffs** and return updated .xlsx files with the full CHANGELOG tabs, or do you want any tweaks to the plan first?

