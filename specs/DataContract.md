# Data Contract
Chinese Folk Music AI Generation Dataset - Data Contract
## Description
This document serves as the data contract for the dataset of the Chinese folk music AI generation system. It specifies the constraints, validation rules, and data quality standards that the dataset must comply with, ensuring the data conforms to specifications during import, usage, and update processes. Failure to meet the contract will trigger a CI check failure and prohibit the dataset from being used for model training.

## 1. Data Format Contract
### 1.1 File Format
- Dataset file format: **CSV** (comma-separated, UTF-8 encoding)
- Prohibited formats: JSONL, Excel, TXT (only CSV is supported to meet assignment requirements)
- File naming convention: `folk_music_dataset_v[version].csv` (Example: folk_music_dataset_v1.0.csv)

### 1.2 Record Delimiter & Encoding
- Field delimiter: comma (,); other delimiters such as semicolons and spaces are prohibited
- Encoding: UTF-8 (ensures proper display of Chinese emotions, styles, and keywords without garbled characters)
- Line break: Unix format (\n); Windows format (\r\n) is avoided to prevent parsing errors

### 1.3 Null Value Handling
- Null values (NULL/empty strings) are prohibited; all mandatory fields must contain valid values
- If data is missing, leaving it blank directly is prohibited; it must be marked as "To be supplemented" (only allowed in temporary versions; official versions must have no missing data)

## 2. Field-Level Contract
Strictly follow the 6 fields defined in DataSpec.md, with the following constraints for each field (must be fully satisfied):

| Column | Type | Constraints | Forbidden Values |
|--------|------|-------------|-----------------|
| emotion | string | 1-20 characters, only allowed enumerated values: happy, sad, calm, excited, nostalgic, festive | Null values, numbers, special symbols, non-enumerated emotions (e.g., angry, bored) |
| style | string | 1-30 characters, only allowed enumerated values: guzheng solo, erhu solo, dizi solo, folk ensemble, ancient style | Null values, numbers, special symbols, non-folk music styles (e.g., rock, pop) |
| keywords | string | 1-5 keywords separated by commas, each keyword 1-15 characters | Null values, single keyword exceeding 15 characters, more than 5 keywords |
| instrument | string | 1-20 characters, only allowed enumerated values: guzheng, erhu, dizi, pipa, ensemble | Null values, numbers, special symbols, non-Chinese traditional instruments (e.g., piano, guitar) |
| duration | int | Value range: 15-60 (unit: seconds), no decimals | Null values, decimals, integers less than 15 or greater than 60 |
| source | string | 1-20 characters, only allowed enumerated values: Manual, Public, Licensed, User | Null values, numbers, special symbols, other undefined data sources |

## 3. Data Quality Contract
### 3.1 Syntax Quality
1. All fields comply with the above field-level contract with no formatting errors
2. No null values, garbled characters, or unparseable characters (e.g., �, □)
3. CSV file is not corrupted (can be opened normally with Excel and Notepad, no messy or incorrect rows)

### 3.2 Structural Quality
1. No duplicate records (records with identical values across all 6 fields are prohibited)
2. No data leakage (the dataset contains no personal information, copyright data, or sensitive data)
3. No label/data mismatch (e.g., instrument marked as guzheng but style marked as erhu solo)
4. Fixed field order (must be: emotion,style,keywords,instrument,duration,source; no arbitrary adjustments allowed)

### 3.3 Statistical Quality
1. Category balance: the proportion of any single emotion, instrument, or style shall not exceed 40% of the total data
2. No distribution shift: the field distribution of new data is consistent with historical data (e.g., the average value of duration fluctuates within ±5 seconds)
3. Reasonable data sources: the proportion of any single data source shall not exceed 50% of the total data to avoid model bias caused by a single source

## 4. Data Validation Rules
All data must pass the following validations; failure to pass will be deemed a breach of contract:
1. Field validation: each field must comply with the constraints of the Field-Level Contract, with verification of field type, value range, and forbidden values one by one
2. Format validation: file format, encoding, and delimiter comply with the Data Format Contract
3. Quality validation: pass three types of quality checks (syntax, structural, statistical), corresponding to the 10 automated checks required by the assignment
4. Version validation: dataset version naming complies with the version specifications in DataSpec.md with no version confusion

## 5. CI Integration
### 5.1 CI Check Requirements
- Integrate GitHub Actions to automatically perform data validation each time the dataset or DataContract.md is submitted
- Validation content: contract compliance, 10 automated data checks (3 syntax, 4 structural, 3 statistical)
- Failure rule: if any validation fails, the CI status will turn red (failed), prohibiting deployment and use for model training

### 5.2 Contract Violation Handling
- If the data contract is violated, the use of the dataset must be stopped immediately
- Troubleshoot issues (e.g., formatting errors, invalid fields, substandard quality) and resubmit for validation after correction
- All contract modifications must be synchronized with updates to DataContract.md, with version change records annotated

## 6. Contract Versioning
### 6.1 Version Naming
Consistent with dataset versioning, following the `v[major].[minor]` rule (e.g., v1.0, v1.1)
- Major version: upgraded when fields are added/deleted or core constraints are changed
- Minor version: upgraded when constraint details are optimized or validation rules are adjusted

### 6.2 Version Binding
- Each dataset version must be bound to a unique DataContract version
- After a contract version change, all historical datasets must be revalidated to ensure compatibility
