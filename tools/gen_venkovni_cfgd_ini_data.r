setwd("/home/hdd/data/16_smod_paper_optim/smoderp2d-optim-sens/")
files_ = list.files('../data_raw/obs_data_venk_raw/', pattern = '*.csv', full.names = T)
# jek pro testovani do tmp adresare
# musi koncit lomitkem /
outs = ''
plocha = 16 #m2

text_optim_cfg <- function(slope,rainfall,n,obs_data,model_out_path) {
  return (paste('[Params]
# in mm per hour
rainfall: ',rainfall,'
# slope [-]
slope: ',slope,'

# data area stored in data file
# where first col is time in minutes
# where second col is runoff in mm/min
# where cols are separated with tab
[ObsData]
rows: ',n,'
file: ',obs_data,'

[Model]
mod_file: ',model_out_path,'/point001.csv
', sep = ''))
}

text_model_ini <- function(model_out_path) {
  return (paste('[GIS]
dem: -
soil: -
lu: -
[shape atr]
soil-atr: -
lu-atr: -
[rainfall]
file: model/indata/rainfall.txt
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

text_cmd <- function(out_dir, model_ini, optim_cgs, mer_name){
  log = paste(outs,'logs/',paste(mer_name,'log',sep='.'),sep='')
  return(paste('./optim.py -o',out_dir,'-m',model_ini,'-O',optim_cgs,'&>',log))
}

for (i.file in files_) {
  r = read.table(i.file, header = TRUE, sep=',', dec='.')
  r = r[order(r$time_min),]
  # plot(r$time_min, r$discharge.l_min.1.)
  slope_prc = slope = r$sklon[1] # TODO prevest na procenta
  rainfall = r$rain[1]
  n = length(r$ID)
  obs_name = basename(i.file)
  mer_name = tools::file_path_sans_ext(obs_name)
  data_path = paste(outs,'obs_data/',obs_name,sep='')
  model_out_path = paste(outs,'model/','out-',mer_name,sep='')
  model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
  conf_path = paste(outs,'cfgs/',mer_name,'.cfgs',sep='')
  cas = r$time_min 
  val = (r$discharge.l_min.1./1000)/plocha*1000 # l/min -> mm/min
  # output path of optimiaztion
  out_pat = paste(outs,'outs/out-',mer_name,sep='')
  
  # write cli run
  write(text_cmd(out_pat,model_ini_path,conf_path,mer_name), 
        file = paste(outs,'runs_field_ds/',mer_name,sep=''))
  
  # write obs data
  write.table(x = data.frame(cas=cas, val=val),
              file = data_path,
              sep = '\t', dec = '.',
              col.names = FALSE, row.names = FALSE, 
              append = FALSE)
  
  # write optim cfg  
  write(text_optim_cfg(slope_prc, rainfall, n, data_path, model_out_path),
        file = conf_path)
  
  # write model ini
  write(text_model_ini(model_out_path), file = model_ini_path)
}



