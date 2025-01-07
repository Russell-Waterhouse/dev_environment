require'nvim-treesitter.configs'.setup {
  highlight = {
    enable = true,
    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false,
  },
}

-- Add custom filetype association for .JSON
-- so that I get syntax highlighting for .JSON files
vim.filetype.add({
  extension = {
    JSON = "json", -- Map .JSON to the json filetype
  },
})
