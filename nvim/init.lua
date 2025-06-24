require("config.lazy")
require('config.core.options')
require('config.core.remap')


require('config.after.config')
require('config.after.telescope')
require('config.after.treesitter')
require('config.after.theme')
require('config.after.comment')
require('config.after.gitsigns')
require('config.after.gitblame')
require('config.after.nvim_cmp')
require('config.after.mason')
require('config.after.lspconfig')
require('config.after.oil')
require('config.after.indent-blankline')
-- Lualine has to be last or else colours don't appear for some reason
require('config.after.lualine')

