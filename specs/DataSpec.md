# Data Spec (Data Specification)
## 1. Sources & Rights
- Data source description
- Data retention period and access roles
- Data legality and access control description (to be clarified before import)

## 2. Data Versioning
- Dataset version naming convention (to be enforced via DVC or lakeFS)
- Note: Each model training run must reference a specific dataset version

## 3. Schema & Semantics
- Data dictionary: description of the meaning and standardization rules for each field
- Include examples of valid and invalid records

## 4. Labeling Protocol
- Labeling guidelines
- Inter-annotator agreement (kappa) threshold
- Note: Labeling will be performed using Label Studio or Prodigy, with quality gates established

## 5. Coverage & Balance
- Minimum count coverage table for key segments
- Note: Analysis notebooks will be used to ensure rare cases are covered
