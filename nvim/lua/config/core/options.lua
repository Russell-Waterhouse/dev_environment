local opt = vim.opt

-- line numbers
opt.relativenumber = true
opt.number = true

-- line wrap
opt.wrap = true

-- tabs and indentation
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.autoindent = true

-- line wrapping
opt.wrap = false

-- search settings
opt.ignorecase = true
opt.smartcase = true

-- cursorline
opt.cursorline = true

-- appearance
opt.cursorline = true
opt.background = "dark"
opt.signcolumn = "yes"

-- backspace works properly
opt.backspace = "indent,eol,start"

-- split windows
opt.splitright = true
opt.splitbelow = true

-- dash "-" is now a part of the word recognized by w key
opt.iskeyword:append("-")

-- see whitespace at the end of lines
opt.list = true

-- max scrolloff of 10 to keep my cursor more centered
opt.scrolloff = 10
opt.colorcolumn = "80"

