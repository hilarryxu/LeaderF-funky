if leaderf#versionCheck() == 0
  finish
endif

execute g:Lf_py 'import vim, sys, os.path'
execute g:Lf_py 'cwd = vim.eval("expand(\"<sfile>:p:h\")")'
execute g:Lf_py 'sys.path.insert(0, os.path.join(cwd, "pythonx"))'
execute g:Lf_py 'from leader_funky import leader_funky_man'

function! leaderf#funky#define_maps() abort
  nmapclear <buffer>
  nnoremap <buffer> <silent> <CR>          :execute g:Lf_py "leader_funky_man.accept()"<CR>
  nnoremap <buffer> <silent> o             :execute g:Lf_py "leader_funky_man.accept()"<CR>
  nnoremap <buffer> <silent> x             :execute g:Lf_py "leader_funky_man.accept('h')"<CR>
  nnoremap <buffer> <silent> v             :execute g:Lf_py "leader_funky_man.accept('v')"<CR>
  nnoremap <buffer> <silent> t             :execute g:Lf_py "leader_funky_man.accept('t')"<CR>
  nnoremap <buffer> <silent> q             :execute g:Lf_py "leader_funky_man.quit()"<CR>
  nnoremap <buffer> <silent> i             :execute g:Lf_py "leader_funky_man.input()"<CR>
  nnoremap <buffer> <silent> <F1>          :execute g:Lf_py "leader_funky_man.toggleHelp()"<CR>

  if has_key(g:Lf_NormalMap, 'Funky')
    for e in g:Lf_NormalMap['Funky']
      exec 'nnoremap <buffer> <silent> '. e[0] . ' ' . e[1]
    endfor
  endif
endfunction

function! leaderf#funky#start_explorer(win_pos, ...) abort
  call leaderf#LfPy('leader_funky_man.startExplorer("' . a:win_pos . '")')
endfunction
