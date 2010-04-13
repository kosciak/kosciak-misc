" An example for a vimrc file.
"
" Maintainer:	Bram Moolenaar <Bram@vim.org>
" Last change:	2006 Nov 16
"
" To use it, copy it to
"     for Unix and OS/2:  ~/.vimrc
"	      for Amiga:  s:.vimrc
"  for MS-DOS and Win32:  $VIM\_vimrc
"	    for OpenVMS:  sys$login:.vimrc

" ----------------------------------------------------------------------
"  General settings
" ----------------------------------------------------------------------

if v:progname =~? "evim"
  finish
endif

set nocompatible	" Vim setings

set history=50		" keep 50 lines of command line history

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
else
  set backup		" keep a backup file
endif


" ----------------------------------------------------------------------
"  VIM interface
" ----------------------------------------------------------------------

set backspace=indent,eol,start

set laststatus=2	" always show status line
set ruler			" show the cursor position all the time
set showcmd			" display incomplete commands
set wildmenu		" wildmenu for comands completion

set magic			" magic on for regular expressions

set incsearch		" do incremental searching
if &t_Co > 2 || has("gui_running")
  syntax on			" syntax highliting
  set hlsearch		" highlight the last used search pattern.
endif

set ignorecase		" ignore case when searching
set smartcase		" override ignorecase when Uppercase in search pattern

set mouse=a			" turn mouse on

set number			" line numbers
set showmatch		" show matching brackets

set wrap
set linebreak
set display+=lastline	" display as much of the last line as possible

" Spellchecking: English and Polish, show 10 best suggestions
set spelllang=en,pl
set spellsuggest=best,10


" ----------------------------------------------------------------------
"  GUI options
" ----------------------------------------------------------------------

set guifont=Monospace\ 9


" ----------------------------------------------------------------------
"  Text, tab, indentation
" ----------------------------------------------------------------------

set tabstop=4
set shiftwidth=4
set expandtab
set smarttab

set listchars=tab:→\ ,eol:¶,extends:>,precedes:<,trail:·,nbsp:°
"set list

set autoindent
set smartindent

" ----------------------------------------------------------------------
"  Windows, tabs, buffers
" ----------------------------------------------------------------------



" ----------------------------------------------------------------------
"  Autocommands
" ----------------------------------------------------------------------

if has("autocmd")

  filetype plugin on	" enable file type detection
  filetype indent on	" load indent files

  " separate autocmd group
  augroup vimrcEx
  " delete previous settings for this group
  au!			

  autocmd BufRead *.txt setfiletype text

  autocmd FileType text setlocal nonumber noexpandtab
  autocmd FileType vim setlocal noexpandtab
  autocmd FileType svn setlocal nonumber

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal! g`\"" |
    \ endif

  augroup END

else

  set autoindent		" always set autoindenting on

endif " has("autocmd")


" ----------------------------------------------------------------------
"  Mappings
" ----------------------------------------------------------------------

" Don't use Ex mode, use Q for formatting
map Q gq

" More logical yanking (like D, C)
map Y y$


" ----------------------------------------------------------------------
"  Commands
" ----------------------------------------------------------------------

" Convenient command to see the difference between the current buffer and the file it was loaded from, thus the changes you made.
command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis
	 	\ | wincmd p | diffthis



" ----------------------------------------------------------------------
"  
" ----------------------------------------------------------------------




