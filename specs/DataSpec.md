# Data Spec (Data Specification)
Chinese Folk Music AI Generation Dataset

## 1. Sources & Rights
### 1.1 Data source description
This dataset is built for training a generative AI model that creates Chinese folk music MIDI and visual sheet music.

Data sources include:
- Publicly licensed Chinese folk music melody libraries
- Tagged MIDI collections of traditional instruments (guzheng, erhu, dizi, etc.)
- Manually composed training samples for emotions, styles, and scenes
- User-provided valid creative data (authorized)

### 1.2 Data retention period and access roles
- Retention period: Permanent (for research and model training)
- Access roles:
  - Admin: full access
  - Developer: read and use
  - Tester: read only
  - External users: no access

### 1.3 Data legality and access control
All data used is:
- Non-copyright-infringing
- Royalty-free for training
- Non-personal and non-sensitive
Access control is enforced before data import. No private or unauthorized data is allowed.

## 2. Data Versioning
### 2.1 Dataset version naming convention
Versions follow the rule:
`v[major].[minor]`
Example:
- v1.0 (initial complete dataset)
- v1.1 (added 100 emotion-style records)
- v2.0 (major structure update)

### 2.2 Management tool
Versioning is managed via:
- DVC (Data Version Control)
- Or GitHub tracking for small datasets

### 2.3 Training binding rule
Every model training run **must reference a fixed dataset version** to ensure reproducibility.

## 3. Schema & Semantics
### 3.1 Data dictionary
All records follow this standardized schema:

| Column | Type | Meaning | Rule |
|--------|------|---------|------|
| emotion | string | Emotion of the music | Required: happy, sad, calm, excited, nostalgic, festive |
| style | string | Folk music style | Required: guzheng solo, erhu solo, dizi solo, folk ensemble, ancient style |
| keywords | string | Scene keywords | 1–5 keywords split by commas |
| instrument | string | Main instrument | Required: guzheng, erhu, dizi, pipa, ensemble |
| duration | int | Music length | 15–60 seconds |
| source | string | Data source | Manual, Public, Licensed, User |

### 3.2 Valid record example

### 3.3 Invalid record examples
- Empty emotion: `,,river,guzheng,30,Manual`
- Duration out of range: `sad,erhu solo,homesick,erhu,100,Public`
- Wrong instrument: `calm,ensemble,forest,piano,30,Licensed`

## 4. Labeling Protocol
### 4.1 Labeling guidelines
Labelers must follow:
- Emotion must match the music style
- Keywords must reflect the scene
- Instruments must be traditional Chinese instruments
- Duration must be within 15–60 seconds

### 4.2 Inter-annotator agreement threshold
- Inter-annotator agreement (Kappa score) ≥ 0.85
- Labels below threshold are re-checked or removed

### 4.3 Labeling tools and quality gates
- Labeling tool: Label Studio
- Quality gates:
  - No empty fields
  - No wrong instruments
  - No out-of-range duration

## 5. Coverage & Balance
### 5.1 Minimum coverage requirement
Key segments must meet minimum sample counts:

| Segment | Min Count |
|---------|-----------|
| Each emotion | ≥ 20 |
| Each instrument | ≥ 20 |
| Each style | ≥ 15 |
| Short duration (15s) | ≥ 10 |
| Long duration (60s) | ≥ 10 |

### 5.2 Balance requirement
- No single emotion > 40% of total data
- No single instrument > 35% of total data
- No single source > 50% of total data

### 5.3 Coverage verification
Analysis notebooks will be used to:
- Verify coverage of rare cases
- Ensure balance across classes
- Detect bias or missing segments
  
