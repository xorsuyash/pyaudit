# pyaudit
# Distributed Auditing Mechanism for Outsourced Data
This repository contains the implementation of a Distributed Auditing (DBA) Mechanism for securely auditing large-scale outsourced data. This work is based on the research that aims to overcome the limitations of traditional Third-Party Auditing (TPA) by eliminating the need for a centralized auditor, leveraging distributed end-user participation for verification.

# Overview
Cloud storage outsourcing has become increasingly popular due to the scalability, accessibility, and cost-effectiveness provided by Cloud Service Providers (CSPs). However, ensuring the integrity of the outsourced data remains a significant concern. Traditional integrity auditing mechanisms rely on Third-Party Auditors (TPAs), which may introduce privacy risks, delays, and trust issues.

This project proposes a Distributed Auditing Mechanism (DBA) that decentralizes the auditing process by distributing the task among end-users. This eliminates the need for a TPA and reduces the burden on the Data Owner (DO) for verifying large files, making the auditing process more efficient and secure.

# Key Features
- End-user Auditing: Auditing tasks are performed by distributed end-users, removing the need for a centralized third party.
- Efficient Large File Auditing: Optimized for handling large multimedia files, reducing the time required for both downloading and auditing.
- Single Re-Verification: Ensures that each file is only verified once by the DO, preventing duplicate verification tasks when multiple integrity violations are reported.
  Research Contributions
- Converts the traditional probabilistic auditing approach to deterministic auditing by involving distributed end-users.
- Eliminates the requirement for Third-Party Auditors (TPAs), enhancing both security and efficiency.
- Optimizes the Data Owner's computation costs and reduces the communication overhead during the auditing process.
# Architecture
The proposed architecture includes the following key components:

- Data Owner (DO): The entity that outsources data to the cloud and performs the final integrity checks.
- Cloud Service Provider (CSP): The entity responsible for storing the data.
- Distributed End-Users: Participate in auditing tasks and report integrity violations to the DO.
![Screenshot from 2024-10-06 15-09-14](https://github.com/user-attachments/assets/774622be-648b-4fb4-aaaf-b3a3d0c0b46c)
