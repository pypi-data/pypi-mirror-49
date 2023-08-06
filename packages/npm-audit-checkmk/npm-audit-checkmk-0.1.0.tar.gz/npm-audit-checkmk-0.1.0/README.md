# NPM Audit Interpreter and Check MK output generator

This program takes the output of a `npm audit --json` run and interprets it.
The parameters given define the thresholds to be used, and the output is written to the given directory for check mk local checks.

Requirements:
 * An npm installation with the `npm audit` command available.

```bash
> npm_audit_checkmk -f tests/example.json -s 'frontend_vulnerabilities'
<<<local>>>
P frontend_vulnerabilities INFO=0|LOW=7;20|MODERATE=2;10;20|HIGH=55;1;3|CRITICAL=2;0;0 See `npm audit` for more details.
```

## Usage

```bash
pushd /path/to/your/project
npm audit --json | npmauditcheckmk -o /var/lib/check_mk_agent/spool/90000_npm_audit.txt
popd
