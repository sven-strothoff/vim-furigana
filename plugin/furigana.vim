" Vim plugin for generating Doxygen comments
" Last Change:  2015 Mar 10
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (vim_furigana.txt)
" 
" Copyright (c) 2015, Sven Strothoff
" All rights reserved.

if exists("g:loaded_furigana")
  finish
endif
let g:loaded_furigana = 1

if !has('python')
  echo "Error: Requires vim compiled with +python"
  finish
endif

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

python import sys
python import vim
exe 'python sys.path = ["' . s:plugin_path . '"] + sys.path'
exe 'pyfile ' . s:plugin_path . '/furigana.py'

" Configuration
if !exists("g:furigana_format_string")
  let g:furigana_format_string = "\\ruby{%k}{%r}"
endif

function s:AddRuby(type, ...)
python << EOF
type = vim.eval('a:type')
format_str = vim.eval('g:furigana_format_string')

cb = vim.current.buffer

if type == 'range': # Used by command definition
  type = 'line'
  start = (int(vim.eval('a:1')), 0)
  end = (int(vim.eval('a:2')), 0)
elif vim.eval('a:0') == '1': # Invoked from Visual mode, use '< and '> marks
  start = cb.mark('<')
  end = cb.mark('>')
else: # line, block, char
  start = cb.mark('[')
  end = cb.mark(']')

start = (start[0] - 1, start[1])
end = (end[0] - 1, end[1])

if type == 'line' or type == 'V':
  for line in range(start[0], end[0] + 1):
    cb[line] = add_ruby(cb[line], format_str)
elif type == 'char' or type == 'v':
  if start[0] == end[0]: # same line
    cb[start[0]] = add_ruby_substring(cb[start[0]], start[1], end[1] + 1, format_str)
  else:
    cb[start[0]] = add_ruby_substring(cb[start[0]], start[1], sys.maxsize, format_str)
    for line in range(start[0] + 1, end[0]):
      cb[line] = add_ruby(cb[line], format_str)
    cb[end[0]] = add_ruby_substring(cb[end[0]], 0, end[1] + 1, format_str)
elif type == 'block' or type == '\x16': # <C-V>
  for line in range(start[0], end[0] + 1):
    cb[line] = add_ruby_substring(cb[line], start[1], end[1] + 1, format_str)
EOF
endfunction

command -range AddRuby call AddRuby('range', <line1>, <line2>)

nnoremap <silent> <Plug>AddRuby :<C-U>set opfunc=<SID>AddRuby<CR>g@
nnoremap <silent> <Plug>AddRubyLine :<C-U>set opfunc=<SID>AddRuby<Bar>exe 'norm! 'v:count1.'g@_'<CR>
vnoremap <silent> <Plug>AddRuby :<C-U>call <SID>AddRuby(visualmode(), 1)<CR>

nmap <silent> gr <Plug>AddRuby
nmap <silent> grr <Plug>AddRubyLine
vmap <silent> gr <Plug>AddRuby
