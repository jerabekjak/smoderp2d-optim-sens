# 1 - nacte merdata.RData
# 2 - udela csv do adresare obs_data
load_data = T
optim_ = T
sens_  = F
obs_dir = 'obs_data'
cfg_dir = 'cfgs'
cfg_dir_bf = 'cfgs_sens'
setwd('/home/jakub/Program/smoderp2d-optim-sens/')
if (load_data) {load('/home/hdd/data/13_smod_paper_citlivost/mer_sim_srovnani/merdata.RData')}

jm_DM = names(DM)

text_optim_cfg <- function(slope,rainfall,n,obs_data,model_out_path) {
  return (paste('[Params]
# in mm per hour
rainfall: ',rainfall,'
# slope [-]
slope: ',slope,'
# length of plot meters
plotlength: 4
# width of plot meters
plotwidth: 1

# data area stored in data file
# where first col is time in minutes
# where second col is runoff in mm/min
# where cols are separated with tab
[ObsData]
rows: ',n,'
file: ',obs_data,'

[Model]
mod_file: ',model_out_path,'/point001.dat
', sep = ''))
}



text_sens_cfg <- function(model_out_path, best_fit_dir) {
  return (paste('[SensParams]
# monte carlo runs
mcruns: 10000

[ParamsMargins]
# X,Y,b and ret are evenly distributed within margins 
X: 1,20
Y: 0.1,1
b: 1,2
Ks: 1e-8, 1e-5
S: 1e-8, 1e-3

# X,Y,b and ret are evenly distributed within margins 
ret: -0.1,0

[Model]
mod_file: ',model_out_path,'/point001.dat

# results folder of ./optim.py
# in this folder are obs data and model best fit (obs_mod.dat)
# and best with params with used rainfall and slope (params.dat)
[BestFit]
dir: ',best_fit_dir,'

', sep = ''))
}

text_cmd <- function(out_dir, model_ini, optim_cgs){
  log = paste('logs',paste(tools::file_path_sans_ext(out_dir),'log',sep='.'),sep='/')
  return(paste('./optim.py -o',out_dir,'-m',model_ini,'-O',optim_cgs,'>',log))
}


text_sens_cmd <- function(out_dir, model_ini, optim_cgs){
  log = paste('logs',paste(tools::file_path_sans_ext(out_dir),'log',sep='.'),sep='/')
  return(paste('./sens.py -o',out_dir,'-m',model_ini,'-O',optim_cgs,'>',log))
}


text_model_ini <- function(model_out_path) {
  return (paste('[GIS]
dem: -
soil: -
lu: -
[shape atr]
soil-atr: -
lu-atr: -
[srazka]
file: model/indata/srazka.txt
[time]
# sec
maxdt: 10
# min
endtime: 30
[Infiltration]
type: 1
[Other]
points: -
outdir: ',model_out_path,'
typecomp: 0
mfda: False
soilvegtab: -
soilvegcode: -
streamshp: -
streamtab: -
streamtabcode: -
arcgis: false
extraout: False
indata: model/indata/mala_ds.save
partialcomp: roff
logging: WARNING
printtimes:
'))
}

if (optim_){
  # for (jm_dm in jm_DM[1:12]){
  for (jm_dm in jm_DM){ # nucice
    # generate observed data 
    cas = DM[[jm_dm]]$usek_prum_min
    val = DM[[jm_dm]]$prutok_mm_min
    cas = cas[!is.na(val)]
    val = val[!is.na(val)]
    n = length(val)
    rainfall = DM[[jm_dm]]$intenzita_dest[1]
    slope_deg = DM[[jm_dm]]$sklon_stup[1]
    slope_prc = tan(slope_deg*pi/180) 
    scen = tools::file_path_sans_ext(jm_dm)
    conf_path = paste(cfg_dir,paste(scen,'cfg',sep='.'),sep='/')
    out_pat   = paste('out',scen,sep='-')
    model_out_path = paste('model',out_pat,sep='/')
    model_ini_path = paste('model',paste(scen,'ini',sep='.'),sep='/')
    data_path = paste(obs_dir,jm_dm,sep='/')
    
    # write cli run
    write(text_cmd(out_pat,model_ini_path,conf_path), file = paste('runs',scen,sep='/'))
    
    # write optim cfg
    write(text_optim_cfg(slope_prc, rainfall, n, data_path, model_out_path), file = conf_path)
    
    # write obs data
    write.table(x = data.frame(cas=cas, val=val),
                file = data_path,
                sep = '\t', dec = '.',col.names = FALSE, row.names = FALSE, append = FALSE)
    
    # write model ini
    write(text_model_ini(model_out_path), file = model_ini_path)
  }
}


if (sens_){
  # for (jm_dm in jm_DM[1:12]){
  for (jm_dm in jm_DM){ # nucice
    # generate observed data 
    cas = DM[[jm_dm]]$usek_prum_min
    val = DM[[jm_dm]]$prutok_mm_min
    cas = cas[!is.na(val)]
    val = val[!is.na(val)]
    n = length(val)
    rainfall = DM[[jm_dm]]$intenzita_dest[1]
    slope_deg = DM[[jm_dm]]$sklon_stup[1]
    slope_prc = tan(6*pi/180) 
    scen = tools::file_path_sans_ext(jm_dm)
    conf_path = paste(cfg_dir_bf,paste(scen,'cfg',sep='.'),sep='/')
    out_pat   = paste('out-sens',scen,sep='-')
    model_out_path = paste('model',paste('out',scen,sep='-'),sep='/')
    model_ini_path = paste('model',paste(scen,'ini',sep='.'),sep='/')
    data_path = paste(obs_dir,jm_dm,sep='/')
    # write cli run
    write(text_sens_cmd(out_pat,model_ini_path,conf_path), file = paste('runs_sens',scen,sep='/'))
    
    best_fit_dir = paste('best_fit',paste('out-',scen,sep=''),sep='/')
    # print (best_fit_dir)
    # write sens cfg
    write(text_sens_cfg(model_out_path,best_fit_dir),file = conf_path)
    

  }
}
