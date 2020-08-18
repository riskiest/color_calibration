## RGB Color Spaces

The RGB color space is a color space defined by three primary colors, and a color in the RGB color space is expressed as the mixing ratio of the three primary colors. If the primary colors are not defined in the absolute color space, the RGB color space is the relative color space. Otherwise, the RGB color space becomes the absolute color space. For example, for a camera that without color correction, the generated RGB image is relative color space, and color values in the image is related to a photosensitive system of the camera. The purpose of color correction is to establish the relationship between the relative color space and the absolute color space. Unless otherwise specified, the color spaces described below are absolute color spaces.

There are many kinds of RGB color spaces, including sRGB, Adobe RGB, etc. The main differences are the definition of primary colors and linearization. 

### Definition of Primaries

When defining the color space, first select the illuminant and the observer (IO) and constructed CIE XYZ color space for the IO. Then select the three primary colors from chromaticity diagram, ignoring the brightness component. After selecting the white point, the observer, and the three primary colors, the linear RGB space is defined.

Some definitions of the primary colors in the RGB color space are as follows[1-9], observers are all the CIE 1931 2° Standard Observer, and therefore not included in this table: 

|                | White Point | xR       | yR       | xG       | yG       | xB       | yB       |
| -------------- | ----------- | -------- | -------- | -------- | -------- | -------- | -------- |
| sRGB           | D65         | 0.64     | 0.33     | 0.30     | 0.60     | 0.15     | 0.06     |
| Adobe RGB      | D65         | 0.64     | 0.33     | 0.21     | 0.71     | 0.15     | 0.06     |
| Wide Gamut RGB | D50         | 0.7347   | 0.2653   | 0.1152   | 0.8264   | 0.1566   | 0.0177   |
| ProPhoto RGB   | D50         | 0.734699 | 0.265301 | 0.159597 | 0.840403 | 0.036598 | 0.000105 |
| DCI P3         | D65         | 0.68     | 0.32     | 0.265    | 0.69     | 0.15     | 0.06     |
| Apple RGB      | D65         | 0.625    | 0.34     | 0.28     | 0.595    | 0.155    | 0.07     |
| REC. 709       | D65         | 0.64     | 0.33     | 0.30     | 0.60     | 0.15     | 0.06     |
| REC. 2020      | D65         | 0.708    | 0.292    | 0.17     | 0.797    | 0.131    | 0.046    |

On the chromaticity diagram, the triangle formed by the three primary colors covers all the colors obtained by combining the three origins, which is called as **gamut**. Since the primaries have been previously defined on the chromaticity diagram, the gamut of RGB color spaces can be drawn on the chromaticity diagram[1]. 

sRGB is the most common color space for computer displays, but the gamut is limited. The gamut of the color space such as Adobe RGB and Wide Gamut RGB is much larger. 

![File:CIE1931xy gamut comparison.svg](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/CIE1931xy_gamut_comparison.svg/512px-CIE1931xy_gamut_comparison.svg.png)

### Linearization and Delinearization

After selecting the white point, the observer, and the three primary colors, the linear RGB space is defined. The color values of the linear RGB color space are proportional to the luminance but not brightness. The human perception of brightness is nonlinear and follows an approximate power function with greater sensitivity to relative differences between darker tones than between lighter tones. Therefore, it is necessary to use **gamma correction** on the linear color space to conform to the human visual perception.

Gamma correction is defined by the following power law expression: 

$$
V_{out} = AV_{in}^{\gamma}
$$

Since the light intensity in early CRT display varies nonlinearly with the electron-gun voltage, gamma correction is not only used to compensate for the nonlinearity of CRT, but also to conform to the human visual perception. Even with the current changes in display equipment, the standard for gamma corrections has been set. Currently, the decoding gamma value of most RGB color spaces is 2.2. That is, the relationship between the linear RGB color space and the nonlinear RGB color space which is more close to human perception of brightness is as follows: 

$$
C_n=C_l^{1/\gamma},\quad \gamma=2.2
$$

where $C_l,C_n$ represents the color channels of linear and nonlinear RGB color space respectively. 

During the color correction process, the color values may exceed [0, 1]. To avoid producing non-real values, a symmetry transformation is made to the gamma corrected images about the origin, so there are

conversion from nonlinear RGB space to linear RGB space: 
$$
C_l=C_n^{\gamma},\qquad C_n\ge0\\
C_l=-(-C_n)^{\gamma},\qquad C_n<0\\\\
$$
and conversion from linear RGB space to nonlinear RGB space: 
$$
C_n=C_l^{1/\gamma},\qquad C_l\ge0\\
C_n=-(-C_l)^{1/\gamma},\qquad C_l<0\\\\
$$
the value of $\gamma$ in the above formula is relative to which space it belongs to. Generally,  the value is 2.2.

