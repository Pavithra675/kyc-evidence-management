# LLM Prompt History and AI Usage Disclosure

## 1. Project Information

- **Project:** KYC Evidence and Review Management System
- **Repository:** https://github.com/Pavithra675/kyc-evidence-management
- **AI tool used:** ChatGPT
- **Other AI tools:** None

## 2. Prompt History

The following is a chronological, reconstructed record of the prompts and requests made to ChatGPT during project development. The wording is summarized where the original wording could not be recovered. It is not a verbatim transcript.

### Phase 1: Understanding and Planning

1. Help me understand the KYC Evidence and Review Management System assignment.
2. Break the challenge into manageable implementation steps.
3. Explain the required entities, relationships and business workflows.
4. Help me understand the data dictionary requirements.
5. Explain how to generate parent records before dependent records.

### Phase 2: Database and Data Generation

6. Help me design the database models for Customer, CustomerType, KYCRequirement, Document and Verification.
7. Help me implement RiskRating, ReviewCase, BeneficialOwner, Alert and AuditEvent.
8. Explain primary keys, foreign keys and relationships.
9. Help me generate synthetic KYC customer and document data using Python.
10. Help me implement deterministic IDs and a fixed random seed.
11. Help me generate business customers and beneficial ownership records.
12. Help me generate document issue dates, expiry dates and verification statuses.
13. Help me generate periodic review records and expiry alerts.
14. Help me create deliberate data anomalies for ground-truth scenarios.
15. Help me export ground-truth labels into CSV and JSON.

### Phase 3: Business Rules and Validation

16. Help me calculate KYC completeness based on customer type and mandatory requirements.
17. Explain how to identify missing and expired documents.
18. Help me validate foreign keys and primary-key uniqueness.
19. Help me identify approved customers missing mandatory evidence.
20. Help me detect ownership percentages above 100%.
21. Help me detect closed reviews without resolutions.
22. Help me identify duplicate documents and document-holder mismatches.
23. Help me validate overdue reviews and missing beneficial owners.
24. Help me implement automated tests using Pytest.
25. Help me understand and fix test failures.

### Phase 4: API Development

26. Help me implement REST API endpoints using FastAPI.
27. Explain how to run the FastAPI application using Uvicorn.
28. Help me understand and test API endpoints using Swagger UI.
29. Help me implement a customer-specific KYC completeness endpoint.
30. Help me implement configurable document expiry warning alerts.
31. Help me prevent duplicate expiry alerts.
32. Help me test the expiry alert endpoint with a 30-day warning period.
33. Help me understand API responses and verify database changes.

### Phase 5: Documentation and Reproducibility

34. Help me prepare the project README with setup and execution instructions.
35. Help me prepare the source manifest.
36. Help me prepare the validation report.
37. Help me export database records into CSV, JSON and SQL formats.
38. Help me generate SHA-256 checksums.
39. Explain how to compare two data generation runs to verify reproducibility.
40. Help me troubleshoot Python package and generator errors.

### Phase 6: GitHub and Submission

41. Help me check which project files should be committed.
42. Explain how to use Git status, add, commit and push.
43. Help me resolve Git and PowerShell command issues.
44. Help me verify that my GitHub repository is public.
45. Help me understand the YottaFlex project submission guidelines.
46. Help me prepare an LLM prompt history and AI disclosure document.
47. Help me understand the additional YottaFlex candidate project FAQ requirements.

### Phase 7: Interview Preparation

48. Help me prepare a simple project introduction.
49. Help me explain the project architecture and workflow.
50. Help me prepare a project demonstration using Swagger UI.
51. Help me practise likely technical interview questions.
52. Help me explain the business rules, testing approach and project limitations.

## 3. How ChatGPT Assisted

ChatGPT was used for:

- Understanding assignment requirements and breaking down tasks.
- Explaining database design and business logic.
- Suggesting and assisting with Python and FastAPI implementation.
- Troubleshooting errors and explaining commands.
- Developing and reviewing validation and test logic.
- Preparing documentation and GitHub submission materials.
- Explaining technical concepts and preparing for the interview.

## 4. My Contribution and Verification

I worked through the project implementation step by step with AI assistance.

I personally executed the project commands and reviewed the resulting application behavior. My verification activities included:

- Setting up the Python project and virtual environment.
- Running synthetic data generation and export scripts.
- Running database validation.
- Starting the FastAPI application.
- Testing API endpoints through Swagger UI.
- Checking customer-specific KYC completeness results.
- Testing expiry alerts and duplicate prevention.
- Running the automated test suite.
- Generating and comparing SHA-256 checksums.
- Reviewing Git changes and pushing the project to GitHub.

I can explain the implementation, business rules, testing process and design decisions during the technical discussion.

## 5. Validation Evidence

- Synthetic customers: 8,000
- Documents: 20,000
- Verification records: 20,000
- Review cases: 3,000
- Ground-truth scenarios: 8
- Database validation checks: 10
- Automated tests: 10 passed, 0 failed
- Export formats: CSV, JSON and SQL
- Reproducibility: checked using SHA-256 checksums

## 6. AI Usage Disclosure and History Limitation

ChatGPT was the only AI tool used for this project.

The prompt history above is a reconstructed and summarized record based on the project conversations available during preparation of this document. It is not a verbatim export of every original prompt. Some earlier conversation wording may not be recoverable.

Full AI responses are not included because the submission guidelines state that AI responses are optional.

AI-assisted suggestions and code were reviewed and tested as part of the development process. I acknowledge the use of AI assistance and am prepared to explain the work honestly.

## 7. Project Limitations

- The dataset contains synthetic information, not real customer records.
- The project is an implementation for the candidate challenge and is not certified for production regulatory compliance.
- The system has not been deployed as a production service.
- Further production hardening, security review and integration testing would be required before real-world use.