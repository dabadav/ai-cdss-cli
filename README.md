


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


#### **recommend**

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

#### **compute-metrics**

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

#### **compute-protocol-metrics**

```bash
$ ai-cdss-cli compute-protocol-metrics --help
                                                                                                                                                                      
 Usage: ai-cdss-cli compute-protocol-metrics [OPTIONS]                                                                                                                
                                                                                                                                                                      
 Computes Protocol Similarity Metrics based on loaded data. Returns the computed metrics.                                                                                                 
                                                                                                                                                                      
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --env-file  -e      PATH  Path to a .env file with environment variables. [default: None]                                                                          │
│ --help                    Show this message and exit.                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
