# timus-sender

Timus sender is simple python script to send solution of problems to [timus](https://timus.online/).

## How to use

Pass required parameters to script:

```
sender.py --judge-id=<your id> --compiler=<compiler code> --problem=<problem id> <path/to/solution>
```

Script will return link to your submissons to this problem.

## Parameters deduction

All parameters can be deducted from context.

### judge-id

If `judge-id` parameter doesn't passed to script it will be read from `.judge_id` file in your home directory.

### compiler

If `compiler` parameter doesn't passed to script compiler will be defined by file extension. Actual default compilers available in source code.

### problem

If `problem` parameter doesn't passed to script problem number will be defined by directory of file.
Possible directory name formats:

- `<problem id>`
- `<problem id>-<description>`
- `<description>-<problem id>`
