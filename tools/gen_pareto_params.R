load('/home/jakub/ownCloud/Data-in-progress/16_smod_paper_optim/rdata.4/field/pareto_front_vysledky.4.04.fieldrs.rda', verbose = T)



npar = names(pareto.lists)

ipars = 18:23
for (inpar in npar)
{
  pars = pareto.lists[[inpar]][,ipars]
  newfiles <- paste('pareto_pars',gsub(".log$", ".paretopars", basename(inpar)),sep = '/')
  
  write.table(pars, file = newfiles, row.names = F, col.names = F)
}

