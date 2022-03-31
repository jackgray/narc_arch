===========================
Pre-Processing Automations
===========================

MRI Data 
---------
# Stages

Collection -> XNAT 
    After collection, MRI data is pushed from the scanning console to a central XNAT database managed by the institute.

    Daily checks should be performed by the private lab server to detect when new data is available on XNAT.

XNAT -> Private Lab Server  
    When new data is detected, a download service will be triggered to download the data, rename, organize, and store according to BIDS 
    criteria. 

    dcm2bids or dcm2niix should be performed on XNAT server prior to downloading to mitigate high I/O load during download of uncompressed DICOM data

nipreps/fmriprep 
    Once the new session is downloaded, further processing steps will be triggered.
        -   fmriprep 
        -   abcd

Additional Processing 
    Once preprocessing is complete, a slack notification will be sent, and additional processing automations can be performed. 

