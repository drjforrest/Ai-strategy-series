from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
B=Path(__file__).resolve().parent
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';WP='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';ns={'w':W,'wp':WP,'a':A};q=lambda x:'{'+W+'}'+x
captions=[
'Figure 1. Similarity to the seven DHC competency domains for four policy units and two programme groups. Programme values are group medians; policy values are scores for each analytic unit. The three EAG reports form one unit. AI4H contributes 10 passages. Values indicate textual similarity, not competence; document genre limits direct comparison.',
'Figure 2. Programme-level similarity to the seven DHC competency domains. Points represent the 30 named and 18 adjacent programmes in the primary analysis. Black bars indicate medians and interquartile ranges. Policy scores are shown as contextual comparators, with differences in document genre limiting direct comparison.',
'Figure S1. Programme-level similarity to the seven DHC competency domains in the primary analysis. Rows show named and adjacent programmes, with policy units above for context. Colour indicates textual similarity; scores do not measure delivered teaching or graduate competence.'
]
for f in B.glob('*v1.1*.docx'):
 with ZipFile(f) as z:parts={n:z.read(n) for n in z.namelist()}
 root=E.fromstring(parts['word/document.xml']);body=root.find('w:body',ns);pp=body.findall('w:p',ns)
 pictures={}
 for anc in root.findall('.//wp:anchor',ns):
  blip=anc.find('.//a:blip',ns)
  if blip is not None:pictures[blip.get('{'+R+'}embed')]=anc
 # Inline images replace floating pictures/text boxes. The original image bytes are unchanged.
 for idx,rid,cap in zip([130,131,133],['rId94','rId93','rId95'],captions):
  p=pp[idx]
  for c in list(p):p.remove(c)
  pr=E.SubElement(p,q('pPr'));E.SubElement(pr,q('keepNext'));E.SubElement(pr,q('jc'),{q('val'):'center'})
  if idx==131:E.SubElement(pr,q('pageBreakBefore'))
  E.SubElement(pr,q('spacing'),{q('after'):'120',q('line'):'240',q('lineRule'):'auto'})
  run=E.SubElement(p,q('r'));drawing=E.SubElement(run,q('drawing'));inline=E.SubElement(drawing,'{'+WP+'}inline',distT='0',distB='0',distL='0',distR='0')
  anc=pictures[rid];ext=anc.find('wp:extent',ns);ow,oh=int(ext.get('cx')),int(ext.get('cy'));width=5943600;height=round(width*oh/ow)
  if height>6300000:width=round(width*6300000/height);height=6300000
  E.SubElement(inline,'{'+WP+'}extent',cx=str(width),cy=str(height))
  for tag in ['docPr','cNvGraphicFramePr']:
   x=anc.find('wp:'+tag,ns)
   if x is not None:inline.append(deepcopy(x))
  graphic=deepcopy(anc.find('a:graphic',ns))
  for ext2 in graphic.findall('.//a:xfrm/a:ext',ns):ext2.set('cx',str(width));ext2.set('cy',str(height))
  inline.append(graphic)
  cp=E.Element(q('p'));pr=E.SubElement(cp,q('pPr'));E.SubElement(pr,q('spacing'),{q('after'):'160',q('line'):'240',q('lineRule'):'auto'});run=E.SubElement(cp,q('r'));rpr=E.SubElement(run,q('rPr'));E.SubElement(rpr,q('sz'),{q('val'):'20'});E.SubElement(run,q('t')).text=cap
  p.addnext(cp)
 # Keep table rows intact and repeat column headings on continuation pages.
 for tbl in body.findall('w:tbl',ns):
  for i,tr in enumerate(tbl.findall('w:tr',ns)):
   pr=tr.find('w:trPr',ns)
   if pr is None:pr=E.Element(q('trPr'));tr.insert(0,pr)
   if pr.find('w:cantSplit',ns) is None:E.SubElement(pr,q('cantSplit'))
   if i==0 and pr.find('w:tblHeader',ns) is None:E.SubElement(pr,q('tblHeader'))
 # Correct editorial queries after inspecting the drawing objects.
 if 'word/comments.xml' in parts:
  cr=E.fromstring(parts['word/comments.xml'])
  for c in cr:
   texts=c.findall('.//w:t',ns)
   t=''.join(x.text or '' for x in texts)
   if t.startswith('The source includes six embedded graphics'):
    texts[0].text='The three figure images were preserved byte-for-byte. Their floating captions overlapped the plots in the source; images are now inline with explanatory captions below. Figure layout and captions were regularised separately from the tracked body-text edits. Figure 1 shows four policy units and two programme groups, not six policy frameworks. Please approve the legends and final figure selection.'
   elif t.startswith('Please assemble the supplementary methods'):
    texts[0].text='Figure S1 is retained. Please add the supplementary methods, programme-flow and eligibility information, AI dictionary, complete domain/group statistics and sensitivity tables; these materials were not supplied in the manuscript.'
  parts['word/comments.xml']=E.tostring(cr,xml_declaration=True,encoding='UTF-8',standalone=True)
 parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 with ZipFile(f,'w',ZIP_DEFLATED) as z:
  for n,d in parts.items():z.writestr(n,d)
 print('Layout corrected',f.name)
