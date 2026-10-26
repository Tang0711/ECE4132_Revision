### Examination Structure & Prediction Analysis

The **ECE4132 Mock Exam** tests core competencies across five modular themes:

1. **Response Classification & System Types** (Questions 1 & 2): Matching loop transfer functions to step/ramp responses and evaluating steady-state error.
2. **Frequency Domain & Sensitivity Analysis** (Question 4): Interpreting loop transfer functions $L(s)$, Nyquist encirclements of $-1$, sensitivity peaks $M_s = \max_\omega |S(j\omega)|$, and tracking bandwidth.
3. **Nonlinear Systems & Equilibrium Linearisation** (Question 5): Determining multiple equilibrium points for autonomous nonlinear differential equations and computing local Jacobian matrices.
4. **State-Space Control & Observer Synthesis** (Question 6): Evaluating internal versus BIBO stability, placing observer eigenvalues ($A - LC$), computing state feedback gains ($A - BK$), and finding the open-loop reference gain $k_r$.
5. **Physical Modelling & Digital Implementation** (Questions 3 & 7): Deriving transfer functions from physical circuits, designing continuous controllers (PI) for transient settling, discretising via Euler methods, and deriving microcontroller difference equations.

---

### Predicted Master Exam Question (25 Marks)

#### Context & Problem Statement

Active magnetic levitation (MagLev) systems are widely used in high-speed rail, magnetic bearings, and frictionless semiconductor manufacturing. A precision magnetic levitation actuator suspends a ferromagnetic sphere of mass $m$ in vertical space using an electromagnet, as shown below:

```
                  +====================+
                  |   Electromagnet    |
                  +=========++=========+
                            || Coil: R, L
                            || Input: v(t), Current: i(t)
                            vv

                            (N)  Electromagnetic Force: f_mag(i, y)

                           ( O ) Suspended Ball: mass m, position y(t)

                            (S)  Gravity: m * g (downward)
```

The vertical position $y(t)$ is measured downward from the electromagnet pole face. The nonlinear equation of motion for the ball and the electrical dynamics of the coil are governed by: $$m \frac{d^2 y(t)}{dt^2} = m g - k \frac{i(t)^2}{y(t)^2}$$ $$v(t) = R i(t) + L \frac{di(t)}{dt}$$

where:

- Ball mass $m = 1\text{ kg}$, acceleration due to gravity $g = 8\text{ m/s}^2$
- Electromagnetic force constant $k = 8\text{ N}\cdot\text{m}^2/\text{A}^2$
- Coil resistance $R = 2,\Omega$, coil inductance $L = 0.5\text{ H}$
- System input is the applied coil voltage $u(t) = v(t)$
- Measurable system output is the vertical position $y(t)$

---

#### Exam Questions

##### **Part (a) Physical Modelling & Equilibrium Analysis [4 marks]**

1. Show that for a desired steady-state levitation gap of $y_0 = 1\text{ m}$, the required equilibrium bias current is $i_0 = 1\text{ A}$ and the equilibrium input voltage is $v_0 = 2\text{ V}$.
2. Define the state vector $x(t) = \begin{bmatrix} x_1(t) & x_2(t) & x_3(t) \end{bmatrix}^T = \begin{bmatrix} y(t) & \dot{y}(t) & i(t) \end{bmatrix}^T$. Define small perturbation variables around the equilibrium point: $\delta x(t) = x(t) - x_0$ and $\delta u(t) = v(t) - v_0$. Derive the linearized state-space matrices $(A, B, C, D)$ governing the perturbation dynamics $\delta \dot{x} = A \delta x + B \delta u$, $\delta y = C \delta x + D \delta u$.

##### **Part (b) Stability & Transfer Function Analysis [3 marks]**

1. Determine the eigenvalues of $A$ and derive the open-loop transfer function $G(s) = \frac{\Delta Y(s)}{\Delta V(s)}$.
2. Is the open-loop linearized system internally stable? Is it bounded-input bounded-output (BIBO) stable? Explain from physical and mathematical perspectives why open-loop feedforward control cannot maintain stable levitation.

