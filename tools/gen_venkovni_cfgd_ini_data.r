setwd("/home/hdd/data/16_smod_paper_optim")
files_ = list.files('data_raw/obs_data_venk_raw/', pattern = '*.csv', full.names = T)
outs = 'rscript-outs/'

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
mod_file: ',model_out_path,'/point001.dat
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

for (i.file in files_[1:3]) {
  r = read.table(i.file, header = TRUE, sep=',', dec='.')
  r = r[order(r$time_min),]
  # plot(r$time_min, r$discharge.l_min.1.)
  slope_prc = slope = r$sklon[1]
  rainfall = r$rain[1]
  n = length(r$ID)
  obs_name = basename(i.file)
  mer_name = tools::file_path_sans_ext(obs_name)
  obs_data = paste(outs,'obs_data/',obs_name,sep='')
  model_out_path = paste(outs,'model/','out-',mer_name,sep='')
  model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
  
  conf_path = paste(outs,'cfgs/',mer_name,'.cfgs',sep='')
  
  # write cli run
  # write(text_cmd(out_pat,model_ini_path,conf_path), file = paste('runs',scen,sep='/'))
  
  # write obs data
  # write.table(x = data.frame(cas=cas, val=val),
              # file = data_path,
              # sep = '\t', dec = '.',col.names = FALSE, row.names = FALSE, append = FALSE)
  
  # write optim cfg  
  write(text_optim_cfg(slope_prc, rainfall, n, obs_data, model_out_path),
        file = conf_path)
  
  # write model ini
  print (model_ini_path)
  write(text_model_ini(model_out_path), file = model_ini_path)
}



