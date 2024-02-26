#!/usr/bin/env python
from sys import argv
import fontforge as ff
from collections import deque
import unicodedata

fontface=argv[1]

mainfont=ff.open(f'newtxtt-{fontface}-main.otf')
scfont=ff.open(f'newtxtt-{fontface}-sc.otf')

mainfont.addLookup('smcp','gsub_single',None,(('smcp',(('latn',('dflt')),)),))
mainfont.addLookupSubtable('smcp','smcp_')
for lut in ['onum','ss01','ss02','ss03','ss04']:
    mainfont.addLookup(lut,'gsub_single',None,((lut,(('dflt',('dflt')),)),))
    mainfont.addLookupSubtable(lut,lut+'_')

style_set_names = (
    ('English (US)', 'ss01', 'form a, narrower than capital O'),
    ('English (US)', 'ss02', 'form c, slashed, narrower than capital O'),
    ('English (US)', 'ss03', 'form d, dotted, narrower than capital O'),
    ('English (US)', 'ss04', 'form e, narrower than capital O, more oblong'),
    )

for g in mainfont.glyphs():
    print(f'[{hex(g.unicode)}]', end='')
    if g.unicode>=0:
        if unicodedata.category(chr(g.unicode))=="Ll": # Letter, Lowercase
            print(f'\nGot lowercase letter \033[1m\033[92m{g.glyphname}\033[0m at \033[96m{hex(g.unicode)}\033[0m', end='')
            mainfont.selection.select(g.unicode)
            #mainfont.addSmallCaps()
            g.addPosSub('smcp_',f'{g.glyphname}.sc')
            scg=mainfont.createChar(-1,f'{g.glyphname}.sc')
            print(f'\nCreated \033[1m\033[92m{g.glyphname}.sc\033[0m at \033[96m{hex(scg.unicode)}\033[0m\n', end='')
            scfont.selection.select(g.unicode)
            scfont.copy()
            mainfont.selection.select(f'{scg.glyphname}')
            mainfont.paste()
        elif unicodedata.category(chr(g.unicode))=="Nd": # Number, Decimal Digit
            print(f'\nGot digit \033[1m\033[92m{g.glyphname}\033[0m at \033[96m{hex(g.unicode)}\033[0m', end='')
            mainfont.selection.select(g.unicode)
            #mainfont.addSmallCaps(symbols=True)
            g.addPosSub('onum_',f'{g.glyphname}.oldstyle')
            osg=mainfont.createChar(-1,f'{g.glyphname}.oldstyle')
            print(f'\nCreated \033[1m\033[92m{g.glyphname}.sc\033[0m at \033[96m{hex(osg.unicode)}\033[0m\n', end='')
            scfont.selection.select(g.unicode)
            scfont.copy()
            mainfont.selection.select(f'{osg.glyphname}')
            mainfont.paste()
            if g.glyphname=='zero':
                deque(map(lambda x:g.addPosSub('ss0'+str(x)+'_','zero.alt'+str(x)),range(1,5)))
print('')
scfont.close()

#mainfont.style_set_names = style_set_names # requires the most recent version of fontforge

mainfont.generate(f'newtxtt-{fontface}.otf')
mainfont.generate(f'newtxtt-{fontface}.woff2')
mainfont.generate(f'newtxtt-{fontface}.eot')
mainfont.generate(f'newtxtt-{fontface}.svg')
mainfont.close()
