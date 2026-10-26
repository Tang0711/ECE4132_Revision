Here is an end-to-end, multi-topic exam review problem that integrates the core principles from **Weeks 7 through 12**.

It traces a single physical process—a **linearised inverted pendulum balance system**—from first-order state-space modeling through to frequency-domain sensitivity and fundamental performance limits.

---

# Integrated Exam Review Problem: The Inverted Pendulum Balancing Mechanism

### Problem Context & Specifications

An inverted pendulum apparatus mounted on a motorized pivot is operated around its upright vertical equilibrium. Let $x_1(t) = \theta(t)$ represent the angular deflection (in radians) from the upright position, and let $x_2(t) = \dot{\theta}(t)$ represent the angular velocity. The input $u(t)$ is the horizontal pivot acceleration.

The continuous-time linearised perturbation equations of motion are given by: $$\dot{x}_1(t) = x_2(t)$$ $$\dot{x}_2(t) = x_1(t) + u(t)$$ $$y(t) = x_1(t)$$

Only the angular position $y(t) = \theta(t)$ is measured by a shaft encoder; angular velocity $x_2(t)$ is unmeasured.

---

### Multi-Part Exam Questions

1. **State-Space Modeling & Frequency-Domain Realisation (Week 7):**
    
    - Write down the matrices $(A, B, C, D)$ of the state-space model.
    - Calculate the eigenvalues of the system dynamics matrix $A$ and assess open-loop internal stability.
    - Compute the resolvent matrix $(sI - A)^{-1}$ and derive the open-loop transfer function $P(s) = \frac{Y(s)}{U(s)}$.
2. **Reachability Analysis & Full-State Feedback Design (Week 8):**
    
    - Construct the reachability matrix $W_r$ and verify whether the pair $(A, B)$ is reachable.
    - Design a full-state feedback gain vector $K = \begin{bmatrix} k_1 & k_2 \end{bmatrix}$ such that the closed-loop system poles are assigned to $s_{1,2} = -2 \pm j2$.
    - Compute the feedforward precompensation gain $k_r$ to ensure unity steady-state tracking gain ($y_{ss} = r_{ss}$) for constant setpoint commands.
3. **Observability & Luenberger State Estimator Design (Week 9):**
    
    - Construct the observability matrix $W_o$ and verify whether the pair $(A, C)$ is observable.
    - Design a Luenberger observer gain vector $L = \begin{bmatrix} l_1 \ l_2 \end{bmatrix}$ to place both observer error poles at $s_{o1,2} = -5$.
    - State the **Separation Principle** and write down the composite 4th-order closed-loop characteristic polynomial.
    - Derive the dynamic feedback compensator transfer function $C_{\text{ctrl}}(s) = \frac{U(s)}{-Y(s)}$.
4. **Loop Frequency Response & The Gang of Four (Week 10):**
    
    - Formulate the open-loop transfer function $L(s) = P(s)C_{\text{ctrl}}(s)$.
    - Formulate the **Sensitivity Function** $S(s)$ and **Complementary Sensitivity Function** $T(s)$.
    - Verify that the closed-loop denominator matches the expected poles from the Separation Principle.
5. **Nyquist Stability Criterion & Robust Stability (Week 11):**
    
    - Identify the number of open-loop right-half-plane poles $P$ of the loop transfer function $L(s)$.
    - Determine the required number of net clockwise encirclements $N$ of the critical point $-1 + j0$ for closed-loop stability using Cauchy's Argument Principle.
    - Express the robust stability condition under multiplicative plant uncertainty $\delta(s)$ using the Small Gain Theorem.
6. **Fundamental Limitations & Bode's Integral (Week 12):**
    
    - Apply the **Generalized Bode Sensitivity Integral** to this system and evaluate the exact integral area: $$\int_{0}^{\infty} \ln |S(j\omega)| , d\omega$$
    - Explain why the unstable pole at $s = +1$ creates a non-zero lower bound on peak sensitivity $M_s$.

---

## Detailed Step-by-Step Solutions & Reasoning

---

### Part 1: State-Space Modeling & Transfer Function (Week 7)

#### Matrix Formulation

From the linearised differential equations: $$\begin{bmatrix} \dot{x}_1(t) \ \dot{x}_2(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} \begin{bmatrix} x_1(t) \ x_2(t) \end{bmatrix} + \begin{bmatrix} 0 \ 1 \end{bmatrix} u(t)$$ $$y(t) = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} x_1(t) \ x_2(t) \end{bmatrix}$$

Thus: $$A = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = 0$$

#### Eigenvalue and Stability Analysis

The characteristic polynomial of $A$ is: $$\det(sI - A) = \det \begin{bmatrix} s & -1 \ -1 & s \end{bmatrix} = s^2 - 1 = (s - 1)(s + 1) = 0$$

