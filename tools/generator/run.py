import os, sys, build, industries
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'standalone')
for ind in industries.ALL:
    if len(sys.argv)>1 and ind['slug'] not in sys.argv[1:]: continue
    open(os.path.join(OUT, 'joulewise-%s.html' % ind['slug']), 'w').write(build.build(ind))
    print('ok',ind['slug'])
