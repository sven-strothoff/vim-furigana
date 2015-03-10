# vim-furigana

Add furigana to your Japanese texts.

This plugin can be used to add furigana to Japanese texts for document formats
that support [ruby text](https://en.wikipedia.org/wiki/Ruby_character).  This
includes some flavours of LaTeX (XeLaTeX for instance) and HTML.

While this plugin could be used for all languages that use Chinese characters
(Chinese, Japanese, Korean) only Japanese is supported out of the box right now.

This is an early development version, that I created mainly for myself. The
current version should be working quite well, if you find any bugs, please open
an issue for them. If you have any ideas or suggestions feel free to share them
with me and I _might_ include them.

## Requirements

You need to have mecab and kakasi installed on your system for this plugin to
work.

This plugin uses Python, so make sure that your Vim version was compiled with
Python support. If `:version` includes `+python` you are good to go.

## Installation

Install to your `~/.vim` (`~\vimfiles` on Windows) folder or better use a
plugin manager like [vundle.vim](https://github.com/gmarik/vundle) or
[pathogen.vim](https://github.com/tpope/vim-pathogen).

## Usage

The plugins defines the `gr` map (mnemonic: generate ruby).  Either follow it by
a motion (for instance, `graw` to add furigana to a word) or use `grr` to add
furigana to the current line.  You can also use `gr` in visual mode to add
furigana to the selected text.

For more information see `:help furigana`.

## License

Copyright (c) 2015, Sven Strothoff
All rights reserved.

For full license see `:help furigana-license`.