When converting the linear RGB space into the nonlinear RGB space, the derivative near the origin approaches infinity. Therefore, for convenience of mathematical calculation, some RGB color spaces (such as sRGB and REC.709) are replacing the curve by a straight line in a small range near the origin. The connection between the straight line segment and the power function segment is continuous and differentiable. 

To ensure the color values is mapped from $[0, 1]$ to $[0, 1]$ during the linearization, the segmental function is generally provided as follows: 
$$
C_l=C_n/\phi,\qquad 0\le C_n\le K_0\\
C_l=(\frac{C_n+a}{1+a})^{\gamma},\qquad C_n>K_0\\\\
$$
In order to maintain the continuity and differentiability of the function, the function value, at $K_0$, is continuous and the left and right derivatives are equal:  
$$
(\frac{K_0+a}{1+a})^{\gamma}=\frac{K_0}{\phi}\\
\gamma(\frac{K_0+a}{1+a})^{\gamma-1}=\frac{1}{\phi}
$$
which means that there is only one independent quantity in $K_0$, $a$, $\phi$. 

Generally, $a$ is used to represents other quantity: 
$$
K_0=\frac{a}{\gamma-1}\\
\phi=\frac{(1+a)^\gamma(\gamma-1)^{\gamma-1}}{a^{\gamma-1}\gamma^{\gamma}}
$$
In addition, the following variables are usually introduced to simplify the expression of delinearization functions:
$$
\alpha=a+1\\
\beta=K_0/\phi
$$
Then the conversion from linear RGB to nonlinear is as follows:
$$
C_n=\phi C_l,\qquad 0\le C_n\le \beta\\
C_l=\alpha C_l^{1/\gamma}-a,\qquad C_n>\beta\\
$$

The following figure shows the transformation curve of sRGB linearization. The red line is the linearization function, the blue is the derivative function, and the black dotted line below the red line is the gamma correction curve when $\gamma = 2.2 $. Since the value near the origin is replaced by a straight line, the power function part of the curve will move down. In order to approximate the pure gamma correction curve with $\gamma=2.2$, the actual $\gamma$ value of sRGB is 2.4. In addition, due to truncation errors, the actual sRGB conversion function might be discontinuous around $K_0$.

![File:SRGB gamma.svg](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/SRGB_gamma.svg/512px-SRGB_gamma.svg.png)

During the color correction process, the color values may exceed [0, 1]. To avoid producing non-real values, a symmetry transformation is made to the (de)linearized function images about the origin.

Some common RGB color space linearization parameters are as follows: 

|                | $\gamma$ | $a$    |
| -------------- | -------- | ------ |
| sRGB           | 2.4      | 0.055  |
| Adobe RGB      | 2.2      | /      |
| Wide Gamut RGB | 2.2      | /      |
| ProPhoto RGB   | 1.8      | /      |
| DCI P3         | 2.6      | /      |
| Apple RGB      | 1.8      | /      |
| REC. 709       | 1/0.45   | 0.099  |
| REC. 2020      | 1/0.45   | 0.0993 |

## Conversion of RGB Color Space

The RGB color space needs to be converted into the CIE lab color space during fitting. The following figure uses sRGB and ProPhoto RGB as examples to show the process of color space conversion. The green arrow represents linear transformation, and the blue indicates non-linear transformation. The color space represented by green box is linear to luminance.

During the whole fitting process, all data values of RGB color spaces should be normalized, that is, in [0, 1].  

![image-20200708154138215](色彩空间.assets/image-20200708154138215.png)

### Conversion from Linear RGB CS to XYZ CS with IO unchanged

The conversion from the Linear RGB color space to CIE XYZ color space with IO unchanged can be done by linear transformation:
$$
\begin{bmatrix}X\\ Y\\ Z\end{bmatrix}=M_{RGBL2XYZ}\begin{bmatrix}R_l\\ G_l\\ B_l\end{bmatrix}
$$
The conversion matrix can be calculated from the xyY values of the three primary colors and the white point[11].

xyY colors needs to be converted into XYZ colors by the formulas[12]:
$$
X=\frac{xY}{y}\\
Y=Y\\
Z=\frac{(1-x-y)Y}{y}
$$

### Chromatic Adaptation

Sometimes the IO value of RGB color space is different from the CIE lab color space, so the conversion between XYZ color space with different IO values is needed, also known as **color adaptation** [18]. Since color is a non-single mapping of the reflection function of each wavelength to the tristimulus value, this means that the same colors under one illuminant may be different under another. Therefore, correct color adaptation is impossible. Usually, linear transformation is used to approximate color adaptation.