##### **Part (c) Full-State Feedback with Integral Tracking Control [5 marks]**

In the mock exam, reference tracking was implemented using a static feedforward gain $k_r$.

1. Explain why this static feedforward architecture fails when the physical mass $m$ or resistance $R$ undergoes parameter drift, or when a constant external force disturbance acts on the sphere.
2. To achieve zero steady-state error to step position commands despite parameter variations, augment the state space with an integrator: $$\dot{x}_I(t) = r(t) - \delta y(t) = r(t) - C \delta x(t)$$ Define the augmented state vector $x_e(t) = \begin{bmatrix} \delta x(t)^T & x_I(t) \end{bmatrix}^T \in \mathbb{R}^4$. Write down the augmented system matrices $A_e$ and $B_e$.
3. Design a state-feedback gain vector $K_e = \begin{bmatrix} k_1 & k_2 & k_3 & -k_I \end{bmatrix}$ such that all four closed-loop poles are placed at $s = -4$.

##### **Part (d) Luenberger State Observer Design & Separation Principle [4 marks]**

In the physical setup, only the vertical displacement $\delta y(t) = \delta x_1(t)$ is measured by an optical sensor; velocity $\delta x_2$ and coil current $\delta x_3$ are not directly measured.

1. Prove that the pair $(A, C)$ is observable.
2. Design a full-order Luenberger state observer $\dot{\hat{x}} = A \hat{x} + B \delta u + L(\delta y - C \hat{x})$ such that the observer estimation error dynamics $e_o(t) = \delta x(t) - \hat{x}(t)$ decay with a triple pole at $s = -8$.
3. State the **Separation Principle**. What are the eigenvalues of the complete 7th-order closed-loop system combining the plant, the integral controller, and the observer?

##### **Part (e) Robustness & Frequency-Domain Performance Trade-offs [4 marks]**

1. Define the **Sensitivity Function** $S(s)$ and the **peak sensitivity** $M_s = \sup_{\omega} |S(j\omega)|$. Why does $M_s$ provide a more reliable guarantee of stability margins than classical gain and phase margins?
2. The open-loop plant has an unstable pole in the right-half plane (RHP). State **Bode's Sensitivity Integral Theorem** (the "Waterbed Effect") for open-loop unstable plants. Explain the fundamental design limitation this imposes on the closed-loop system when attempting to reduce sensitivity over a wide tracking bandwidth.

##### **Part (f) Digital Microcontroller Implementation [5 marks]**

1. Compare the **Forward Euler**, **Backward Euler**, and **Bilinear (Tustin)** transform methods for discretising continuous-time compensators. Why is the Tustin transform preferred when digitising controllers with fast dynamics?
2. Using the **Backward Euler method** with sampling period $T_s$, derive the explicit difference equations that must be executed in real time on the digital signal processor / microcontroller at sample step $k$ to compute the control output $u[k]$ from the reference $r[k]$ and measured position $y[k]$.
3. State the engineering rule of thumb for selecting an appropriate sampling period $T_s$ based on the closed-loop pole locations, and recommend a specific value for this system.

---

### Complete Answer Key & Marking Guide

#### Solution to Part (a) [4 marks]

**1. Equilibrium Point Derivation [1 mark]** At steady state, all time derivatives vanish: $\ddot{y} = 0$, $\dot{y} = 0$, $\frac{di}{dt} = 0$. From the mechanical equation: $$0 = mg - k \frac{i_0^2}{y_0^2} \implies mg = k \left(\frac{i_0}{y_0}\right)^2$$ Substitute the given numerical parameters $m = 1\text{ kg}$, $g = 8\text{ m/s}^2$, $k = 8\text{ N}\cdot\text{m}^2/\text{A}^2$, and $y_0 = 1\text{ m}$: $$1 \times 8 = 8 \left(\frac{i_0}{1}\right)^2 \implies i_0^2 = 1 \implies i_0 = 1\text{ A} \quad (\text{since } i_0 > 0)$$ From the electrical equation: $$v_0 = R i_0 = 2,\Omega \times 1\text{ A} = 2\text{ V}$$ Thus, the equilibrium state and input are: $$x_0 = \begin{bmatrix} y_0 \\ \dot{y}_0 \\ i_0 \end{bmatrix} = \begin{bmatrix} 1 \ 0 \ 1 \end{bmatrix}, \quad u_0 = v_0 = 2\text{ V}$$

