## CCM Matrix

CCM matrix is usually used as an approximation for the transformation from linearized input color space to linear absolute color space during color correction. 

The shape of the CCM matrix is usually $3\times3$ or $4\times3$[1-2]. The former performs linear transformation on the value of color, while the latter performs affine transformation. In other words. The color space keeps the origin unchanged after linear transformation, while the latter will be translated. It can be seen that the transform set of the CCM matrix of $3\times3$ is the proper subset of $4\times3$, which means that the solution set fitted by the $4\times3$ CCM matrix is larger. However, the latest papers prefer to use the CCM matrix of $3\times3$ instead of the latter.

### $3\times3$ CCM matrix

#### Used for Fitting and Inference

The input may be <font color=red>a list of colors</font> at fitting while an image at inference, so let's take a simple two-dimensional matrix as an example. Assume that the linearized color space of the input is: 
$$
S_l=
\begin{bmatrix}
R_{l1} & G_{l1} & B_{l1}\\ 
R_{l2} & G_{l2} & B_{l2}\\ 
... & ... & ...
\end{bmatrix}
$$
The linearized absolute color space of the output is: 
$$
D_l=
\begin{bmatrix}
R_{l1}' & G_{l1}' & B_{l1}'\\ 
R_{l2}' & G_{l2}' & B_{l2}'\\ 
... & ... & ...
\end{bmatrix}
$$
Then we have:
$$
D_l=S_l\times M_{CCM}
$$
the multiplication symbol is shown in the above formula. This multiplication is the same as the matrix multiplication, and could be implemented by using the numpy.dot, numpy.matmul or the symbol @ in numpy. In addition, the CCM matrix in the preceding formula is as follows:  
$$
M_{CCM}=
\begin{bmatrix}
a_{11} & a_{12} & a_{13}\\ 
a_{21} & a_{22} & a_{23}\\ 
a_{31} & a_{32} & a_{33}\\
\end{bmatrix}
$$
If the input is a multi-order tensor, it could be  expressed as: 
$$
T_{D}
=
T_{S}
\times 
M_{CCM}
$$
Here, the multiplication is extended matrix multiplication, and may still be implemented by using the numpy.dot, numpy.matmul or the symbol @.  The result of the numpy.dot is the same as numpy.matmul.

#### Initial Value

The program provides two methods. 

One is white balance method[1]. The initial value is: 
$$
M_{CCM}=
\begin{bmatrix}
k_R & 0 & 0\\ 
0 & k_G & 0\\ 
0 & 0 & k_B\\
\end{bmatrix}
$$
where
$$
k_R=mean(R_{li}')/mean(R_{li})\\
k_R=mean(G_{li}')/mean(G_{li})\\
k_R=mean(B_{li}')/mean(B_{li})
$$
The second is a least square method. That is an optimal solution obtained <font color=red>after using a linear RGB distance function.</font> The initial value is: 
$$
M_{CCM}=(S_l^TS_l)^{-1}S_l^TD_l
$$
This could be implemented by numpy.linalg.lstsq in numpy, which can be simply expressed as follows: 
$$
M_{CCM}=ls(S_l,D_l)
$$
If there is a weight: 
$$
w=[w_1, w_2, ...]
$$
Remark: 
$$
W=
\begin{bmatrix}
\sqrt{w_1} & 0 & ...\\ 
0 & \sqrt{w_2} & ...\\ 
... & ... & ...\\
\end{bmatrix}
$$
Then we have: 
$$
M_{CCM}=ls(W\times S_l,W\times D_l)
$$

#### Inverse

During model evaluation, the original image before the color is multiplied by the CCM will be  obtained. For a 3x3 matrix, the inverse of matrix is directly used to calculate the original image if the inverse exists.
$$
S_l=D_lM_{CCM}^{-1}
$$


### $4\times3$ CCM matrix

#### Used for Fitting and Inference

$4 \times 3$ CCM matrix can be expressed as:
$$
M_{CCM}=
\begin{bmatrix}
a_{11} & a_{12} & a_{13}\\ 
a_{21} & a_{22} & a_{23}\\ 
a_{31} & a_{32} & a_{33}\\
a_{41} & a_{42} & a_{43}\\
\end{bmatrix}
$$
Remark:
$$
S_l^+=
\begin{bmatrix}
S_l & 1_{col}\\ 
\end{bmatrix}
=
\begin{bmatrix}
R_{l1} & G_{l1} & B_{l1} & 1\\ 
R_{l2} & G_{l2} & B_{l2} & 1\\ 
... & ... & ... & ...
\end{bmatrix}
$$
Then we have:
$$
D_l=S_l^+\times M_{CCM}
$$
For multi-order tensors: 
$$
T_{D}
=
T_{S}^+
\times 
M_{CCM}
$$

#### Initial Value

The program provides two methods. 

One is white balance method[1]. The initial value is: 
$$
M_{CCM}=
\begin{bmatrix}
k_R & 0 & 0\\ 
0 & k_G & 0\\ 
0 & 0 & k_B\\
0 & 0 & 0\\
\end{bmatrix}
$$
where
$$
k_R=mean(R_{li}')/mean(R_{li})\\
k_R=mean(G_{li}')/mean(G_{li})\\
k_R=mean(B_{li}')/mean(B_{li})
$$
The second is a least square method. That is an optimal solution obtained <font color=red>after using a linear RGB distance function.</font> The initial value is:
$$
M_{CCM}=(S_l^{+T}S_l^+)^{-1}S_l^{+T}D_l
$$

This coule be implemened by numpy.linalg.lstsq in numpy, which can be simply expressed as follows: 
$$
M_{CCM}=ls(S_l^+,D_l)
$$
If there is a weight: 
$$
w=[w_1, w_2, ...] 
$$
Remark: 
$$
W=
\begin{bmatrix}
\sqrt{w_1} & 0 & ...\\ 
0 & \sqrt{w_2} & ...\\ 
... & ... & ...\\
\end{bmatrix}
$$
Then we have: 
$$
M_{CCM}=ls(W\times S_l^+,W\times D_l)
$$

#### Inverse
During model evaluation, the original image before the color is multiplied by the CCM will be  obtained. Because:
$$
D_l=S_l^+ M_{CCM}=
\begin{bmatrix}
S_l & 1_{col}\\ 
\end{bmatrix}
\begin{bmatrix}
Up_{(3,3)}\\ 
Down_{(1,3)}\\
\end{bmatrix}
=S_lUp_{(3,3)}+
1_{col}Down_{(1,3)}
$$
Therefore: 
$$
S_l=(D_l-1_{col}Down_{(1,3)})Up_{(3,3)}^{-1}
$$
It can also be equivalently expressed as: 
$$
S_l=
\begin{bmatrix}
D_l & 1_{col}\\ 
\end{bmatrix}
\begin{bmatrix}
Up_{(3,3)}^{-1}\\ 
-Down_{(1,3)}Up_{(3,3)}^{-1}\\ 
\end{bmatrix}
$$


## References

1. https://www.imatest.com/docs/colormatrix/
2. http://www.its.bldrdoc.gov/pub/ntia-rpt/04-406/
