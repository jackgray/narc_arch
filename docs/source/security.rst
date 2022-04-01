=====================
Security 
=====================
HIPAA Compliance 
-----------------
Security practices should be monitored closely in order to maintain 
HIPAA compliance for all services and safeguard PHI.

From HIPAA:   
(https://www.hipaajournal.com/hipaa-compliance-checklist/)

Technical Safeguards
   The Technical Safeguards concern the technology that is used to protect ePHI and provide 
   access to the data. The only stipulation is that ePHI; whether at rest or in transit; must 
   be encrypted to NIST standards once it travels beyond an organizations internal firewalled 
   servers. This is so that any breach of confidential patient data renders the data unreadable, 
   undecipherable and unusable. Thereafter organizations are free to select whichever mechanisms 
   are most appropriate to:
.. .. image:: ./hipaa-technical-safeguards.png
..    :width: 650
..    :alt: Could not load technical safeguards table
.. csv-table:: Technical Safeguards :rst:dir:`csv-table`
   :header: "Implementation Specification", "Required or Addressable", "Further Information"
   :widths: 20, 7, 30

   "Implement a means of access control",               "Required",    "This not only means assigning a centrally-controlled unique username and PIN code for each user, but also establishing procedures to govern the release or disclosure of ePHI during an emergency."
   "Introduce a mechanism to authenticate ePHI",        "Addressable", "This mechanism is essential in order to comply with HIPAA regulations as it confirms whether ePHI has been altered or destroyed in an unauthorized manner."
   "Implement tools for encryption and decryption",     "Addressable", "This guideline relates to the devices used by authorized users, which must have the functionality to encrypt messages when they are sent beyond an internal firewalled server, and decrypt those messages when they are received."
   "Introduce activity logs and audit controls",        "Required",    "The audit controls required under the technical safeguards are there to register attempted access to ePHI and record what is done with that data once it has been accessed."
   "Facilitate automatic log-off of PCs and devices",   "Addressable", "This function logs authorized personnel off of the device they are using to access or communicate ePHI after a pre-defined period of time. This prevents unauthorized access of ePHI should the device be left unattended."




Physical Safeguards
   The Physical Safeguards focus on physical access to ePHI irrespective of its location. 
   ePHI could be stored in a remote data center, in the cloud, or on servers which are 
   located within the premises of the HIPAA Covered Entity. They also stipulate how 
   workstations and mobile devices should be secured against unauthorized access:
.. .. image:: ./hipaa-physical-safeguards.png
..    :width: 650
..    :alt: Could not load physical safeguards table
.. csv-table:: Technical Safeguards :rst:dir:`csv-table`
   :header: "Implementation Specification", "Required or Addressable", "Further Information"
   :widths: 20, 7, 30

   "Facility access controls must be implemented",          "Addressable",      "Controls who has physical access to the location where ePHI is stored and includes software engineers, cleaners, etc. The procedures must also include safeguards to prevent unauthorized physical access, tampering, and theft."
   "Policies for the use/positioning of workstations",      "Required",         "Policies must be devised and implemented to restrict the use of workstations that have access to ePHI, to specify the protective surrounding of a workstation and govern how functions are to be performed on the workstations."
   "Policies and procedures for mobile devices	",          "Required",         "If users are allowed to access ePHI from their mobile devices, policies must be devised and implemented to govern how ePHI is removed from the devices if the user leaves the organization or the device is re-used, sold, etc."
   "Introduce activity logs and audit controls",            "Addressable",      "An inventory of all hardware must be maintained, together with a record of the movements of each item. A retrievable exact copy of ePHI must be made before any equipment is moved."




Administrative Safeguards
   The Administrative Safeguards are the policies and procedures which bring the 
   Privacy Rule and the Security Rule together. They are the pivotal elements of 
   a HIPAA compliance checklist and require that a Security Officer and a Privacy 
   Officer be assigned to put the measures in place to protect ePHI, while they 
   also govern the conduct of the workforce.

   The OCR pilot audits identified risk assessments as the major area of Security 
   Rule non-compliance. Risk assessments are going to be checked thoroughly in 
   subsequent audit phases; not just to make sure that the organization in question 
   has conducted one, but to ensure to ensure they are comprehensive and ongoing. 
   A HIPAA compliant risk assessment is not a one-time requirement, but a regular 
   task necessary to ensure continued HIPAA compliance.

.. csv-table:: Technical Safeguards :rst:dir:`csv-table`
:header: "Implementation Specification", "Required or Addressable", "Further Information"
:widths: 20, 7, 30

"Facility access controls must be implemented",          "Addressable",      "Controls who has physical access to the location where ePHI is stored and includes software engineers, cleaners, etc. The procedures must also include safeguards to prevent unauthorized physical access, tampering, and theft."
"Policies for the use/positioning of workstations",      "Required",         "Policies must be devised and implemented to restrict the use of workstations that have access to ePHI, to specify the protective surrounding of a workstation and govern how functions are to be performed on the workstations."
"Policies and procedures for mobile devices	",          "Required",         "If users are allowed to access ePHI from their mobile devices, policies must be devised and implemented to govern how ePHI is removed from the devices if the user leaves the organization or the device is re-used, sold, etc."
"Introduce activity logs and audit controls",            "Addressable",      "An inventory of all hardware must be maintained, together with a record of the movements of each item. A retrievable exact copy of ePHI must be made before any equipment is moved."

.. RST documentation lies a lot.... below does not work
.. .. image:: ./hipaa-administrative-safeguards.png
..    :width: 650
..    :alt: Could not load administrative safeguards table
.. csv-table:: Administrative Safeguards :rst:dir:`csv-table`
   :header: "Implementation Specification", "Required or Addressable", "Further Information"
   :widths: 20, 7, 30

"Conducting risk assessments",	         "Required",	      "Among the Security Officers main tasks is the compilation of a risk assessment to identify every area in which ePHI is being used, and to determine all of the ways in which breaches of ePHI could occur."
"Introducing a risk management policy",	"Required",	      "The risk assessment must be repeated at regular intervals with measures introduced to reduce the risks to an appropriate level. A sanctions policy for employees who fail to comply with HIPAA regulations must also be introduced."
"Training employees to be secure",	      "Addressable",	   "Training schedules must be introduced to raise awareness of the policies and procedures governing access to ePHI and how to identify malicious software attacks and malware. All training must be documented."
"Developing a contingency plan",	         "Required",	      "In the event of an emergency, a contingency plan must be ready to enable the continuation of critical business processes while protecting the integrity of ePHI while an organization operates in emergency mode."
"Testing of contingency plan",	         "Addressable",	   "The contingency plan must be tested periodically to assess the relative criticality of specific applications. There must also be accessible backups of ePHI and procedures to restore lost data in the event of an emergency."
"Restricting third-party access",	      "Required",    	"It is vital to ensure ePHI is not accessed by unauthorized parent organizations and subcontractors, and that Business Associate Agreements are signed with business partners who will have access to ePHI."
"Reporting security incidents",	         "Addressable", 	"The reporting of security incidents is different from the Breach Notification Rule (below) inasmuch as incidents can be contained and data retrieved before the incident develops into a breach."

Key Management System (KMS)
----------------------------
A central key management system will be employed to integrate with all cluster 
services requiring authentication.

This will allow:
   -  Automatic generation of keys during most service installations that implement security.
   -  One key for every user 
   -  RBAC: Role-based Access Control 
      -  Unique access profiles for each user 
      -  Granular control over access and permissions

Hashicorp Vault Keystore
-------------------------
Reccommended KMS

Hashicorp Vault is free to use as a self-hosted solution, and supported by 
all major clustering solutions.

https://github.com/minio/kes/wiki/Hashicorp-Vault-Keystore

-   Reputible 
-   Widely used and supported
-   Self-hosted (more secure)
-   Free
-   Established/Good Support Community

MinIO Automatic Encryption
---------------------------
"Zero-knowledge" encryption of data at rest 

Uses central KMS 

NIST Cybersecurity Framework 
-----------------------------