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

text_sens_cfg <- function(model_out_path, best_fit_dir) {
  return (paste('[SensParams]
### NOT USED IN q_h_optim branch
[SensParams]
# monte carlo runs
mcruns: 10000

### NOT USED IN q_h_optim branch
[ParamsMargins]
# X,Y,b and ret are evenly distributed within margins 
X: 1,10
Y: 0.1,1
b: 1,2
Ks: 5.578442e-07, 7.727984e-06
S: 0.0000839344, 0.0003146327

# X,Y,b and ret are evenly distributed within margins 
ret: -0.01,0

[Params]
# length of plot meters
plotlength: 4
# width of plot meters
plotwidth: 0.9

[Model]
mod_file: ',model_out_path,'/point001.csv

# results folder of ./optim.py
# in this folder are obs data and model best fit (obs_mod.dat)
# and best with params with used rainfall and slope (params.dat)
[BestFit]
dir: ',best_fit_dir,'

', sep = ''))
}

text_cmd <- function(out_dir, model_ini, conf_path, mer_name){
  log = paste(outs,'logs_sens/',paste(mer_name,'log',sep='.'),sep='')
  return(paste('./sens.py -o',out_dir,'-m',model_ini,'-O',conf_path,'&>',log))
}


# 
if (pdf_) {pdf('Rplot.pdf')}
for (i.sheet in sheets) {
  r = read_xlsx(file_, sheet=i.sheet, col_names = F)
  id = paste(iconv(substring(r$...2[3], 1, 3),from="UTF-8",to="ASCII//TRANSLIT"),
             r$...2[2], r$...2[1], sep='-')
  mer_name = paste(id, 'labds', sep='-')
  
  #obs_name.h = paste(mer_name,'-h', '.csv', sep = '')
  #obs_name.q = paste(mer_name,'-q', '.csv', sep = '')
  #data_path.h = paste(outs,'obs_data/',obs_name.h, sep='')
  #data_path.q = paste(outs,'obs_data/',obs_name.q, sep='')
  model_out_path = paste(outs,'model/',mer_name,sep='')
  model_ini_path =paste(outs,'model/',paste(mer_name,'ini',sep='.'),sep='')
  conf_path = paste(outs,'cfgs_sens/',mer_name,'.cfgs',sep='')
  # output path of optimiaztion
  best_fit_dir = paste(outs,'best_fit/',mer_name,sep='')
  out_dir = paste(outs,'outs_sens/',mer_name,sep='')
  
  
  # 
  # # write cli run
  write(text_cmd(out_dir,model_ini_path,conf_path,mer_name),
        file = paste(outs,'runs_sens_lab_ds_waterlevel/',mer_name,sep=''))
  #  
  # # write optim cfg
  write(text_sens_cfg(model_out_path, 
                       best_fit_dir),
        file = conf_path)
  
}
if (pdf_) {dev.off()}
