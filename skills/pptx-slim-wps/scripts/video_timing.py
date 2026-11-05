"""WPS-compatible video timing templates (proven click-play; autoplay variants all dead).

Inject into slide XML by replacing <p:timing>...</p:timing>:
  xml = re.sub(r'<p:timing>.*</p:timing>', timing_click_only(spid),
               xml, flags=re.S)
Find the video shape's spid first: grep the slide xml for <p:video>/<a:videoFile> rId,
then match rId -> media target in slideN.xml.rels, then the <p:sp> whose blipFill refs it.
WPS re-save reshuffles spids — always re-derive per deck.
"""
import re

def video_node(cid, spid):
    return (f'<p:video><p:cMediaNode><p:cTn id="{cid}" fill="hold" display="1">'
            f'<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>')

def interactive_seq(ids, spid):
    a, b, c, d, e_, f_ = ids
    return (f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="{a}" restart="whenNotActive" fill="hold" evtFilter="cancelBubble" nodeType="interactiveSeq">'
            f'<p:stCondLst><p:cond evt="onClick" delay="0"><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cond></p:stCondLst>'
            f'<p:endSync evt="end" delay="0"><p:rtn val="all"/></p:endSync>'
            f'<p:childTnLst><p:par><p:cTn id="{b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{c}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{d}" presetID="2" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:cmd type="call" cmd="togglePause"><p:cBhvr additive="base"><p:cTn id="{e_}" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
            f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            f'<p:nextCondLst><p:cond evt="onClick" delay="0"><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cond></p:nextCondLst></p:seq>')

def timing_click_only(spid):
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            + video_node(2, spid) + interactive_seq((3, 4, 5, 6, 7, 8), spid)
            + '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')

def inject(path, slide_no, spid):
    """Rewrite pptx with click-play timing on given slide."""
    import zipfile
    z = zipfile.ZipFile(path)
    e = {i.filename: z.read(i.filename) for i in z.infolist()}
    z.close()
    key = f'ppt/slides/slide{slide_no}.xml'
    e[key] = re.sub(r'<p:timing>.*</p:timing>', timing_click_only(spid),
                    e[key].decode('utf-8'), flags=re.S).encode('utf-8')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for k in ['[Content_Types].xml'] + [x for x in e if x != '[Content_Types].xml']:
            zout.writestr(k, e[k])
    print(f'{path} slide{slide_no} spid{spid}: click-play timing injected')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('usage: python video_timing.py deck.pptx slideNo spid')
    else:
        inject(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
