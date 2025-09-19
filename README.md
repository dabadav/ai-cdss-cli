
## AI-CDSS CLI tool

### Installation

Install directly from GitHub:

- Lastest release:

```bash
pip install "git+https://github.com/dabadav/ai-cdss-cli.git@v0.1.2"
```

- Use a python version of >= 3.12 to install the package

```bash
python -m pip install "git+https://github.com/dabadav/ai-cdss-cli.git@v0.1.2"
```

### CLI Entrypoint

After installation, run the CLI tool with:

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

### .env file

A .env filepath must be used as argument to the cli tool to define the DB credentials. It expects these fields:
```
DB_USER=
DB_PASS=
DB_HOST=
DB_NAME=
```


## How to use?

The system is expected to be used in three scenarios: i) when recommending weekly schedule for patients, ii) when new patient registered in a study, and iii) when new protocol is added to RGS.

#### **i) Weekly Recommendations - **recommend** command**

Example for running recommendations in production environment for patients that are in study 42, or patients with id 7 and id 8:

```
# All patients in study 42  (study-level run, applies weekly filters)
$ ai-cdss-cli recommend -s 42

# Specific patients 7 and 8  (direct run, skips weekly filters)
$ ai-cdss-cli recommend -p 7 -p 8
```

---

Here’s an updated **README snippet** that reflects the new behaviour and clarifies when the weekly-milestone filters apply.

---

#### **i) Weekly Recommendations – `recommend` command**

You can generate recommendations either **for an entire study cohort** or **for specific patients**.

```
# All patients in study 42  (study-level run, applies weekly filters)
$ ai-cdss-cli recommend -s 42

# Specific patients 7 and 8  (direct run, skips weekly filters)
$ ai-cdss-cli recommend -p 7 -p 8
```

**How patient selection works:**

| Mode                    | Command               | Filters applied                                                                                                                                            | Typical use                                                                                                             |
| ----------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Study mode**          | `--study-id` / `-s`   | **Weekly-milestone filters are enforced:**<br>• `RECOMMEND = 1`<br>• `start_date <= today <= end_date`<br>• `DATEDIFF(CURDATE(), start_date) % 7 = 0`    | Daily/cron job to issue new weekly prescriptions for all eligible patients in the study.                                |
| **Direct patient mode** | `--patient-id` / `-p` | *No automatic filters*. Recommendations are generated immediately for the specified patient(s), regardless of weekly milestones or recommendation flags. | Ad-hoc run when a new patient is added or an urgent re-recommendation is needed, without reprocessing the entire study. |

> \[!IMPORTANT]
> **Run the study-level command daily** (for example, via a cron job) so that weekly recommendations are processed each day for all eligible patients.
> Use the **patient-level command only for exceptions**, e.g. when a patient is registered after the daily cron job has executed and you need immediate recommendations without duplicating prescriptions for the whole study.


<details>

<summary>more details (--help)</summary>

```bash
$ ai-cdss-cli recommend --help
                                                                                                                                                                                                                                                                        
 Usage: ai-cdss-cli recommend [OPTIONS]                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                        
 Generate treatment recommendations for a study OR explicit patient list. Use --study-id for a cohort run, or --patient-id for targeted patients.                                                                                                                       
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --study-id           -s      INTEGER  Study cohort ID(s). Repeat to provide multiple integers. [default: None]                                                                                                                                                       │
│ --patient-id         -p      INTEGER  Explicit patient ID(s). Repeat to provide multiple integers. [default: None]                                                                                                                                                   │
│ --n                  -n      INTEGER  Number of recommendations per patient. [default: None]                                                                                                                                                                         │
│ --days               -d      INTEGER  Number of days to cover in the recommendation. [default: None]                                                                                                                                                                 │
│ --protocols-per-day  -P      INTEGER  Number of protocols per day. [default: None]                                                                                                                                                                                   │
│ --env-file           -e      PATH     Path to a .env file with environment variables. [default: None]                                                                                                                                                                │
│ --help                                Show this message and exit.                                                                                                                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
</details>

#### **ii) Patient Registration - compute-metrics** command

When a new patient is recruited for a study, clinicians will have to input the patient details through the MIMS - Medical Information Management System. Including information about baseline clinical assessments, study start date, and whether this patient needs recommendations. Once the patient is registered, the precomputation of PPF needs to be triggered, in order to update the internal files powering the AI-CDSS engine.

Example to precompute PPF metric when a patient signs up to clinical study.

```bash
$ ai-cdss-cli compute-metrics --patient-id 103 --env-file .ai_cdss/env/.env.prod
```

> [!IMPORTANT]
> After all **baseline clinical scores** for a newly registered patient are entered, this command should run **automatically** to pre-compute the PPF metric. **This metrics are required** for generating future recommendations.

<details>

<summary>more details (--help)</summary>

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
</details>

<p align="center">
  <img width="1317" height="1191" alt="image" src="https://github.com/user-attachments/assets/13e1f60c-8cc1-461e-95d8-083c4b210d8b" style="width:40%; height:auto;"/>
</p>

#### **iii) New protocol - compute-protocol-metrics command**

When a new protocol is included in the RGS platform, for the CDSS system to work, the attributes that this protocol target will need to be inputted. In order for the system to compute similarity with other RGS protocols.

Example to update the protocol_similarity file upon new protocol added. 

```bash
$ ai-cdss-cli compute-protocol-metrics --env-file .ai_cdss/env/.env.prod
```

> [!NOTE]
> This assumes that the new protocol and its attributes have been added to the internal ai_cdss/data/protocol_attributes.csv file. Which at the moment **requires manually modifying the file**.

<details>

<summary>more details (--help)</summary>

```bash
$ ai-cdss-cli compute-protocol-metrics --help
                                                                                                                                                                      
 Usage: ai-cdss-cli compute-protocol-metrics [OPTIONS]                                                                                                                
                                                                                                                                                                      
 Computes Protocol Similarity Metrics based on loaded data. Returns the computed metrics.                                                                                                 
                                                                                                                                                                      
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --env-file  -e      PATH  Path to a .env file with environment variables. [default: None]                                                                          │
│ --help                    Show this message and exit.                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
</details>

<p align="center">
  <img width="829" height="1172" alt="image" src="https://github.com/user-attachments/assets/deb4fabb-2968-4e1b-9fdb-a37b9f329592" style="width:20%; height:auto;"/>
</p>
