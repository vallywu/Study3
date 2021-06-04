Installation and Tutorials
--------------------------

Installing the nPYc-Toolbox
===========================

We recommend running the nPYc-Toolbox pipeline using Jupyter notebooks, this can either be done through the data science platform Anaconda (recommended), or alternatively through installing Python and the Jupyter notebooks independently.

**Using Anaconda - recommended**

- Install Anaconda with Python 3.6 or above from `Anaconda Download Link <https://www.anaconda.com/distribution/>`_
- Install the nPYc-Toolbox by opening the Anaconda Prompt (see `Getting started with Anaconda <https://docs.anaconda.com/anaconda/user-guide/getting-started/>`_ for details) and typing ‘pip install nPYc’, this will install the toolbox alongside any required dependencies and make it available as a general python package
- Note, if you have an older version of Anaconda, it should first be updated by using the Anaconda Prompt and typing 'conda update conda' and 'conda update --all' (it may be necessary to run the prompt as administrator by selecting this option on the right click menu as you open it). For very old versions, it may be necessary to uninstall and reinstall the latest version

**Using Python and Jupyter**

- Install Python 3.6 or above from `Python Download Link <https://www.python.org/downloads/>`_
- Install the nPYc-Toolbox by opening a command (Windows) or terminal (macOS) window and typing ‘pip install nPYc’, this will install the toolbox alongside any required dependencies and make it available as a general python package
- Install Juypter from `Jupyter Download Link <https://jupyter.readthedocs.io/en/latest/install.html>`_

For advanced users, the toolbox source code can be downloaded directly from the `nPYc-Toolbox GitHub Repository <https://github.com/phenomecentre/nPYc-Toolbox>`_

We strongly recommend additionally downloading the nPYc-toolbox-tutorials, which give detailed worked examples of using the nPYc-Toolbox.


Installing the nPYc-toolbox-tutorials
=====================================

We strongly recommend downloading the nPYc-toolbox-tutorials, which use Jupyter notebooks to demonstrate the application of the nPYc-Toolbox for the preprocessing and quality control of exemplar LC-MS, NMR and targeted NMR (Bruker IVDr) metabolic profiling datasets. These tutorials work through each step in detail, with links to relevant documentation.

- Download the nPYc-toolbox-tutorials from `nPYc-toolbox-tutorials GitHub repository <https://github.com/phenomecentre/nPYc-toolbox-tutorials>`_
- Click on the green 'Clone or download' dropdown menu, then the tutorials can be downloaded as a ZIP file and saved in a suitable location


Using the Jupyter Notebooks
===========================

**Opening a Jupyter Notebook**

Jupyter can be opened from the Anaconda navigator (recommended) or from the command line.

- Using the Anaconda Navigator, launch a Jupyter Notebook session by clicking on the 'Jupyter Notebook' icon
- Alternatively, from the command (Windows) or terminal (macOS) window, launch Jupyter by typing 'jupyter notebook', for more details see `Running Jupyter <https://jupyter.readthedocs.io/en/latest/running.html>`_
- Either of the options above will result in an instance of the Jupyter Notebooks opening in a browser window

**Running the nPYc-toolbox-tutorials**

- Open a Jupyter Notebook session (as described above)
- Click on the 'File' tab and navigate to the location where the nPYc-toolbox-tutorials are saved
- Jupyter notebooks save with the file extension 'ipynb'
- Click on the required Jupyter notebook example (MS, NMR and targeted NMR examples available, as described below) to open in a new browser window
- To run the notebook, click through the cells using the 'Run' button
- Notebooks can be reset and restarted using 'Kernal > Restart & Clear Output'
- Notebooks can be saved using 'File > Save and Checkpoint' (notebooks can then be shared, and others will be able to view their contents)
- Full details on using the Jupyter Notebooks can be found here `Jupyter Read the Docs <https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/examples_index.html>`_

**Running your own notebook**

