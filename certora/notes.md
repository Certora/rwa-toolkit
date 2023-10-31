# General
## Prepare for using Vim terminal mode
- CTRL-W N to change to Terminal-Normal mode
- Use `i` (insert) to switch back to Terminal-Job


# Dispatch vs. Linking
Demonstrates:
- Multi contract setup
- Linking vs. Dispatch

*To do:* Review and prepare


# Jug Example
The "Jug example spec" (`jug.spec`) demonstrates:
- Multi contract setup
- Linking
- Summarization (both `NONDET` and using a CVL function)
- Loops
- _Missing_ from this example is the use of `DISPATCHER`

## Initial setup
Show simple setup using linking and `optimistic_loop`.
For rules use `reachability` and `rateCheck`.


## Loop issues
Explain loop problem: What is `optimistic_loop` and handling of `loop_iter`.
Show what happens without `optimistic_loop`. Explain that high `loop_iter` will
result in timeout.


## Summary
Show `NONDET` summary is insufficient. Show function summary.


# Additional summaries
## View summaries
Namely: `ALWAYS`, `CONSTANT`, `PER_CALLEE_CONSTANT`, and `NONDET`.
Use the square root example with a configuration contract.

## Havoc summaries
Namely: `HAVOC_ALL` and `HAVOC_ECF`/

## Dispatcher summaries
### Unknown contract
Using `DISPATCHER(true)` - an unknown contract is also assumed to be in the scene
and the relevant `AUTO` summary for it is applied.

### Wild card

## Auto summaries
