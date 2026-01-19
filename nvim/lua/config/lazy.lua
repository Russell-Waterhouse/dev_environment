local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  -- bootstrap lazy.nvim
  -- stylua: ignore
  vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable", lazypath })
end
vim.opt.rtp:prepend(vim.env.LAZY or lazypath)


require("lazy").setup({
  {
    {
      "m4xshen/hardtime.nvim",
      lazy = false,
      dependencies = { "MunifTanjim/nui.nvim" },
      opts = {},
    },

    -- Treesitter: Better highlighting
    { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },

    -- Monokai theme
    { "tanvirtin/monokai.nvim" },

    -- Bottom status bar
    { 'nvim-lualine/lualine.nvim', dependencies = { 'nvim-tree/nvim-web-devicons' } },

    -- Telescope: fuzzy finder
    {
      'nvim-telescope/telescope.nvim', tag = 'v0.2.1',
      dependencies = {
        'nvim-lua/plenary.nvim',
        -- optional but recommended
        { 'nvim-telescope/telescope-fzf-native.nvim', build = 'make' },
      }
    },

    -- nvim-surround: surround text with whatever characters you give it.
    {
      "kylechui/nvim-surround",
      version = "*", -- Use for stability; omit to use `main` branch for the latest features event = "VeryLazy",
      config = function()
        require("nvim-surround").setup({
          -- Configuration here, or leave empty to use defaults
          -- use ys{motion}{char} for surround {motion} with {character}
          -- use ds{char} for delete surrounding {char}
          -- use cs{target}{replacement} to replace {target} with {replacement}
        })
      end
    },

    -- can now use gc<motion> to toggle comments
    -- i.e. gcc to toggle line comments, or
    -- gcap to toggle comments around a paragraph
    { "numToStr/Comment.nvim" },

    -- Git integrations
    { "lewis6991/gitsigns.nvim" },
    { "f-person/git-blame.nvim" },
    { "sindrets/diffview.nvim" },

    {
      'stevearc/dressing.nvim',
      opts = {},
    },

    {
      'hrsh7th/nvim-cmp',
      dependencies = {
        'hrsh7th/cmp-buffer', -- use current buffer as completions source 
        'hrsh7th/cmp-path', -- use filesystem as completions source
        'L3MON4D3/LuaSnip', -- snippet engine
        'saadparwaiz1/cmp_luasnip', -- completion source for luasnip
        "rafamadriz/friendly-snippets" -- useful snippets
      }
    },

    {
      "williamboman/mason.nvim",
      dependencies = {
        "williamboman/mason-lspconfig.nvim",
      }
    },

    {
      "neovim/nvim-lspconfig",
      event = { "BufReadPre", "BufNewFile" },
      dependencies = {
        "hrsh7th/cmp-nvim-lsp",
      },
    },

    {
      'Wansmer/treesj',
      keys = { '<space>m', '<space>J', '<space>S' },
      dependencies = { 'nvim-treesitter/nvim-treesitter' },
      config = function()
        require('treesj').setup({
          max_join_length = 1200,
        })
      end,
    },

    {
      'stevearc/oil.nvim',
      opts = {},
      -- Optional dependencies
      dependencies = { "nvim-tree/nvim-web-devicons" },
    },

    { "lukas-reineke/indent-blankline.nvim", main = "ibl", opts = {} },

    -- { "github/copilot.vim" },

    {
      "iamcco/markdown-preview.nvim",
      cmd = { "MarkdownPreviewToggle", "MarkdownPreview", "MarkdownPreviewStop" },
      ft = { "markdown" },
      build = function() vim.fn["mkdp#util#install"]() end,
    },

    {
      "sphamba/smear-cursor.nvim",

      opts = {
        -- Smear cursor when switching buffers or windows.
        smear_between_buffers = true,

        -- Smear cursor when moving within line or to neighbor lines.
        -- Use `min_horizontal_distance_smear` and `min_vertical_distance_smear` for finer control
        smear_between_neighbor_lines = true,

        -- Draw the smear in buffer space instead of screen space when scrolling
        scroll_buffer_space = true,

        -- Set to `true` if your font supports legacy computing symbols (block unicode symbols).
        -- Smears and particles will look a lot less blocky.
        legacy_computing_symbols_support = false,

        -- Smear cursor in insert mode.
        -- See also `vertical_bar_cursor_insert_mode` and `distance_stop_animating_vertical_bar`.
        smear_insert_mode = true,
      },
    },
  },
})

