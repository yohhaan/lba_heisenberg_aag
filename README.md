# Length Based Attack on AAG Key Exchange using as a platform the Heisenberg Group

This is a quick implementation of:
- the AAG key exchange protocol using as a platform the Heisenberg Group
$\mathbb{H}_3$
- and a length based attack against it

The main purpose of this implementation was to be used for a class project for
UW-Madison MATH 842: Applied Topics in Linear Algebra. The project is about
studying the length based attack on the Anshel-Anshel-Goldfeld key exchange
protocol using as a platform the discrete Heisenberg group $\mathbb{H}_3$. The
code in this repository was used as an illustration of this type of attacks when
presenting the concepts to the rest of the class.

## Docker Deployment

The `.devcontainer` folder contains the config to open this repository into a
Docker container with VS code and the [VS code Dev Containers
extension](https://code.visualstudio.com/docs/devcontainers/containers).

The Docker container comes with [SAGE](https://www.sagemath.org/) installed. You
can also deploy the container directly from the command line:
```
docker run -it -v $(pwd):/home/sage/project sagemath/sagemath:latest /bin/bash
cd project
sage
sage: load("filename")
```

## References

### Sage
- [Sage Programming and compiled
  code](https://doc.sagemath.org/html/en/tutorial/programming.html)
- [Sage Heisenberg Group](https://doc.sagemath.org/html/en/reference/groups/sage/groups/matrix_gps/heisenberg.html)
- [Sage Heisenberg
  Algebra](https://doc.sagemath.org/html/en/reference/algebras/sage/algebras/lie_algebras/heisenberg.html)

### Related Work
- [Heisenberg groups as platform for the AAG key-exchange
  protocol](https://arxiv.org/pdf/1403.4165.pdf) (missing details about length
  function used, code not available publicly)
- [Word distance on the discrete Heisenberg Group](https://doi.org/10.4064/CM95-1-2) (Closed form for length function for $\mathbb{H}_3$)
- [Wikipedi Heisenberg Group](https://en.wikipedia.org/wiki/Heisenberg_group) & [Geometric Aspects of the Heisenberg
  Group](https://www.math.arizona.edu/~ura-reports/061/Pate.John/Final.pdf)
  (some background on Heisenberg Group)
- [Asymptotic Properties of the Heisenberg
  Group](https://doi.org/10.1023/A%3A1015306413677) (some proofs related to $\mathbb{H}_3$)

