library("readxl")
setwd("/home/hdd/data/16_smod_paper_optim/smoderp2d-optim-sens/")
file_ = '../data_raw/obs_data_vnitrni_rychlosti/trebsin2_smoderp.xlsx'
file_ = '../data_raw/obs_data_vnitrni_rychlosti/trebsin2_smoderp_opraveno.xlsx'
file_ = '../data_raw/obs_data_vnitrni_rychlosti/nucice_rychlosti.xlsx'
file_ = '../data_raw/obs_data_vnitrni_rychlosti/vsetaty1_rychlosti.xlsx'
sheets = excel_sheets(file_)
pdf_ = T

outs = ''
plocha = 0.9*4 # m2 #TODO - skontrolovat
sirka = 0.9 # m #TODO - skontrolovat

text_optim_cfg <- function(slope,rainfall,
                           n.h, data_path.h,
                           n.q, data_path.q,
                           model_out_path) {
  return (paste('[Params]
# in mm per hour
rainfall: ',rainfall,'
# slope [-]
slope: ',slope,'
# length of plot meters
plotlength: 4
# width of plot meters
plotwidth: 0.9


# data area stored in data file
# where first col is time in minutes
# where second col is runoff in mm/min
# where cols are separated with tab
[ObsDataWLevel]
rows: ',n.h,'
file: ',data_path.h,'
[ObsDataDischarge]
rows: ',n.q,'
file: ',data_path.q,'

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


# 
if (pdf_) {pdf('Rplot.pdf')}
for (i.sheet in sheets) {
  r = read_xlsx(file_, sheet=i.sheet, col_names = F)
  id = paste(iconv(substring(r$...2[3], 1, 3),from="UTF-8",to="ASCII//TRANSLIT"),
             r$...2[2], r$...2[1], sep='-')
  mer_name = paste(id, 'labds', sep='-')
  
  obs_name.h = paste(mer_name,'-h', '.csv', sep = '')
  obs_name.q = paste(mer_name,'-q', '.csv', sep = '')
  data_path.h = paste(outs,'obs_data/',obs_name.h, sep='')
  data_path.q = paste(outs,'obs_data/',obs_name.q, sep='')
  model_out_path = paste(outs,'model/',mer_name,sep='')
  model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
  conf_path = paste(outs,'cfgs/',mer_name,'.cfgs',sep='')
  # output path of optimiaztion
  out_pat = paste(outs,'outs/',mer_name,sep='')
  
  n = length(r$...1)
  slope_stup = as.numeric(r$...2[5])
  slope_rad = slope_stup*pi/180
  slope_prc = tan(slope_rad)
  rainfall = as.numeric(r$...2[4])
  
  # vypocet prutoku
  cas.q = as.numeric(r$...1[8:length(r$...1)])
  prutok_kg = as.numeric(r$...2[8:length(r$...1)])
  cas.q = cas.q[!is.na(prutok_kg)]
  prutok_kg = prutok_kg[!is.na(prutok_kg)]
  n.cas.q = length(cas.q)
  n.q = length(which(!is.na(r$...2[8:length(r$...1)])))
  dt = cas.q[2:n.cas.q] - cas.q[1:(n.cas.q-1)] # minuty
  prutok_l_min = prutok_kg[2:n.q]/dt
  prutok_m3_s = prutok_l_min/1000/60 

  # prutok jde ven
  prutok = prutok_m3_s/plocha*1000*60 # m3/sec -> mm/min 
  
  # zapis 
  outdata = data.frame(cas.q,c(0,prutok))
  plot(outdata, main=mer_name)
  write.table(outdata, file = data_path.q, sep = '\t',
              col.names = F, row.names = F)
  
  # # vyska hladiny
  cas.h = as.numeric(r$...1[8:length(r$...1)])
  v = as.numeric(r$...3[8:length(r$...1)]) # cas v sec za 0.5 metru
  v = 0.5/v # m/s
  cas.h = cas.h[!is.na(v)]
  v = v[!is.na(v)]
  n.h = length(which(!is.na(r$...3[8:length(r$...1)])))

  # pritok pro cas mereni rychlosti
  splfun = splinefun(x=cas.q, y=c(0,prutok_m3_s))
  # h jde ven
  h = splfun(cas.h)/v/sirka # vyska hladiny na useku m
  
  # zapis 
  outdata = data.frame(cas.h, h)
  plot(outdata, main=mer_name)
  write.table(outdata, file = data_path.h, sep = '\t',
              col.names = F, row.names = F)
  
  # 
  # # write cli run
  write(text_cmd(out_pat,model_ini_path,conf_path,mer_name),
        file = paste(outs,'runs_lab_ds_waterheight/',mer_name,sep=''))
  #  
  # # write optim cfg
  write(text_optim_cfg(slope_prc, rainfall,
                       n.h, data_path.h,
                       n.q, data_path.q,
                       model_out_path),
        file = conf_path)
  # 
  # write model ini
  write(text_model_ini(model_out_path), file = model_ini_path)
  
  #TODO - ju jsem skoncil
  
#   for (i.id in id) 
#   {
#     ii = which(r$ID.simulace == i.id)
#     d = r[ii,]
#     
#     # moje id simulace
#     mer_name = paste(
#       as.character(as.Date(d$datum[1], "%d. %m. %Y")),
#       chartr("řščý", "rscy", tolower(d$lokalita[1])),
#       as.character(d$ID.simulace[1]),
#       sep = '-'
#     )
#     # csv simulace
#     obs_name.h = paste(mer_name,'-h', '.csv', sep = '')
#     obs_name.q = paste(mer_name,'-q', '.csv', sep = '')
#     data_path.h = paste(outs,'obs_data/',obs_name.h, sep='')
#     data_path.q = paste(outs,'obs_data/',obs_name.q, sep='')
#     model_out_path = paste(outs,'model/','out-',mer_name,sep='')
#     model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
#     conf_path = paste(outs,'cfgs/',mer_name,'.cfgs',sep='')
#     # output path of optimiaztion
#     out_pat = paste(outs,'outs/out-',mer_name,sep='')
#     
#     cas = as.POSIXct(strptime(d$čas.od.začátku.simulace, "%H:%M:%S"))
#     cas = minute(cas) + second(cas)/60
#     slope_prc = d$sklon.terénu[1]
#     rainfall = d$intenzita[1]
#     n.h = length(d$rychlost.na.posledním.úseku..m.s.[!is.na(d$rychlost.na.posledním.úseku..m.s.)])
#     n.q = length(d$průtok..l.min.[!is.na(d$průtok..l.min.)])
#     prutok_m3_s = d$průtok..l.min./1000/60
#     # prutok jde ven
#     prutok = (d$průtok..l.min./1000)/plocha*1000 # l/min -> mm/min
#     v = d$rychlost.na.posledním.úseku..m.s. # m/s
#     # h jde ven
#     h = prutok_m3_s/v/sirka # vyska hladiny na useku m
#     
#     # zapis pozorovanych dat
#     # outdata = data.frame(cas, prutok, h)
#     outdata = data.frame(cas, h)
#     outdata = outdata[!is.na(outdata$h),]
#     outdata = outdata[order(outdata$cas),]
#     plot(outdata, main=mer_name)
#     write.table(outdata, file = data_path.h, sep = '\t', 
#                 col.names = F, row.names = F)
#     outdata = data.frame(cas, prutok)
#     outdata = outdata[order(outdata$cas),]
#     plot(outdata, main=mer_name, ylim=range(outdata$prutok, rainfall/60))
#     abline(h = rainfall/60)
#     write.table(outdata, file = data_path.q, sep = '\t', 
#                 col.names = F, row.names = F)
#     # 
#     # # write cli run
#     write(text_cmd(out_pat,model_ini_path,conf_path,mer_name),
#           file = paste(outs,'runs_field_ds_waterheight/',mer_name,sep=''))
#     #  
#     # # write optim cfg
#     write(text_optim_cfg(slope_prc, rainfall,
#                          n.h, data_path.h,
#                          n.q, data_path.q,
#                          model_out_path),
#           file = conf_path)
#     # 
#     # write model ini
#     write(text_model_ini(model_out_path), file = model_ini_path)
#   }
}
if (pdf_) {dev.off()}
# 
# 
# 
