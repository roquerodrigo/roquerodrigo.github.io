\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/07/10 Minimalist ATS-friendly resume]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[10pt,a4paper]{article}

\RequirePackage[left=1.6cm,right=1.6cm,top=1.3cm,bottom=1.3cm]{geometry}

\RequirePackage[sfdefault]{FiraSans}
\RequirePackage{FiraMono}
\RequirePackage{microtype}

\RequirePackage{xcolor}
\definecolor{accent}{HTML}{0F766E}
\definecolor{ink}{HTML}{1F2937}
\definecolor{muted}{HTML}{5B6472}
\definecolor{rulecol}{HTML}{D5DBE1}

\RequirePackage[hidelinks]{hyperref}
\hypersetup{
  colorlinks=true,
  urlcolor=accent,
  linkcolor=accent,
  pdfborder={0 0 0},
}

\RequirePackage{enumitem}
\newlist{cvitems}{itemize}{1}
\setlist[cvitems]{
  leftmargin=1.3em,
  itemsep=1.5pt,
  topsep=2.5pt,
  parsep=0pt,
  label={\textcolor{accent}{\footnotesize\textbullet}},
}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\linespread{1.3}
\pagestyle{empty}
\AtBeginDocument{\color{ink}}

\newcommand{\cvheader}[3]{
  {\fontsize{23}{26}\selectfont\bfseries\color{accent}#1\par}
  \vspace{2pt}
  {\fontsize{11.5}{14}\selectfont\color{muted}#2\par}
  \vspace{5pt}
  {\small\color{ink}#3\par}
  \vspace{4pt}
  {\color{rulecol}\hrule height 0.6pt}
  \vspace{7pt}
}

\newcommand{\cvsep}{\hspace{0.4em}\textcolor{rulecol}{\textbullet}\hspace{0.4em}}

\newcommand{\cvsection}[1]{
  \vspace{7pt}
  {\normalsize\bfseries\color{accent}\MakeUppercase{#1}\par}
  \vspace{1pt}
  {\color{rulecol}\hrule height 0.5pt}
  \vspace{5pt}
}

\newcommand{\cvevent}[4]{
  \vspace{5pt}
  \noindent{\bfseries\color{ink}#1}\hfill{\small\color{muted}#2}\par
  \vspace{1.5pt}
  \noindent{\small\color{muted}#3\ifx\relax#4\relax\else\cvsep#4\fi}\par
  \vspace{2.5pt}
}

\newcommand{\cvsummary}[1]{\noindent{\color{ink}#1}\par\vspace{1pt}}

\newcommand{\cvline}[2]{
  \vspace{2pt}
  \noindent{\bfseries\color{ink}#1}\hfill{\small\color{muted}#2}\par
}
