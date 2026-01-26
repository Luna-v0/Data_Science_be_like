Are a set of techniques for creating better [[Language Models#Prompts|prompts]]. The main topic on it is context, there are many problems involved context, like missing information, bad training data, hallucination, ambiguity, etc.

## Guidelines
Those are 5 main guidelines for creating better prompts.

1. **Clarity:** It must be exact about what you want.
2. **Context**: More information about the subject helps the [[Language Models|LM]] to respond better, but they must be relevant, sufficient and not large as it can be to avoid [[Language Models#Prompts|Context Window]] problems. 
3. **Objective:** Be concise and avoid ambiguity.
4. **Detail:** Detail makes guides better the response.
5. **Purpose:** What is the objective. 

Other useful stuff is to deal with [[Model Learning#Hyperparameters|Hyperparameters]] for instance lower temperature tend to avoid hallucination.


## Roles 
For most APIs of LMs there are 3 types of roles. The **user**, which is the one that will create the end question. The **system**, which is often used for defining the tone of the conversation, and setting a role for the LM, like saying it's an expert in determinate domain. And the last role is the **assistant** used for adding context to the model.


## Few, one and zero Shot
"Shot" in this sense is examples of response. 

## Iterative Prompting
Improving by testing the prompt. Its the most common and simple technique of prompt engineering that can be used together with other techniques. 

## Chain of thought (CoT) prompt
Is a induction technique to induce the response of the [[Language Models]] linearly, some of the most common:
* Asking for solving step by step
* Ask it to argument its response
* Giving fixed options for its response

**Example:**
```
Problem: Sarah has 15 apples. She gives 1/3 of them to her friend and then buys 8 more. How many apples does she have now?

Solve this step by step:
1. First, calculate how many apples Sarah gave away
2. Then, calculate how many apples she has left
3. Finally, add the new apples she bought
4. Provide the final answer
```
## Tree of thought (ToT) prompt
It's a hierarchic technique for prompting, this is some template for it:

**Example:**
```
Task: Plan a weekend trip to a new city with a $500 budget.

Explore different approaches:

Branch 1: Focus on accommodation
- Option A: Luxury hotel ($300) → limited budget for activities
- Option B: Budget hostel ($80) → more budget for experiences
- Option C: Airbnb ($150) → balanced approach

Branch 2: Focus on transportation
- Option A: Rent a car ($200) → freedom but high cost
- Option B: Public transport ($30) → economical but limited
- Option C: Bike rental ($50) → eco-friendly and flexible

Evaluate each branch and select the best combination based on:
1. Total cost
2. Experience quality
3. Flexibility

Provide the optimal plan.
```

## Graph of thought (GoT)
Extends ToT by allowing thoughts to connect in a non-hierarchical graph structure, enabling cycles and multiple connections between concepts.

**Example:**
```
Task: Debug why a web application is running slowly.

Create a graph of interconnected potential causes:

Node A: Slow database queries
  → connects to Node C (inefficient indexes)
  → connects to Node E (too many connections)

Node B: Large bundle size
  → connects to Node D (unoptimized images)
  → connects to Node F (unused dependencies)

Node C: Inefficient indexes
  → connects back to Node A (affects query speed)
  → connects to Node G (poor database schema)

Node D: Unoptimized images
  → connects to Node B (increases bundle)
  → connects to Node H (slow CDN delivery)

Node E: Too many connections
  → connects to Node A (database bottleneck)
  → connects to Node I (connection pooling issues)

Analyze the graph to identify:
1. Most connected nodes (likely root causes)
2. Cycles that compound the problem
3. Priority order for fixes
```

## Prompt Agentic
Its based on an autonomous agent approach for the LM, its principal are to plan, decide, execute action, evaluate the result and iterate over it. The prompt must define behavior of the agent, responsibility, limits, decision criteria, a "reasoning" and "action" loop.

This is one of the best resulting prompt techniques.

**Example:**
```
You are a research agent tasked with analyzing market trends for electric vehicles.

Behavior: You are analytical, data-driven, and thorough.
Responsibility: Gather data, identify trends, and provide actionable insights.
Limits: Use only publicly available data from 2020-2025. Do not speculate beyond available data.

Decision Criteria:
- Prioritize data from reputable sources (government reports, industry publications)
- Cross-reference multiple sources for validation
- Focus on trends with statistical significance

Reasoning and Action Loop:
1. PLAN: Identify what information is needed
2. ACT: Describe what data sources you would access
3. OBSERVE: Summarize the findings from each source
4. REASON: Analyze patterns and connections
5. DECIDE: Determine if more information is needed or if conclusions can be drawn
6. ITERATE: If needed, return to step 1 with refined focus

Task: Analyze the adoption rate of electric vehicles in Europe from 2020-2025.
Begin with your plan.
``` 