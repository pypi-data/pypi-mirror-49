Classical PSHA with NZ NSHM
===========================

============== ===================
checksum32     3,211,843,635      
date           2019-06-24T15:34:29
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 1, num_levels = 29, num_rlzs = 1

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 400.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                0.1               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     23                
master_seed                     0                 
ses_seed                        42                
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= ================ ================
smlt_path weight  gsim_logic_tree  num_realizations
========= ======= ================ ================
b1        1.00000 trivial(1,1,0,0) 1               
========= ======= ================ ================

Required parameters per tectonic region type
--------------------------------------------
====== ===================== ========= ========== ===================
grp_id gsims                 distances siteparams ruptparams         
====== ===================== ========= ========== ===================
0      '[McVerry2006Asc]'    rrup      vs30       hypo_depth mag rake
1      '[McVerry2006SInter]' rrup      vs30       hypo_depth mag rake
====== ===================== ========= ========== ===================

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=1)>

Number of ruptures per tectonic region type
-------------------------------------------
================================ ====== ==================== ============ ============
source_model                     grp_id trt                  eff_ruptures tot_ruptures
================================ ====== ==================== ============ ============
NSHM_source_model-editedbkgd.xml 0      Active Shallow Crust 40           40          
NSHM_source_model-editedbkgd.xml 1      Subduction Interface 2            2           
================================ ====== ==================== ============ ============

============= ==
#TRT models   2 
#eff_ruptures 42
#tot_ruptures 42
#tot_weight   42
============= ==

Slowest sources
---------------
====== ========= ==== ====== ====== ============ ========= ========= ======= =============
grp_id source_id code gidx1  gidx2  num_ruptures calc_time num_sites weight  checksum     
====== ========= ==== ====== ====== ============ ========= ========= ======= =============
1      21444     X    2      20,504 1            0.00254   1.00000   1.00000 4,233,194,492
0      1         P    0      1      20           0.00250   1.00000   20      2,880,202,396
0      2         P    1      2      20           2.894E-04 1.00000   20      1,098,999,712
1      21445     X    20,504 34,373 1            2.761E-04 1.00000   1.00000 683,422,937  
====== ========= ==== ====== ====== ============ ========= ========= ======= =============

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
P    0.00278   2     
X    0.00281   2     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ========= ======= ======= =======
operation-duration mean    stddev    min     max     outputs
preclassical       0.00338 6.912E-06 0.00338 0.00339 2      
read_source_models 0.21629 NaN       0.21629 0.21629 1      
================== ======= ========= ======= ======= =======

Data transfer
-------------
================== ========================================================= =========
task               sent                                                      received 
preclassical       srcs=808.98 KB params=1.34 KB srcfilter=440 B gsims=302 B 778 B    
read_source_models converter=313 B fnames=123 B                              809.06 KB
================== ========================================================= =========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total read_source_models 0.21629   0.19922   1     
total preclassical       0.00677   0.0       2     
managing sources         0.00347   0.0       1     
store source_info        0.00154   0.0       1     
aggregate curves         3.126E-04 0.0       2     
======================== ========= ========= ======