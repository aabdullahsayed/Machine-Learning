# Gradient

> The mathematical foundation behind optimization in Machine Learning and Deep Learning.

---

# Learning Objectives

After reading this note, you will understand:

- What a gradient is mathematically
- Why gradients exist
- How to calculate gradients
- Geometric intuition
- Relationship with derivatives and partial derivatives
- How gradients solve optimization problems
- How ML/DL use gradients to train models

---

# Prerequisites

Before learning gradients, you should know:

- Functions
- Limits
- Derivatives
- Partial Derivatives
- Vectors

---

# 1. The Mathematical Problem

Suppose we have a function

\[
f(x)
\]

We know the derivative tells us

- how fast the function changes
- whether it increases or decreases

Example

\[
f(x)=x^2
\]

Derivative

\[
f'(x)=2x
\]

This works perfectly...

**until the function has multiple variables.**

Example

\[
f(x,y)=x^2+y^2
\]

Now there is no single derivative.

We need a way to measure change with respect to **every variable**.

This leads to the concept of the **Gradient**.

---

# 2. Partial Derivatives

For

\[
f(x,y)=x^2+y^2
\]

Partial derivative with respect to x

\[
\frac{\partial f}{\partial x}=2x
\]

Partial derivative with respect to y

\[
\frac{\partial f}{\partial y}=2y
\]

Each partial derivative tells us

> "How much does the function change if only one variable changes?"

---

# 3. Definition of Gradient

The gradient is simply a collection of all partial derivatives.

\[
\nabla f=
\left(
\frac{\partial f}{\partial x},
\frac{\partial f}{\partial y}
\right)
\]

For n variables,

\[
\nabla f=
\left(
\frac{\partial f}{\partial x_1},
\frac{\partial f}{\partial x_2},
...
\frac{\partial f}{\partial x_n}
\right)
\]

Notice

Derivative

```
One variable
↓

One slope
```

Gradient

```
Many variables
↓

Many slopes
↓

One vector
```

---

# 4. Why is Gradient a Vector?

Each partial derivative is one number.

Example

\[
\frac{\partial f}{\partial x}=4
\]

\[
\frac{\partial f}{\partial y}=6
\]

Combine them

```
(4,6)
```

A collection of numbers describing direction is called a **vector**.

Therefore

```
Gradient = Vector
```

---

# 5. Example

Function

\[
f(x,y)=x^2+y^2
\]

Gradient

\[
\nabla f=(2x,2y)
\]

At point

\[
(2,3)
\]

Gradient becomes

\[
(4,6)
\]

Meaning

```
Moving in x changes the function by 4.

Moving in y changes the function by 6.
```

---

# 6. Geometric Meaning

Imagine standing on a mountain.

```
          ▲
       ▲
    ▲
 ● You
```

The gradient always points toward

```
Steepest uphill direction
```

If you want to reach the bottom,

walk in the opposite direction.

---

# 7. Important Properties

## Gradient points toward maximum increase

\[
\nabla f
\]

always points in the direction where the function increases the fastest.

---

## Negative Gradient points toward minimum

\[
-\nabla f
\]

points toward the fastest decrease.

---

## Zero Gradient

If

\[
\nabla f=0
\]

then the point is called a **stationary point**.

It may be

- local minimum
- local maximum
- saddle point

---

# 8. Why Was Gradient Invented?

Mathematicians wanted to solve optimization problems like

```
Find the highest point.

Find the lowest point.

Find the shortest path.

Find the minimum cost.
```

For one variable,

derivatives were enough.

For many variables,

they invented the **Gradient**.

---

# 9. From Mathematics to Machine Learning

Machine Learning is simply an optimization problem.

Instead of minimizing

```
Distance
```

or

```
Height
```

we minimize

```
Prediction Error
```

The error is called the **Loss Function**.

Example

\[
L(w,b)
\]

where

- w = weight
- b = bias

The goal is

```
Find values of w and b

that make Loss as small as possible.
```

How do we know which direction to change them?

Using the **Gradient**.

---

# 10. Gradient in Machine Learning

Suppose

Prediction

```
ŷ = wx+b
```

Loss

\[
L=(y-\hat y)^2
\]

Compute

```
∂L/∂w

∂L/∂b
```

These form the gradient

```
(∂L/∂w, ∂L/∂b)
```

Now update

\[
w=w-\eta\frac{\partial L}{\partial w}
\]

\[
b=b-\eta\frac{\partial L}{\partial b}
\]

Repeat until the loss is minimized.

---

# 11. Gradient in Deep Learning

A neural network may contain

- millions of weights
- thousands of biases

The loss depends on every parameter.

Backpropagation computes

```
Gradient of every parameter
```

Then an optimizer updates them.

Workflow

```
Input

↓

Prediction

↓

Loss

↓

Backpropagation

↓

Gradient

↓

Optimizer

↓

Updated Weights
```

This process repeats for every training batch until the network learns.

---

# 12. Why Gradient is Essential in ML/DL

Without gradients:

- We wouldn't know how to update weights.
- Training would require guessing parameter values.
- Modern neural networks with millions of parameters would be computationally impractical.

Gradients provide the direction and magnitude needed for efficient optimization.

---

# Summary

**Mathematics**

- Derivative → one variable
- Partial derivative → one variable while others are fixed
- Gradient → vector of all partial derivatives
- Gradient points toward the steepest increase
- Negative gradient points toward the steepest decrease

**Machine Learning**

- Loss is a mathematical function.
- Gradient measures how the loss changes with each parameter.
- Optimizers use gradients to update weights.
- Backpropagation computes gradients efficiently for deep neural networks.