This conversion process  needs to convert the white point from XYZ color space into the cone response space (CRD), $(\rho,\gamma,\beta)$, there are[13]:
$$
\begin{bmatrix}\rho\\ \gamma\\ \beta\end{bmatrix}=M_{XYZ2CRD}\begin{bmatrix}X_w\\ Y_w\\ Z_w\end{bmatrix}
$$
where $M_{XYZ2CRD}$ can select from identity matrix, Bradford matrix and Von Kries matrix. The Bradford matrix is selected by default.

Color adaptation can ultimately be expressed as:
$$
\begin{bmatrix}X_d\\ Y_d\\ Z_d\end{bmatrix}=M_{XYZ2XYZ}\begin{bmatrix}X_s\\ Y_s\\ Z_s\end{bmatrix}
$$
where subscript s is the source XYZ color space, and subscript d is the target XYZ color space, and
$$
M_{XYZ2XYZ}=M_{XYZ2CRD}^{-1}\begin{bmatrix}
\rho_d/\rho_s & 0 & 0\\ 
 0& \gamma_d/\gamma_s & 0\\ 
0 & 0 & \beta_d/\beta_s
\end{bmatrix}M_{XYZ2CRD}
$$
where  $(\rho_s,\gamma_s,\beta_s)$ and $(\rho_d,\gamma_d,\beta_d)$ are the CRD values of the source white point and the target white point, respectively.

### Conversion from Linear RGB CS to XYZ CS

Therefore, the conversion from linear RGB color space to XYZ color space with IO changed or unchanged may be expressed as:
$$
\begin{bmatrix}X'\\ Y'\\ Z'\end{bmatrix}=M_{XYZ2XYZ'}M_{RGBL2XYZ}\begin{bmatrix}R_l\\ G_l\\ B_l\end{bmatrix}
$$
When the program is implemented, multiple colors are usually calculated at one time, and the color channel is used as the last order. If the input is a list of colors, the conversion can be expressed as:
$$
\begin{bmatrix}
X_1' & Y_1' & Z_1'\\ 
 X_2'& Y_2' & Z_2'\\ 
... & ... & ...
\end{bmatrix}
=
\begin{bmatrix}
R_{l1} & G_{l1} & B_{l1}\\ 
R_{l2} & G_{l2} & B_{l2}\\ 
... & ... & ...
\end{bmatrix}
\times 
(M_{XYZ2XYZ'}M_{RGBL2XYZ})^T
$$
In the above formula, the multiplication symbol is purposely not omitted. This multiplication is the same as the matrix multiplication, and could be implemented by using the numpy.dot, numpy.matmul or the symbol @ in numpy. 

If the input is a multi-level tensor (for example, an image can be view as a third-order tensor of w×h×3), it can be expressed as:
$$
T_{XYZ'}
=
T_{RGBL}
\times 
(M_{XYZ2XYZ}M_{RGBL2XYZ})^T
$$

Here, the multiplication is extended matrix multiplication, and may still be implemented by using the numpy.dot, numpy.matmul or the symbol @.  In this case, the results of numpy.dot and numpy.matmul are consistent.
### Conversion from XYZ CS to Linear RGB CS

To convert XYZ space into linear RGB space, we only need to multiply the inverse of the conversion matrix.

### Conversion from an RGB CS to another RGB CS

After the RGB space is converted into XYZ space, it is then converted from XYZ space to other RGB spaces. All linear RGB color spaces are differ by one linear transformation:
$$
T_{RGBL}'
=
T_{RGBL}
\times 
(M_{RGBL2RGBL'})^T
$$
where 
$$
M_{RGBL2RGBL'}
= 
(M_{XYZ'2RGBL'}M_{XYZ2XYZ'}M_{RGBL2XYZ})^T
$$
### Conversion Between RGB CS and CIE lab CS

The conversion between RGB color space and CIE lab color space can be realized through XYZ color space. The conversion between XYZ and CIE lab space can be seen here [14-15] for details.


## References

1. https://en.wikipedia.org/wiki/RGB_color_space
2. https://en.wikipedia.org/wiki/SRGB
3. https://en.wikipedia.org/wiki/Adobe_RGB_color_space
4. https://en.wikipedia.org/wiki/Wide-gamut_RGB_color_space
5. https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
6. https://en.wikipedia.org/wiki/DCI-P3
7. https://en.wikipedia.org/wiki/Rec._709
8. https://en.wikipedia.org/wiki/Rec._2020
9. http://www.brucelindbloom.com/WorkingSpaceInfo.html
10. https://en.wikipedia.org/wiki/Gamma_correction
11. http://www.brucelindbloom.com/Eqn_RGB_XYZ_Matrix.html
12. http://www.brucelindbloom.com/Eqn_xyY_to_XYZ.html
13. http://www.brucelindbloom.com/Eqn_ChromAdapt.html
14. http://www.brucelindbloom.com/Eqn_XYZ_to_Lab.html
15. http://www.brucelindbloom.com/Eqn_Lab_to_XYZ.html