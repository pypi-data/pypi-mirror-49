# ASG Scaling Processes

Suspends or resumes autoscaling scaling processes.

Syntax:

```yaml
<hook_point>:
  - !asg_scaling_processes <suspend|resume>::<process-name>
```

Example:

```yaml
before_update:
  - !asg_scaling_processes suspend::ScheduledActions
```

More information on suspend and resume processes can be found in the AWS
[documentation](http://docs.aws.amazon.com/autoscaling/latest/userguide/as-suspend-resume-processes.html).