**2. Jacobian Linearisation [3 marks]** The nonlinear state equations $\dot{x} = f(x, u)$ are: $$f_1(x, u) = x_2$$ $$f_2(x, u) = g - \frac{k}{m} \frac{x_3^2}{x_1^2}$$ $$f_3(x, u) = -\frac{R}{L} x_3 + \frac{1}{L} u$$

Compute the partial derivatives evaluated at $(x_0, u_0)$: $$\frac{\partial f_1}{\partial x} = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}, \quad \frac{\partial f_1}{\partial u} = 0$$ $$\frac{\partial f_2}{\partial x_1} = \frac{2k x_3^2}{m x_1^3}\Bigg|_{x_0} = \frac{2(8)(1)^2}{(1)(1)^3} = 16, \quad \frac{\partial f_2}{\partial x_2} = 0$$ $$\frac{\partial f_2}{\partial x_3} = -\frac{2k x_3}{m x_1^2}\Bigg|_{x_0} = -\frac{2(8)(1)}{(1)(1)^2} = -16, \quad \frac{\partial f_2}{\partial u} = 0$$ $$\frac{\partial f_3}{\partial x_1} = 0, \quad \frac{\partial f_3}{\partial x_2} = 0, \quad \frac{\partial f_3}{\partial x_3} = -\frac{R}{L} = -\frac{2}{0.5} = -4, \quad \frac{\partial f_3}{\partial u} = \frac{1}{L} = \frac{1}{0.5} = 2$$

Since the output is vertical position $\delta y = \delta x_1$: $$C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}, \quad D = 0$$ The linearized state-space matrices are: $$A = \begin{bmatrix} 0 & 1 & 0 \ 16 & 0 & -16 \ 0 & 0 & -4 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \ 0 \ 2 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}, \quad D = 0$$

---

#### Solution to Part (b) [3 marks]

**1. Eigenvalues and Transfer Function [2 marks]** Compute the characteristic polynomial of $A$: $$\det(sI - A) = \det\begin{bmatrix} s & -1 & 0 \ -16 & s & 16 \ 0 & 0 & s + 4 \end{bmatrix} = (s + 4) \left( s^2 - 16 \right) = (s + 4)^2 (s - 4) = s^3 + 4s^2 - 16s - 64$$ The open-loop eigenvalues are: $$\lambda_1 = +4, \quad \lambda_2 = -4, \quad \lambda_3 = -4$$ To find the transfer function $G(s) = C(sI - A)^{-1} B$: $$(sI - A) X(s) = B U(s) \implies \begin{bmatrix} s & -1 & 0 \ -16 & s & 16 \ 0 & 0 & s + 4 \end{bmatrix} \begin{bmatrix} X_1(s) \ X_2(s) \ X_3(s) \end{bmatrix} = \begin{bmatrix} 0 \ 0 \ 2 \end{bmatrix} U(s)$$ From the third row: $X_3(s) = \frac{2}{s + 4} U(s)$. From the first row: $X_2(s) = s X_1(s)$. Substitute into the second row: $$-16 X_1(s) + s(s X_1(s)) + 16 X_3(s) = 0 \implies (s^2 - 16) X_1(s) = -16 X_3(s) = -\frac{32}{s + 4} U(s)$$ $$X_1(s) = \frac{-32}{(s^2 - 16)(s + 4)} U(s) = \frac{-32}{(s - 4)(s + 4)^2} U(s)$$ Because $Y(s) = X_1(s)$, the transfer function is: $$G(s) = \frac{-32}{s^3 + 4s^2 - 16s - 64}$$

