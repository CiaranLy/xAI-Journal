%% harvard-ul.bst
%% BibTeX style for the University of Limerick "Cite it Right" Harvard style
%% (Glucksman Library, https://libguides.ul.ie/citeitright).
%%
%% Use with natbib:
%%   \usepackage[round]{natbib}
%%   \setcitestyle{aysep={}}          % (Smith 2010) - no comma, as UL requires
%%   \bibliographystyle{harvard-ul}
%%
%% Reference list examples produced:
%%   Smith, J.A. (2019) \emph{Book title}, 2nd ed., Dublin: Example Press.
%%   Murphy, K. and Lee, T. (2018) `Article title', \emph{Journal}, 12(3), 45--60.
%%   Brown, C. (2010) `Chapter' in Green, D. ed., \emph{Book}, London: Pub, 139--162.
%%   Kingspan (2016) \emph{Page title}, available: URL [accessed 14 Jul 2016].
%%
%% Extra fields understood: doi, url, urldate (e.g. {2026-10-22} or {22 Oct 2026}),
%% venue (conference location), eventdate (conference dates / blog post date).
%% Extra entry types: @online / @webpage / @www / @electronic, @blog.
%%
%% In-text: 1 author (Smith 2010); 2 authors (Murphy and Lee 2018);
%% 3+ authors (Wallace et al. 2013). All authors are listed in the reference list.
%%
%% To show web addresses in angle brackets <...>, add to your preamble:
%%   \newcommand{\ulurl}[1]{\textless\url{#1}\textgreater}
%%
%% Free to use and modify.

ENTRY
  { address author booktitle chapter doi edition editor eventdate
    howpublished institution journal key medium month note number organization
    pages publisher school series title translator type url urldate venue volume year }
  {}
  { label extra.label short.label full.label }

INTEGERS { first.part nameptr namesleft numnames len use.ed }

STRINGS { out s t u v ftitle thtype }

%% ---------- logic helpers ----------

FUNCTION {not}
{   { #0 }
    { #1 }
  if$
}

FUNCTION {and}
{   'skip$
    { pop$ #0 }
  if$
}

FUNCTION {or}
{   { pop$ #1 }
    'skip$
  if$
}

FUNCTION {field.or.null}
{ duplicate$ empty$
    { pop$ "" }
    'skip$
  if$
}

FUNCTION {emphasize}
{ duplicate$ empty$
    { pop$ "" }
    { "\emph{" swap$ * "}" * }
  if$
}

FUNCTION {quote.title}
{ duplicate$ empty$
    { pop$ "" }
    { "`" swap$ * "'" * }
  if$
}

%% ---------- output assembly ----------
%% The first item after "Author (Year)" is joined with a space,
%% every later item with ", ".

FUNCTION {add.part}
{ duplicate$ empty$
    { pop$ }
    { first.part
        { out " " * swap$ * 'out :=
          #0 'first.part :=
        }
        { out ", " * swap$ * 'out := }
      if$
    }
  if$
}

FUNCTION {add.space}
{ duplicate$ empty$
    { pop$ }
    { out " " * swap$ * 'out :=
      #0 'first.part :=
    }
  if$
}

%% ---------- names ----------

%% remove ties/spaces so initials read "J.A." (keeps hyphens: "J.-J.")
FUNCTION {squeeze}
{ 'v :=
  ""
    { v empty$ not }
    { v #1 #1 substring$ duplicate$ "~" = swap$ " " = or
        'skip$
        { v #1 #1 substring$ * }
      if$
      v #2 global.max$ substring$ 'v :=
    }
  while$
}

FUNCTION {format.one.name}
{ s nameptr "{vv~}{ll}{, jj}" format.name$
  s nameptr "{f.}" format.name$ squeeze
  duplicate$ empty$
    { pop$ }
    { ", " swap$ * * }
  if$
}

FUNCTION {format.names}
{ 's :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
  "" 't :=
    { namesleft #0 > }
    { format.one.name 'u :=
      nameptr #1 >
        { namesleft #1 >
            { t ", " * u * 't := }
            { u "others" =
                { t " \emph{et~al.}" * 't := }
                { t " and " * u * 't := }
              if$
            }
          if$
        }
        { u 't := }
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
  t
}

FUNCTION {ed.suffix}
{ editor num.names$ #1 >
    { "eds." }
    { "ed." }
  if$
}

%% ---------- years ----------

FUNCTION {year.text}
{ year empty$
    { "n.d." }
    { year }
  if$
}

FUNCTION {year.label}
{ year.text extra.label * }

%% ---------- "Author (Year)" head ----------

FUNCTION {make.head}
{ medium empty$
    'skip$
    { ftitle " [" * medium * "]" * 'ftitle := }
  if$
  author empty$ not
    { author format.names }
    { editor empty$ not use.ed and
        { editor format.names " " * ed.suffix * }
        { organization empty$ not
            { organization }
            { ftitle "" 'ftitle := }
          if$
        }
      if$
    }
  if$
  " (" * year.label * ")" * 'out :=
  #1 'first.part :=
}

%% ---------- misc formatting ----------

FUNCTION {n.dashify}
{ 't :=
  ""
    { t empty$ not }
    { t #1 #1 substring$ "-" =
        { t #1 #2 substring$ "--" = not
            { "--" *
              t #2 global.max$ substring$ 't :=
            }
            {   { t #1 #1 substring$ "-" = }
                { "-" *
                  t #2 global.max$ substring$ 't :=
                }
              while$
            }
          if$
        }
        { t #1 #1 substring$ *
          t #2 global.max$ substring$ 't :=
        }
      if$
    }
  while$
}

FUNCTION {format.pages}
{ pages empty$
    { "" }
    { pages n.dashify }
  if$
}

FUNCTION {is.digit}
{ chr.to.int$ 'len :=
  len #47 > len #58 < and
}

FUNCTION {format.edition}
{ edition empty$
    { "" }
    { edition "1" = edition "First" = or edition "first" = or edition "1st" = or
        { "" }
        { edition #-1 #1 substring$ is.digit
            { edition #-1 #1 substring$ 's :=
              edition text.length$ #1 >
                { edition #-2 #1 substring$ "1" = }
                { #0 }
              if$
                { "th" }
                { s "1" =
                    { "st" }
                    { s "2" =
                        { "nd" }
                        { s "3" =
                            { "rd" }
                            { "th" }
                          if$
                        }
                      if$
                    }
                  if$
                }
              if$
              edition swap$ * " ed." *
            }
            { edition " ed." * }
          if$
        }
      if$
    }
  if$
}

FUNCTION {format.volume}
{ volume empty$
    { "" }
    { "vol. " volume * }
  if$
}

FUNCTION {format.place.pub}
{ 't :=
  address empty$
    { t }
    { t empty$
        { address }
        { address ": " * t * }
      if$
    }
  if$
}

FUNCTION {event.date}
{ eventdate empty$
    { month field.or.null }
    { eventdate }
  if$
}

FUNCTION {format.vol.num}
{ volume field.or.null
  number empty$
    'skip$
    { "(" * number * ")" * }
  if$
}

FUNCTION {month.abbr}
{ 't :=
  t "01" = { "Jan" } {
  t "02" = { "Feb" } {
  t "03" = { "Mar" } {
  t "04" = { "Apr" } {
  t "05" = { "May" } {
  t "06" = { "Jun" } {
  t "07" = { "Jul" } {
  t "08" = { "Aug" } {
  t "09" = { "Sep" } {
  t "10" = { "Oct" } {
  t "11" = { "Nov" } {
  t "12" = { "Dec" } { t }
  if$ } if$ } if$ } if$ } if$ } if$ } if$ } if$ } if$ } if$ } if$ } if$
}

%% urldate in ISO form (2026-10-22) becomes "22 Oct 2026"; anything else is used as written
FUNCTION {format.urldate}
{ urldate text.length$ #10 =
  urldate #5 #1 substring$ "-" = and
    { urldate #9 #2 substring$ " " *
      urldate #6 #2 substring$ month.abbr * " " *
      urldate #1 #4 substring$ *
    }
    { urldate }
  if$
}

%% DOI preferred (no access date needed); otherwise URL + [accessed date]
FUNCTION {format.available}
{ doi empty$
    { url empty$
        { "" }
        { "available: \ulurl{" url * "}" *
          urldate empty$
            'skip$
            { " [accessed " * format.urldate * "]" * }
          if$
        }
      if$
    }
    { doi #1 #4 substring$ "http" =
        { doi }
        { "http://dx.doi.org/" doi * }
      if$
      "available: \ulurl{" swap$ * "}" *
    }
  if$
}

%% web pages always get the access date if given
FUNCTION {format.available.web}
{ url empty$
    { format.available }
    { "available: \ulurl{" url * "}" *
      urldate empty$
        'skip$
        { " [accessed " * format.urldate * "]" * }
      if$
    }
  if$
}

FUNCTION {output.bibitem}
{ newline$
  "\bibitem[{" write$
  short.label write$
  "(" write$
  year.label write$
  ")" write$
  full.label write$
  "}]{" write$
  cite$ write$
  "}" write$
  newline$
}

FUNCTION {finish.entry}
{ note field.or.null add.part
  out add.period$ write$
  newline$
}

%% ---------- entry types ----------

FUNCTION {article}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  journal emphasize add.part
  format.vol.num add.part
  format.pages add.part
  format.available add.part
  finish.entry
}

FUNCTION {book}
{ output.bibitem
  title emphasize 'ftitle :=
  #1 'use.ed :=
  make.head
  ftitle add.part
  translator empty$
    'skip$
    { "translated by " translator format.names * add.part }
  if$
  format.volume add.part
  format.edition add.part
  publisher field.or.null format.place.pub add.part
  format.available add.part
  finish.entry
}

FUNCTION {booklet} { book }

FUNCTION {manual} { book }

FUNCTION {incollection}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  booktitle empty$
    { "" }
    { editor empty$
        { "in " booktitle emphasize * }
        { "in " editor format.names * ", " * ed.suffix * ", " *
          booktitle emphasize *
        }
      if$
    }
  if$
  add.space
  format.edition add.part
  publisher field.or.null format.place.pub add.part
  format.pages add.part
  format.available add.part
  finish.entry
}

FUNCTION {inbook}
{ booktitle empty$
    { book }
    { incollection }
  if$
}

FUNCTION {inproceedings}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  publisher empty$ address empty$ and editor empty$ and pages empty$ and
  doi empty$ and url empty$ and
    { %% unpublished conference paper
      booktitle emphasize
      duplicate$ empty$
        'skip$
        { "presented at " swap$ * }
      if$
      add.part
      event.date add.part
    }
    { editor empty$
        { booktitle emphasize
          duplicate$ empty$
            'skip$
            { "in " swap$ * }
          if$
          add.part
        }
        { "in " editor format.names * ", " * ed.suffix * add.part
          booktitle emphasize add.part
        }
      if$
      venue field.or.null add.part
      event.date add.part
      publisher empty$
        { organization field.or.null }
        { publisher }
      if$
      format.place.pub add.part
      format.pages add.part
      format.available add.part
    }
  if$
  finish.entry
}

FUNCTION {conference} { inproceedings }

FUNCTION {proceedings}
{ output.bibitem
  title emphasize 'ftitle :=
  #1 'use.ed :=
  make.head
  ftitle add.part
  venue field.or.null add.part
  event.date add.part
  publisher empty$
    { organization field.or.null }
    { publisher }
  if$
  format.place.pub add.part
  format.available add.part
  finish.entry
}

FUNCTION {thesis}
{ output.bibitem
  title emphasize 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  "unpublished thesis ("
  type empty$
    { thtype }
    { type }
  if$
  * ")" * add.part
  school field.or.null add.part
  format.available add.part
  finish.entry
}

FUNCTION {phdthesis}
{ "Ph.D." 'thtype :=
  thesis
}

FUNCTION {mastersthesis}
{ "Masters" 'thtype :=
  thesis
}

FUNCTION {techreport}
{ output.bibitem
  title emphasize 'ftitle :=
  #1 'use.ed :=
  make.head
  ftitle add.part
  number empty$
    { "" }
    { type empty$
        { number }
        { type " " * number * }
      if$
    }
  if$
  add.part
  publisher empty$
    { institution field.or.null }
    { publisher }
  if$
  format.place.pub add.part
  format.available add.part
  finish.entry
}

FUNCTION {workingpaper}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  series empty$
    { institution emphasize }
    { series emphasize }
  if$
  add.part
  number empty$
    { "" }
    { "No. " number * }
  if$
  add.part
  format.available add.part
  finish.entry
}

FUNCTION {online}
{ output.bibitem
  title emphasize 'ftitle :=
  #1 'use.ed :=
  make.head
  ftitle add.part
  howpublished field.or.null add.part
  format.available.web add.part
  finish.entry
}

FUNCTION {webpage} { online }
FUNCTION {www} { online }
FUNCTION {electronic} { online }
FUNCTION {misc} { online }

FUNCTION {blog}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  journal empty$
    { howpublished field.or.null }
    { journal }
  if$
  emphasize add.part
  event.date add.part
  format.available.web add.part
  finish.entry
}

FUNCTION {unpublished}
{ output.bibitem
  title quote.title 'ftitle :=
  #0 'use.ed :=
  make.head
  ftitle add.part
  howpublished field.or.null add.part
  format.available add.part
  finish.entry
}

FUNCTION {default.type} { misc }

MACRO {jan} {"Jan"}
MACRO {feb} {"Feb"}
MACRO {mar} {"Mar"}
MACRO {apr} {"Apr"}
MACRO {may} {"May"}
MACRO {jun} {"Jun"}
MACRO {jul} {"Jul"}
MACRO {aug} {"Aug"}
MACRO {sep} {"Sep"}
MACRO {oct} {"Oct"}
MACRO {nov} {"Nov"}
MACRO {dec} {"Dec"}

READ

%% ---------- labels and sorting ----------

FUNCTION {sortify}
{ purify$
  "l" change.case$
}

FUNCTION {format.lab.names}
{ 's :=
  s num.names$ 'numnames :=
  s #1 "{vv~}{ll}" format.name$ 't :=
  numnames #1 >
    { numnames #2 =
        { s #2 "{ff }{vv }{ll}{ jj}" format.name$ "others" =
            { t " \emph{et~al.}" * }
            { t " and " * s #2 "{vv~}{ll}" format.name$ * }
          if$
        }
        { t " \emph{et~al.}" * }
      if$
    }
    { t }
  if$
}

FUNCTION {format.full.lab.names}
{ 's :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
  "" 't :=
    { namesleft #0 > }
    { s nameptr "{vv~}{ll}" format.name$ 'u :=
      nameptr #1 >
        { namesleft #1 >
            { t ", " * u * 't := }
            { u "others" =
                { t " \emph{et~al.}" * 't := }
                { t " and " * u * 't := }
              if$
            }
          if$
        }
        { u 't := }
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
  t
}

FUNCTION {calc.label}
{ author empty$ not
    { author format.lab.names 'short.label :=
      author format.full.lab.names 'full.label :=
    }
    { editor empty$ not
        { editor format.lab.names 'short.label :=
          editor format.full.lab.names 'full.label :=
        }
        { organization empty$ not
            { organization 'short.label :=
              organization 'full.label :=
            }
            { key empty$ not
                { key 'short.label :=
                  key 'full.label :=
                }
                { title emphasize 'short.label :=
                  title emphasize 'full.label :=
                }
              if$
            }
          if$
        }
      if$
    }
  if$
  short.label " " * year.text * 'label :=
}

FUNCTION {sort.format.names}
{ 's :=
  #1 'nameptr :=
  "" 't :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
    { namesleft #0 > }
    { s nameptr "{vv{ } }{ll{ }}{  ff{ }}{  jj{ }}" format.name$ 'u :=
      nameptr #1 >
        { t "   " * u * 't := }
        { u 't := }
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
  t
}

FUNCTION {presort}
{ calc.label
  author empty$ not
    { author sort.format.names }
    { editor empty$ not
        { editor sort.format.names }
        { organization empty$ not
            { organization }
            { key empty$ not
                { key }
                { title field.or.null }
              if$
            }
          if$
        }
      if$
    }
  if$
  sortify
  "    " *
  year.text sortify *
  "    " *
  title field.or.null sortify *
  #1 entry.max$ substring$
  'sort.key$ :=
}

ITERATE {presort}

SORT

STRINGS { last.label next.extra }

INTEGERS { last.extra.num number.label }

FUNCTION {initialize.extra.label.stuff}
{ #0 int.to.chr$ 'last.label :=
  "" 'next.extra :=
  #0 'last.extra.num :=
  #0 'number.label :=
}

FUNCTION {forward.pass}
{ last.label label =
    { last.extra.num #1 + 'last.extra.num :=
      last.extra.num int.to.chr$ 'extra.label :=
    }
    { "a" chr.to.int$ 'last.extra.num :=
      "" 'extra.label :=
      label 'last.label :=
    }
  if$
  number.label #1 + 'number.label :=
}

FUNCTION {reverse.pass}
{ next.extra "b" =
    { "a" 'extra.label := }
    'skip$
  if$
  extra.label 'next.extra :=
  extra.label empty$
    'skip$
    { "{\natexlab{" extra.label * "}}" * 'extra.label := }
  if$
}

EXECUTE {initialize.extra.label.stuff}

ITERATE {forward.pass}

REVERSE {reverse.pass}

FUNCTION {begin.bib}
{ preamble$ empty$
    'skip$
    { preamble$ write$ newline$ }
  if$
  "\providecommand{\natexlab}[1]{#1}" write$ newline$
  "\providecommand{\url}[1]{\texttt{#1}}" write$ newline$
  "\providecommand{\ulurl}[1]{\url{#1}}" write$ newline$
  "\begin{thebibliography}{" number.label int.to.str$ * "}" * write$ newline$
}

EXECUTE {begin.bib}

ITERATE {call.type$}

FUNCTION {end.bib}
{ newline$
  "\end{thebibliography}" write$ newline$
}

EXECUTE {end.bib}
