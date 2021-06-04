Built-in Configuration SOPs
===========================

The following tables list, define and give default values for all of the SOP parameters for each method.

All Dataset Objects
^^^^^^^^^^^^^^^^^^^

.. table::  Required SOP parameters for all :py:class:`~nPYc.objects.Dataset` objects
	:widths: auto

	================ ========================================= ===================== ============
	Key              Type                                      Default value         Role
	================ ========================================= ===================== ============
	'noFiles'        int                                       10                    When showing a ranked list of files show only the top/bottom *noFiles*
	'dpi'            int                                       300                   Raster resolution when plotting figures
	'figureSize'     list of float                             [11,7]                Size to plot figures
	'figureFormat'   str                                       'png'                 Format to save figures in
	'histBins'       int                                       100                   Number of bins to use when drawing histograms
	'quantiles'      list of float                             [25, 75]              When calculating percentiles, use this default range
	================ ========================================= ===================== ============

.. table::  Optional SOP parameters for all :py:class:`~nPYc.objects.Dataset` objects
	:widths: auto

	=============================== ============= ===================== ============
	Key                             Type          Default value         Role
	=============================== ============= ===================== ============
	'analyticalMeasurements'        dict          {}                    Set of key, value pairs where each key is a column in :py:attr:`~nPYc.objects.Dataset.sampleMetadata` and the value is 'categorical' or 'continuous' depending on parameter type. Columns described here will be checked for association in the multivariate quality control reports when run with the analytical setting.
	'excludeFromPlotting'           list of str   []                    Column names in :py:attr:`~nPYc.objects.Dataset.sampleMetadata` to exclude from plotting
	'sampleMetadataNotExported'     list of str   ["Exclusion Details"] Column names in :py:attr:`~nPYc.objects.Dataset.sampleMetadata` to exclude from data export
	'featureMetadataNotExported'    list of str   []                    Column names in :py:attr:`~nPYc.objects.Dataset.featureMetadata` to exclude from data export    
	=============================== ============= ===================== ============


MSDataset Objects
^^^^^^^^^^^^^^^^^

.. table:: SOP parameters for all :py:class:`~nPYc.objects.MSDataset` objects
	:widths: auto

	============================= ============ ========================== ==================================================================================
	Parameter                     Type    	   Default value              Role
	============================= ============ ========================== ==================================================================================            
	'corrThreshold'                float       0.7                        When filtering features by correlation to dilution using the :term:`Serial Dilution Sample`, the correlation must be above this
	'corrMethod'                   str         'pearson'                  Type of correlation to linearity to calculate, must be 'pearson' or 'spearman'
	'rsdThreshold'                 float       30                         When filtering features by :term:`RSD`, the RSD must be below this
	'varianceRatio'                float       1.1                        When filtering features RSD in Study Samples must be at least RSD in Precision Reference * this value
	'blankThreshold'               float       1.1                        When filtering features RSD in Study Samples must be at least RSD in Procedural Blank samples * this value
	'artifactualFilter'            str (bool)  'False'                    Flag for whether artifactual filtering should be applied when filtering features
	'deltaMzArtifactual'           float       0.1                        'artifactualFilter' parameter: Maximum allowed m/z distance between two grouped features
	'overlapThresholdArtifactual'  int         50                         'artifactualFilter' parameter: Minimum peak overlap between two grouped features
	'corrThresholdArtifactual'     float       0.9                        'artifactualFilter' parameter: Minimum correlation between two grouped features
	'filenameSpec'                 str (regex) see 'GenericMS.json'       Regular expression to pull out information from raw MS data filenames (as per NPC standard naming conventions)
	============================= ============ ========================== ==================================================================================


NMRDataset Objects
^^^^^^^^^^^^^^^^^^

.. table:: SOP parameters for all :py:class:`~nPYc.objects.NMRDataset` objects
	:widths: auto

	============================= ============================= ======================================= ======================================= ==================================================================================
	Parameter                     Type                          Default value (for GenericNMRUrine)     Default value (for GenericNMRBlood)     Role
	============================= ============================= ======================================= ======================================= ==================================================================================
	'bounds'                      list of float                 [-1, 10]                                [-1, 10]                                Region of the original spectrum to re-interpolate and retain
	'variableSize'                int                           20000                                   20000                                   Number of points in the re-interpolated spectrum
	'alignTo'                     str                           ‘singlet’                               ‘doublet’                               Type of signal to calibrate to
	'calibrateTo'                 float                         0                                       5.233                                   Chemical shift value to calibrate to
	'ppmSearchRange'              list of float                 [-0.3, 0.3]                             [4.9, 5.733]                            Chemical shift region to search for calibration signal
	'LWpeakMultiplicity'          str                           ‘singlet’                               'quartet'								Type of signal used to measure line width
	'LWpeakRange'                 list of float                 [-0.1, 0.1]                             [4.08, 4.14]                            Chemical shift region to search for line width signal
	'LWFailThreshold'             float                         1.3										1.3                                     Line-width check cut-off in Hz
	'baselineCheckRegion'         list of list pairs of floats  [[-2, -0.5], [9.5, 12.5]]				[[-2, -0.5], [9.5, 12.5]]               Chemical shift regions to use in baseline quality checks
	'solventPeakCheckRegion'      list of list pairs of floats  [[4.6, 4.7],[4.9,5]]                    [[4.4, 4.5], [4.85,5]]                  Chemical shift regions to use in water suppression quality checks
	'exclusionRegions'            list of list pairs of floats  [[-0.2,0.2],[4.7,4.9]]                  [[-0.2,0.2],[4.5,4.85]]                 Chemical shift regions to mark for exclusion by default during pre-processing
	============================= ============================= ======================================= ======================================= ==================================================================================
