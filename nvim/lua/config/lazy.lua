local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    -- bootstrap lazy.nvim
    -- stylua: ignore
    vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable", lazypath })
end
vim.opt.rtp:prepend(vim.env.LAZY or lazypath)


require("lazy").setup({
    {
        -- Treesitter: Better highlighting
        { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },

        -- Monokai theme
        { "tanvirtin/monokai.nvim" },

        -- Bottom status bar
        { 'nvim-lualine/lualine.nvim', dependencies = { 'nvim-tree/nvim-web-devicons' } },

        -- Telescope: fuzzy finder
        {
            'nvim-telescope/telescope.nvim', tag = '0.1.5',
            dependencies = { 'nvim-lua/plenary.nvim' }
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
            -- TODO: Make this actually work in haskell or find a better plugin
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

    },
})

