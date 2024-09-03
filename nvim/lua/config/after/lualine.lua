function MonokaiTheme()
    local colors = {
        white='#fcfcfa',
        black='#2d2a2e',
        gray='#727072',
        red='#ff6188',
        green='#a9dc76',
        yellow='#ffd866',
        cyan='#ab9df2',
        blue='#78dce8',
        magenta='#fc9867',
    }

    return {
        normal = {
            a = { fg = colors.black, bg = colors.cyan, gui = 'bold' },
            b = { fg = colors.black, bg = colors.magenta },
            c = { fg = colors.white, bg = colors.gray },
        },
        insert = { a = { fg = colors.black, bg = colors.green, gui = 'bold' } },
        visual = { a = { fg = colors.black, bg = colors.yellow, gui = 'bold' } },
        replace = { a = { fg = colors.black, bg = colors.red, gui = 'bold' } },
        inactive = {
            a = { fg = colors.blue, bg = colors.black, gui = 'bold' },
            b = { fg = colors.white, bg = colors.blue },
            c = { fg = colors.gray, bg = colors.white },
        },
    }

end


require('lualine').setup {
    options = {
        theme = MonokaiTheme(),
        icons_enabled = true,
        component_separators = { left = '', right = ''},
        section_separators = { left = '', right = ''},
        disabled_filetypes = {
            statusline = {},
            winbar = {},
        },
        ignore_focus = {},
        always_divide_middle = true,
        globalstatus = false,
        refresh = {
            statusline = 1000,
            tabline = 1000,
            winbar = 1000,
        }
    },
    sections = {
        lualine_a = {'mode'},
        lualine_b = {'branch', 'diff', 'diagnostics'},
        lualine_c = {
            {
                'filename',
                path = 1,
            }
        },
        lualine_x = {'encoding', 'fileformat', 'filetype'},
        lualine_y = {'progress'},
        lualine_z = {'location'}
    },
    inactive_sections = {
        lualine_a = {},
        lualine_b = {},
        lualine_c = {
            {
                'filename',
                path = 1
            },
        },
        lualine_x = {'location'},
        lualine_y = {},
        lualine_z = {}
    },
    tabline = {},
    winbar = {},
    inactive_winbar = {},
    extensions = {}
}

