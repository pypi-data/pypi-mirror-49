# StackOutput Resolver

Fetches the value of an output from a different Stack controlled by Sceptre.

Syntax:

```yaml
parameters | sceptre_user_data:
  <name>: !stack_output <stack_name>.yaml::<output_name>
```

Example:

```yaml
parameters:
  VpcIdParameter: !stack_output shared/vpc.yaml::VpcIdOutput
```

Sceptre infers that the Stack to fetch the output value from is a dependency,
and builds that Stack before the current one.

This resolver will add a dependency for the Stack in which needs the output
from.
