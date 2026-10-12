# KnowledgeSuperposition — arXiv 2408.07413

Source: https://arxiv.org/html/2408.07413

## Headings
# Knowledge in Superposition: Unveiling the Failures of Lifelong Knowledge Editing for Large Language Models
## Introduction
## Related Work
### Knowledge Editing
### Superposition
## Preliminary
## Expanding to Lifelong Editing
### Interference Term of Original Knowledge Δ o \Delta_{o}
### Interference Term of Edited Knowledge Δ e \Delta_{e}
### How to Understand p ⁡ ( ⋅ , ⋅ ) p(\cdot,\cdot)
## Knowledge in Superposition
### Universal in Language Models
### Heavy-Tailed Distribution in Language Models
### Scaling Law for Superposition
### Superposition in Whitening Space
## Conclusion
## Acknowledgements
## References
## Appendix A A. Proof in Preliminary
## Appendix B B. Proof of Whitening Matrix
## Appendix C C. Number of Knowledge Items m m
## Appendix D D. Visualization of P P Matrices for All Layers
## Appendix E E. KDE of P P Matrices for All Layers
## Appendix F F. Case Study
## Appendix G G. Experimental Detail
## Appendix H H. Continuous Editing Causes Models’ Failure
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 1, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 5, "zsre": 0, "teacher forc": 0, "autoregressive": 1, "first token": 0, "subject": 6, "last token": 2, "embedding": 0, "vocabulary": 0}


## SECTION: Appendix G G. Experimental Detail



 
 Specifically, we intersect the data items from CounterFact that all the language models can correctly complete, and we randomly select 128 items from this intersection. 
 
 
 The activation extraction is performed at the last token of the subject, which has been shown by multiple studies to be the location where knowledge is extracted in language models ( Meng et al. 2022a ; Geva et al. 2023 ). For instance, in the sentence “The mother tongue of Danielle Darrieux is French,” we extract activation values from the last token of subject, namely ”Darrieux”, at each layer’s MLP in language models. 
 
 
 For the computation of C C , we pre-cache the non-centered covariance of activations k k estimated from Wikipedia text ( Lhoest et al. 2021 ) , specifically from the Wikipedia ”20220301.en” dataset. 
 
 
 All our experiments can be conducted on a single 80G A100 GPU. 
 
 
 

