library(lubridate)
setwd("/home/hdd/data/16_smod_paper_optim/smoderp2d-optim-sens/")
files_ = list.files('../data_raw/obs_data_venku_prutok_ruchlost_raw/', pattern = '*.csv', full.names = T)

outs = ''
plocha = 16 # m2
sirka = 2 # m

text_optim_cfg <- function(slope,rainfall,n,obs_data,model_out_path) {
  return (paste('[Params]
# in mm per hour
rainfall: ',rainfall,'
# slope [-]
slope: ',slope,'
# length of plot meters
plotlength: 8
# width of plot meters
plotwidth: 2
 

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
  id = unique(r$ID.simulace)
  for (i.id in id) 
  {
    ii = which(r$ID.simulace == i.id)
    d = r[ii,]
    
    # moje id simulace
    mer_name = paste(
      as.character(as.Date(d$datum[1], "%d. %m. %Y")),
      chartr("řščý", "rscy", tolower(d$lokalita[1])),
      as.character(d$ID.simulace[1]),
      sep = '-'
    )
    # csv simulace
    obs_name = paste(mer_name, 'csv', sep = '.')
    data_path = paste(outs,'obs_data/',obs_name, sep='')
    model_out_path = paste(outs,'model/','out-',mer_name,sep='')
    model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
    conf_path = paste(outs,'cfgs/',mer_name,'.cfgs',sep='')
    # output path of optimiaztion
    out_pat = paste(outs,'outs/out-',mer_name,sep='')
    
    cas = as.POSIXct(strptime(d$čas.od.začátku.simulace, "%H:%M:%S"))
    cas = minute(cas) + second(cas)/60
    slope_prc = d$sklon.terénu[1]
    rainfall = d$intenzita[1]
    n = length(d$ID.simulace)
    prutok_m3_s = d$průtok..l.min./1000/60
    # prutok jde ven
    prutok = (d$průtok..l.min./1000)/plocha*1000 # l/min -> mm/min
    v = d$rychlost.na.posledním.úseku..m.s. # m/s
    # h jde ven
    h = prutok_m3_s/v/sirka # vyska hladiny na useku m
    
    # zapis pozorovanych dat
    # outdata = data.frame(cas, prutok, h)
    outdata = data.frame(cas, h)
    write.table(outdata, file = data_path, sep = '\t', col.names = F, row.names = F)

    # write cli run
    write(text_cmd(out_pat,model_ini_path,conf_path,mer_name),
          file = paste(outs,'runs_field_ds_waterheight/',mer_name,sep=''))
     
    # write optim cfg
    write(text_optim_cfg(slope_prc, rainfall, n, data_path, model_out_path),
          file = conf_path)

    # write model ini
    write(text_model_ini(model_out_path), file = model_ini_path)
  }
}



