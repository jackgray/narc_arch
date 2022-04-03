=========================
Pipelines 
=========================

fmriprep
--------------------------

abcd 
-----

MNE-BIDS-Pipeline
------------------
MNE: MEG & EEG Analysis and Visualization. 
A full-fledged processing pipeline for MEG and EEG data.

It operates on raw data stored according to the Brain 
Imaging Data Structure (BIDS). Processing is controlled 
using a simple human-readable configuration file.

http://mne.tools/mne-bids-pipeline/index.html

HAPPE- Harvard Automated Processing Pipeline for EEG 
------------------------------------------------------
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