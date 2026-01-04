-- Add custom filetype association for .JSON
-- so that I get syntax highlighting for .JSON files
vim.filetype.add({
  extension = {
    JSON = "json", -- Map .JSON to the json filetype
  },
})
