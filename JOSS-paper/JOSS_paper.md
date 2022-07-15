---
title: 'Package name: words and things'
tags:
  - Python
  - data science
  - data exploration
  - text processing
authors:
  - name: Adrian M. Price-Whelan
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Author with no affiliation
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 3
affiliations:
 - name: Lyman Spitzer, Jr. Fellow, Princeton University, USA
   index: 1
 - name: Institution Name, Country
   index: 2
 - name: Independent Researcher, Country
   index: 3
date: Fall 2022
bibliography: paper.bib

---


## Everything above from template 

# Summary

In this paper, we present **CODE NAME** to support the automatic searching of collegiete course catalogs to find courses related to a set of search terms. 
In addition to justifying the need for this kind of package, we will share a few examples of using this code on real course catalogs from US institutions, finding courses from a variety of subject-interests. 

The package **CODE NAME** processes the course catalog and then visualizes their recommended courses in a few views. 
For processing the course catalogs, **CODE NAME** first leverages tools for digitizing course catalog PDFs. 
Then it processes those digitalized catalogs to find course descriptions that are related to a list of provided. 
Finally, there are functions to support visualizing the output recommendations, highlighting the department codes for the recommendations as well as the level for each course. 

- Discuss why PDFs (ie. static version of catalog, many have historical pdfs)
- Should we add ML extensions or no? 
- Add origin story? 


# Statement of need

With the growing number of interdisciplinary and cross-displinary courses and programs--like data science--there is a need to unearth where and in which departments certain concepts and topics are explored. 
For exmaple, a student may have enjoyed a course on Korean Art and is looking to take courses on similar content. 
These classes could be in an art history department, but there also may be related courses in a Film and Media studies department or in an East Asian Studies department. 
If our example student constrains herself only to the 'traditional' or 'expected' art history department, she may miss out on courses that would captivate her interest. 
This package seeks to support exploring a course catalog begining with a PDF of a catalog and a coherent list of search terms. 



# Examples

In this section, we document a few examples from three different institutions. These examples represent different course catalog structures as well as showing the kinds of exploration that this tool can support from very narrow search parameters to much wider ones. 

- Smith examples: SDS, Korean, Engineering, and Theatre.   
  - Should we do one for the 5C? 
- Brown U examples: 
- Valpo? 

## Everything below from template 
# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

- Add NSF grant numbers

# References