- Open the required the nPYc-toolbox-tutorials (as described above)
- Select 'File > Make a copy..' to make a copy of the notebook
- Select 'File > Rename..' to rename the copied notebook
- Replace the file paths in the document with your own data path files
- Run the notebook!


Tutorial Datasets
=================

Exemplar data, as part of the nPYc-toolbox-tutorials, can be downloaded from the `nPYc-toolbox-tutorial GitHub repository <https://github.com/phenomecentre/nPYc-toolbox-tutorials>`_. This repository contains all the data and files required to run the tutorials (as described below). Data (including all raw LC-MS data files) is also available from the `Metabolights <https://www.ebi.ac.uk/metabolights>`_ repository under accession number MTBLS694.

The dataset used in these tutorials (DevSet) is comprised of three distinct pooled samples of human urine, with three additional samples generated by pairwise mixing of each primary sample, resulting in a sample set of six:

- DevSet1
- DevSet2
- DevSet3
- DevSet1v2
- DevSet1v3
- DevSet2v3

The samples were then split into 13 equivalent aliquots, and each independently prepared and measured by ultra-performance liquid chromatography coupled to reversed-phase positive ionisation mode spectrometry (LC-MS, RPOS) and 1H nuclear magnetic resonance (NMR) spectroscopy according to Phenome Centre protocols (LC-MS: Lewis *et al* [#]_, NMR: Dona *et al* [#]_). As per these protocols, a pooled QC :term:`Study Reference` sample and independent external reference (:term:`Long-Term Reference`) of a comparable matrix was also acquired to assist in assessing analytical precision.

Urine samples used for generating of the exemplar matrices were collected with informed written consent and ethical approval from the Imperial College Healthcare Tissue Bank (12/WA/0196, project R13053).


Preprocessing and Quality Control of LC-MS Data with the nPYc-Toolbox
=====================================================================

This tutorial demonstrates how to use the LC-MS data processing modules of the nPYc-Toolbox, to import and perform some basic preprocessing and quality control of LC-MS data, and to output a final high quality dataset ready for data modeling.

Required files in nPYc-toolbox-tutorials:

- Preprocessing and Quality Control of LC-MS Data with the nPYc-Toolbox.ipynb: Jupyter notebook tutorial for LC-MS RPOS (XCMS) data
- DEVSET U RPOS xcms.csv: feature extracted (XCMS) LC-MS RPOS data (see below)
- DEVSET U RPOS Basic CSV.csv: CSV file containing basic metadata about each of the acquired samples

Additional files (for example, the raw LC-MS data files) can be found in `Metabolights MTBLS694 <https://www.ebi.ac.uk/metabolights/MTBLS694>`_

Feature extraction of the LC-MS dataset (generation of 'DEVSET U RPOS xcms.csv' from the raw data files) was conducted with the R package `XCMS <https://bioconductor.org/packages/release/bioc/html/xcms.html>`_ , using the following script::

	##
	# NPC Reverse-Phase Urine XCMS params
	##

	#########################################
	###---SAMPLESET-DEPENDENT VARIABLES---###
	#########################################


	  dataDirectory <- "/Volumes/Promise R6/Raw_Data/mzMLRPOS/"
	  savePath <- "/Volumes/Promise R6/Raw_Data/Example U RPOS XCMS.csv"
  
	  workers <- 8

	  setwd(dataDirectory)

	#########################################
	###----------DATA EXTRACTION----------###
	######################################### 

	  library(xcms)

	### centWave peak detection: suitable algorithm for high resolution LC/ToF data in centroid mode.  
	### note the parameters below have been optimised for Xevo G2-S data originating from the NPC Urine RP analysis in POS mode

	  ds <- xcmsSet(method="centWave", 
		  noise=600, 
		  ppm=25,
		  prefilter=c(8, 6000),
		  snthresh = 10,
		  peakwidth=c(1.5,5), 
		  mzdiff=0.01,
		  mzCenterFun="wMean",
		  integrate=2, 
		  lock=F,
		  fitgauss=F,
	      BPPARAM=SnowParam (workers = workers),  # number of core processors  
		  )

	#  Matches ("groups") peaks across samples (rtCheck = maximum amount of time from the median RT)

	# density method
	  gds<-group(ds, method="density",
		  minfrac=0,
		  minsamp=0,
		  bw=1,
		  mzwid=0.01,
		  sleep=0
		  )


	#   identify peak groups and integrate samples
	  fds <- fillPeaks(gds, method="chrom", BPPARAM=SnowParam (workers = workers))

	  write.csv(peakTable(fds), file=savePath)


Preprocessing and Quality Control of NMR Data with the nPYc-Toolbox
===================================================================

This tutorial demonstrates how to use the NMR data processing modules of the nPYc-Toolbox, to import and perform some basic preprocessing and quality control of NMR data, and to output a final high quality dataset ready for data modeling.

Required files in nPYc-toolbox-tutorials:

- Preprocessing and Quality Control of NMR Data with the nPYc-Toolbox.ipynb: Jupyter notebook tutorial for NMR (Bruker) data
- DEVSET U 1D NMR raw data files: folder containing the 1D NMR raw data files (Bruker format)
- DEVSET U 1D NMR Basic CSV.csv: CSV file containing basic metadata about each of the acquired samples


Preprocessing and Quality Control of NMR Targeted Data with the nPYc-Toolbox
============================================================================

This tutorial demonstrates how to use the NMR targeted data processing modules of the nPYc-Toolbox to 
import and perform some basic quality control of outputs from the Bruker IVDr targeted quantification methods and generate a final high
quality dataset ready for data modeling.

Required files in nPYc-toolbox-tutorials:

- Preprocessing and Quality Control of Targeted NMR Data (Bruker IVDr) with the nPYc-toolbox.ipynb: Jupyter notebook tutorial for targeted NMR (Bruker IVDr) data
- DEVSET U 1D NMR raw data files: folder containing the 1D NMR raw data files and the Bruker IVDr xml quantification files
- DEVSET U 1D NMR IVDr Basic CSV.csv: CSV file containing basic metadata about each of the acquired samples


.. [#] Matthew R Lewis, Jake TM Pearce, Konstantina Spagou, Martin Green, Anthony C Dona, Ada HY Yuen, Mark David, David J Berry, Katie Chappell, Verena Horneffer-van der Sluis, Rachel Shaw, Simon Lovestone, Paul Elliott, John Shockcor, John C Lindon, Olivier Cloarec, Zoltan Takats, Elaine Holmes and Jeremy K Nicholson. Development and Application of Ultra-Performance Liquid Chromatography-TOF MS for Precision Large Scale Urinary Metabolic Phenotyping. Analytical Chemistry, 88(18):9004-9013, 2016. URL: http://dx.doi.org/10.1021/acs.analchem.6b01481

.. [#] Jake TM Pearce, Toby J Athersuch, Timothy MD Ebbels, John C Lindon, Jeremy K Nicholson and Hector C Keun. Robust Algorithms for Automated Chemical Shift Calibration of 1D 1H NMR Spectra of Blood Serum. Analytical Chemistry, 80(18):7158-62, 2008. URL: http://dx.doi.org/10.1021/ac8011494

.. [#] Anthony C Dona, Beatriz Jiménez, Hartmut Schäfer, Eberhard Humpfer, Manfred Spraul, Matthew R Lewis, Jake TM Pearce, Elaine Holmes, John C Lindon and Jeremy K Nicholson. Precision High-Throughput Proton NMR Spectroscopy of Human Urine, Serum, and Plasma for Large-Scale Metabolic Phenotyping. Analytical Chemistry, 86(19):9887-9894, 2014. URL: http://dx.doi.org/10.1021/ac5025039