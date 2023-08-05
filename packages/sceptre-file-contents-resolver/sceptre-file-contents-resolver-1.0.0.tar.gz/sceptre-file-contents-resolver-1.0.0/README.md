# File Contents Resolver

Reads in the contents of a file.

Syntax:

```yaml
parameters|sceptre_user_data:
  <name>: !file_contents /path/to/file.txt
```

Example:

```yaml
sceptre_user_data:
  iam_policy: !file_contents /path/to/policy.json
```
