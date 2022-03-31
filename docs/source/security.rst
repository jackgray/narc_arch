=====================
Security 
=====================
HIPAA Compliance 
-----------------
Security practices should be monitored closely in order to maintain 
HIPAA compliance 
    https://www.hipaajournal.com/hipaa-compliance-checklist/

From HIPAA:
Technical Safeguards
   The Technical Safeguards concern the technology that is used to protect ePHI and provide 
   access to the data. The only stipulation is that ePHI; whether at rest or in transit; must 
   be encrypted to NIST standards once it travels beyond an organizations internal firewalled 
   servers. This is so that any breach of confidential patient data renders the data unreadable, 
   undecipherable and unusable. Thereafter organizations are free to select whichever mechanisms 
   are most appropriate to:


.. .. csv-table:: Technical Safeguards :rst:dir:`csv-table`
..    :header: "Implementation Specification", "Required or Addressable", "Further Information"
..    :widths: 20, 7, 30

..    "Implement a means of access control",               "Required",    "This not only means assigning a centrally-controlled 
..    unique username and PIN code for each user, but also 
..    establishing procedures to govern the release or 
..    disclosure of ePHI during an emergency."
..    "Introduce a mechanism to authenticate ePHI",        "Addressable", "This mechanism is essential in order to comply with HIPAA regulations as it confirms whether ePHI has been altered or destroyed in an unauthorized manner."
..    "Implement tools for encryption and decryption",     "Addressable", "This guideline relates to the devices used by authorized users, which must have the functionality to encrypt messages when they are sent beyond an internal firewalled server, and decrypt those messages when they are received."
..    "Introduce activity logs and audit controls",        "Required",    "The audit controls required under the technical safeguards are there to register attempted access to ePHI and record what is done with that data once it has been accessed."
..    "Facilitate automatic log-off of PCs and devices",   "Addressable", "This function logs authorized personnel off of the device they are using to access or communicate ePHI after a pre-defined period of time. This prevents unauthorized access of ePHI should the device be left unattended."

+--------------------------------------------------+-------------+------------------------------------------------------+ 
|  Implementation                                  | Required or | Further Information                                  | 
|  Specification                                   | Addressable |                                                      |        
+==================================================+=============+======================================================+ 
| Implement a means of access control              | Required    | This not only means assigning a centrally controlled | 
|                                                  |             | unique username and PIN code for each user, but also | 
|                                                  |             | establishing procedures to govern the release or     | 
|                                                  |             | disclosure of ePHI during an emergency.              |   
+--------------------------------------------------+-------------+------------------------------------------------------+ 
| Introduce a mechanism to authenticate ePHI       | Required    | This not only means assigning a centrally controlled | 
|                                                  |             | unique username and PIN code for each user, but also | 
|                                                  |             | establishing procedures to govern the release or     | 
|                                                  |             | disclosure of ePHI during an emergency.              |   
+--------------------------------------------------+-------------+------------------------------------------------------+ 
| Implement tools for encryption and decryption    | Required    | This not only means assigning a centrally controlled | 
|                                                  |             | unique username and PIN code for each user, but also | 
|                                                  |             | establishing procedures to govern the release or     | 
|                                                  |             | disclosure of ePHI during an emergency.              |   
+--------------------------------------------------+-------------+------------------------------------------------------+ 
| Introduce activity logs and audit controls       | Required    | This not only means assigning a centrally controlled | 
|                                                  |             | unique username and PIN code for each user, but also | 
|                                                  |             | establishing procedures to govern the release or     | 
|                                                  |             | disclosure of ePHI during an emergency.              |   
+--------------------------------------------------+-------------+------------------------------------------------------+ 
| Facilitate automatic log-off of PCs and devices  | Required    | This not only means assigning a centrally controlled | 
|                                                  |             | unique username and PIN code for each user, but also | 
|                                                  |             | establishing procedures to govern the release or     | 
|                                                  |             | disclosure of ePHI during an emergency.              |   
+--------------------------------------------------+-------------+------------------------------------------------------+

Pysical Safeguards
   The Physical Safeguards focus on physical access to ePHI irrespective of its location. 
   ePHI could be stored in a remote data center, in the cloud, or on servers which are 
   located within the premises of the HIPAA Covered Entity. They also stipulate how 
   workstations and mobile devices should be secured against unauthorized access:

   .. "Facility access controls must be implemented",          "Required",      "This not only means assigning a centrally-controlled unique username and PIN code for each user, but also establishing procedures to govern the release or disclosure of ePHI during an emergency."
   .. "Policies for the use/positioning of workstations",      "Addressable",   "This mechanism is essential in order to comply with HIPAA regulations as it confirms whether ePHI has been altered or destroyed in an unauthorized manner."
   .. "Policies and procedures for mobile devices	",          "Addressable",   "This guideline relates to the devices used by authorized users, which must have the functionality to encrypt messages when they are sent beyond an internal firewalled server, and decrypt those messages when they are received."
   .. "Introduce activity logs and audit controls",            "Required",      "The audit controls required under the technical safeguards are there to register attempted access to ePHI and record what is done with that data once it has been accessed."
   .. "Inventory of hardware",                                 "Addressable",   "This function logs authorized personnel off of the device they are using to access or communicate ePHI after a pre-defined period of time. This prevents unauthorized access of ePHI should the device be left unattended."

+--------------------------------------------------+-------------+---------------------------------------------------------+
|  Implementation Specification                    | Required or | Further Information                                     |
|                                                  | Addressable |                                                         |       
+==================================================+=============+=========================================================+
| Facility access controls must be implemented     | Required    |   This not only means assigning a centrally controlled  |
|                                                  |             |   unique username and PIN code for each user, but also  |
|                                                  |             |   establishing procedures to govern the release or      |
|                                                  |             |   disclosure of ePHI during an emergency.               |   
+--------------------------------------------------+-------------+---------------------------------------------------------+
| Policies for the use/positioning of workstations | Required    |   This not only means assigning a centrally controlled  |
|                                                  |             |   unique username and PIN code for each user, but also  |
|                                                  |             |   establishing procedures to govern the release or      |
|                                                  |             |   disclosure of ePHI during an emergency.               |   
+--------------------------------------------------+-------------+---------------------------------------------------------+
| Policies and procedures for mobile devices       | Required    | This not only means assigning a centrally controlled    |
|                                                  |             | unique username and PIN code for each user, but also    |
|                                                  |             | establishing procedures to govern the release or        |
|                                                  |             | disclosure of ePHI during an emergency.                 |   
+--------------------------------------------------+-------------+---------------------------------------------------------+
| Introduce activity logs and audit controls       | Required    | This not only means assigning a centrally controlled    |
|                                                  |             | unique username and PIN code for each user, but also    |
|                                                  |             | establishing procedures to govern the release or        |
|                                                  |             | disclosure of ePHI during an emergency.                 |   
+--------------------------------------------------+-------------+---------------------------------------------------------+
| Inventory of hardware                            | Required    | This not only means assigning a centrally controlled    |
|                                                  |             | unique username and PIN code for each user, but also    |
|                                                  |             | establishing procedures to govern the release or        |
|                                                  |             | disclosure of ePHI during an emergency.                 |   
+--------------------------------------------------+-------------+---------------------------------------------------------+


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

