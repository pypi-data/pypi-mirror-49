QA test for blocksize independence (hazard)
===========================================

============== ===================
checksum32     2,348,158,649      
date           2019-06-24T15:33:44
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 2, num_levels = 4, num_rlzs = ?

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    1                 
maximum_distance                {'default': 400.0}
investigation_time              5.0               
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            20.0              
complex_fault_mesh_spacing      20.0              
width_of_mfd_bin                0.5               
area_source_discretization      20.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     42                
master_seed                     0                 
ses_seed                        1024              
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

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ====== =============
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight checksum     
====== ========= ==== ===== ===== ============ ========= ========= ====== =============
0      9         A    32    36    222          0.0       0.0       0.0    4,100,510,775
0      8         A    28    32    447          0.0       0.0       0.0    4,081,254,924
0      7         A    24    28    1,028        0.0       0.0       0.0    3,332,044,830
0      6         A    20    24    316          0.0       0.0       0.0    2,904,739,031
0      5         A    16    20    518          0.0       0.0       0.0    6,747,738    
0      4         A    12    16    267          0.0       0.0       0.0    1,512,426,850
0      3         A    8     12    440          0.0       0.0       0.0    3,749,296,307
0      2         A    4     8     582          0.0       0.0       0.0    2,638,530,210
0      1         A    0     4     1,752        0.0       0.0       0.0    2,668,493,271
====== ========= ==== ===== ===== ============ ========= ========= ====== =============

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    0.0       9     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =======
operation-duration mean    stddev min     max     outputs
read_source_models 0.50215 NaN    0.50215 0.50215 1      
================== ======= ====== ======= ======= =======

Data transfer
-------------
================== ============================ ========
task               sent                         received
read_source_models converter=313 B fnames=111 B 9.45 KB 
================== ============================ ========

Slowest operations
------------------
======================== ======== ========= ======
operation                time_sec memory_mb counts
======================== ======== ========= ======
total read_source_models 0.50215  0.0       1     
======================== ======== ========= ======