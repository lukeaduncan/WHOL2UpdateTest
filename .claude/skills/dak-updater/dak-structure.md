# SMART Guidelines DAK - Common Excel File Structure

## Overview

WHO SMART Guidelines Digital Adaptation Kits (DAKs) are structured as Excel workbooks containing standardized sheets that define the digital health intervention logic. Each DAK covers a specific health area (e.g., HIV, Immunization, ANC) and follows a consistent structure.

## Common Sheet Types

### Health Interventions & Recommendations
- Contains the health recommendations from WHO guidelines
- Key columns: Recommendation ID, Recommendation, Guideline Source, Strength, Quality of Evidence

### Business Processes and Workflows
- Defines the workflows and business processes
- Key columns: Process ID, Process Name, Task, Input, Output

### Core Data Elements / Data Dictionary
- Defines all data elements used across the DAK
- Key columns: Data Element ID, Data Element Label, Description, Data Type, Input Options, Validation, Multiple Choice (if applicable)

### Decision-support Logic / Decision Tables
- Contains the clinical decision logic
- Key columns: Decision ID, Activity ID, Input, Output, Condition, Action, Annotation, Reference

### Scheduling Logic
- Defines scheduling rules for services
- Key columns: Schedule ID, Activity, Due Date Logic, Overdue, Expiry

### Indicators & Performance Metrics
- Defines monitoring indicators
- Key columns: Indicator ID, Indicator Name, Numerator, Denominator, Disaggregation, Reference

### Functional Requirements
- Maps business requirements to system functionality
- Key columns: Requirement ID, Category, Requirement, Activity ID, As a..., I want..., So that...

### Component (L2) Sheets
- L2 refers to the Level 2 adaptation layer
- These are typically the sheets most frequently updated
- Changes to L2 often cascade to decision tables and indicators

## Key Identifiers

- **Activity ID**: Format like `HIV.B7.DT` — identifies specific clinical activities
- **Data Element ID**: Format like `HIV.B.DE1` — identifies data elements  
- **Decision ID**: Links to specific decision table entries
- **Indicator ID**: Format like `HIV.IND.1` — identifies indicators

## File Naming Conventions

DAK files are typically named like:
- `HIV_DAK.xlsx` or `SMART-HIV-DAK.xlsx`
- `ANC_DAK.xlsx` or `SMART-ANC-DAK.xlsx`
- Sometimes split into multiple files per component

## Important Considerations

- Column headers may vary slightly between DAKs — always inspect the actual file
- Some DAKs use merged cells for grouping — handle with care
- Data validation dropdowns may be present — preserve them when modifying
- Conditional formatting rules should be preserved
- Some cells contain formulas (e.g., for indicator calculations)
