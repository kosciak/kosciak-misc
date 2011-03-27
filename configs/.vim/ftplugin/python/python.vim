set tabstop=8
set softtabstop=4
set shiftwidth=4
set noshiftround
set expandtab
set smarttab

set autoindent
set nosmartindent

set omnifunc=pythoncomplete#Complete

" Open all folds on start
autocmd Syntax python normal zR

highlight OverLength ctermbg=darkred ctermfg=white guibg=#592929
match OverLength /\%81v.\+/