**2. Stability Discussion [1 mark]**

- **Internal Stability:** The system is **internally unstable** because there is an eigenvalue $\lambda_1 = +4$ in the open right-half plane ($\text{Re}(\lambda) > 0$).
- **BIBO Stability:** The transfer function possesses an uncancelled pole at $s = +4 \in \text{ORHP}$, so the system is **not BIBO stable**.
- **Physical Failure of Feedforward:** Open-loop feedforward cannot stabilize this plant. Because the magnetic force is inversely proportional to $y^2$, an infinitesimal upward displacement increases the upward magnetic force, accelerating the ball into the magnet; an infinitesimal downward displacement decreases the magnetic force, causing the ball to fall under gravity. The mode $e^{+4t}$ diverges exponentially to infinity without feedback.

---

#### Solution to Part (c) [5 marks]

**1. Failure of Open-Loop Reference Gain $k_r$ [1 mark]** In the static state-feedback architecture $u = -K x + k_r r$, the steady-state tracking gain is derived from the model nominal matrices: $k_r = -[C(A - BK)^{-1}B]^{-1}$. This constitutes open-loop inversion. Any mismatch between the true physical plant and the model (e.g., changes in mass $m$, coil heating altering $R$, or an external wind/load disturbance $v(t)$) causes the DC gain to shift away from unity, resulting in steady-state error ($e_{ss} \neq 0$).

**2. Augmented State-Space Formulation [1 mark]** Introducing the integrator state $\dot{x}_I(t) = r(t) - C \delta x(t)$ forces $e(t) = r(t) - y(t) \to 0$ at steady state via the Internal Model Principle. The augmented state equations are: $$\begin{bmatrix} \delta \dot{x} \ \dot{x}_I \end{bmatrix} = \begin{bmatrix} A & 0_{3 \times 1} \ -C & 0 \end{bmatrix} \begin{bmatrix} \delta x \ x_I \end{bmatrix} + \begin{bmatrix} B \ 0 \end{bmatrix} \delta u + \begin{bmatrix} 0_{3 \times 1} \ 1 \end{bmatrix} r$$ $$A_e = \begin{bmatrix} 0 & 1 & 0 & 0 \ 16 & 0 & -16 & 0 \ 0 & 0 & -4 & 0 \ -1 & 0 & 0 & 0 \end{bmatrix}, \quad B_e = \begin{bmatrix} 0 \ 0 \ 2 \ 0 \end{bmatrix}$$

**3. State Feedback Gain Computation [3 marks]** The feedback law is: $$\delta u = -K \delta x + k_I x_I = -K_e x_e, \quad \text{where } K_e = \begin{bmatrix} k_1 & k_2 & k_3 & -k_I \end{bmatrix}$$ The closed-loop dynamics matrix is: $$A_e - B_e K_e = \begin{bmatrix} 0 & 1 & 0 & 0 \ 16 & 0 & -16 & 0 \ -2k_1 & -2k_2 & -4 - 2k_3 & 2k_I \ -1 & 0 & 0 & 0 \end{bmatrix}$$ Evaluate the closed-loop characteristic polynomial: $$\det(sI - (A_e - B_e K_e)) = s^4 + (2k_3 + 4)s^3 - (32k_2 + 16)s^2 - (32k_1 + 32k_3 + 64)s - 32k_I$$ The desired closed-loop polynomial with four poles at $s = -4$ is: $$\alpha_d(s) = (s + 4)^4 = s^4 + 16s^3 + 96s^2 + 256s + 256$$ Equating coefficients term-by-term:

- Coefficient of $s^3$: $$2k_3 + 4 = 16 \implies 2k_3 = 12 \implies \mathbf{k_3 = 6}$$
- Coefficient of $s^2$: $$-32k_2 - 16 = 96 \implies -32k_2 = 112 \implies \mathbf{k_2 = -3.5 = -\frac{7}{2}}$$
- Constant term ($s^0$): $$-32k_I = 256 \implies \mathbf{k_I = -8}$$
- Coefficient of $s^1$: $$-32k_1 - 32k_3 - 64 = 256 \implies -32k_1 - 32(6) - 64 = 256$$ $$-32k_1 - 256 = 256 \implies -32k_1 = 512 \implies \mathbf{k_1 = -16}$$

