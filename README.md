
## AI-CDSS CLI tool

```bash
$ ai-cdss-cli --help
                                                                                                                                                                      
 Usage: ai-cdss-cli [OPTIONS] COMMAND [ARGS]...                                                                                                                       
                                                                                                                                                                      
 CLI for the AI-CDSS Client.                                                                                                                                          
                                                                                                                                                            
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                        Show this message and exit.                                                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ recommend                  Generate treatment recommendations for a given patient.                                                                                 │
│ compute-metrics            Computes Patient-Protocol Fit (PPF) based on loaded data. Returns the computed PPF with contributions.                                  │
│ compute-protocol-metrics   Computes Protocol Similarity Metrics based on loaded data. Returns the computed metrics.                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Usage

### **recommend** command

```bash
$ ai-cdss-cli recommend --help
                                                                                                                                                                      
 Usage: ai-cdss-cli recommend [OPTIONS]                                                                                                                               
                                                                                                                                                                      
 Generate treatment recommendations for a given patient.                                                                                                              
                                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --study-id           -s      INTEGER  Repeat this option to provide multiple integers. [default: None] [required]                                               │
│    --n                  -n      INTEGER  Number of recommendations per patient. [default: None]                                                                    │
│    --days               -d      INTEGER  Number of days to cover in the recommendation [default: None]                                                             │
│    --protocols-per-day  -p      INTEGER  Number of protocols per day. [default: None]                                                                              │
│    --env-file           -e      PATH     Path to a .env file with environment variables. [default: None]                                                           │
│    --help                                Show this message and exit.                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### **compute-metrics** command

Precompute PPF when a patient signs up to clinical study.

```bash
$ ai-cdss-cli compute-metrics --help

 Usage: ai-cdss-cli compute-metrics [OPTIONS]                                                                                                                         
                                                                                                                                                                      
 Computes Patient-Protocol Fit (PPF) based on loaded data. Returns the computed PPF with contributions.                                                                                   
                                                                                                                                                                      
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --patient-id  -p      INTEGER  Patient ID to compute metrics for. [default: None] [required]                                                                    │
│    --env-file    -e      PATH     Path to a .env file with environment variables. [default: None]                                                                  │
│    --help                         Show this message and exit.                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

**Scenario**

When a new patient is recruited for a study, clinicians will have to input the patient details through the MIMS - Medical Information Management System. Including information about baseline clinical assessments, study start date, and whether this patient needs recommendations. Once the patient is registered, the precomputation of PPF needs to be triggered, in order to update the internal files powering the AI-CDSS engine.

<p align="center">
  <img width="1317" height="1191" alt="image" src="https://github.com/user-attachments/assets/13e1f60c-8cc1-461e-95d8-083c4b210d8b" style="width:40%; height:auto;"/>
</p>

### **compute-protocol-metrics**

```bash
$ ai-cdss-cli compute-protocol-metrics --help
                                                                                                                                                                      
 Usage: ai-cdss-cli compute-protocol-metrics [OPTIONS]                                                                                                                
                                                                                                                                                                      
 Computes Protocol Similarity Metrics based on loaded data. Returns the computed metrics.                                                                                                 
                                                                                                                                                                      
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --env-file  -e      PATH  Path to a .env file with environment variables. [default: None]                                                                          │
│ --help                    Show this message and exit.                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

**Scenario**

<p align="center">
  <img width="829" height="1172" alt="image" src="https://github.com/user-attachments/assets/6087e74e-4908-4fb3-ad53-23ed039ffb32" />
</p>

When a new protocol is included in the RGS platform, for the CDSS system to work, the attributes that this protocol target will need to be inputted. In order for the system to compute similarity with other RGS protocols.

<p align="center">
<img width="829" height="1172" alt="image" src="https://github.com/user-attachments/assets/deb4fabb-2968-4e1b-9fdb-a37b9f329592" style="width:40%; height:auto;"/>
</p>
