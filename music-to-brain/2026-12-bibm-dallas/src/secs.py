import re,sys
def top_sections(s):
    i=s.find('<div class="slides">')+len('<div class="slides">')
    out=[];depth=0;start=None
    for m in re.finditer(r'<section\b|</section>',s[i:]):
        p=i+m.start()
        if m.group(0)=='<section':
            if depth==0: start=p
            depth+=1
        else:
            depth-=1
            if depth==0: out.append(s[start:p+10])
    return out
def title(sec):
    h=re.search(r'<h2[^>]*>(.*?)</h2>',sec,re.S)
    return re.sub('<[^>]+>','',h.group(1)).strip() if h else '(none) '+re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',sec))[:70]
if __name__=='__main__':
    s=open(sys.argv[1]).read()
    for k,t in enumerate(top_sections(s)):
        inner=t.count('<section')
        print(k,inner,title(t)[:90])
