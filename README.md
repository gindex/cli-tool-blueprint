## Blueprint for pythonic CLI tools and scripts

Opinionated blueprint for building modern pythonic CLI tools aiming to speedup development by providing
basic structure and boilerplate code. The blueprint helps with occasional creation of CLI tools and scripts
allowing to copy the basic structure and remove unnecessary parts.
 
The blueprint covers following functionality:
1. Modern CLI with [Typer](https://github.com/fastapi/typer) providing examples for several option types.
2. Basic structure to read input from a files, process it and write the output to another file.
3. Shows the processing status with a progress bar using [rich](https://github.com/Textualize/rich).
4. Configuration for dev and prod environments. 
5. Stubs to call a remote http API with [requests](https://github.com/psf/requests).
6. Stubs to execute queries on Postgres with [psycopg2](https://github.com/psycopg/psycopg2). 

### Example

#### Run help 

```txt
➜ ./cli-tool-blueprint.py --help

 Usage: cli-tool-blueprint.py [OPTIONS]

 Opinionated blueprint for building modern python CLI tools aiming to speedup development by providing basic structure and boilerplate
 code.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --token                                 TEXT        Token of http API. [default: None] [required]                                 │
│ *  --db-user                               TEXT        DB user. [default: None] [required]                                           │
│ *  --db-password                           TEXT        DB password. [default: None] [required]                                       │
│    --input-file                            FILENAME    Input file to process. [default: in.txt]                                      │
│    --output-file                           FILENAME    Path to output file. [default: out.txt]                                       │
│    --dry-run               --no-dry-run                Dry run executes the script without changing external resources.              │
│                                                        [default: no-dry-run]                                                         │
│    --environment                           [prod|dev]  [default: dev]                                                                │
│    --install-completion                                Install completion for the current shell.                                     │
│    --show-completion                                   Show completion for the current shell, to copy it or customize the            │
│                                                        installation.                                                                 │
│    --help                                              Show this message and exit.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Run application 

```txt
➜ ./cli-tool-blueprint.py --token token --db-user postgres --db-password postgres --dry-run
[10:30:04] Initialization finished.                                                                             cli-tool-blueprint.py:42
           Processing line 1                                                                                    cli-tool-blueprint.py:42

[10:30:05] Finished processing line 1                                                                           cli-tool-blueprint.py:42

           Processing line 2                                                                                    cli-tool-blueprint.py:42

[10:30:08] Finished processing line 2                                                                           cli-tool-blueprint.py:42

           Processing line 3                                                                                    cli-tool-blueprint.py:42
           Finished processing line 3                                                                           cli-tool-blueprint.py:42
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:04
           Processing finished.                                                                                 cli-tool-blueprint.py:42
```

### Output in case of an error
```
➜ poetry run python cli-tool-blueprint.py --token token --db-user postgres --db-password postgres --dry-run
[10:32:05] Initialization finished.                                                                             cli-tool-blueprint.py:42
╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮
│ /Users/yyy/repos/python3-script-blueprint/cli-tool-blueprint.py:151 in main                      │
│                                                                                                  │
│   148 │                                                                                          │
│   149 │   log("Initialization finished.")                                                        │
│   150 │                                                                                          │
│ ❱ 151 │   raise ValueError                                                                       │
│   152 │                                                                                          │
│   153 │   for line in track(input_file.readlines()):                                             │
│   154 │   │   result = process(line, conf)                                                       │
│                                                                                                  │
│ ╭──────────────────────────────────── locals ────────────────────────────────────╮               │
│ │        conf = Config(                                                          │               │
│ │               │   service_url='http://api.open-notify.org/astros.json',        │               │
│ │               │   service_token='token',                                       │               │
│ │               │   db_url='localhost',                                          │               │
│ │               │   db_password='postgres',                                      │               │
│ │               │   db_port='5432',                                              │               │
│ │               │   db_user='postgres',                                          │               │
│ │               │   db_name='postgres',                                          │               │
│ │               │   db_sslmode='disable',                                        │               │
│ │               │   dry_run=True,                                                │               │
│ │               │   db_conn=None                                                 │               │
│ │               )                                                                │               │
│ │ db_password = 'postgres'                                                       │               │
│ │     db_user = 'postgres'                                                       │               │
│ │     dry_run = True                                                             │               │
│ │ environment = <Env.dev: 'dev'>                                                 │               │
│ │  input_file = <_io.TextIOWrapper name='in.txt' mode='r' encoding='UTF-8'>      │               │
│ │ output_file = <_io.TextIOWrapper name='out.txt' mode='w' encoding='UTF-8'>     │               │
│ │  properties = {                                                                │               │
│ │               │   'dev': {                                                     │               │
│ │               │   │   'service_url': 'http://api.open-notify.org/astros.json', │               │
│ │               │   │   'db_url': 'localhost',                                   │               │
│ │               │   │   'sslmode': 'disable'                                     │               │
│ │               │   },                                                           │               │
│ │               │   'prod': {                                                    │               │
│ │               │   │   'service_url': 'http://api.open-notify.org/astros.json', │               │
│ │               │   │   'db_url': 'my-prod',                                     │               │
│ │               │   │   'sslmode': 'require'                                     │               │
│ │               │   }                                                            │               │
│ │               }                                                                │               │
│ │       token = 'token'                                                          │               │
│ ╰────────────────────────────────────────────────────────────────────────────────╯               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
ValueError
```