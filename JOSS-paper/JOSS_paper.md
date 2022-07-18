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

To identify such courses across disciplines, researchers have turned to college course catalogs. 
From the course catalogs, we extract the course ID, title, and description for each course. 
The goal is to create a list of course IDs that contain content that _might_ be of interest given a list of set of search terms. 
**CODE NAME** leverages the words in the course decriptions and the titles to build the list of course IDs. 
The course ID will contain both the course's department code as well as the specific course number, but it does not contain any "content" words. 
For example, SDS 100 is the course ID where SDS is the department code for "Program in Statistical and Data Sciences" and 100 is the course number, while the course title and description give information about what content is in SDS 100. 

Course catalogs exist in a variety of forms and styles, from searchable databases to printed books of information. 
**CODE NAME** works on a PDF version of course catalogs as most schools continue to print physical course catalogs, meaning that PDFs of that printed catalog are often availab. 
**CODE NAME** has a three-step pipeline to ultimately offer a list of courses related to a set of search terms. The pipeline consists of preprocessing, processing, and finally analysis:

1. The **_preprocessing_** stage converts course catalog PDFs to a paresable XML file. During the preprocessing stage, irrelevant information is removed so parsing can begin right when courses are formally being listed in a catalog. Once these sections are removed, the cleaned XML is passed into the processing stage. 
2. The **_processing_** stage converts the cleaned XML into a CSV file that is used for analysis. 
3. The **_analysis_** stage identifies courses in the CSV file that teach concepts listed in a keywords list of given search terms. Once those courses are identified they are appended to a list of recommendations.

Each step includes wrestles with slightly different challenges of this task. 
In the preprocessing step, the code must accommodate different formatting and spacing issues present after doing a direct PDF to XML conversion. 
Then the processing stage must be nimble enough to recognize the difference between a list of courses (like would be in a list of major requirements) and a course that names another course ID (or its own course ID) in the description. 
The analysis stage then makes use of text analysis techniques to then select courses that are potentially related to the list of supplied terms. 

# Statement of need

With the growing number of interdisciplinary and cross-displinary courses and programs--like data science--there is a need to unearth where and in which departments certain concepts and topics are explored. 
For exmaple, a student may have enjoyed a course on Korean Art and is looking to take courses on similar content. 
These classes could be in an art history department, but there also may be related courses in a Film and Media studies department or in an East Asian Studies department. 
If our example student constrains herself only to the 'traditional' or 'expected' art history department, she may miss out on courses that would captivate her interest. 
This package seeks to support exploring a course catalog begining with a PDF of a catalog and a coherent list of search terms. 

This kind of exporation can be key as colleges seek to develop new programs. One particularly timely example is Data Science. 
Departments such as psychology or biology also teach statistical concepts, which leads researchers to believe that many other departments may be teaching data science concepts. 
Identifying departments in which data science concepts are taught can allow colleges and universities to restructure or develop their data science curriculum. 




# Examples

In this section, we document a few examples from three different institutions. These examples represent different course catalog structures as well as showing the kinds of exploration that this tool can support from very narrow search parameters to much wider ones. 

- Smith examples: SDS, Korean, Engineering, and Theatre.   
  - Should we do one for the 5C? 
- Brown U examples: 
- Valpo? 

## Smith College

### Data Science

We derived a keywords list that consists of data science terms from the Edison Body of Knowledge. The Edison Body of Knowledge is used to provide universities guidance when structuring their data science curriculum. By combining both components the output is a file that contains all courses labeled as relevant to Data Science.

## Keyword lists

- How to "augment" them by adding "s" and "es" to each term
- This tool does not overcome "garbage in, garbage out" 


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