The feedback gain vector is: $$K_e = \begin{bmatrix} -16 & -3.5 & 6 & 8 \end{bmatrix}$$ The resulting continuous control law is: $$\delta u(t) = 16 \delta x_1(t) + 3.5 \delta x_2(t) - 6 \delta x_3(t) - 8 x_I(t)$$

---

#### Solution to Part (d) [4 marks]

**1. Observability Rank Test [1 mark]** The observability matrix $W_o$ is: $$W_o = \begin{bmatrix} C \ CA \ CA^2 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 \ 0 & 1 & 0 \ 16 & 0 & -16 \end{bmatrix}$$ $$\det(W_o) = 1 \times (1 \times (-16) - 0) = -16 \neq 0$$ Since $\text{rank}(W_o) = 3 = n$, the system is completely observable.

**2. Observer Gain Computation [2 marks]** The observer dynamics matrix is $A - LC$, where $L = \begin{bmatrix} l_1 & l_2 & l_3 \end{bmatrix}^T$: $$A - LC = \begin{bmatrix} 0 & 1 & 0 \ 16 & 0 & -16 \ 0 & 0 & -4 \end{bmatrix} - \begin{bmatrix} l_1 & 0 & 0 \ l_2 & 0 & 0 \ l_3 & 0 & 0 \end{bmatrix} = \begin{bmatrix} -l_1 & 1 & 0 \ 16 - l_2 & 0 & -16 \ -l_3 & 0 & -4 \end{bmatrix}$$ Compute $\det(sI - (A - LC))$: $$\det\begin{bmatrix} s + l_1 & -1 & 0 \ l_2 - 16 & s & 16 \ l_3 & 0 & s + 4 \end{bmatrix} = (s + l_1)s(s + 4) + (l_2 - 16)(s + 4) - 16 l_3$$ $$= s^3 + (l_1 + 4)s^2 + (4l_1 + l_2 - 16)s + (4l_2 - 16l_3 - 64)$$ The target observer characteristic polynomial with triple pole at $s = -8$ is: $$\beta_d(s) = (s + 8)^3 = s^3 + 24s^2 + 192s + 512$$ Equating coefficients:

- $s^2$ term: $$l_1 + 4 = 24 \implies \mathbf{l_1 = 20}$$
- $s^1$ term: $$4l_1 + l_2 - 16 = 192 \implies 4(20) + l_2 - 16 = 192 \implies 64 + l_2 = 192 \implies \mathbf{l_2 = 128}$$
- Constant term ($s^0$): $$4l_2 - 16l_3 - 64 = 512 \implies 4(128) - 16l_3 - 64 = 512$$ $$512 - 16l_3 - 64 = 512 \implies -16l_3 = 64 \implies \mathbf{l_3 = -4}$$

The observer gain matrix is: $$L = \begin{bmatrix} 20 \ 128 \ -4 \end{bmatrix}$$

**3. The Separation Principle & Closed-Loop Poles [1 mark]**

- **Statement:** For a linear time-invariant system, the state feedback gains $K_e$ and the observer gains $L$ can be designed completely independently. The closed-loop poles of the combined output-feedback system are the eigenvalues of $(A_e - B_e K_e)$ along with the eigenvalues of $(A - LC)$.
- **Eigenvalues:** The composite 7th-order system ($3$ plant states + $1$ integrator state + $3$ observer estimation error states) has closed-loop eigenvalues: $$\lambda_{cl} = { -4, -4, -4, -4, -8, -8, -8 }$$

---

#### Solution to Part (e) [4 marks]

