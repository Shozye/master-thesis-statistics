# Plot Guidance
This file contains information about how plots should look like and how experiments should handle plot creation

## Title
Plot in matplotlib shouldn't have got a title as it duplicates information and uses wrong font.
The caption is what should be used.
The only exception is when a plot have many subplots, then subplots are allowed to have short subtitles like: "Fixed N= 200, varying Lambda". 

## Caption
The caption is the source of truth, 
it shall not explain how experiment was done, 
it shall say what the plot shows. 
Caption should not use hardcoded values like m=512 but rather m={m}

### Antipatterns, do not use 
- mentions of legend in caption like: "solid and dashed"
- describing what is visible from the legend (e.g. "Dashed line: ExpSketch baseline")
- describing what is visible from subplot titles or axis labels (e.g. "for q in {5, 7, 9}")
- stating conclusions the plot gives (e.g. "Error stabilizes from g >= 5", "All three converge to the true value")
- the ' \( \) ' should be used, not ' $ $ '

## OX 
If experiment is one where it is viable that we have got many points on OX,
then the experiment should have at least 30 dots to assert smoothness.
The great deal is 100 dots.
It would be nice to have a variable in quality parameters that say of how many points the plot is created
Of course, there are experiments where it isn't viable like there are buckets.
