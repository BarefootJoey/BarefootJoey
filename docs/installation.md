## Installation & Setup (Windows)

### Prerequisites

- Python 3.10+ installed (`py -3.10 --version`)
- Git installed

### Create and activate a virtual environment

```powershell
# From the repo root
py -3.10 -m venv venv
venv\Scripts\Activate.ps1

# Confirm the prompt shows (venv)
python --version
```

### Install dependencies

Option 1: install from the module requirements file

```powershell
pip install -r contrib_writer\requirements.txt
```

Option 2: install packages directly

```powershell
pip install structlog pydantic
```

### Verify installation

```powershell
python -c "import structlog; import pydantic; print('ok')"
```

### License policy

This project aims to use permissive licenses (MIT/BSD/Apache-2.0). The main Python deps are `structlog` (BSD) and `pydantic` (MIT).