- The eigenvalues of the open-loop matrix $A$ are: $$\lambda_1 = +1, \quad \lambda_2 = -1$$
- **Internal Stability Check:** Because $\lambda_1 = +1 > 0$ resides strictly in the right-half plane, the unforced pendulum equilibrium is **internally unstable**.

#### Resolvent Matrix & Plant Transfer Function

Compute the resolvent $(sI - A)^{-1}$: $$(sI - A)^{-1} = \frac{1}{s^2 - 1} \begin{bmatrix} s & 1 \ 1 & s \end{bmatrix}$$

Using the transfer function formula $P(s) = C(sI - A)^{-1}B + D$: $$P(s) = \begin{bmatrix} 1 & 0 \end{bmatrix} \left( \frac{1}{s^2 - 1} \begin{bmatrix} s & 1 \ 1 & s \end{bmatrix} \right) \begin{bmatrix} 0 \ 1 \end{bmatrix} = \frac{1}{s^2 - 1} \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} 1 \ s \end{bmatrix} = \frac{1}{s^2 - 1}$$

The plant has an unstable open-loop pole at $s = +1$ and a stable open-loop pole at $s = -1$.

---

### Part 2: Reachability & Full-State Feedback Design (Week 8)

#### Reachability Verification

Compute the Reachability Matrix $W_r$: $$AB = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} \begin{bmatrix} 0 \ 1 \end{bmatrix} = \begin{bmatrix} 1 \ 0 \end{bmatrix}$$ $$W_r = \begin{bmatrix} B & AB \end{bmatrix} = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix}$$

Evaluating the determinant: $$\det(W_r) = (0)(0) - (1)(1) = -1 \neq 0 \implies \text{rank}(W_r) = 2$$ Because $\text{rank}(W_r) = n = 2$, the system is **completely reachable**. All closed-loop eigenvalues can be placed at arbitrary complex conjugate locations.

#### State Feedback Gain Computation

The desired closed-loop poles are $s_{1,2} = -2 \pm j2$. The target closed-loop characteristic polynomial is: $$\alpha_d(s) = (s - (-2 + j2))(s - (-2 - j2)) = (s + 2)^2 + 4 = s^2 + 4s + 8$$

Let $K = \begin{bmatrix} k_1 & k_2 \end{bmatrix}$. The closed-loop dynamics matrix is: $$A - BK = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} - \begin{bmatrix} 0 \ 1 \end{bmatrix} \begin{bmatrix} k_1 & k_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \ 1 - k_1 & -k_2 \end{bmatrix}$$

Its characteristic equation is: $$\det(sI - (A - BK)) = \det \begin{bmatrix} s & -1 \ k_1 - 1 & s + k_2 \end{bmatrix} = s(s + k_2) + (k_1 - 1) = s^2 + k_2 s + (k_1 - 1)$$

Equating coefficients with $\alpha_d(s) = s^2 + 4s + 8$: $$k_2 = 4$$ $$k_1 - 1 = 8 \implies k_1 = 9$$

Therefore, the state feedback gain vector is: $$K = \begin{bmatrix} 9 & 4 \end{bmatrix}$$

#### Reference Precompensation Gain ($k_r$)

To ensure zero steady-state tracking error ($y_{ss} = r_{ss}$), the feedforward gain is set to the reciprocal of the closed-loop DC gain: $$k_r = -\frac{1}{C(A - BK)^{-1}B}$$

Evaluating $(A - BK)^{-1}$: $$A - BK = \begin{bmatrix} 0 & 1 \ -8 & -4 \end{bmatrix} \implies (A - BK)^{-1} = \frac{1}{0 - (-8)} \begin{bmatrix} -4 & -1 \ 8 & 0 \end{bmatrix} = \frac{1}{8} \begin{bmatrix} -4 & -1 \ 8 & 0 \end{bmatrix}$$ $$C(A - BK)^{-1}B = \begin{bmatrix} 1 & 0 \end{bmatrix} \left( \frac{1}{8} \begin{bmatrix} -4 & -1 \ 8 & 0 \end{bmatrix} \right) \begin{bmatrix} 0 \ 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} -1/8 \ 0 \end{bmatrix} = -\frac{1}{8}$$

Thus: $$k_r = -\frac{1}{-1/8} = 8$$

---

### Part 3: Observability & Observer-Based Controller (Week 9)

#### Observability Verification

Compute the Observability Matrix $W_o$: $$CA = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 \end{bmatrix}$$ $$W_o = \begin{bmatrix} C \ CA \end{bmatrix} = \begin{bmatrix} 1 & 0 \ 0 & 1 \end{bmatrix}$$

$$\det(W_o) = 1 \neq 0 \implies \text{rank}(W_o) = 2$$ The pair $(A, C)$ is **completely observable**.

#### Observer Gain Synthesis

