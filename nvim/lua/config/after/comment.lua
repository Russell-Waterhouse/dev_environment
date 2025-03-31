-- protected call to not call setup if we don't have comment plugin installed.
local setup, comment = pcall(require, "Comment")
if not setup then
    return
end
comment.setup()

