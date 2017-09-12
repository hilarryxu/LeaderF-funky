if exists('g:loaded_leaderf_funky') || &cp || v:version < 700
  finish
endif
let g:loaded_leaderf_funky = 1

command! -nargs=? LeaderfFunky call leaderf#funky#start_explorer(g:Lf_WindowPosition, <q-args>)

call g:LfRegisterSelf('LeaderfFunky', 'A super simple function navigator')
