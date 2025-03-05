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
badd +1 ~/Desktop/tuda-desktop/backend/main.py
badd +900 term://~/Desktop/tuda-desktop/backend//26812:C:/windows/system32/cmd.exe
badd +44 ~/Desktop/tuda-desktop/backend/api/projects/general.py
badd +13 ~/Desktop/tuda-desktop/backend/shared.py
badd +694 term://~/Desktop/tuda-desktop/backend//20020:C:/windows/system32/cmd.exe
argglobal
%argdel
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabrewind
argglobal
if bufexists(fnamemodify("term://~/Desktop/tuda-desktop/backend//26812:C:/windows/system32/cmd.exe", ":p")) | buffer term://~/Desktop/tuda-desktop/backend//26812:C:/windows/system32/cmd.exe | else | edit term://~/Desktop/tuda-desktop/backend//26812:C:/windows/system32/cmd.exe | endif
if &buftype ==# 'terminal'
  silent file term://~/Desktop/tuda-desktop/backend//26812:C:/windows/system32/cmd.exe
endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 900 - ((46 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 900
normal! 0
tabnext
edit ~/Desktop/tuda-desktop/backend/main.py
argglobal
balt ~/Desktop/tuda-desktop/backend/api/projects/general.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 1 - ((0 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 014|
tabnext
edit ~/Desktop/tuda-desktop/backend/api/projects/general.py
argglobal
balt ~/Desktop/tuda-desktop/backend/main.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 44 - ((43 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 44
normal! 016|
tabnext 1
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
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
