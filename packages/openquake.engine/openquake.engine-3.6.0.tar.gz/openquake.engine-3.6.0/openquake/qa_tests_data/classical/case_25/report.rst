Classical Hazard QA Test, Case 25, topographic surface1 (Mt Etna)
=================================================================

============== ===================
checksum32     3,398,720,512      
date           2019-06-24T15:34:04
engine_version 3.6.0-git4b6205639c
============== ===================

num_sites = 6, num_levels = 3, num_rlzs = 1

Parameters
----------
=============================== ==================
calculation_mode                'preclassical'    
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                0.1               
area_source_discretization      1.0               
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
sites                   `sites.csv <sites.csv>`_                                    
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        1.00000 trivial(1)      1               
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ======================= ========== ========== ==========
grp_id gsims                   distances  siteparams ruptparams
====== ======================= ========== ========== ==========
0      '[TusaLanger2016Rhypo]' rhypo rrup vs30       mag       
====== ======================= ========== ========== ==========

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ======== ============ ============
source_model     grp_id trt      eff_ruptures tot_ruptures
================ ====== ======== ============ ============
source_model.xml 0      Volcanic 440          440         
================ ====== ======== ============ ============

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========
grp_id source_id code gidx1 gidx2 num_ruptures calc_time num_sites weight checksum   
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========
0      1         A    0     8     440          0.00173   6.00000   597    108,330,929
====== ========= ==== ===== ===== ============ ========= ========= ====== ===========

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    0.00173   1     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =======
operation-duration mean    stddev min     max     outputs
preclassical       0.00211 NaN    0.00211 0.00211 1      
read_source_models 0.01570 NaN    0.01570 0.01570 1      
================== ======= ====== ======= ======= =======

Data transfer
-------------
================== ===================================================== ========
task               sent                                                  received
preclassical       srcs=2.04 KB params=478 B srcfilter=220 B gsims=162 B 344 B   
read_source_models converter=313 B fnames=107 B                          2.38 KB 
================== ===================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total read_source_models 0.01570   0.0       1     
managing sources         0.00268   0.0       1     
total preclassical       0.00211   0.0       1     
store source_info        0.00150   0.0       1     
aggregate curves         1.435E-04 0.0       1     
======================== ========= ========= ======