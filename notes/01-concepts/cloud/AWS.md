This is a map of AWS services that are useful for me. This notes are part of my preparation for the AWS Certified AI Practitioner. 


# History Lesson
AWS Cloud started internally at Amazon in 2002. 2004 they started doing for orgs outside Amazon, staring with SQS (Message queue service). In 2006 they re-launched publicly with S3, EC2 and SQS in the US. In 2007 they launched in Europe. 

# Divisions
## Hierarchy

## Regions
They are named, like **us-east-1**, **eu-west-3**. It is a cluster of data centers, and most services are region scoped. Some factors that are important for choosing a Region: **Compliance** with legal requirements, data governance and org; **Proximity** for latency; **Availability** of Services since they could be unavailable in certain regions; **Pricing**, since it may vary in different regions. 

## Availability Zones
Each Region has from 3 to 6 availability zones, usually being 3. They are also named like **ap-sotheast-2a**. Each availability zone is **one or more** discrete data center with redundant resources (network, power, etc). They are physically separated from each other for disasters reasons and redundancy, the availability zones inside a region are connect using high bandwidth and low latency networks.

## Points of presence
They are edge locations and regional caches for low latency to the end user.


# Pricing
You only pay for 3 things on AWS, the **Compute** (RAM, CPU, GPU, etc), the **Storage** and that can be files or data in a DB, and for **Data transfer <b><u>OUT</u></b> of the cloud**.

# Services
## Basic
* **Lambda:** A function calling tool for simple computation, it is spawned on demand, best for occasional executions.
* 