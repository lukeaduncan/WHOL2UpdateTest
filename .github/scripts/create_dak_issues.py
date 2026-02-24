#!/usr/bin/env python3
"""
DAK GitHub Updater - Creates GitHub issues from HIV recommendations Excel.
Reads only Excel files. Maps each recommendation to affected DAK Excel files.
Uses GITHUB_TOKEN env var (set by GitHub Actions) to create issues.
"""

import os
import sys
import time
import json

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "lukeaduncan/WHOL2UpdateTest")
OWNER, REPO = REPOSITORY.split("/")

UPDATES_FILE = "HIV recs to test_v1.xlsx"

DAK_FILE_ROLES = {
    "WHO-UCN-HHS-SIA-2023.27-eng.xlsx": "Annex A - Data Dictionary",
    "WHO-UCN-HHS-SIA-2023.28-eng.xlsx": "Annex B - Decision Support Logic & Schedules",
    "WHO-UCN-HHS-SIA-2023.29-eng.xlsx": "Annex C - Indicators",
    "WHO-UCN-HHS-SIA-2023.30-eng.xlsx": "Annex D - Functional Requirements",
}

# ---------------------------------------------------------------------------
# Mapping: recommendation prefix → affected DAK files, sheets, and changes.
# Derived by reading each recommendation from the Excel and cross-referencing
# the DAK Excel sheet structures (2023.27, 2023.28, 2023.29).
# ---------------------------------------------------------------------------
MAPPING = {
    "HIV.TST.2025.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.B HTS visit", "HIV.C PrEP visit"],
                "changes": [
                    "HIV.B HTS visit: Add new data element 'HIV test type' (Coding, select-one; "
                    "options: Rapid diagnostic test (RDT), Laboratory assay, Self-test (reported)). "
                    "Required when 'HIV test conducted' = True. Add linkages to HIV.C7.DT and HIV.C23.DT.",
                    "HIV.B HTS visit: Modify existing elements 'HIV test result', 'HIV test date', "
                    "'Date HIV test results returned' — add linkages to HIV.C (PrEP) activities so "
                    "these fields are available at long-acting PrEP dosing encounters.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": [
                    "HIV.C7.DT PrEP Suitability",
                    "HIV.C23.DT PEP or PrEP Regimen",
                    "HIV.S.1 Recommended Services",
                ],
                "changes": [
                    "HIV.C7.DT PrEP Suitability: Add input column 'HIV test type'. Add rule row: "
                    "IF 'HIV test type' = 'RDT' AND 'HIV test result' = 'Negative' AND risk criteria "
                    "met → Output: 'Recommend PrEP (RDT accepted)'. Guidance: 'RDT result acceptable "
                    "for LA-PrEP initiation, continuation, and discontinuation.'",
                    "HIV.C23.DT PEP or PrEP Regimen: Add input logic to accept RDT-based negative "
                    "results at initiation and continuation of long-acting injectable PrEP.",
                    "HIV.S.1 Recommended Services: Add schedule row 'HIV test prior to LA-PrEP injection': "
                    "Trigger = PrEP injection due; Condition = 'PrEP product = long-acting injectable'; "
                    "Due date = same day as dosing; Completion = valid negative RDT result recorded.",
                ],
            },
        ]
    },
    "HIV.PRV.2025.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.C PrEP visit", "HIV.Prevention"],
                "changes": [
                    "HIV.C PrEP visit: Add 'Lenacapavir (long-acting injectable)' as a new option "
                    "value in the 'PrEP product prescribed' option list.",
                    "HIV.C PrEP visit: Add 'PrEP administration route' field (select-one; options: "
                    "Oral, Injectable) if not already present.",
                    "HIV.C PrEP visit: Add 'PrEP injection date' field (DateTime) if not already present.",
                    "HIV.C PrEP visit: Update linkages for 'PrEP product prescribed' to include "
                    "HIV.C7.DT and HIV.C23.DT.",
                    "HIV.Prevention: Add 'Lenacapavir (long-acting injectable)' to 'Medications "
                    "prescribed' option list.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": [
                    "HIV.C7.DT PrEP Suitability",
                    "HIV.C23.DT PEP or PrEP Regimen",
                    "HIV.S.1 Recommended Services",
                ],
                "changes": [
                    "HIV.C7.DT PrEP Suitability: Add rule rows for lenacapavir LA eligibility when "
                    "risk criteria are met and HIV-negative test is documented.",
                    "HIV.C23.DT PEP or PrEP Regimen: Add output row to recommend lenacapavir LA; "
                    "include dosing guidance and scheduling hint to HIV.S.1 for injection visits.",
                    "HIV.S.1 Recommended Services: Add/adjust visit cadence for lenacapavir dosing "
                    "cycle (injection due reminders at appropriate intervals).",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.29-eng.xlsx",
                "sheets": ["Indicator definitions"],
                "changes": [
                    "Indicator definitions: For HIV.IND.2 (Total PrEP recipients), HIV.IND.3 "
                    "(PrEP coverage), HIV.IND.4 (Volume of PrEP prescribed) — add 'Lenacapavir "
                    "(long-acting injectable)' as a value in the 'PrEP product and formulation' "
                    "disaggregation column.",
                    "Indicator definitions (HIV.IND.4): Add note in Method of measurement for "
                    "person-time of protection conversion specific to lenacapavir dosing cycle.",
                ],
            },
        ]
    },
    "HIV.VER.2021.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.S.1 Recommended Services: Verify existing breastfeeding support guidance "
                    "text is current and intact. No structural changes required — this recommendation "
                    "is unchanged from 2021.",
                ],
            },
        ]
    },
    "HIV.VER.2025.002": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.E-F PMTCT"],
                "changes": [
                    "HIV.E-F PMTCT: Add 'Enhanced BF support provided' (multi-select; options: "
                    "Counselling, Peer support, Adherence plan, Home visit scheduled, Other).",
                    "HIV.E-F PMTCT: Add 'Mother-infant pair retained in care' status element (Boolean).",
                    "HIV.E-F PMTCT: Link new elements to PMTCT follow-up schedules in HIV.S.1.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.S.1 Recommended Services: Add PMTCT follow-up schedule rows for enhanced "
                    "breastfeeding support contacts (facility and community-based) during the "
                    "breastfeeding period. Include actions for adherence support, peer support, and "
                    "visit reminders. Trigger at delivery and at periodic breastfeeding contacts.",
                ],
            },
        ]
    },
    "HIV.VER.2025.003": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.E-F PMTCT"],
                "changes": [
                    "HIV.E-F PMTCT: Add 'Infant risk classification' (select-one; options: "
                    "High risk, Not high risk).",
                    "HIV.E-F PMTCT: Add/confirm 'Infant prophylaxis regimen' option list includes "
                    "NVP single-drug and ABC+3TC+DTG 3-drug.",
                    "HIV.E-F PMTCT: Add 'Prophylaxis start date' (Date) and 'Planned prophylaxis "
                    "duration' (Duration; default 6 weeks for not-high-risk).",
                    "HIV.E-F PMTCT: Link all new elements to PMTCT infant management decision table.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "PMTCT infant management decision (create or extend existing table): Add rule: "
                    "IF 'Infant risk classification' = 'Not high risk' THEN Output: MedicationRequest "
                    "for NVP single-drug x 6 weeks. Include dosing guidance annotation.",
                ],
            },
        ]
    },
    "HIV.VER.2025.004": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.E-F PMTCT"],
                "changes": [
                    "HIV.E-F PMTCT: Extend 'Infant prophylaxis regimen' option list to include "
                    "'ABC+3TC+DTG (3-drug)'.",
                    "HIV.E-F PMTCT: Add dosing fields for weight/age bands as needed for 3-drug regimen.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "PMTCT infant management decision table: Add rule: IF 'Infant risk classification' "
                    "= 'High risk' THEN Output: MedicationRequest for ABC+3TC+DTG (3-drug regimen) "
                    "with dosing guidance. Use hit policy R with explicit priority over legacy rules.",
                ],
            },
        ]
    },
    "HIV.VER.2025.005": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.E-F PMTCT"],
                "changes": [
                    "HIV.E-F PMTCT: Add 'Maternal viral suppression status' (Boolean; derived "
                    "from viral load result).",
                    "HIV.E-F PMTCT: Add 'Date maternal suppression achieved' (Date).",
                    "HIV.E-F PMTCT: Confirm 'Breastfeeding status' element exists with correct "
                    "linkages to step-down logic.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen", "HIV.S.2 Monitoring ART response"],
                "changes": [
                    "PMTCT infant management decision table: Add step-down rule: IF infant completed "
                    "3-drug regimen AND breastfeeding = True AND maternal viral suppression ≠ True "
                    "THEN continue single-drug NVP until breastfeeding ends or maternal suppression "
                    "achieved.",
                    "HIV.S.2 Monitoring ART response: Add schedule row to check maternal VL at "
                    "recommended intervals during breastfeeding to evaluate the step-down stop "
                    "condition.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Ensure ART regimen option list includes DRV/r "
                    "(Darunavir/ritonavir) labelled as preferred boosted PI, with ATV/r and LPV/r "
                    "as listed alternatives.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Update first-line and second-line PI rule rows to "
                    "rank DRV/r (Darunavir/ritonavir) as the preferred boosted PI. Add guidance "
                    "annotation: 'If DRV/r unavailable or contraindicated, consider ATV/r or LPV/r "
                    "as alternatives.' Ensure consistency across adult, adolescent, and pediatric "
                    "branches.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.002": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Add/update rule rows to designate ATV/r "
                    "(Atazanavir/ritonavir) and LPV/r (Lopinavir/ritonavir) as alternative boosted "
                    "PI options when DRV/r is not available or suitable. These should appear as "
                    "fallback outputs after DRV/r in rule priority order.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.003": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add/confirm 'Weight' or 'Weight band' (Quantity/select) "
                    "data element with explicit linkage to HIV.D21.1.DT backbone selection.",
                    "HIV.D Care-Treatment: Add/confirm 'Prior ARV exposure' (Boolean or categorical) "
                    "data element with linkage to HIV.D21.1.DT.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Add/refine backbone selection rule: IF weight ≥ 30 kg "
                    "(adults/adolescents/children) THEN preferred NRTI backbone = TDF (or TAF) + 3TC "
                    "(or FTC) for both initial and subsequent ART, including patients with prior TDF "
                    "or AZT exposure. Add 'Prior ARV exposure' as explicit input column.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.004": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Add rule: IF child weight < 30 kg AND on subsequent "
                    "ART THEN suggested NRTI backbone = ABC+3TC OR TAF+3TC/FTC. Be explicit on "
                    "weight/age cut-point input columns.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.005": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment", "HIV.G Diagnostics"],
                "changes": [
                    "HIV.D Care-Treatment: Ensure HBV infection status element exists (derived from "
                    "HBsAg/anti-HBc/anti-HBs) and is linked to HIV.D21.1.DT.",
                    "HIV.G Diagnostics: Confirm HBsAg, anti-HBc, anti-HBs fields exist and feed "
                    "into HBV infection status derivation.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Add simplification branch rule: IF viral load "
                    "undetectable AND HBV infection status = Negative THEN recommend DTG+3TC for "
                    "treatment simplification. Add guidance: 'Contraindicated in patients with "
                    "active HBV co-infection.'",
                ],
            },
        ]
    },
    "HIV_HEP.TRT.2025.006": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add 'CAB+RPV (long-acting injectable)' to 'Medications "
                    "prescribed' (treatment) option list.",
                    "HIV.D Care-Treatment: Add 'ART administration route' field (select-one; options: "
                    "Oral, Injectable) if not already present.",
                    "HIV.D Care-Treatment: Add injection scheduling field (e.g., 'CAB+RPV injection "
                    "date') if not present. Ensure linkage to HBV infection status for "
                    "contraindication checking.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D21.1.DT ART Regimen", "HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.D21.1.DT ART Regimen: Add alternative switch rule: IF viral load "
                    "undetectable AND HBV negative AND patient is virologically suppressed "
                    "adult/adolescent THEN recommend CAB+RPV LA as alternative switching option "
                    "(where available). Include guidance on HBV contraindication.",
                    "HIV.S.1 Recommended Services: Add injection visit schedule entries for "
                    "CAB+RPV LA dosing cycle (similar pattern to existing viral-load review "
                    "schedules).",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.29-eng.xlsx",
                "sheets": ["Indicator definitions"],
                "changes": [
                    "Indicator definitions: ART.1 (People on ART) — add optional local "
                    "disaggregation note for 'regimen category: LA CAB+RPV' to support "
                    "country-level programme tracking.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.007": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment", "HIV.G Diagnostics"],
                "changes": [
                    "HIV.D Care-Treatment: Confirm CD4 count element exists and has explicit "
                    "linkage to advanced HIV disease (AHD) identification decision.",
                    "HIV.G Diagnostics: Confirm CD4 count field links to AHD identification logic.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D12.DT Det Screenings", "HIV.S.2 Monitoring ART response"],
                "changes": [
                    "HIV.D12.DT Det Screenings: Add/update AHD identification rule: IF CD4 test "
                    "result available THEN use CD4 threshold to identify advanced HIV disease. "
                    "Add action to trigger AHD management package when AHD identified.",
                    "HIV.S.2 Monitoring ART response: Reinforce baseline CD4 at "
                    "diagnosis/ART initiation schedule. Add annotation that CD4 is the preferred "
                    "method for AHD identification.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.008": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D12.DT Det Screenings", "HIV.D15.DT Clinical stage HIV "],
                "changes": [
                    "HIV.D12.DT Det Screenings: Add fallback AHD identification rule: IF CD4 "
                    "testing not available THEN use WHO clinical staging to identify advanced HIV "
                    "disease. Must follow the CD4-based rule in priority order.",
                    "HIV.D15.DT Clinical stage HIV: Verify existing WHO clinical staging logic "
                    "is current and linked to the AHD identification rule in HIV.D12.DT.",
                ],
            },
        ]
    },
    "HIV.TRT.2025.009": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add 'Kaposi sarcoma (KS) diagnosed' flag (Boolean).",
                    "HIV.D Care-Treatment: Add 'Planned KS chemotherapy regimen' (select-one; "
                    "options: Paclitaxel, Pegylated liposomal doxorubicin (PLD)).",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D12.DT Det Screenings"],
                "changes": [
                    "HIV.D12.DT Det Screenings: Add decision rule: IF 'Kaposi sarcoma diagnosed' "
                    "= True THEN create ServiceRequest/MedicationRequest for paclitaxel OR "
                    "pegylated liposomal doxorubicin (per local availability). Add guidance for "
                    "oncology referral coordination. Use hit policy F.",
                ],
            },
        ]
    },
    "HIV.TBH.2025.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D HIV-TB"],
                "changes": [
                    "HIV.D HIV-TB: Add 'Eligible for TPT' (Boolean).",
                    "HIV.D HIV-TB: Add 'Chosen TPT regimen' (select-one; options: 3HP - "
                    "Rifapentine+INH 3 months (Preferred), 6H, 9H, 3HR, 1HP, 4R, 6Lfx).",
                    "HIV.D HIV-TB: Add 'TPT start date' (Date), 'TPT completion date' (Date), "
                    "'TPT contraindications present' (Boolean).",
                    "HIV.D HIV-TB: Link all TPT elements to TPT decision table and indicators.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": [
                    "HIV.D4.DT Screen for TB",
                    "HIV.D12.DT Det Screenings",
                    "HIV.S.1 Recommended Services",
                ],
                "changes": [
                    "HIV.D4.DT / HIV.D12.DT: Add/extend 'Select TPT regimen' decision logic: "
                    "Rule 1 (Preferred): IF eligible AND no contraindications AND rifapentine "
                    "available THEN recommend 3HP. "
                    "Rule 2 (Alternative): ELSE recommend 6H or 9H. "
                    "Rule 3+ (Special): Branches for 3HR, 1HP, 4R, 6Lfx with clinical annotations.",
                    "HIV.S.1 Recommended Services: Add TPT follow-up schedule rows: initiation "
                    "visit, monthly monitoring visits as required, completion documentation.",
                ],
            },
        ]
    },
    "HIV.SRV.2025.001": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment", "HIV.H Follow-up"],
                "changes": [
                    "HIV.D Care-Treatment / HIV.H Follow-up: Add transitional care data elements: "
                    "'Pre-discharge goal set' (Boolean), 'Medication review completed' (Boolean), "
                    "'Transitional care plan documented' (Boolean), 'Phone follow-up scheduled' "
                    "(Boolean/Date), 'Home visit scheduled' (Boolean/Date), 'Peer support assigned' "
                    "(Boolean).",
                    "Link all new elements to post-discharge follow-up schedule in HIV.S.1.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.S.1 Recommended Services: Add new schedule set: Trigger = inpatient "
                    "discharge for PLHIV. Schedule rows for: phone follow-up (within 48-72h), "
                    "home visit (within 1-2 weeks), peer support assignment, outpatient clinic "
                    "appointment. Completion = documented contact/attendance.",
                ],
            },
        ]
    },
    "HIV.SRV.2025.002": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add 'Adherence support provided' (multi-select; options: "
                    "Individual counselling, Group counselling, SMS reminder, Peer/lay support, "
                    "Patient education, Other).",
                    "HIV.D Care-Treatment: Add 'Adherence plan agreed' (Boolean).",
                    "Link new elements to HIV.S.2 monitoring schedules.",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.S.2 Monitoring ART response"],
                "changes": [
                    "HIV.S.2 Monitoring ART response: Confirm adherence support is a completion "
                    "criterion in existing VL monitoring lines.",
                    "HIV.S.2 Monitoring ART response: Add proactive schedule row for adherence "
                    "support interventions at ART initiation.",
                    "HIV.S.2 Monitoring ART response: Add proactive schedule row for adherence "
                    "support at elevated VL follow-up visits.",
                ],
            },
        ]
    },
    "HIV_DIA_HTN.SRV.2025.003": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add 'Blood pressure (systolic)' and 'Blood pressure "
                    "(diastolic)' (Quantity) or a combined BP measurement field.",
                    "HIV.D Care-Treatment: Add 'Diabetes screening result' (select or Quantity; "
                    "FBG or HbA1c).",
                    "HIV.D Care-Treatment: Add 'Hypertension diagnosis' (Boolean) and 'Diabetes "
                    "diagnosis' (Boolean).",
                    "HIV.D Care-Treatment: Add 'NCD referral provided' (Boolean) and 'NCD "
                    "treatment started' (Boolean).",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D12.DT Det Screenings", "HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.D12.DT Det Screenings: Add screening rules for blood pressure measurement "
                    "and diabetes screening (FBG/HbA1c) per recommended periodicity for PLHIV.",
                    "HIV.S.1 Recommended Services: Add schedule rows for hypertension/diabetes "
                    "management follow-up and referral actions.",
                ],
            },
        ]
    },
    "HIV_MNH.SRV.2025.004": {
        "affected": [
            {
                "file": "WHO-UCN-HHS-SIA-2023.27-eng.xlsx",
                "sheets": ["HIV.D Care-Treatment"],
                "changes": [
                    "HIV.D Care-Treatment: Add 'PHQ-9 score' (Integer/Quantity) for depression "
                    "screening.",
                    "HIV.D Care-Treatment: Add 'GAD-7 score' (Integer/Quantity) for anxiety "
                    "screening.",
                    "HIV.D Care-Treatment: Add 'AUDIT-C score' (Integer/Quantity) for alcohol use "
                    "disorder screening.",
                    "HIV.D Care-Treatment: Add 'Mental health diagnosis' flag(s) (Boolean or select).",
                    "HIV.D Care-Treatment: Add 'Mental health referral provided' (Boolean) and "
                    "'Mental health treatment started' (Boolean).",
                ],
            },
            {
                "file": "WHO-UCN-HHS-SIA-2023.28-eng.xlsx",
                "sheets": ["HIV.D12.DT Det Screenings", "HIV.S.1 Recommended Services"],
                "changes": [
                    "HIV.D12.DT Det Screenings: Add mental health screening rules: PHQ-9 for "
                    "depression, GAD-7 for anxiety, AUDIT-C for alcohol use disorders. Include "
                    "referral/treatment action outputs.",
                    "HIV.S.1 Recommended Services: Add schedule rows for mental health referral "
                    "follow-up and ongoing care.",
                ],
            },
        ]
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_mapping_key(rec_num: str):
    clean = rec_num.strip().replace(" ", "")
    for key in MAPPING:
        if clean.startswith(key.replace(" ", "")):
            return key
    parts = clean.split(".")
    for key in MAPPING:
        kparts = key.split(".")
        if len(parts) >= 3 and len(kparts) >= 3 and parts[:3] == kparts[:3]:
            return key
    return None


def ensure_label(headers: dict, name: str, color: str, description: str = ""):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/labels"
    r = requests.get(f"{url}/{requests.utils.quote(name)}", headers=headers)
    if r.status_code == 404:
        requests.post(url, headers=headers,
                      json={"name": name, "color": color, "description": description})


def format_body(rec_num, rec_text, rec_type, topic, rationale, prev, info):
    lines = ["## Summary\n"]
    lines += [
        f"**Recommendation ID:** `{rec_num.strip()}`  ",
        f"**Recommendation Type:** {rec_type}  ",
        f"**Topic Area:** {topic}  ",
        "",
        f"> {rec_text}",
        "",
    ]
    if prev and str(prev).strip() not in ("", "nan"):
        lines += [f"**Previous recommendation:** {prev}", ""]
    lines += [f"## Rationale\n{rationale}\n", "## Affected DAK Files\n"]
    for item in info.get("affected", []):
        role = DAK_FILE_ROLES.get(item["file"], item["file"])
        lines += [
            f"### `{item['file']}` — {role}",
            f"**Target sheets:** {', '.join(item['sheets'])}",
            "",
            "**Required changes:**",
        ]
        for j, c in enumerate(item["changes"], 1):
            lines.append(f"{j}. {c}")
        lines.append("")
    lines += ["## Implementation Instructions\n",
              "Implement all changes listed above in the respective DAK Excel files:\n"]
    for item in info.get("affected", []):
        lines.append(f"**`{item['file']}`:**")
        for j, c in enumerate(item["changes"], 1):
            lines.append(f"{j}. {c}")
        lines.append("")
    lines += [
        "Preserve all existing Excel formatting, data validation, merged cells, and "
        "conditional formatting.",
        "",
        "---",
        "_Auto-generated by the DAK GitHub Updater._",
        "_@copilot — please implement this change and open a pull request._",
    ]
    return "\n".join(lines)


def create_issue(headers, title, body, labels, assignees):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    payload = {"title": title, "body": body, "labels": labels, "assignees": assignees}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 422 and assignees:
        payload["assignees"] = []
        payload["body"] = body + (
            "\n\n---\n_@copilot — please implement this change and open a pull request._"
        )
        r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 201:
        d = r.json()
        return {"success": True, "number": d["number"], "url": d["html_url"], "title": title}
    return {
        "success": False,
        "status_code": r.status_code,
        "error": r.text[:300],
        "title": title,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Read recommendations from Excel only
    df = pd.read_excel(UPDATES_FILE, sheet_name="Sheet1", dtype=str)
    df = df.dropna(subset=["Recommendation Number"])
    print(f"Found {len(df)} recommendations in {UPDATES_FILE}\n")

    # Ensure labels exist
    ensure_label(headers, "dak-update", "0075ca", "DAK Excel file update")
    ensure_label(headers, "data-dictionary", "e4e669", "Annex A Data Dictionary update")
    ensure_label(headers, "decision-logic", "d93f0b", "Annex B Decision Logic update")
    ensure_label(headers, "indicators", "0e8a16", "Annex C Indicators update")

    results = []
    for _, row in df.iterrows():
        rec_num  = str(row.get("Recommendation Number", "")).strip()
        rec_type = str(row.get("Recommendation Type", "")).strip()
        topic    = str(row.get("Topic Area", "")).strip()
        rec_text = str(row.get("Recommendation Text", "")).strip()
        rationale= str(row.get("Rationale for change", "")).strip()
        prev     = row.get("Previous recommendations", "")

        key  = get_mapping_key(rec_num)
        info = MAPPING.get(key, {"affected": []}) if key else {"affected": []}
        if not key:
            print(f"  WARNING: No mapping found for {rec_num}")

        labels = ["dak-update"]
        files  = [i["file"] for i in info.get("affected", [])]
        if any("27" in f for f in files):
            labels.append("data-dictionary")
        if any("28" in f for f in files):
            labels.append("decision-logic")
        if any("29" in f for f in files):
            labels.append("indicators")

        short = rec_text[:65] + "..." if len(rec_text) > 65 else rec_text
        title = f"[DAK Update] {rec_type} - {topic}: {short}"
        body  = format_body(rec_num, rec_text, rec_type, topic, rationale, prev, info)

        print(f"Creating issue for: {rec_num}")
        result = create_issue(headers, title, body, labels, ["copilot"])
        results.append(result)

        if result["success"]:
            print(f"  ✓ #{result['number']}: {result['url']}")
        else:
            print(f"  ✗ Failed ({result.get('status_code')}): {result.get('error', '')[:120]}")

        time.sleep(1.0)

    succeeded = sum(1 for r in results if r["success"])
    failed = len(results) - succeeded
    print(f"\n{'='*60}")
    print(f"Complete: {succeeded} issues created, {failed} failed.")
    print("\nCreated issues:")
    for r in results:
        if r["success"]:
            print(f"  #{r['number']}: {r['url']}")

    if failed > 0:
        print("\nFailed:")
        for r in results:
            if not r["success"]:
                print(f"  {r['title']}")

    # Write results summary
    with open("dak-issues-results.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\nResults saved to dak-issues-results.json")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
