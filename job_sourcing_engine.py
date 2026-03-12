#!/usr/bin/env python3
"""
Daily Job Sourcing & ClickUp Population Engine
Executive-level job search automation for Revenue Operations, GTM Systems, CRM Strategy roles
"""

import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

# Configuration
CLICKUP_API_TOKEN = "pk_162147868_O3XBRNT93T29NH7252EM687YRF79I0H8"
CLICKUP_LIST_ID = "901326308224"
CLICKUP_API_BASE = "https://api.clickup.com/api/v2"

# Resume variant keywords
REVENUE_OPS_KEYWORDS = [
      "revenue operations", "revops", "go-to-market", "gtm",
      "sales operations", "operations strategy", "funnel", "pipeline",
      "revenue intelligence", "analytics", "reporting", "dashboard"
]

CRM_MARKETING_KEYWORDS = [
      "crm", "marketing operations", "martech", "marketing technology", "customer data",
      "cdp", "campaign management", "marketing automation", "customer experience",
      "marketing systems", "marketing infrastructure"
]

REQUIRED_KEYWORDS = [
      "vp", "director", "head of", "revenue operations", "revops", "gtm", "crm", "systems"
]

def get_existing_jobs_from_clickup() -> Dict[str, set]:
      """Fetch existing jobs from ClickUp for duplicate detection (90-day window)"""
      try:
                headers = {"Authorization": f"Token {CLICKUP_API_TOKEN}"}
                url = f"{CLICKUP_API_BASE}/list/{CLICKUP_LIST_ID}/task"
                params = {"limit": 100}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        tasks = response.json().get("tasks", [])
        existing_jobs = set()
        ninety_days_ago = datetime.now() - timedelta(days=90)

        for task in tasks:
                      task_name = task.get("name", "")
                      if " – " in task_name:
                                        company = task_name.split(" – ")[0].strip()
                                        job_title = task_name.split(" – ")[1].strip()

                date_created = int(task.get("date_created", 0)) / 1000
                task_date = datetime.fromtimestamp(date_created)

                if task_date > ninety_days_ago:
                                      existing_jobs.add((company.lower(), job_title.lower()))

        return existing_jobs

except Exception as e:
        print(f"⚠ Error fetching existing jobs: {e}")
        return set()

def search_indeed_rss() -> List[Dict]:
      """Search Indeed using RSS feed with built-in XML parsing"""
    jobs = []
    try:
              search_terms = [
                            ("VP+Revenue+Operations", "Remote"),
                            ("Director+GTM+Systems", "Remote"),
                            ("VP+GTM+Operations", "Remote"),
              ]

        for term, location in search_terms:
                      try:
                                        rss_url = f"https://www.indeed.com/rss?q={term}&l={location}&sort=date"
                                        response = requests.get(rss_url, timeout=10)
                                        response.raise_for_status()

                # Parse XML
                          root = ET.fromstring(response.content)

                for item in root.findall(".//item")[:5]:
                                      title_elem = item.find("title")
                                      link_elem = item.find("link")
                                      desc_elem = item.find("description")

                    if title_elem is not None and link_elem is not None:
                                              title = title_elem.text or ""
                                              link = link_elem.text or ""
                                              description = desc_elem.text or "" if desc_elem is not None else ""

                        # Extract company from description (Indeed format)
                                              company_match = re.search(r"<b>([^<]+)</b>", description)
                                              company = company_match.group(1) if company_match else "Indeed Job"

                        job = {
                                                      "title": title,
                                                      "company": company,
                                                      "link": link,
                                                      "description": re.sub('<[^<]+?>', '', description),  # Strip HTML
                                                      "source": "Indeed",
                                                      "salary": extract_salary(description),
                                                      "location": location,
                                                      "date_found": datetime.now().isoformat(),
                        }

                        if is_relevant_job(job):
                                                      jobs.append(job)

except Exception as e:
                print(f"  ⚠ Error parsing Indeed feed: {e}")
                continue

        return jobs

