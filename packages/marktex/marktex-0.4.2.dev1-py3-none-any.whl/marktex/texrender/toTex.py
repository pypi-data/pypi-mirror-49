from marktex.markast.document import Document
from marktex.markast.environment import *
from marktex.markast.line import *
from marktex.markast.token import *
import config
from marktex.markast.parser import Scanner
from marktex.markast.utils import ImageTool,CleanTool
from marktex.texrender.texutils import *
from marktex.texrender import texparam

from pylatex.utils import bold,italic,escape_latex,dumps_list
from pylatex import NoEscape,NewLine as TNewLine,Center,Command
from pylatex import Document as TDoc,Section as TSection,Subsection,Subsubsection
from pylatex import Itemize as TItem,Enumerate as TEnum,Tabular,Math

# \usepackage[colorlinks=false,urlbordercolor=linkgray,pdfborderstyle={/S/U/W 1}]{hyperref}
class MarkTex(TDoc):


    def __init__(self,doc:Document,texconfig = None, default_filepath='default_filepath',image_dir = None):
        super().__init__(default_filepath, documentclass="ctexart", document_options="UTF8",
                         inputenc=None, fontenc=None, lmodern=False, textcomp=False)

        if texconfig is None:
            texconfig = config
        self.config = texconfig

        if image_dir is None:
            image_dir = "./"
        self.image_dir = image_dir
        self.doc = doc
        self.has_toc = False

        self.packages |= texparam.build_basic_package(self.config)
        self.preamble.extend(texparam.build_basic_preamble(self.config))



    @staticmethod
    def convert_from_file(fpath):
        with open(fpath,encoding="utf-8") as f:
            lines = f.readlines()
            lines = [i.strip() for i in lines]

        doc = Scanner().analyse(lines)
        mark = MarkTex(doc)
        mark.convert()
        return mark

    def convert(self):
        doc = self.doc
        if doc.has_toc:
            self.append(tablecontent())

        for envi in doc.content:
            if isinstance(envi,Quote):
                envi = self.fromQuote(envi)
            elif isinstance(envi,Paragraph):
                envi = self.fromParagraph(envi)
            elif isinstance(envi,Itemize):
                envi = self.fromItemize(envi)
            elif isinstance(envi,Enumerate):
                envi = self.fromEnumerate(envi)
            elif isinstance(envi,Formula):
                envi = self.fromFormula(envi)
            elif isinstance(envi,Code):
                envi = self.fromCode(envi)
            elif isinstance(envi,Table):
                envi = self.fromTable(envi)
            elif isinstance(envi,MultiBox):
                envi = self.fromMultiBox(envi)
            else:
                raise Exception(f"Doc error {envi},{envi.__class__.__name__}")
            self.append(envi)

    def fromToken(self,s:Token):
        s = escape_latex(s.string)
        return NoEscape(s)

    def fromBold(self,s:Bold):
        return bold(s.string)
    
    def fromItalic(self,s:Italic):
        return italic(s.string)

    def fromDeleteLine(self,s:DeleteLine):
        s = escape_latex(s.string)
        return NoEscape(rf"\sout{{{s}}}")

    def fromUnderLine(self,s:UnderLine):
        s = escape_latex(s.string)
        return NoEscape(rf"\underline{{{s}}}")

    def fromInCode(self,s:InCode):
        s = escape_latex(s.string)

        return NoEscape(rf"\adjustbox{{margin=1pt 1pt 1pt 2pt,bgcolor=aliceblue}}{{\small{{{s}}}}}")
    
    def fromInFormula(self,s:InFormula):
        return NoEscape(f"${s.string}$")
    
    def fromHyperlink(self,s:Hyperlink):
        desc,link = escape_latex(s.desc),s.link
        return NoEscape(rf"\href{{{link}}}{{{desc}}}")

    def fromFootnote(self,s:Footnote):
        s = f"[{s}]"
        s = escape_latex(s)
        return NoEscape(s)
    
    def fromInImage(self,s:InImage):
        s = f"[ImageError]"
        s = escape_latex(s)
        return NoEscape(s)

    def fromSection(self,s:Section):
        level,content = s.level,s.content
        if s.level == 1:
            return TSection(content,label=False)
        elif level == 2:
            return Subsection(content,label=False)
        elif level == 3:
            return Subsubsection(content,label=False)
        elif level == 4:
            return NoEscape(r"\\\noindent{{\large\textbf{{{}}}}}\\".format(content))
            # TODO 使用paragraph还需要一些其他的包括字体在内的设置
            # return NoEscape(rf"\paragraph{{\textbf{{{content}}}}}\\")
        elif level == 5:
            return NoEscape(r"\\\noindent{{\textbf{{{}}}}}\\".format(content))
    
    def fromImage(self,s:Image):

        link = s.link
        link = ImageTool.verify(link,self.image_dir)
        c = Center()
        t = Text()
        t.append(NoEscape(
            rf"\vspace{{\baselineskip}}"
            rf"\includegraphics[width=0.8\textwidth]{{{link}}}"
            rf"\vspace{{\baselineskip}}"))

        c.append(t)
        return c

    def fromTokenLine(self,s:TokenLine):
        tokens = s.tokens
        strs = []
        for token in tokens:
            if isinstance(token,Bold):
                token = self.fromBold(token)
            elif isinstance(token,Italic):
                token = self.fromItalic(token)
            elif isinstance(token,DeleteLine):
                token = self.fromDeleteLine(token)
            elif isinstance(token,Footnote):
                token = self.fromFootnote(token)
            elif isinstance(token,UnderLine):
                token = self.fromUnderLine(token)
            elif isinstance(token,InCode):
                token = self.fromInCode(token)
            elif isinstance(token,InFormula):
                token = self.fromInFormula(token)
            elif isinstance(token,Hyperlink):
                token = self.fromHyperlink(token)
            elif isinstance(token,InImage):
                token = self.fromInImage(token)
            elif isinstance(token,Token):
                token = self.fromToken(token)
            else:
                raise Exception(f"TokenLine error {token},{token.__class__.__name__}")

            strs.append(token)

        strs = NoEscape("".join(strs))
        return strs


    def fromRawLine(self,s:RawLine):
        return NoEscape(s.s)
    
    def fromNewLine(self,s:NewLine):
        return NoEscape("\n")

    def fromParagraph(self,s:Paragraph):
        t = Text()
        # Section / NewLine / TokenLine / Image
        for line in s.buffer:
            if isinstance(line,Section):
                line = self.fromSection(line)
            elif isinstance(line,NewLine):
                line = self.fromNewLine(line)
            elif isinstance(line,TokenLine):
                line = self.fromTokenLine(line)
            elif isinstance(line,Image):
                line = self.fromImage(line)
            else:
                raise Exception(f"Paragraph line error {line} is {line.__class__}")
            t.append(line)

        if t.empty:
            return NoEscape("\n")
        return t

    def fromQuote(self,s:Quote):
        content = s.doc.content
        q = QuoteEnvironment()
        for envi in content:
            if isinstance(envi,Paragraph):
                envi = self.fromParagraph(envi)
            elif isinstance(envi,Table):
                envi = self.fromTable(envi)
            elif isinstance(envi,Itemize):
                envi = self.fromItemize(envi)
            elif isinstance(envi,Enumerate):
                envi = self.fromEnumerate(envi)
            elif isinstance(envi,Formula):
                envi = self.fromFormula(envi)
            elif isinstance(envi,Code):
                envi = self.fromCode(envi)
            else:
                raise Exception(f"Quote doc error:{envi},{envi.__class__.__name__}")
            q.append(envi)
            q.append(NoEscape("\n"))

        return q

    def fromItemize(self,s:Itemize):
        tokens = [self.fromTokenLine(c) for c in s.buffer]
        ui = TItem()
        for line in tokens:
            ui.add_item(line)
        return ui
    
    def fromMultiBox(self,s:MultiBox):
        cl = CheckList()
        for [ct,s] in s.lines:
            cl.add_item(ct,s)
        return cl
    
    def fromEnumerate(self,s:Enumerate):
        tokens = [self.fromTokenLine(c) for c in s.buffer]
        ui = TEnum()
        for line in tokens:
            ui.add_item(line)
        return ui

    def fromFormula(self,s:Formula):
        code = [self.fromRawLine(c) for c in s.formula]

        data = []
        for line in code:
            data.append(NoEscape(f"{line}\\\\"))

        m = Math(data=data)
        # eq = Equation()
        # for line in code:
        #     eq.append(line)
        return m

    def fromCode(self,s:Code):
        code = [self.fromRawLine(c) for c in s.code]
        c = CodeEnvironment(self.config)
        for line in code:
            c.append(line)

        return c

    def fromTable(self,s:Table):
        c = Center()
        # c.append(NoEscape(r"\newlength\q"))
        c.append(
            NoEscape(
                rf"\setlength\tablewidth{{\dimexpr (\textwidth -{2*s.col_num}\tabcolsep)}}"))
        c.append(NoEscape(r"\arrayrulecolor{tablelinegray!75}"))
        c.append(NoEscape(r"\rowcolors{2}{tablerowgray}{white}"))


        ratios = s.cacu_col_ratio()
        # format = "|".join([rf"p{{{r}\textwidth}}<{{\centering}}" for r in ratios])
        format = "|".join([rf"p{{{r}\tablewidth}}<{{\centering}}" for r in ratios])
        format = f"|{format}|"

        t = Tabular(format)
        t.add_hline()
        for i,row in enumerate(s.tables):
            if i == 0:
                t.append(NoEscape(r"\rowcolor{tabletopgray}"))

            row = [self.fromTokenLine(c) for c in row]
            if i == 0:
                row = [bold(c) for c in row]

            t.add_row(row)
            t.add_hline()

        c.append(t)
        return c

    def dumps(self):
        string = super().dumps()
        string = CleanTool.clean_comment(string)
        return string



