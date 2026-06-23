-- CUSTOM MACROS --
-- Inspired by https://www.youtube.com/watch?v=Y3XWijJgdJs --

vim.fn.setreg("p", "gqap")
vim.fn.setreg("m", "V:s/, /,\\r/g\r")