Desired observer error poles are placed at $s_{o1,2} = -5$. The desired observer characteristic polynomial is: $$\alpha_o(s) = (s + 5)^2 = s^2 + 10s + 25$$

Let $L = \begin{bmatrix} l_1 \ l_2 \end{bmatrix}$. The observer error dynamics matrix is: $$A - LC = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} - \begin{bmatrix} l_1 \ l_2 \end{bmatrix} \begin{bmatrix} 1 & 0 \end{bmatrix} = \begin{bmatrix} -l_1 & 1 \ 1 - l_2 & 0 \end{bmatrix}$$

Its characteristic equation is: $$\det(sI - (A - LC)) = \det \begin{bmatrix} s + l_1 & -1 \ l_2 - 1 & s \end{bmatrix} = s(s + l_1) + (l_2 - 1) = s^2 + l_1 s + (l_2 - 1)$$

Matching coefficients with $\alpha_o(s) = s^2 + 10s + 25$: $$l_1 = 10$$ $$l_2 - 1 = 25 \implies l_2 = 26$$

Thus, the observer gain vector is: $$L = \begin{bmatrix} 10 \ 26 \end{bmatrix}$$

#### The Separation Principle

By the **Separation Principle**, the $2n = 4$ closed-loop eigenvalues of the observer-based feedback system split into the independent union of controller poles and observer poles: $$\det \left( sI - \begin{bmatrix} A - BK & BK \ 0 & A - LC \end{bmatrix} \right) = \det(sI - (A - BK)) \cdot \det(sI - (A - LC)) = \alpha_d(s) \cdot \alpha_o(s)$$

The composite 4th-order closed-loop characteristic polynomial is: $$\Delta_{cl}(s) = (s^2 + 4s + 8)(s^2 + 10s + 25) = s^4 + 14s^3 + 73s^2 + 180s + 200$$

#### Dynamic Controller Transfer Function

Eliminating the estimated state vector $\hat{x}(t)$ gives the feedback compensator transfer function: $$C_{\text{ctrl}}(s) = K \left( sI - (A - BK - LC) \right)^{-1} L$$

Calculate the internal dynamics matrix: $$A - BK - LC = \begin{bmatrix} 0 & 1 \ 1 & 0 \end{bmatrix} - \begin{bmatrix} 0 & 0 \ 9 & 4 \end{bmatrix} - \begin{bmatrix} 10 & 0 \ 26 & 0 \end{bmatrix} = \begin{bmatrix} -10 & 1 \ -34 & -4 \end{bmatrix}$$

Invert the resolvent matrix: $$sI - (A - BK - LC) = \begin{bmatrix} s + 10 & -1 \ 34 & s + 4 \end{bmatrix}$$ $$\det(sI - (A - BK - LC)) = (s + 10)(s + 4) - (-34) = s^2 + 14s + 74$$ $$(sI - (A - BK - LC))^{-1} = \frac{1}{s^2 + 14s + 74} \begin{bmatrix} s + 4 & 1 \ -34 & s + 10 \end{bmatrix}$$

Multiply by $L$ and $K$: $$\begin{bmatrix} s + 4 & 1 \ -34 & s + 10 \end{bmatrix} \begin{bmatrix} 10 \ 26 \end{bmatrix} = \begin{bmatrix} 10s + 66 \ 26s - 80 \end{bmatrix}$$ $$C_{\text{ctrl}}(s) = \begin{bmatrix} 9 & 4 \end{bmatrix} \left( \frac{1}{s^2 + 14s + 74} \begin{bmatrix} 10s + 66 \ 26s - 80 \end{bmatrix} \right) = \frac{9(10s + 66) + 4(26s - 80)}{s^2 + 14s + 74}$$ $$C_{\text{ctrl}}(s) = \frac{194s + 274}{s^2 + 14s + 74}$$

The controller poles are the roots of $s^2 + 14s + 74 = (s + 7)^2 + 25 = 0 \implies s = -7 \pm j5$ (the compensator is open-loop stable).

---

### Part 4: Frequency Response & The Gang of Four (Week 10)

#### Loop Transfer Function $L(s)$

The open-loop loop transfer function is: $$L(s) = P(s)C_{\text{ctrl}}(s) = \left( \frac{1}{s^2 - 1} \right) \left( \frac{194s + 274}{s^2 + 14s + 74} \right) = \frac{194s + 274}{(s^2 - 1)(s^2 + 14s + 74)}$$

#### Sensitivity and Complementary Sensitivity

Form the sensitivity functions: $$S(s) = \frac{1}{1 + L(s)} = \frac{(s^2 - 1)(s^2 + 14s + 74)}{(s^2 - 1)(s^2 + 14s + 74) + (194s + 274)}$$ $$T(s) = \frac{L(s)}{1 + L(s)} = \frac{194s + 274}{(s^2 - 1)(s^2 + 14s + 74) + (194s + 274)}$$

