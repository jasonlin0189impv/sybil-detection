# Sybil Detection

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


## About this
This notebook contains a SybilEdge algorithm for detect sybil account in Facebook. The algorithm is described in \[1\].

It's a practice for implement algorithm from the paper, I just test it on a small network which generate by myself. If you see any mistake in ```.py``` file, feel free to tell me :).


## Sybil Equation
Follow from two rules, 1. User's selection of target, 2. Targets' response, to detect whether the new user is sybil or not.

<img src="/fig/rules.png" alt="drawing" width="60%"/>

More detail in reference\[1\]


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Cheng-Hsin Lin - chenshin2475@gmail.com


<!-- REFERENCE -->
## Reference
\[1\] [Friend or Faux: Graph-Based Early Detection of Fake accounts on Social Networks](https://arxiv.org/abs/2004.04834)

