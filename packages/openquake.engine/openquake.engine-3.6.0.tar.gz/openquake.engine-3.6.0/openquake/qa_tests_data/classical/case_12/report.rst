Classical Hazard QA Test, Case 12
=================================

============== ===================
checksum32     662,604,775        
date           2019-06-24T15:34:26
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 1, num_levels = 3, num_rlzs = 1

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                2.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     1066              
master_seed                     0                 
ses_seed                        42                
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        1.00000 trivial(1,1)    1               
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ==================================================== ========= ========== ==========
grp_id gsims                                                distances siteparams ruptparams
====== ==================================================== ========= ========== ==========
0      '[SadighEtAl1997]'                                   rrup      vs30       mag rake  
1      '[NRCan15SiteTerm]\ngmpe_name = "BooreAtkinson2008"' rjb       vs30       mag rake  
====== ==================================================== ========= ========== ==========

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=1)>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 1            1           
source_model.xml 1      Stable Continental   1            1           
================ ====== ==================== ============ ============

============= =======
#TRT models   2      
#eff_ruptures 2      
#tot_ruptures 2      
#tot_weight   2.00000
============= =======

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ======= =============
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight  checksum     
====== ========= ==== ===== ===== ============ ========= ========= ======= =============
0      1         P    0     1     1            0.00251   1.00000   1.00000 3,030,339,619
1      2         P    1     2     1            0.00247   1.00000   1.00000 27,612,088   
====== ========= ==== ===== ===== ============ ========= ========= ======= =============

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
P    0.00498   2     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ========= ======= ======= =======
operation-duration mean    stddev    min     max     outputs
preclassical       0.00303 4.350E-05 0.00300 0.00306 2      
read_source_models 0.00224 NaN       0.00224 0.00224 1      
================== ======= ========= ======= ======= =======

Data transfer
-------------
================== ===================================================== ========
task               sent                                                  received
preclassical       srcs=2.31 KB params=956 B gsims=920 B srcfilter=440 B 686 B   
read_source_models converter=313 B fnames=107 B                          1.98 KB 
================== ===================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total preclassical       0.00607   0.0       2     
managing sources         0.00342   0.0       1     
total read_source_models 0.00224   0.0       1     
store source_info        0.00165   0.0       1     
aggregate curves         3.588E-04 0.0       2     
======================== ========= ========= ======