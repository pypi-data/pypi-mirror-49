Classical Hazard QA Test, Case 17
=================================

============== ===================
checksum32     1,496,028,179      
date           2019-06-24T15:34:12
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 1, num_levels = 3, num_rlzs = 5

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    5                 
maximum_distance                {'default': 200.0}
investigation_time              1000.0            
ses_per_logic_tree_path         1                 
truncation_level                2.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     106               
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
b1        0.20000 trivial(1)      1               
b2        0.20000 trivial(1)      1               
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

  <RlzsAssoc(size=2, rlzs=5)>

Number of ruptures per tectonic region type
-------------------------------------------
================== ====== ==================== ============ ============
source_model       grp_id trt                  eff_ruptures tot_ruptures
================== ====== ==================== ============ ============
source_model_1.xml 0      Active Shallow Crust 39           39          
source_model_2.xml 1      Active Shallow Crust 7            7           
================== ====== ==================== ============ ============

============= ==
#TRT models   2 
#eff_ruptures 46
#tot_ruptures 46
#tot_weight   46
============= ==

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ======= =============
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight  checksum     
====== ========= ==== ===== ===== ============ ========= ========= ======= =============
0      1         P    0     1     39           0.00246   1.00000   39      2,332,403,911
1      2         P    1     2     7            2.325E-04 1.00000   7.00000 3,408,621,621
====== ========= ==== ===== ===== ============ ========= ========= ======= =============

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
P    0.00269   2     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ========= ======= ======= =======
operation-duration mean    stddev    min     max     outputs
preclassical       0.00325 NaN       0.00325 0.00325 1      
read_source_models 0.00162 9.609E-05 0.00156 0.00169 2      
================== ======= ========= ======= ======= =======

Data transfer
-------------
================== ==================================================== ========
task               sent                                                 received
preclassical       srcs=1.8 KB params=478 B srcfilter=220 B gsims=147 B 394 B   
read_source_models converter=626 B fnames=218 B                         3.4 KB  
================== ==================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total preclassical       0.00325   0.0       1     
total read_source_models 0.00325   0.0       2     
managing sources         0.00259   0.0       1     
store source_info        0.00165   0.0       1     
aggregate curves         1.516E-04 0.0       1     
======================== ========= ========= ======