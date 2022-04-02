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
    Once the new session is downloaded, further processing steps will be triggered: fmriprep, abcd, etc.

Additional Processing 
    Once preprocessing is complete, a slack notification will be sent, and additional processing automations can be performed. 

EEG Data
-----------

HAPPE- Harvard Automated Processing Pipeline for EEG 
    HAPPE is "a pipeline for taking unprocessed EEG data and automatically processing it 
    to be input to frequency domain analyses. It translates recent advances in adult EEG 
    processing to developmental data context and implements wavelet-enhanced-ICA + ICA 
    approaches for EEG artifact removal." (HAPPE README) 
    
    It's agnostic to and programs used for subsequent analyses, and is compatible with 
    BEAPP, EEGLAB, Matlab, or any other programs that accept .txt EEG data. It also 
    produces a processing report with data quality metrics for assessing data, reporting 
    in manuscripts, setting quality thresholds for removing data from further analysis. 

    HAPPE Requirements
        -   Matlab + signal processing, optimization, and statistics toolboxes 
        -   EEGLAB + MARA & Cleanline plugins (free/included with HAPPE download)
        -   FASTER functions 
        -   Mac or Windows environment 
