local builtin = require('telescope.builtin')
-- show hidden files in find_files and live_grep
vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})

local telescope_setup, telescope = pcall(require, "telescope")
if not telescope_setup then
    return
end

local actions_setup, actions = pcall(require, "telescope.actions")
if not actions_setup then
    return
end

telescope.setup({
    defaults = {
        mappings = {
            i = {
                ["<C-k>"] = actions.move_selection_previous,
                ["<C-j>"] = actions.move_selection_next,
                ["<C-q>"] = actions.send_selected_to_qflist + actions.open_qflist,
            }
        },
        vimgrep_arguments = {
            'rg',
            '--with-filename',
            '--line-number',
            '--column',
            '--smart-case',
            '--hidden',
        }
    },
    pickers = {
        find_files = {
            hidden = true,
        },
        live_grep = {
            hidden = true,
        },
    },
    ignore_patterns = { ".git" }
})


-- basic telescope configuration
local conf = require("telescope.config").values