Expanding the characteristic denominator: $$(s^2 - 1)(s^2 + 14s + 74) + 194s + 274 = s^4 + 14s^3 + 73s^2 - 14s - 74 + 194s + 274$$ $$D_{cl}(s) = s^4 + 14s^3 + 73s^2 + 180s + 200$$

This matches the composite polynomial $\Delta_{cl}(s) = \alpha_d(s)\alpha_o(s)$ derived in Part 3, verifying that all four closed-loop poles are stable.

---

### Part 5: Nyquist Stability & Robust Stability (Week 11)

#### Nyquist Stability Criterion

1. **Count Open-Loop RHP Poles ($P$):** The loop transfer function is: $$L(s) = \frac{194s + 274}{(s - 1)(s + 1)(s^2 + 14s + 74)}$$ The poles of $L(s)$ are at $s = +1, -1, -7 \pm j5$. Therefore, there is **$P = 1$ open-loop pole in the right-half plane**.
2. **Cauchy's Argument Equation:** $$Z = N + P$$ For the closed-loop system to be internally stable, we require **$Z = 0$** (zero unstable closed-loop poles).
3. **Required Encirclement Count:** $$0 = N + 1 \implies N = -1$$ The Nyquist plot of $L(s)$ must encircle the critical point $-1 + j0$ **exactly once in the counter-clockwise direction** ($N = -1$).

#### Robust Stability under Multiplicative Uncertainty

Assume the true physical plant dynamics are subject to multiplicative uncertainty: $$P_{\text{actual}}(s) = P(s)(1 + \delta(s)), \quad |\delta(j\omega)| \le |W_m(j\omega)|$$

By the Small Gain Theorem, the feedback loop remains robustly stable for all stable perturbations satisfying the bound if and only if: $$|T(s) W_m(s)|_\infty < 1 \iff |T(j\omega)| < \frac{1}{|W_m(j\omega)|}, \quad \forall \omega \in [0, \infty)$$

---

### Part 6: Fundamental Limitations & Bode's Integral (Week 12)

#### The Generalized Bode Sensitivity Integral

Because the open-loop transfer function $L(s)$ has a relative degree of $4 - 1 = 3 \ge 2$, the high-frequency roll-off condition $\lim_{s \to \infty} s L(s) = 0$ holds. Applying the Generalized Bode Integral Formula for an open-loop system with $P = 1$ unstable pole at $p_1 = +1$:

$$\int_{0}^{\infty} \ln |S(j\omega)| , d\omega = \pi \sum_{\text{Re}(p_k) > 0} p_k = \pi \cdot (1) = \pi \approx 3.1416$$

#### Physical Significance

1. **The Positive Area Penalty:** For a stable plant, this integral equals zero. For this inverted pendulum, the area is strictly positive ($\pi$). The disturbance amplification area (where $|S(j\omega)| > 1$) must exceed the disturbance attenuation area (where $|S(j\omega)| < 1$) by at least $3.1416$.
2. **The Waterbed Effect:** Suppressing tracking error at low frequencies ($\ln |S| \ll 0$) forces a pronounced sensitivity peak $M_s = \max |S(j\omega)| > 1$ at intermediate frequencies.
3. **Stability Margin:** Because $s_m = 1/M_s$, the presence of the unstable pole at $s = +1$ introduces an inherent limit on the achievable distance to the critical point $-1$, requiring sufficient actuator bandwidth to maintain stabilization without fragile margins.

---

### Summary Checklist for Exam Revision

```
+-------+-----------------------------+------------------------------------+----------------------------------------+
| Part  | Core Concept                | Governing Formula / Tool           | Key Numerical Outcome                  |
+-------+-----------------------------+------------------------------------+----------------------------------------+
| 1     | State-Space & Resolvent     | P(s) = C(sI - A)^(-1) B            | P(s) = 1 / (s^2 - 1), poles at ±1      |
| 2     | State Feedback Gains        | A - BK matching target alpha_d(s)  | K =, Precompensation kr = 8     |
| 3     | Observer & 2-DOF Controller | C_ctrl(s) = K(sI - A + BK + LC)^-1L| C_ctrl(s) = (194s + 274)/(s^2+14s+74)  |
| 4     | Gang of Four Formulation    | S = 1/(1+L),  T = L/(1+L)          | Denominator: s^4+14s^3+73s^2+180s+200  |
| 5     | Nyquist Stability Criterion | Z = N + P = 0                      | P = 1, N = -1 (1 counter-clockwise)    |
| 6     | Bode's Integral Formula     | Integral ln|S| dω = π * sum(p_k)   | Total area = π (unstable pole penalty) |
+-------+-----------------------------+------------------------------------+----------------------------------------+
```

---
