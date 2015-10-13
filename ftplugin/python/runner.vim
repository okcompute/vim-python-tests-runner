" ftplugin/python/runner.vim
" Author: Pascal Lalancette (okcompute@icloud.com)

" Only do this when not done yet for this buffer
if exists("b:runner_ftplugin")
    finish
endif
let b:runner_ftplugin = 1

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

" Set compiler
compiler runner

