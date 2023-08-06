Classical Hazard QA Test, Case 7
================================

============== ===================
checksum32     750,810,642        
date           2019-06-24T15:34:16
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 1, num_levels = 3, num_rlzs = 2

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                0.0               
rupture_mesh_spacing            0.1               
complex_fault_mesh_spacing      0.1               
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
b1        0.70000 trivial(1)      1               
b2        0.30000 trivial(1)      1               
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================== ========= ========== ==========
grp_id gsims              distances siteparams ruptparams
====== ================== ========= ========== ==========
0      '[SadighEtAl1997]' rrup      vs30       mag rake  
1      '[SadighEtAl1997]' rrup      vs30       mag rake  
====== ================== ========= ========== ==========

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=2)>

Number of ruptures per tectonic region type
-------------------------------------------
================== ====== ==================== ============ ============
source_model       grp_id trt                  eff_ruptures tot_ruptures
================== ====== ==================== ============ ============
source_model_1.xml 0      Active Shallow Crust 140          140         
source_model_2.xml 1      Active Shallow Crust 91           91          
================== ====== ==================== ============ ============

============= ===
#TRT models   2  
#eff_ruptures 231
#tot_ruptures 231
#tot_weight   231
============= ===

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ====== =============
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight checksum     
====== ========= ==== ===== ===== ============ ========= ========= ====== =============
0      1         S    0     2     91           0.00585   1.00000   91     2,467,051,443
0      2         C    2     8     49           0.00454   1.00000   49     3,136,832,506
1      1         S    8     10    91           0.0       0.0       0.0    2,467,051,443
====== ========= ==== ===== ===== ============ ========= ========= ====== =============

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
C    0.00454   1     
S    0.00585   2     
==== ========= ======

Duplicated sources
------------------
Found 1 source(s) with the same ID and 1 true duplicate(s): ['1']

Information about the tasks
---------------------------
================== ======= ========= ======= ======= =======
operation-duration mean    stddev    min     max     outputs
preclassical       0.00572 9.510E-04 0.00505 0.00640 2      
read_source_models 0.08812 0.08234   0.02989 0.14634 2      
================== ======= ========= ======= ======= =======

Data transfer
-------------
================== ===================================================== ========
task               sent                                                  received
preclassical       srcs=2.24 KB params=956 B srcfilter=440 B gsims=294 B 691 B   
read_source_models converter=626 B fnames=216 B                          3.54 KB 
================== ===================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total read_source_models 0.17623   0.0       2     
total preclassical       0.01145   0.0       2     
managing sources         0.00295   0.0       1     
store source_info        0.00185   0.0       1     
aggregate curves         4.673E-04 0.0       2     
======================== ========= ========= ======