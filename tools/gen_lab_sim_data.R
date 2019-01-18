# 1 - nacte merdata.RData
# 2 - udela csv do adresare obs_data
load_data = FALSE
setwd('/home/jakub/Program/smoderp2d-optim-sens/')
if (load_data) {load('/home/hdd/data/13_smod_paper_citlivost/mer_sim_srovnani/merdata.RData')}

jm_DM = names(DM)

for (jm_dm in jm_DM){
  cas = DM[[jm_dm]]$usek_prum_min
  val = DM[[jm_dm]]$prutok_mm_min
  write.table(x = data.frame(cas=cas, val=val), 
              file = paste('obs_data',jm_dm,sep='/'),
              sep = '\t', dec = '.',col.names = FALSE, row.names = FALSE)
}



