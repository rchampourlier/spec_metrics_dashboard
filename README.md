# SpecMetrics Dashboard

Dashboard to visualize information from SpecMetrics logs on RSpec runs.

## Current insights

- List of branches with builds: `/branches`
- List of runs for a given branch: `/branches/<branch_name>/runs`
- Overview for a given run: `/run/<run_key>/overview` (includes a chart with run time on first two levels of spec directories)
- List of examples in a given run, sorted by runtime: `/run/<run_key>/examples_by_runtime`

## How to use it

```
# Start a local development server
bin/dev
```

## How to deploy

For now, it's made for easy deployment on Heroku. You may use `bin/deploy` (it assumes you have created the application with `heroku create` first).
