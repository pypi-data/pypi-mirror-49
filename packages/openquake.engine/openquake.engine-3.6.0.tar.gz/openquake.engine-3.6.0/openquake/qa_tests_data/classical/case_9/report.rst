Classical Hazard QA Test, Case 9
================================

============== ===================
checksum32     774,957,335        
date           2019-06-24T15:34:10
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 1, num_levels = 4, num_rlzs = 2

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                0.0               
rupture_mesh_spacing            0.01              
complex_fault_mesh_spacing      0.01              
width_of_mfd_bin                0.001             
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
b1_b2     0.50000 trivial(1)      1               
b1_b3     0.50000 trivial(1)      1               
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
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 3,000        3,000       
source_model.xml 1      Active Shallow Crust 3,500        3,000       
================ ====== ==================== ============ ============

============= =====
#TRT models   2    
#eff_ruptures 6,500
#tot_ruptures 6,000
#tot_weight   6,500
============= =====

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight checksum   
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========
1      1         P    1     2     3,500        0.01162   1.00000   3,500  413,684,838
0      1         P    0     1     3,000        0.01070   1.00000   3,000  960,386,158
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
P    0.02232   2     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ========= ======= ======= =======
operation-duration mean    stddev    min     max     outputs
preclassical       0.01161 5.595E-04 0.01121 0.01200 2      
read_source_models 0.01814 0.02025   0.00383 0.03246 2      
================== ======= ========= ======= ======= =======

Data transfer
-------------
================== ===================================================== ========
task               sent                                                  received
preclassical       srcs=2.34 KB params=974 B srcfilter=440 B gsims=294 B 688 B   
read_source_models converter=626 B fnames=212 B                          3.13 KB 
================== ===================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total read_source_models 0.03629   0.0       2     
total preclassical       0.02322   0.0       2     
managing sources         0.00301   0.0       1     
store source_info        0.00181   0.0       1     
aggregate curves         3.493E-04 0.0       2     
======================== ========= ========= ======