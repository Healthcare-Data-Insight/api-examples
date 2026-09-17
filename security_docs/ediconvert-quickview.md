# Docker Scout quick view

Image: `myarch/ediconvert:2.15.5`

Policy configuration excludes copyleft-license and supply-chain-attestations checks.

```text


 Target   │  myarch/ediconvert:2.15.5  │    0C     0H     0M     0L  
   digest │  e45445771099              │                             

Policy status  SUCCESS  (5/5 policies met)
Health score  A  (100%)

 Status │                   Policy                    │           Results           
────────┼─────────────────────────────────────────────┼─────────────────────────────
 ✓      │ Default non-root user                       │                             
 ✓      │ No fixable critical or high vulnerabilities │    0C     0H     0M     0L  
 ✓      │ No high-profile vulnerabilities             │    0C     0H     0M     0L  
 ✓      │ No outdated base images                     │                             
 ✓      │ No unapproved base images                   │    0 deviations             

What's next:
    View policy violations → docker scout policy myarch/ediconvert:2.15.5
    Compare with the latest in the registry → docker scout compare --to-latest myarch/ediconvert:2.15.5


```
