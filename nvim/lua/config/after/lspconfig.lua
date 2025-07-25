local lsp = require('lspconfig')
local lsp_completions = require('cmp_nvim_lsp')
local keymap = vim.keymap
local opts = { noremap = true, silent = true }
local on_attach = function(client, bufnr)
    opts.buffer = bufnr
    opts.desc = "Show LSP references"
    keymap.set("n", "gR", "<cmd>Telescope lsp_references<CR>", opts) -- show definition, references

    opts.desc = "Go to declaration"
    keymap.set("n", "gD", vim.lsp.buf.declaration, opts) -- go to declaration

    opts.desc = "Show LSP definitions"
    keymap.set("n", "gd", "<cmd>Telescope lsp_definitions<CR>", opts) -- show lsp definitions

    opts.desc = "Show LSP implementations"
    keymap.set("n", "gi", "<cmd>Telescope lsp_implementations<CR>", opts) -- show lsp implementations

    opts.desc = "Show LSP type definitions"
    keymap.set("n", "gt", "<cmd>Telescope lsp_type_definitions<CR>", opts) -- show lsp type definitions

    opts.desc = "See available code actions"
    keymap.set({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, opts) -- see available code actions, in visual mode will apply to selection

    opts.desc = "Smart rename"
    keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts) -- smart rename

    opts.desc = "Show buffer diagnostics"
    keymap.set("n", "<leader>D", "<cmd>Telescope diagnostics bufnr=0<CR>", opts) -- show  diagnostics for file

    opts.desc = "Show line diagnostics"
    keymap.set("n", "<leader>d", vim.diagnostic.open_float, opts) -- show diagnostics for line

    opts.desc = "Go to previous diagnostic"
    keymap.set("n", "[d", vim.diagnostic.goto_prev, opts) -- jump to previous diagnostic in buffer

    opts.desc = "Go to next diagnostic"
    keymap.set("n", "]d", vim.diagnostic.goto_next, opts) -- jump to next diagnostic in buffer

    opts.desc = "Show documentation for what is under cursor"
    keymap.set("n", "K", vim.lsp.buf.hover, opts) -- show documentation for what is under cursor

    opts.desc = "Restart LSP"
    keymap.set("n", "<leader>rs", ":LspRestart<CR>", opts) -- mapping to restart lsp if necessary
end


-- used to enable autocompletion (assign to every lsp server config)
local capabilities = lsp_completions.default_capabilities()



-- configure lua server (with special settings)
lsp["lua_ls"].setup({
    capabilities = capabilities,
    on_attach = on_attach,
    settings = { -- custom settings for lua
    Lua = {
        -- make the language server recognize "vim" global
        diagnostics = {
            globals = { "vim" },
        },
        workspace = {
            -- make language server aware of runtime files
            library = {
                [vim.fn.expand("$VIMRUNTIME/lua")] = true,
                [vim.fn.stdpath("config") .. "/lua"] = true,
            },
        },
    },
}
})

-- lsp['hls'].setup{
--     capabilities = capabilities,
--     on_attach = on_attach,
--     filetypes = { 'haskell', 'lhaskell', 'cabal' },
-- }

lsp['clangd'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['ts_ls'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['pylsp'].setup{
    capabilities = capabilities,
    on_attach = on_attach,
    settings = {
      pylsp = {
        plugins = {
          pycodestyle = {
            -- Ignore line too long (E501)
            -- Ignore line break before binary operator (W503)
            -- Ignore line break after binary operator (W504)
            ignore = {'E501', 'W503', 'W504'},
            maxLineLength = 100
          }
        }
      }
    }
}


lsp['ltex'].setup{
    capabilities = capabilities,
    on_attach = on_attach,
    settings = {
      ltex = {
        language = "en-CA",
        dictionary = {
          ["en-CA"] = {
            "Neovim",
            "devops",
            "CommonJS",
            "bork",
            "borked",
            "borking",
            "borks",
            "VSCode",
            "cli",
            "SMConverter",
            "tximport",
            "dependabot",
            "fastp",
            "MLFunction",
            "Oncohelix",
            "repos",
            "PII",
            "QMD",
            "venv",
            "gitignore",
            "django",
            "npm",
            "QUALISURE",
            "Qualisure",
            "PascalCase",
            "camelCase",
            "snake_case",
            "ui",
            "UI",
            "ux",
            "UX",
            "vite",
            "Vite",
            "WebUI",
            "webUI",
            "webui",
            "kubernetes",
            "configmap",
            "vue",
            "pvc",
            "tf",
            "api",
            "websocket",
            "kubectl",
            "Rspec",
            "postgres",
            "js",
            "ts",
            "tsx",
            "jsx",
            "yaml",
            "yml",
            "json",
            "html",
            "kube",
            "ini-files",
            "ini-file",
            "ini",
            "VueJS",
            "llm",
            "LLM",
            "reauth",
            "reauthed",
            "Runpod",
            "NextUI",
            "HeroUI",
            "csv",
            "CSV",
            "powershell",
            "Powershell",
            "mysql",
            "linux",
            "prisma",
            "Prisma",
            "justfile",
            "ARGS",
            "args",
            "async",
            "Async",
            "NextJS",
            "Preact",
            "Vercel",
            "Actix",
            "Yesod",
            "AlpineJS",
            "TailWindCSS",
            "SvelteKit",
            "Nuxt",
            "dockerfile",
            "debian",
            "cd",
            "zig",
            "Zig",
            "enum",
            "enums",
          },
        },
        disabledRules = {
          ["en-CA"] = { 'ENGLISH_WORD_REPEAT_BEGINNING_RULE' },
        },
      }
    }
}

lsp['rust_analyzer'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['volar'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['ruby_lsp'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['gopls'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

lsp['zls'].setup{
    capabilities = capabilities,
    on_attach = on_attach
}

