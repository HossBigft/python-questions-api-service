# How to run
## Preparation
1. Install uv 
`pip install uv`
2. Open root directory.
3. Install dependencies with
`uv sync`
45. Activate virtual environment with `source` command, script is based on your shell
`source .venv/bin/activate`


## Execution
1. Run project with command below in root directory activated virtual environment
`fastapi run --reload 'app/main.py'`
2. Run test with 
`pytest`
3. To run backend in local mode with requests to test containers
`fastapi run  'app/run_local_stack_without_plesk_access.py'`

