library(r3dmol)
library(shiny)
options(scipen = 999) #Prevent scientific notation



# Plot 3D structure

template <- '---
title: "Plot AlphaFold2 Structures of rep sequences from OGs"
author: "Timothy Stephens"
date: "`r format(Sys.time(), \'%d %B, %Y\')`"
output:
  html_document
---



## Setup

Setup R env. Load packages and set default image export formats, size and resolution.

```{r setup}
knitr::opts_chunk$set(echo = TRUE,
                      fig.height = 16, 
                      fig.width = 12, 
                      dev = c("png", "pdf"),
                      dpi = 1000)
library(r3dmol)
options(scipen = 999) #Prevent scientific notation
```





# Function to plot 3D structure

```{r plot_AlphaFold2_structure}
OG  <- "<<<OG>>>"
html.out1 <- paste(OG,".alphafold.3Dinteractive.html", sep="")
html.out2 <- paste(OG,".alphafold.3D.html", sep="")
pdb.file  <- OG
pdb.id    <- OG

width=800
height=800

## Setup initial protein 3D viewer
viewer <- r3dmol(
    width=width,
    height=height,
  viewer_spec = m_viewer_spec(
    cartoonQuality = 10,
    lowerZoomLimit = 50,
    upperZoomLimit = 350,
  ),
  id = pdb.id,
  elementId = pdb.id
) %>%
  # Add model to scene
  m_add_model(data = pdb.file, format = "pdb") %>%
  # Zoom to encompass the whole scene
  m_zoom_to() %>%
  # Set style of structures
  m_set_style(style = m_style_cartoon(
    colorfunc = "
        function(atom) {
          if (atom.b < 50) {return \'#ef7c45\'};
          if (atom.b < 70 && atom.b >= 50) {return \'#f8db13\'};
          if (atom.b < 90 && atom.b >= 70) {return \'#65cbf3\'};
          if (atom.b >= 90) {return \'#2a54d6\'};
          return \'white\';
        }"
  )) %>% 
  m_button_manual(
    name = "cartoon",
    label = "Cartoon",
    align_items = "flex-end",
    justify_content = "center",
    func = "
      function() {
        viewer.setStyle({cartoon:{arrows:true, colorfunc:function(atom) {
          if (atom.b < 50) {return \'#ef7c45\'};
          if (atom.b < 70 && atom.b >= 50) {return \'#f8db13\'};
          if (atom.b < 90 && atom.b >= 70) {return \'#65cbf3\'};
          if (atom.b >= 90) {return \'#2a54d6\'};
          return \'white\';
        }}});
        viewer.render();
      }"
  ) %>%
  m_button_manual(
    name = "stick",
    label = "Stick",
    func = "
      function() {
        viewer.setStyle({stick:{}});
        viewer.render();
      }
    "
  ) %>%
  m_button_spin()


## Rotate view
#viewer <- viewer %>% m_rotate(angle = 90, axis = "y")
#viewer

## Create interactive results HTML
legend <- htmltools::img(src = knitr::image_uri("Plot_AlphaFold2-legend.png"), 
                    alt = "logo", 
                    style = paste(\'float: bottom;padding-bottom:0px;height:\',40*4,\'px;width:\',160*4,\'px\', sep="")
                    )
viewer <- htmlwidgets::prependContent(viewer, legend)
htmltools::save_html(viewer, html.out1)

## Create static results HTML
viewer <- viewer %>% m_png()
htmltools::save_html(viewer, html.out2)
```




# Session Info

```{r ressionInfo}
sessionInfo()
```
'

PDB <- "best.pdb"
print(paste("Plotting: ", PDB, sep=''))
rmd <- paste(PDB,".alphafold.Rmd", sep="")
out <- paste(PDB,".alphafold.html", sep="") # Needs to be relative to the *Rmd file. So we dont need the directory for this file name.

s <- gsub("<<<OG>>>", PDB, template)
write(s, rmd)

# Render Rmarkdown file
rmarkdown::render(rmd, output_file = out)





# Session Info
sessionInfo()