**1. Sensitivity Peak $M_s$ vs. Classical Margins [2 marks]** The sensitivity function is $S(s) = \frac{1}{1 + L(s)}$, where $L(s)$ is the open-loop return ratio. The peak sensitivity is defined as: $$M_s = \sup_{\omega \ge 0} |S(j\omega)| = \frac{1}{\inf_{\omega} |1 + L(j\omega)|}$$ Geometrically, $|1 + L(j\omega)|$ is the distance from the Nyquist trajectory $L(j\omega)$ to the critical point $-1$ in the complex plane. Therefore: $$\text{Distance to }-1 = \frac{1}{M_s}$$

- Classical **Gain Margin (GM)** only tests distance to $-1$ along the negative real axis (where phase is $-180^\circ$).
- Classical **Phase Margin (PM)** only tests distance to $-1$ along the unit circle (where magnitude is $1$).
- **Why $M_s$ is superior:** A system can have high GM and PM while the Nyquist curve passes dangerously close to $-1$ at an intermediate angle. The metric $M_s$ accounts for simultaneous magnitude and phase uncertainties: $$GM \ge \frac{M_s}{M_s - 1}, \quad PM \ge 2 \arcsin\left(\frac{1}{2M_s}\right)$$

**2. Bode's Sensitivity Integral & The Waterbed Effect [2 marks]** For an open-loop plant with relative degree $\ge 2$ and open-loop unstable poles $p_k \in \text{ORHP}$, Bode's Sensitivity Integral states: $$\int_{0}^{\infty} \ln |S(j\omega)| , d\omega = \pi \sum_{k} \text{Re}(p_k)$$ For this MagLev plant, there is an open-loop unstable pole at $p_1 = +4$: $$\int_{0}^{\infty} \ln |S(j\omega)| , d\omega = 4\pi > 0$$

- **Fundamental Limitation:** To achieve accurate tracking and disturbance rejection over the control bandwidth $[0, \omega_B]$, we require $|S(j\omega)| < 1$, which makes $\ln |S(j\omega)| < 0$ (a sensitivity "valley").
- Because the total area under $\ln |S(j\omega)|$ across all frequencies is fixed to $+4\pi$, pressing down sensitivity at low frequencies forces a severe amplification $|S(j\omega)| > 1$ ($\ln |S| > 0$) at higher frequencies (a sensitivity "peak").
- This fundamental trade-off means that improving tracking performance inevitably worsens high-frequency noise amplification and reduces robustness margins.

---

#### Solution to Part (f) [5 marks]

**1. Comparison of Discretisation Operators [1 mark]**

- **Forward Euler ($s \approx \frac{z - 1}{T_s}$):** Maps the open left-half $s$-plane into a circle of radius $\frac{1}{T_s}$ centered at $z = 1 - \frac{1}{T_s}$. Stable continuous poles with large negative real parts (such as the observer poles at $-8$) will map outside the unit disk $|z| > 1$ if $T_s > \frac{2}{|\text{pole}|}$, making the discrete implementation unstable.
- **Backward Euler ($s \approx \frac{1 - z^{-1}}{T_s}$):** Maps the open left-half $s$-plane into the interior of a circle inside the unit disk. Stability is always preserved, but it adds artificial numerical damping.
- **Bilinear / Tustin Transform ($s \approx \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}}$):** A conformal mapping that maps the entire open left-half $s$-plane directly onto the open unit disk in the $z$-plane ($|z| < 1$). It unconditionally preserves continuous-time stability without adding artificial damping, making it the preferred method for digital controllers.

**2. Microcontroller Real-Time Difference Equations [3 marks]** Using Backward Euler ($s \to \frac{1 - z^{-1}}{T_s}$):