except Exception as e:
        print(f"⚠ #E!r/ruosrr /sbeianr/cehnivn gp yItnhdoene3d
        :" "{"e
              }D"a)i
              l y   J o b   S oruertcuirnng  [&] 
              C
              ldiecfk Uepx tProapcutl_astailoanr yE(ntgeixnte:
               Esxterc)u t-i>v eO-plteivoenla lj[osbt rs]e:a
               r c h   a"u"t"oEmxattriaocnt  fsoarl aRreyv efnruoem  Ojpoebr adteisocnrsi,p tGiToMn "S"y"s
               t e m s ,i fC RnMo tS ttreaxtte:g
               y   r o l e s 
                "r"e"t
                u
                rinm pNoornte 
                r e q u essatlsa
                riym_ppoarttt ejrsno n=
                 irm'p\o$r[t\ dr,e]
                 +f(r?o:m\ sd*a-t\est*i\m$e[ \idm,p]o+r)t? (d?a:tKe)t?i'm
                 e ,   t immaetdcehletsa 
                 =f rroem. ftiynpdianlgl (ismaploarrty _Lpiasttt,e rDni,c tt,e xOtp)t
                 i o n a lr
                 eitmupronr tm axtmclh.eest[r0e]e .iEfl emmaetncthTerse ee lasse  ENTo
                 n
                 e#

                  Cdoenff iigsu_rraetlieovna
                  nCtL_IjCoKbU(Pj_oAbP:I _DTiOcKtE)N  -=>  "bpoko_l1:6
                  2 1 4 7 8"6"8"_COh3eXcBkR NiTf9 3jTo2b9 NmHa7t2c5h2eEsM 6t8a7rYgReFt7 9cIr0iHt8e"r
                  iCaL"I"C"K
                  U P _ L IcSoTm_bIiDn e=d  "=9 0f1"3{2j6o3b0.8g2e2t4("'
              tCiLtIlCeK'U,P _'A'P)I}_ B{AjSoEb .=g e"th(t'tdpess:c/r/iapptii.ocnl'i,c k'u'p).}c"o.ml/oawpeir/(v)2
              " 

                #  hRaess_urmeeq uviarreida n=t  akneyy(wkoerydwso
                rRdE ViEnN UcEo_mObPiSn_eKdE YfWoOrR DkSe y=w o[r
                d   i n  "RrEeQvUeInRuEeD _oKpEeYrWaOtRiDoSn)s
                " ,   " rreevjoepcst"i,o n"_gkoe-ytwoo-rmdasr k=e t["",e n"tgrtym"",, 
                " j u n i"osra"l,e s" ionpteerrant"i,o n"ss"u,p p"oorpte"r]a
                t i o n sh asst_rraetjeegcyt"i,o n" f=u nanneyl("k,e y"wpoirpde liinn ej"o,b
                . g e t ("'rteivtelneu'e,  i'n't)e.llloiwgeern(c)e "f,o r" akneaylwyotridc si"n,  r"erjeepcotritoinn_gk"e,y w"odradssh)b
                o a r d "r
                e]t
                u
                rCnR Mh_aMsA_RrKeEqTuIiNrGe_dK EaYnWdO RnDoSt  =h a[s
                _ r e j e"cctrimo"n,

                 "dmeafr ksectoirneg_ joopbe(rjaotbi:o nDsi"c,t )" m-a>r tiencth:"
                 ,   " m a"r"k"eStcionrge  tjeocbh noonl o2g5y-"p,o i"nctu sstcoamleer" "d"a
                 t a " , 
                 s c o r e" c=d p0"
                 ,   " c atmiptalieg_nl omwaenra g=e mjeonbt."g,e t"(m"atrikteltei"n,g  "a"u)t.olmoawteiro(n)"
                 ,   " c u
                 s t o m e#r  Seexnpieorriietnyc e("0,-
                 5 ) 
                     " m airfk eatniyn(gw  siyns tteimtsl"e,_ l"omwaerrk eftoirn gw  iinnf r[a"svtpr u"c,t u"rvei"c
                     e] 
                     p
                     rReEsQiUdIeRnEtD"_,K E"YhWeOaRdD So f=" ,[ 
                     " c h i e"fv"p]"),: 
                     " d i r e c t o rs"c,o r"eh e+a=d  5o
                     f " ,   "erleivfe n"udei roepcetroart"i oinns "t,i t"lree_vloopwse"r,: 
                     " g t m " ,   " csrcmo"r,e  "+s=y s4t
                     e m s " 
                     e]l
                     s
                     ed:e
                     f   g e t _ e x issctoirneg _+j=o b2s
                     _ f r o m
                     _ c l i c#k uCpo(m)p e-n>s aDtiicotn[ s(t0r-,5 )s
                     e t ] : 
                     s a l a r"y" "=F ejtocbh. geexti(s"tsianlga rjyo"b,s  "f"r)o
                     m   C l iicfk Uspa lfaorry :d
                     u p l i c a t e  tdreyt:e
                     c t i o n   ( 9 0 - d a yn uwmibnedrosw )=" "r"e
                     . f i n dtarlyl:(
                     r ' \ d + ' ,   shaelaadreyr.sr e=p l{a"cAeu(t"h,o"r,i z"a"t)i)o
                     n " :   f " T o k e n   {iCfL InCuKmUbPe_rAsP:I
                     _ T O K E N } " } 
                                   v aulr l=  =i nft"({nCuLmIbCeKrUsP[_0A]P)I
                                   _ B A S E } / l i s t / { C L I CsKcUoPr_eL I+S=T _5I Di}f/ tvaaslk ">
                                   =   2 5 0   e l spea r(a4m si f=  v{a"ll i>m=i t2"0:0  1e0l0s}e
                                     ( 3   i f   v a
                                     l   > =   1 5 0  reelsspeo n2s)e) 
                                     =   r e q u e s tesx.cgeeptt(:u
                                     r l ,   h e a d e r s = hsecaodreer s+,=  p2a
                                     r a m s =eplasrea:m
                                     s ,   t i m e o ustc=o1r0e) 
                                     + =   2 
                                             r
                                             e s p o n#s eS.krialilsse _(f0o-r5_)s
                                             t a t u sd(e)s
                                             c   =   f " { t i
                                             t l e _ l o w e rt}a s{kjso b=. greets(p'odnessec.rjispotni(o)n.'g,e t'('")t.alsokwse"r,( )[}]")

                                                     m a t c heexsi s=t isnugm_(j1o bfso r=  ss eitn( )[
                                                     " r e v e n u e "n,i n"eotpye_rdaatyiso_nasg"o,  =" gdtamt"e,t i"mcer.mn"o,w (")s y-s tteimmse"d]e litfa (sd aiyns =d9e0s)c
                                                     ) 
                                                              s c o
                                                              r e   + =   m i nf(o5r,  tmaastkc hiens  t+a s1k)s
                                                              : 

                                                                             #   C o mtpaasnky_ n(a0m-e5 )=
                                                                               t a s ks.cgoerte( "+n=a m4e "i,f  "j"o)b
                                                                               . g e t ( " s a l a r y "i)f  e"l s– e"  2i
                                                                               n   t a s
                                                                               k _ n a m#e :L
                                                                               e v e r a g e   ( 0 - 5 ) 
                                                                                     c ocmopmapnayn y=_ ltoawsekr_ n=a mjeo.bs.pgleitt((""c o–m p"a)n[y0"],. s"t"r)i.pl(o)w
                                                                                     e r ( ) 
                                                                                              k n o w n   =  j[o"bs_ttriitplee" ,=  "tfaisgkm_an"a,m e".nsoptliiotn("",  – ""d)a[t1a]d.osgt"r,i p"(a)n
                                                                                              t h r o p i c " ,   " c a l e n d
                                                                                              l y " ,   " k l a v i y o " ] 
                                                                                                d a t es_ccorreea t+e=d  5=  iifn ta(ntya(skk .igne tc(o"mdpaatney__clroewaetre df"o,r  0k) )i n/  k1n0o0w0n
                                                                                                )   e l s e   3 
                                                                                                         
                                                                                                               t arsekt_udrant em i=n (d2a5t,e tsicmoer.ef)r
                                                                                                               o
                                                                                                               mdteifm essetlaemcpt(_draetseu_mcer_evaatreida)n
                                                                                                               t ( j o b :   D i c t )   - >   s
                                                                                                               t r : 
                                                                                                                        " " " S e l e c ti fr etsausmke_ dvaatrei a>n tn ibnaesteyd_ doany sk_eaygwoo:r
                                                                                                                        d s " " " 
                                                                                                                                 d e s c   =   f " { jeoxbi.sgteitn(g'_tjiotblse.'a,d d'('()c}o m{pjaonby..gleotw(e'rd(e)s,c rjiopbt_itoint'l,e .'l'o)w}e"r.(l)o)w)e
                                                                                                                                 r ( ) 
                                                                                                                                          c
                                                                                                                                          r m _ m a t c h erse t=u rsnu me(x1i sftoirn gk_wj oibns 
                                                                                                                                          C R M _ M A R K E
                                                                                                                                          T I N G _eKxEcYeWpOtR DESx ciefp tkiwo ni na sd ees:c
                                                                                                                                          ) 
                                                                                                                                                   r e vporpisn_tm(aft"c⚠h eEsr r=o rs ufme(t1c hfionrg  kewx iisnt iRnEgV EjNoUbEs_:O P{Se_}K"E)Y
                                                                                                                                                   W O R D S   i f  rkewt uirnn  dseestc())
                                                                                                                                                   
                                                                                                                                                    
                                                                                                                                                     d e fr esteuarrnc h"_CiRnMd e&e dM_arrskse(t)i n-g>  TLeicshtn[oDliocgty]": 
                                                                                                                                                     i f   c r"m"_"mSaetacrhcehs  I>n dreeevdo puss_imnagt cRhSeSs  feelesde  w"iRtehv ebnuuiel tT-eicnh nXoMlLo gpya r&s iOnpge"r"a"t
                                                                                                                                                     i o n s "j
                                                                                                                                                     o
                                                                                                                                                     bdse f=  c[r]e
                                                                                                                                                     a t e _ ctlriyc:k
                                                                                                                                                     u p _ t a s k ( jsoeba:r cDhi_ctte,r mssc o=r e[:
                                                                                                                                                       i n t ,   r e s u m e _(v"aVrPi+aRnetv:e nsuter+)O p-e>r aOtpitoinosn"a,l ["sRterm]o:t
                                                                                                                                                       e " ) , 
                                                                                                                                                       " " " C r e a t e   C l i(c"kDUipr etcatsokr +fGoTrM +jSoybs"t"e"m
                                                                                                                                                       s " ,   "tRreym:o
                                                                                                                                                       t e " ) , 
                                                                                                                                                             h e a d e r s   =  ({"
                                                                                                                                                             V P + G T M + O p e r a t"iAountsh"o,r i"zRaetmiootne"":) ,f
                                                                                                                                                             " T o k e n   { C]L
                                                                                                                                                             I C K U P _ A P I
                                                                                                                                                             _ T O K E N } " ,f
                                                                                                                                                             o r   t e r m ,   l o c a"tCioonnt einnt -sTeyaprec"h:_ t"earpmpsl:i
                                                                                                                                                             c a t i o n / j s o n " 
                                                                                                                                                             t r y : 
                                                                                                                                                                     } 
                                                                                                                                                                                      
                                                                                                                                                                                          r s s _ u r lp a=y lfo"ahdt t=p s{:
                                                                                                                                                                                          / / w w w . i n d e e d ."cnoamm/er"s:s ?fq"={{jtoebr[m'}c&olm=p{alnoyc'a]t}i o–n }{&jsoobr[t'=tdiattlee"'
              ] } " , 
                                      r"edsepsocnrsiep t=i orne"q:u efs"tSso.ugrecte(:r s{sj_oubr[l',s otuirmceeo'u]t}=\1n0L)i
                                      n k :   { j o b [ ' l i n k ' ] }r\ensSpaolnasrey.:r a{ijsoeb_.fgoert_(s'tsaatluasr(y)'
              ,   ' N o t   l i s t e d ' ) } \
              n \ n { j o b [ ' d e s c r i p t#i oPna'r]s[e: 3X0M0L]
              } " , 
                                       "rporoito r=i tEyT".:f r2o misft rsicnogr(er e>s=p o2n2s ee.lcsoen t3e,n
                                       t ) 
                                                   } 


                                                                                    u r l   =   f " {fCoLrI CiKtUePm_ AiPnI _rBoAoStE.}f/ilnidsatl/l{(C"L.I/C/KiUtPe_mL"I)S[T:_5I]D:}
                                                                                    / t a s k " 
                                                                                                     r e s p o ntsiet l=e _reelqeume s=t si.tpeoms.tf(iunrdl(," thietaldee"r)s
                                                                                                     = h e a d e r s ,   j s o n = p a y l o aldi,n kt_iemleeomu t== 1i0t)e
                                                                                                     m . f i n d ( " lrienskp"o)n
                                                                                                     s e . r a i s e _ f o r _ s t a t u s ( )d
                                                                                                     e s c _ e l e m  
                                                                                                     =   i t e m . f irnedt(u"rdne srcersippotnisoen."j)s
                                                                                                     o n ( ) . g e t ( " i d " ) 
                                                                                                                 
                                                                                                                     
                                                                                                                              e x c e p t   E x c e p t iiofn  taist lee:_
                                                                                                                              e l e m   i s   nporti nNto(nfe" ⚠ aEnrdr olri nckr_eealteimn gi sC lnioctk UNpo ntea:s
                                                                                                                              k :   { e } " ) 
                                                                                                                                               r e t u r n   Ntointel
                                                                                                                                               e
                                                                                                                                                d=e ft iitsl_ed_ueplleimc.atteex(tj oobr:  "D"i
                                                                                                                                                c t ,   e x i s t i n g :   s e t )   - >   b o olli:n
                                                                                                                                                k   =   l"i"n"kC_heelcekm .ftoerx td uoprl i"c"a
                                                                                                                                                t e s " " " 
                                                                                                                                                         k e y   =   ( j o b . g e td(e"sccormippatniyo"n,  =" "d)e.slco_weelre(m).,t ejxotb .ogre t"("" tiift ldee"s,c _"e"l)e.ml oiwse rn(o)t) 
                                                                                                                                                         N o n e  reeltsuer n" "k
                                                                                                                                                         e y   i n   e x i s t i n g 
                                                                                                                                                          
                                                                                                                                                           d e f   r u n _ d
                                                                                                                                                           a i l y _ j o b _ s o u r c i n g ( )   - >   D i#c tE:x
                                                                                                                                                           t r a c t" "c"oMmapiann ye xfercoumt idoens"c"r"i
                                                                                                                                                           p t i o np r(iInntd(efe"d\ nf{o'r=m'a*t7)0
                                                                                                                                                           } " ) 
                                                                                                                                                                    p r i n t ( f " J O B   S O U R CcIoNmGp aEnNyG_ImNaEt c-h  {=d artee.tsiemaer.cnho(wr(")<.bs>t(r[f^t<i]m+e)(<'/%bY>-"%,m -d%eds c%rHi:p%tMi:o%nS) 
                                                                                                                                                                    M T ' ) } " ) 
                                                                                                                                                                             p r i n t ( f " { ' = ' *c7o0m}p\ann"y) 
                                                                                                                                                                             =   c o m
                                                                                                                                                                             p a n y _rmeastuclht.sg r=o u{p
                                                                                                                                                                             ( 1 )   i f   c o"mtpiamneys_tmaamtpc"h:  edlastee t"iImned.eneodw (J)o.bi"s
                                                                                                                                                                             o f o r m a t ( ) , 
                                                                                                                                                                                              " j o b s _
                                                                                                                                                                                              f o u n d " :   0 , 
                                                                                                                                                                                                               " j o b s _jporbo c=e s{s
                                                                                                                                                                                                               e d " :   0 , 
                                                                                                                                                                                                                                " j o b s _ c r e a t e d""t:i t0l,e
                                                                                                                                                                                                                                " :   t i t l e ,"
                                                                                                                                                                                                                                d u p l i c a t e s _ s k i p p e d " :   0 , 
                                                                                                                                                                                                                                          " c o m"phaingyh"_:s ccoormep_ajnoyb,s
                                                                                                                                                                                                                                          " :   [ ] , 
                                                                                                                                                                                                                                                           " e r r o r s " :   [ ] 
                                                                                                                                                                                                                                                             " l i n}k
                                                                                                                                                                                                                                                             " :   l i
                                                                                                                                                                                                                                                             n k , 
                                                                                                                                                                                                                                                               t r y : 
                                                                                                                                                                                                                                                                                p r i n t ( " [ 1 / 4 ]   C h"edceksicnrgi pftoiro ne"x:i srtei.nsgu bj(o'b<s[ ^i<n] +C?l>i'c,k U'p'.,. .d"e)s
                                                                                                                                                                                                                                                                                c r i p t i o n )e,x i s#t iSntgr_ijpo bHsT M=L 
                                                                                                                                                                                                                                                                                g e t _ e x i s t i n g _ j o b s _ f r o m _ c l i c k u"ps(o)u
                                                                                                                                                                                                                                                                                r c e " :   " I npdreiendt"(,f
                                                                                                                                                                                                                                                                                "             ✓   { l e n ( e x i s t i n g _ j o b s ) }" sjaolbasr yf"o:u nedx tirna c9t0_-sdaalya rwyi(nddeoswc\rni"p)t
                                                                                                                                                                                                                                                                                i o n ) , 
                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                       p r i n t ( " [ 2 / 4 ]   S e a r"clhoicnagt ijoonb" :b olaorcdast.i.o.n",)
                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                        a l l _ j o b s   =   s e a r c h _ i n"ddeaetde__rfsosu(n)d
                                                                                                                                                                                                                                                                                                                        " :   d a t e t ipmrei.nnto(wf(") . i s o f o✓ r{mlaetn(()a,l
                                                                                                                                                                                                                                                                                                                        l _ j o b s ) }   r e l e v a n t   j o b s   f o}u
                                                                                                                                                                                                                                                                                                                        n d \ n " ) 
                                                                                                                                                                                                                                                                                                                                         r e s u l t s [ " j
                                                                                                                                                                                                                                                                                                                                         o b s _ f o u n d " ]   =   l e n ( a l l _ j o bisf) 
                                                                                                                                                                                                                                                                                                                                         i s _ r e l e v a
                                                                                                                                                                                                                                                                                                                                         n t _ j o b ( j opbr)i:n
                                                                                                                                                                                                                                                                                                                                         t ( " [ 3 / 4 ]   P r o c e s s i n g   &   S c o r i n gj ojbosb.sa.p.p.e"n)d
                                                                                                                                                                                                                                                                                                                                         ( j o b ) 
                                                                                                                                                                                                                                                                                                                                               j o b s _ t o _ c r e a t e   =   [ ] 
                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                               f o r   j o b   i n  eaxlcle_pjto bEsx:c
                                                                                                                                                                                                                                                                                                                                                               e p t i o n   a s   e : 
                                                                                                                                                                                                                                                                                                                                                               s c o r e   =   s c o r e _ j o bp(rjionbt)(
                                                                                                                                                                                                                                                                                                                                                               f "     ⚠  E r r o r   p ajrosbi[n"gs cIonrdee"e]d  =f esecdo:r e{
                                                                                                                                                                                                                                                                                                                                                               e } " ) 
                                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                               c o n t iinfu ei
                                                                                                                                                                                                                                                                                                                                                                                               s _ d u p l i c a
                                                                                                                                                                                                                                                                                                                                                                                               t e ( j o b ,   erxeitsutrinn gj_ojbosb
                                                                                                                                                                                                                                                                                                                                                                                               s ) : 
                                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                  e x c e p t  rEexscuelpttsi[o"nd uapsl iec:a
                                                                                                                                                                                                                                                                                                                                                                                                                  t e s _ s k i p pperdi"n]t (+f=" ⚠1 
                                                                                                                                                                                                                                                                                                                                                                                                                  E r r o r   s e a r c h i n g   Ipnrdienetd(:f "{ e } " ) 
                                                                                                                                                                                                                                                                                                                                                                                                                    ⊘   D U P L I CrAeTtEu:r n{ j[o]b
                                                                                                                                                                                                                                                                                                                                                                                                                    [
                                                                                                                                                                                                                                                                                                                                                                                                                    'dceofm peaxntyr'a]c}t _-s a{ljaorby[('tteixttl:e 's]t}r")) 
                                                                                                                                                                                                                                                                                                                                                                                                                    - >   O p t i o n a l [ s t r ] :c
                                                                                                                                                                                                                                                                                                                                                                                                                    o n t i n"u"e"
                                                                                                                                                                                                                                                                                                                                                                                                                    E x t r a c t   s a l a r
                                                                                                                                                                                                                                                                                                                                                                                                                    y   f r o m   j o b   d ejsocbrsi_pttoi_ocnr"e"a"t
                                                                                                                                                                                                                                                                                                                                                                                                                    e . a p piefn dn(ojto bt)e
                                                                                                                                                                                                                                                                                                                                                                                                                    x t : 
                                                                                                                                                                                                                                                                                                                                                                                                                                     rsettautruns  N=o n"e★"
                                                                                                                                                                                                                                                                                                                                                                                                                                       i f   sscaolraer y>_=p a2t2t eerlns e=  "r○'"\
              $ [ \ d , ] + ( ? : \ s *p-r\isn*t\($f["\ d , ] + ) ?{(s?t:aKt)u?s'}
                [ { s cmoartec}h/e2s5 ]=  {rjeo.bf[i'ncdoamlpla(nsya'l]a}r y-_ p{ajtotbe[r'nt,i ttleex't])}
                " ) 
                    r e t u r n  
                    m a t c h e s [ 0r]e siufl tmsa[t"cjhoebss _eplrsoec eNsosneed
                    "
                    ]d e=f  liesn_(rjeolbesv_atnot__cjroeba(tjeo)b
                    :   D i c t )   -p>r ibnoto(lf:"
                    \ n [ 4 /"4"]" CChreecakt iinfg  j{olbe nm(ajtocbhse_st ot_acrrgeeatt ec)r}i tCelriicak"U"p" 
                    t a s k sc.o.m.b"i)n
                    e d   =   f " { j
                    o b . g e t ( ' tfiotrl ej'o,b  'i'n) }j o{bjso_bt.og_ectr(e'adtees:c
                    r i p t i o n ' ,   ' ' )v}a"r.ilaonwte r=( )s
                    e l e c th_arse_sruemqeu_ivraerdi a=n ta(njyo(bk)e
                    y w o r d   i n   c o m bjionbe[d" rfeosru mkee_yvwaorrida nitn" ]R E=Q UvIaRrEiDa_nKtE
                    Y W O R D S ) 
                             r
                             e j e c t i o n _ k e y wtoarsdks_ i=d  [=" ecnrterayt"e,_ c"ljiucnkiuopr_"t,a s"ki(njtoebr,n "j,o b"[s"uspcpoorret""]],
                               v a r ihaanst_)r
                               e j e c t i o n   =   a niyf( kteayswko_ridd :i
                               n   j o b . g e t ( ' t i t l e 'r,e s'u'l)t.sl[o"wjeorb(s)_ cfroera tkeedy"w]o r+d=  i1n
                                 r e j e c t i o n _ k e y w o rpdrsi)n
                                 t ( f "  r e t u r n✓  {hjaosb_[r'ecqoumipraendy 'a]n}d  (nSocto rhea:s _{rjeojbe[c'tsicoonr
                                 e
                                 'd]e}f/ 2s5c,o rIeD_:j o{bt(ajsokb_:i dD}i)c"t))
                                   - >   i n t : 
                                            " " " S
                                            c o r e   j o b   o n   2 5 - p oiifn tj osbc[a"lsec"o"r"e
                                            " ]   > =s c2o2r:e
                                              =   0 
                                                       t i t l e _ l o w e r  r=e sjuolbt.sg[e"th(i"gthi_tslceo"r,e _"j"o)b.sl"o]w.earp(p)e
                                                       n d ( j o
                                                       b ) 
                                                           #   S e n i o r i t ye l(s0e-:5
                                                           ) 
                                                                    i f   a n y ( w   i nr etsiutlltes_[l"oewrerro rfso"r] .wa pipne n[d"(vfp" F"a,i l"evdi:c e{ jporbe[s'icdoemnpta"n,y '"]h}e"a)d
                                                                      o f " ,   " c h
                                                                      i e f " ] ) : 
                                                                        p r i n t ( f "s\cno{r'e= '+*=7 05}
                                                                        " ) 
                                                                            e l i f   " dpirrienctt(ofr""R EiSnU LtTiSt lSeU_MlMoAwReYr::"
                                                                            ) 
                                                                                          s cporrien t+(=f "4 
                                                                                            •   J oeblss eF:o
                                                                                            u n d :          s c o r{er e+s=u l2t
                                                                                            s [ ' j o
                                                                                            b s _ f o#u nCdo'm]p}e"n)s
                                                                                            a t i o n   ( 0 -p5r)i
                                                                                            n t ( f "s a l• aUrnyi q=u ej oJbo.bgse:t ( " s a l a r{yr"e,s u"l"t)s
                                                                                            [ ' j o bisf_ psraolcaersys:e
                                                                                            d ' ] } " ) 
                                                                                                t r y : 
                                                                                                    p r i n t ( f "     •n uCmrbeeartse d=:  r e . f i n d a l l ({rr'e\sdu+l't,s [s'ajloabrsy_.crreepaltaecde'(]"},""),
                                                                                                      " " ) ) 
                                                                                                            p r i n t ( f "    i• fD unpulmibceartse:s
                                                                                                            :                 { r e s u l t sv[a'ld u=p liincta(tneusm_bsekrisp[p0e]d)'
              ] } " ) 
                               p r i nstc(ofr"e   +•=  H5i gihf  Pvrailo r>i=t y2 5(02 2e+l)s:e  {(l4e ni(fr evsaull t>s=[ '2h0i0g he_lssceo r(e3_ jiofb sv'a]l) }>"=) 
                               1 5 0   e l s e  i2f) )r
                               e s u l t s [ ' eerxrcoerpst':]
                               : 
                                                     s cporrien t+(=f "2 
                                                       •  E r reolrsse:: 
                                                                        s c o{rlee n+(=r e2s
                                                                        u l t s [
                                                                        ' e r r o#r sS'k]i)l}l"s) 
                                                                        ( 0 - 5 ) 
                                                                              p rdienstc( f=" {f'"={'t*i7t0l}e\_nl"o)w
                                                                              e r }   { j o b .
                                                                              g e t ( 'edxecsecprti pEtxicoenp't,i o'n' )a.sl oew:e
                                                                              r ( ) } " 
                                                                                    r emsautlcthse[s" e=r rsourms("1] .faoprp esn di(ns t[r"(ree)v)e
                                                                                    n u e " ,   " o pperriantti(ofn"s✗" ,C R"IgTtImC"A,L  "EcRrRmO"R,:  "{sey}s\tne"m)s
                                                                                    " ]   i f
                                                                                      s   i nr edteusrcn) 
                                                                                      r e s u lstcso
                                                                                      r
                                                                                      ei f+ =_ _mnianm(e5_,_  m=a=t c"h_e_sm a+i n1_)_
                                                                                      " : 

                                                                                              r e s#u lCtosm p=a nryu n(_0d-a5i)l
                                                                                              y _ j o bs_csooruer c+i=n g4( )i
                                                                                              f   j o b
                                                                                              . g e t (r"essaullatrsy_"f)i leel s=e  f2"
                                                                                              / s e s s
                                                                                              i o n s /#a dLoervienrga-geex c(i0t-i5n)g
                                                                                              - f r a nckolmipna/nmyn_tl/oowuetrp u=t sj/ojbo.bg_esto(u"rccoimnpga_nrye"s,u l"t"s)_.{ldoawteert(i)m
                                                                                              e . n o wk(n)o.wsnt r=f t[i"mset(r'i%pYe%"m,% d"_f%iHg%mMa'"),} ."jnsootni"o
                                                                                              n " ,   "wdiattha doopge"n,( r"easnutlhtrso_pfiicl"e,,  "'cwa'l)e nadsl yf":,
                                                                                                " k l a v i y oj"s]o
                                                                                                n . d u mspc(orrees u+l=t s5,  iff,  ainnyd(ekn ti=n2 ,c odmepfaanuyl_tl=oswterr) 
                                                                                                f o r   k
                                                                                                  i n   kpnroiwnnt)( fe"l✓ sRee s3u
                                                                                                  l t s   s
                                                                                                  a v e d :r e{truersnu lmtisn_(f2i5l,e }s"c)ore)

                                                                                                  def select_resume_variant(job: Dict) -> str:
                                                                                                      """Select resume variant based on keywords"""
                                                                                                          desc = f"{job.get('title', '')} {job.get('description', '')}".lower()
                                                                                                              crm_matches = sum(1 for kw in CRM_MARKETING_KEYWORDS if kw in desc)
                                                                                                                  revops_matches = sum(1 for kw in REVENUE_OPS_KEYWORDS if kw in desc)
                                                                                                                      return "CRM & Marketing Technology" if crm_matches > revops_matches else "Revenue Technology & Operations"
                                                                                                                      
                                                                                                                      def create_clickup_task(job: Dict, score: int, resume_variant: str) -> Optional[str]:
                                                                                                                          """Create ClickUp task for job"""
                                                                                                                              try:
                                                                                                                                      headers = {
                                                                                                                                                  "Authorization": f"Token {CLICKUP_API_TOKEN}",
                                                                                                                                                              "Content-Type": "application/json"
                                                                                                                                                                      }
                                                                                                                                                                              
                                                                                                                                                                                      payload = {
                                                                                                                                                                                                  "name": f"{job['company']} – {job['title']}",
                                                                                                                                                                                                              "description": f"Source: {job['source']}\nLink: {job['link']}\nSalary: {job.get('salary', 'Not listed')}\n\n{job['description'][:300]}",
                                                                                                                                                                                                                          "priority": 2 if score >= 22 else 3,
                                                                                                                                                                                                                                  }
                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                  url = f"{CLICKUP_API_BASE}/list/{CLICKUP_LIST_ID}/task"
                                                                                                                                                                                                                                                          response = requests.post(url, headers=headers, json=payload, timeout=10)
                                                                                                                                                                                                                                                                  response.raise_for_status()
                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                  return response.json().get("id")
                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                              except Exception as e:
                                                                                                                                                                                                                                                                                                      print(f"⚠ Error creating ClickUp task: {e}")
                                                                                                                                                                                                                                                                                                              return None
                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                              def is_duplicate(job: Dict, existing: set) -> bool:
                                                                                                                                                                                                                                                                                                                  """Check for duplicates"""
                                                                                                                                                                                                                                                                                                                      key = (job.get("company", "").lower(), job.get("title", "").lower())
                                                                                                                                                                                                                                                                                                                          return key in existing
                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                          def run_daily_job_sourcing() -> Dict:
                                                                                                                                                                                                                                                                                                                              """Main execution"""
                                                                                                                                                                                                                                                                                                                                  print(f"\n{'='*70}")
                                                                                                                                                                                                                                                                                                                                      print(f"JOB SOURCING ENGINE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S MT')}")
                                                                                                                                                                                                                                                                                                                                          print(f"{'='*70}\n")
                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                  results = {
                                                                                                                                                                                                                                                                                                                                                          "timestamp": datetime.now().isoformat(),
                                                                                                                                                                                                                                                                                                                                                                  "jobs_found": 0,
                                                                                                                                                                                                                                                                                                                                                                          "jobs_processed": 0,
                                                                                                                                                                                                                                                                                                                                                                                  "jobs_created": 0,
                                                                                                                                                                                                                                                                                                                                                                                          "duplicates_skipped": 0,
                                                                                                                                                                                                                                                                                                                                                                                                  "high_score_jobs": [],
                                                                                                                                                                                                                                                                                                                                                                                                          "errors": []
                                                                                                                                                                                                                                                                                                                                                                                                              }
                                                                                                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                                      try:
                                                                                                                                                                                                                                                                                                                                                                                                                              print("[1/4] Checking for existing jobs in ClickUp...")
                                                                                                                                                                                                                                                                                                                                                                                                                                      existing_jobs = get_existing_jobs_from_clickup()
                                                                                                                                                                                                                                                                                                                                                                                                                                              print(f"      ✓ {len(existing_jobs)} jobs found in 90-day window\n")
                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                                                                                                              print("[2/4] Searching job boards...")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                      all_jobs = search_indeed_rss()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                              print(f"      ✓ {len(all_jobs)} relevant jobs found\n")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      results["jobs_found"] = len(all_jobs)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      print("[3/4] Processing & Scoring jobs...")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              jobs_to_create = []
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      for job in all_jobs:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  score = score_job(job)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              job["score"] = score
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      if is_duplicate(job, existing_jobs):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      results["duplicates_skipped"] += 1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      print(f"      ⊘ DUPLICATE: {job['company']} - {job['title']}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      continue
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              jobs_to_create.append(job)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          status = "★" if score >= 22 else "○"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      print(f"      {status} [{score}/25] {job['company']} - {job['title']}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      results["jobs_processed"] = len(jobs_to_create)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              print(f"\n[4/4] Creating {len(jobs_to_create)} ClickUp tasks...")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
