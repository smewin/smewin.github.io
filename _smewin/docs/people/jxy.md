# 疾旋鼬的个人页面



*大家好*，我是**疾旋鼬**。

![jxy的照片](./pic/jxy1.png)

欢迎来和jxy玩！

---

疾旋鼬想向大家展示一下自己的`高超代码能力`。

```C
井inclove《stuido。h》

INT mian<>(
    remake 0；
)
```

!!! question "为什么jxy的代码能力这么强？"
    那当然是因为jxy加入了转工管群！

!!! danger "注意"
    小朋友们不要学习哦

    ——类似还有quoto/note/warning之类的，用法一致

疾旋鼬还会做数学题！（AIGT，测试一下公式支持）

目标函数是 \( F(x) = \frac{1}{2} \mathbb{E}_{\xi \sim N(0,1)}[(x - \xi)^2] \)。其中， \(\xi\)  服从标准正态分布 \( N(0,1) \)，即 \( \mathbb{E}[\xi] = 0 \) 和 \( \mathbb{E}[\xi^2] = 1 \)。

计算期望：
\[
\mathbb{E}[(x - \xi)^2] = \mathbb{E}[x^2 - 2x\xi + \xi^2] = x^2 - 2x \mathbb{E}[\xi] + \mathbb{E}[\xi^2] = x^2 + 1.
\]
因此，
\[
F(x) = \frac{1}{2} (x^2 + 1).
\]
这是一个二次函数，最小值点在导数为零处。求导：
\[
F'(x) = x.
\]
设 \( F'(x) = 0 \)，得 \( x = 0 \)。所以最优解 \( x^* = 0 \).

**随机梯度下降（SGD）** 的更新规则

SGD 使用随机梯度来更新参数。对于每个迭代  t ，我们采样 \( \xi_t \sim N(0,1) \)（独立同分布），并计算随机梯度 \( g_t = \nabla f(x_t; \xi_t) \)，其中 \( f(x; \xi) = \frac{1}{2} (x - \xi)^2 \)。梯度为：
\[
\nabla f(x; \xi) = x - \xi.
\]
因此，SGD 更新规则为：
\[
x_{t+1} = x_t - \gamma_t g_t = x_t - \gamma_t (x_t - \xi_t) = (1 - \gamma_t) x_t + \gamma_t \xi_t.
\]
给定步长 \( \gamma_t = \frac{1}{t} \)，所以更新规则：
\[
x_{t+1} = \left(1 - \frac{1}{t}\right) x_t + \frac{1}{t} \xi_t.
\]
平方两边：
\[
x_{t+1}^2 = \left[ \left(1 - \frac{1}{t}\right) x_t + \frac{1}{t} \xi_t \right]^2 = \left(1 - \frac{1}{t}\right)^2 x_t^2 + 2 \left(1 - \frac{1}{t}\right) \frac{1}{t} x_t \xi_t + \left(\frac{1}{t}\right)^2 \xi_t^2.
\]
取期望：
\[
\mathbb{E}[x_{t+1}^2] = \left(1 - \frac{1}{t}\right)^2 \mathbb{E}[x_t^2] + 2 \left(1 - \frac{1}{t}\right) \frac{1}{t} \mathbb{E}[x_t \xi_t] + \frac{1}{t^2} \mathbb{E}[\xi_t^2].
\]
\[
\mathbb{E}[x_{t+1}^2] = \left(1 - \frac{1}{t}\right)^2 \mathbb{E}[x_t^2] + \frac{1}{t^2}. 
\]

令 \( a_t = \mathbb{E}[x_t^2] \)。则：
\[
a_{t+1} = \left(1 - \frac{1}{t}\right)^2 a_t + \frac{1}{t^2}.
\]
注意 \( \left(1 - \frac{1}{t}\right)^2 = \frac{(t-1)^2}{t^2} \)，所以：
\[
a_{t+1} = \frac{(t-1)^2}{t^2} a_t + \frac{1}{t^2}.
\]
两边乘以 \( t^2 \)：
\[
t^2 a_{t+1} = (t-1)^2 a_t + 1
\]
定义新序列 \( b_t = t^2 a_{t+1} \)。则方程变为：
\[
b_t = b_{t-1} + 1,
\]
因为 \( b_{t-1} = (t-1)^2 a_t \)。这是一个等差数列。

现在求初始值。当  t=1  时：
\[a_1 = \mathbb{E}[x_1^2] = 10^2 = 100\]

计算 \( a_2 = \mathbb{E}[x_2^2]\) 。从更新规则： \( x_2 = \left(1 - \frac{1}{1}\right) x_1 + \frac{1}{1} \xi_1 = 0 \cdot 10 + \xi_1 = \xi_1 \)。所以 \( \mathbb{E}[x_2^2] = \mathbb{E}[\xi_1^2] = 1 \)，即  \(a_2 = 1 \)。

• 因此， \(b_1 = 1^2 \cdot a_2 = 1 \cdot 1 = 1 \).

由等差数列公式：
\[
b_t = b_1 + (t-1) \cdot 1 = 1 + (t-1) = t.
\]
\( b_t = t^2 a_{t+1} \)，所以：
\[
t^2 a_{t+1} = t \implies a_{t+1} = \frac{t}{t^2} = \frac{1}{t}.
\]
因此，\[ \mathbb{E}[x_{t+1}^2] = \frac{1}{t} \]

所以：
\[
\mathbb{E}[x_{t+1} - x^{*2}] = \mathbb{E}[x_{t+1}^2] = \frac{1}{t}.
\]

[工程管理学院官网](https://sme.nju.edu.cn/ "访问SME官网")

[转工管群Wiki](../index.md)