1. **Integrator update:** $$\frac{x_I[k] - x_I[k-1]}{T_s} = r[k] - y[k] \implies \mathbf{x_I[k] = x_I[k-1] + T_s \left( r[k] - y[k] \right)}$$
2. **Observer state estimation:** $$\hat{x}[k] = \hat{x}[k-1] + T_s \left[ (A - LC) \hat{x}[k-1] + B \delta u[k-1] + L y[k-1] \right]$$ Substituting the matrices from Parts (a), (c), and (d): $$(A - LC) = \begin{bmatrix} -20 & 1 & 0 \ -112 & 0 & -16 \ 4 & 0 & -4 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \ 0 \ 2 \end{bmatrix}, \quad L = \begin{bmatrix} 20 \ 128 \ -4 \end{bmatrix}$$ Expanding into scalar update equations: $$\mathbf{\hat{x}_1[k] = \hat{x}_1[k-1] + T_s \left( -20 \hat{x}_1[k-1] + \hat{x}_2[k-1] + 20 y[k-1] \right)}$$ $$\mathbf{\hat{x}_2[k] = \hat{x}_2[k-1] + T_s \left( -112 \hat{x}_1[k-1] - 16 \hat{x}_3[k-1] + 128 y[k-1] \right)}$$ $$\mathbf{\hat{x}_3[k] = \hat{x}_3[k-1] + T_s \left( 4 \hat{x}_1[k-1] - 4 \hat{x}_3[k-1] + 2 \delta u[k-1] - 4 y[k-1] \right)}$$
3. **Control output computation:** $$\delta u[k] = 16 \hat{x}_1[k] + 3.5 \hat{x}_2[k] - 6 \hat{x}_3[k] - 8 x_I[k]$$ $$u_{total}[k] = v_0 + \delta u[k] = \mathbf{2 + 16 \hat{x}_1[k] + 3.5 \hat{x}_2[k] - 6 \hat{x}_3[k] - 8 x_I[k]}$$

**3. Sampling Period Selection [1 mark]**

- **Rule of Thumb:** To avoid excessive digital phase lag and sampling-induced destabilization, the sampling frequency $\omega_s = \frac{2\pi}{T_s}$ should be selected between $20$ and $40$ times higher than the highest bandwidth or pole magnitude of the closed-loop system: $$\omega_s \ge 20 \times \max_i |\lambda_i| \implies T_s \le \frac{2\pi}{20 \times |\lambda_{max}|} \approx \frac{1}{3 \times |\lambda_{max}|}$$
- For this closed-loop system, the fastest poles are the observer poles at $|\lambda| = 8\text{ rad/s}$. $$T_s \le \frac{2\pi}{20 \times 8} \approx 0.039\text{ s}$$
- **Recommendation:** Select $\mathbf{T_s = 0.01\text{ s}}$ ($10\text{ ms}$, corresponding to a sampling rate of $100\text{ Hz}$). This is well within the capability of standard microcontrollers (e.g., STM32, ARM Cortex-M) and ensures that continuous-time design assumptions remain valid.

---

### Key Formulas & Verification Summary

| Component                     | Continuous System                        | Synthesized Value / Characteristic                   |
| :---------------------------- | :--------------------------------------- | :--------------------------------------------------- |
| **Equilibrium**               | $(y_0, \dot{y}_0, i_0, v_0)$             | $(1\text{ m}, 0\text{ m/s}, 1\text{ A}, 2\text{ V})$ |
| **Open-Loop Poles**           | $\det(sI - A) = 0$                       | $s = +4\text{ (unstable)}, -4, -4$                   |
| **Plant Transfer Function**   | $G(s) = \frac{\Delta Y(s)}{\Delta V(s)}$ | $\frac{-32}{(s - 4)(s + 4)^2}$                       |
| **Controller Gains**          | $K_e = [k_1, k_2, k_3, -k_I]$            | $[-16, -3.5, 6, 8]$ (Closed-loop poles at $-4$)      |
| **Observer Gains**            | $L = [l_1, l_2, l_3]^T$                  | $[20, 128, -4]^T$ (Observer poles at $-8$)           |
| **Bode Sensitivity Integral** | $\int_0^\infty \ln \|S(j\omega)\|$       |                                                      |
| **Sampling Interval**         | $T_s$                                    | $0.01\text{ s}$ ($100\text{ Hz}$)                    |

Would you like to step through the numerical root locus for this closed-loop system, or explore an alternative multi-variable design using the Linear Quadratic Regulator (LQR) and Kalman Filter from Week 7?