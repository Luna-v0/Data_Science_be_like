## Trial
A single complete training run, normally used as parameter of [[Hyperparameter Tuning|HPO]]. 

## Step
Atomic unit of the observation of the state (normally signed with a $t$)

## Trajectory
Ordered sequence of steps 

## Horizon
The max episode length before truncation

## Episode (full trajectory)
A trajectory from start to end state 
## Rollout 
A chunk of the trajectory collected before each update (you can think this as the complete dataset but it gets reset each iteration)
## Epoch (number of rollouts)
It is **different** from the simple [[Neural Networks (NN)]] terminology. A epoch means a full pass over collected rollout buffer. 

## Iteration
The number of times you generate a full rollout. 


# Visualizing the terminology

```python
for iteration in range(num_iterations):       # OUTER: each makes a FRESH rollout
    rollout = collect(n_steps)                # the rollout, one batch of experience
    for epoch in range(n_epochs):             # reuse rollout n_epochs times
        for minibatch in split(rollout, batch_size):
            gradient_step(minibatch)          # one weight update
```

