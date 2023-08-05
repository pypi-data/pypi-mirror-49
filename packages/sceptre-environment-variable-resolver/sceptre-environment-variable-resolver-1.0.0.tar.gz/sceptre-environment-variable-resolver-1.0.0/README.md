# Environment Variable Resolver

Fetches the value from an environment variable.

Syntax:

```yaml
parameter|sceptre_user_data:
  <name>: !environment_variable ENVIRONMENT_VARIABLE_NAME
```

Example:

```yaml
parameters:
  database_password: !environment_variable DATABASE_PASSWORD
```
