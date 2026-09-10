tlmgr option repository https://mirror.ctan.org/systems/texlive/tlnet
tlmgr update --self
xargs tlmgr install < dependencies.txt
