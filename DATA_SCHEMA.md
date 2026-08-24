# Data schema for SIG WUS platform catalog

The JSON file `data/platforms.json` contains an array of platform objects. Each object must conform to the following schema (also defined in `data/schema.json`):

| Field | Type | Description |
|-------|------|-------------|
| `platform` | string | Human‑readable name of the platform (e.g. `WMAUS`). |
| `reference` | string \| null | BibTeX key of the primary reference; `null` if not available. |
| `transducer` | string | Brief description of the transducer (e.g. `8 ch. in wristband`). |
| `tx_path` | string | Transmit‑path description (voltage, frequency, etc.). |
| `rx_path` | string | Receive‑path description (muxing, sampling, etc.). |
| `design` | string | Design details such as controller, ASIC, FPGA, MCU, etc. |
| `data_link` | string | Communication interface for raw data (e.g. `\bluetooth{} raw data`). |
| `specifications` | string | Key performance specifications: frame rate, weight, size, power, battery operation, etc. LaTeX macros are kept for rendering on the site. |
| `application` | string | Typical application(s) and citation list. |
| `access` | string | Availability indicator (`CA` for commercially available, `API`, `\faCode{}` for open‑source, etc.). |

All fields are required (except `reference` which may be `null`). No additional properties are permitted. The schema file `data/schema.json` can be used for automated validation.
