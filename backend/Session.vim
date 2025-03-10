let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Desktop/tuda-desktop/backend
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +214 term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe
badd +87 ~/Desktop/tuda-desktop/backend/api/projects_general.py
badd +11 ~/Desktop/tuda-desktop/backend/main.py
argglobal
%argdel
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit ~/Desktop/tuda-desktop/backend/api/projects_general.py
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal nofen
silent! normal! zE
let &fdl = &fdl
let s:l = 87 - ((45 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 87
normal! 082|
tabnext
argglobal
if bufexists(fnamemodify("term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe", ":p")) | buffer term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe | else | edit term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe | endif
if &buftype ==# 'terminal'
  silent file term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe
endif
balt term://~/Desktop/tuda-desktop/backend//8432:C:/WINDOWS/system32/cmd.exe
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1967 - ((54 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1967
normal! 0
tabnext 2
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
