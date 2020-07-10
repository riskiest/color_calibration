## Definition of RGB Color Space

The RGB color space is a color space of three primary colors, and a color in the RGB color space is defined by components of the three primary colors. If the colors of the primary colors are not defined, the RGB color space is the relative color space. However, when the RGB primary colors red, green, and blue are defined in the absolute color space, the RGB color space becomes the absolute color space. For example, for a camera that without  color correction, the generated RGB image is relative color space, and data of the RGB three components of the color in the image is related to a photosensitive system of the camera. The purpose of color correction is to establish the relationship between the relative color space and the absolute color space. 

The RGB color space is a series of color spaces. The following mainly describe the absolute color space, including sRGB and Adobe RGB. The main differences between these absolute color spaces are the definition of the three primary colors and the criteria for linearization. 

### Definition of Three Primary Colors

The red, green, and blue primary colors of the RGB space are defined in the CIE xyY color space. The red color of the sRGB is defined in the position where x = 0.64 and y = 0.33. Although the chromaticity  is defined, if the <font color=red>illumination where chromaticity diagram located is not defined</font>, the three  primary colors cannot be defined absolutely. The RGB space uses the standard illumination to define white points to determine the position of the primary colors in the absolute color space.

Some definitions of the primary colors in the RGB color space are as follows[1-9]: 

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


The triangle formed by three origins covers all the colors obtained by combining the three origins, which is also called the **color gamut**.<font color=red> Therefore, the position of the three origins of the RGB image on the color gamut map was previously defined, and the color gamut of each RGB space map can be drawn on the color gamut map [1].</font>

sRGB is the most common color space for computer displays, but the color gamut is limited. The color gamut of the color space such as Adobe RGB and Wide Gamut RGB is much larger. 

![图片](https://uploader.shimo.im/f/Iwf7cGpRPoAY8SUn!thumbnail)

### Linearization and Delinearization

By defining the three primary colors and white dots, the linearized RGB color space is determined. At this time, the color space is proportional to the color component value and illumination, but does not <font color=red>conform </font>the human visual perception. Human perception of brightness is nonlinear and follows an approximate power function, which is more sensitive to the relative difference between darker tones than to the relative difference between bright tones. Therefore, it is usually necessary to use the **gamma correction** for color space to <font color=red>conform </font>to the human visual perception. 

Gamma correction is defined by the following power law expression: 

$$
V_{out} = AV_{in}^{\gamma}
$$

Since the intensity of light in early display devices cathode ray tube(CRT)  changes nonlinearly with the voltage of the electron gun. So gamma correction is not only used to compensate for the nonlinearity of CRT, but also to correct the human visual perception. Even with the current changes in display equipment, the standard for gamma corrections has been set. Currently, the decoding gamma value of most RGB color spaces is 2.2. That is, the relationship between the linear RGB color space and the nonlinear RGB color space which is suitable for human eye luminance perception is as follows: 

$$
C_n=C_l^{1/\gamma},\quad \gamma=2.2
$$

where $C_l,C_n$ represents the color channels of linear and nonlinear RGB color space respectively. 

During the process of color conversion, the calculated value may exceed [0, 1]. To avoid calculation bugs, we make a symmetry transformation to the gamma corrected image about the origin, or:

Conversion from nonlinear RGB space to linear RGB space: 
$$
C_l=C_n^{\gamma},\qquad C_n\ge0\\
C_l=-(-C_n)^{\gamma},\qquad C_n<0\\\\
$$
Conversion from linear RGB space to nonlinear RGB space: 
$$
C_n=C_l^{1/\gamma},\qquad C_l\ge0\\
C_n=-(-C_l)^{1/\gamma},\qquad C_l<0\\\\
$$
the value of $\gamma$ in the above formula is relative to which space it belongs to. Generally,  the value is 2.2.

In the formula for converting the linear RGB space into the nonlinear RGB space, a derivative near the origin approaches infinity. Therefore, for convenience of mathematical calculation, a part of color space (such as sRGB and REC.709) is replaced with a straight line in a certain range near the origin, the connection point between the straight line segment and the power function segment is continuous and differentiable. 

To ensure that the color space of a single channel before and after correction is mapped from $[0, 1]$ to $[0, 1]$, a segmental function is generally provided as follows: 
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

Generally, $a$ is used to represents other quantity, including: 
$$
K_0=\frac{a}{\gamma-1}\\
\phi=\frac{(1+a)^\gamma(\gamma-1)^{\gamma-1}}{a^{\gamma-1}\gamma^{\gamma}}
$$
In addition, the following variables are usually introduced to simplify the expression of delinearization functions:
$$
\alpha=a+1\\
\beta=K_0\phi
$$
Then the process from linear RGB to nonlinear is as follows:
$$
C_n=\phi C_l,\qquad 0\le C_n\le \beta\\
C_l=\alpha C_l^{1/\gamma}-a,\qquad C_n>\beta\\
$$

The following figure shows the transformation curve of sRGB linearization. The red line is the linearization function, the blue is the derivative function, and the black dotted line below the red line is the gamma correction curve when $/ gamma = 2.2 $. Some curves of power function will shift for the values near the origin are replaced by straight lines. In order to get the result of averaged value $\gamma$=2.2, sRGB uses a value of 2.4. In addition, due to the truncation error, the sRGB transfer function will be discontinuities around  $K_0$. 

![File:SRGB gamma.svg](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/SRGB_gamma.svg/512px-SRGB_gamma.svg.png)

During color correction, the input value may be less than 0. To ensure that the output value of the function is still real,  the function is also to make a centro symmetry about the origin. 

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

In color correction, the RGB color space needs to be converted into the CIE lab color space. The following figure uses sRGB and ProPhoto RGB as examples to show the process of color space conversion. The green arrow represents linear transformation, and the blue indicates non-linear transformation. The color space represented by green box can be realized by linear transformation.

All RGB color space values must be normalized, that is, the values are between [0,1] In the whole fitting process.

![image-20200708154138215](色彩空间.assets/image-20200708154138215.png)

###<font color=red> Convert Linear RGB To Same White Point XYZ </font>

Once the three primary colors and the white point have been determined, the linear RGB space has been sett. The XYZ space also needs to define a white point to represent absolute colors, so we can express the RGB space as the XYZ color space where the white point is defined on the white point of the RGB space.
$$
\begin{bmatrix}X\\ Y\\ Z\end{bmatrix}=M_{RGBL2XYZ}\begin{bmatrix}R_l\\ G_l\\ B_l\end{bmatrix}
$$
where transfer matrix could be evaluated by theree primary colors and white xyY value[11].

And  xyY color needs to be converted into XYZ color, the specific formula is [12]:
$$
X=\frac{xY}{y}\\
Y=Y\\
Z=\frac{(1-x-y)Y}{y}
$$

### Chromatic Adaptation

Although it is converted into XYZ space, the white points of the space are different. For this reason, it is necessary to convert between XYZ spaces of different white points. This process is called **chromatic adaptation**, or **white balance**.

This conversion process  needs to convert the XYZ space of the white point into the cone response space (CRD), $(\rho,\gamma,\beta)$, there are[13]:
$$
\begin{bmatrix}\rho\\ \gamma\\ \beta\end{bmatrix}=M_{XYZ2CRD}\begin{bmatrix}X_w\\ Y_w\\ Z_w\end{bmatrix}
$$
where $M_{XYZ2CRD}$ can choose identity matrix, Bradford matrix and Von Kries matrix. The Bradford matrix is selected by default.

Color adaptation can ultimately be expressed as:
$$
\begin{bmatrix}X_d\\ Y_d\\ Z_d\end{bmatrix}=M_{XYZ2XYZ}\begin{bmatrix}X_s\\ Y_s\\ Z_s\end{bmatrix}
$$
where subscript s is the source XYZ space, and subscript d is the target XYZ space, and
$$
M_{XYZ2XYZ}=M_{XYZ2CRD}^{-1}\begin{bmatrix}
\rho_d/\rho_s & 0 & 0\\ 
 0& \gamma_d/\gamma_s & 0\\ 
0 & 0 & \beta_d/\beta_s
\end{bmatrix}M_{XYZ2CRD}
$$
where  $(\rho_s,\gamma_s,\beta_s)$ and $(\rho_d,\gamma_d,\beta_d)$ are the CRD values of the source XYZ space white point and the target XYZ space white point, respectively.

### Convert Linear RGB to XYZ

Therefore, the linear RGB space is converted into a white point XYZ space, and the final expression is:
$$
\begin{bmatrix}X'\\ Y'\\ Z'\end{bmatrix}=M_{XYZ2XYZ'}M_{RGBL2XYZ}\begin{bmatrix}R_l\\ G_l\\ B_l\end{bmatrix}
$$
When the program is implemented, multiple colors are usually calculated at one time, and the channel is used as the last dimension. Therefore, if it is a two-dimensional matrix, it can be expressed as:
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
In the above formula, the multiplication symbol is displayed. At this time, the multiplication is the same as the matrix multiplication. could be implemented by using the numpy.dot, numpy.matmul or the symbol @ in numpy

If it is a multi-level tensor (for example, a picture shows the third-order tensor of w×h×3), it can be expressed as:
$$
T_{XYZ'}
=
T_{RGBL}
\times 
(M_{XYZ2XYZ}M_{RGBL2XYZ})^T
$$

Here, the multiplication is extended matrix multiplication, and may still be implemented by using the numpy.dot, numpy.matmul or the symbol @.  The result of the numpy.dot is the same as numpy.matmul.
### Convert XYZ to Linear RGB

To convert XYZ space into linear RGB space, we only need to multiply the inverse of the conversion matrix.

### Convert RGB Space to Other Space

After the RGB space is converted into XYZ space, it is then converted from XYZ space to other RGB spaces. If the linear RGB space is converted into another linear RGB space, the two differ by only one matrix, namely:
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
### Conversion Between RGB  and CIE lab

In addition, <font color=red>it can be converted into CIE lab space by converting into XYZ space</font>. Similarly, CIE lab space can be converted into a certain XYZ space. The conversion relationship between XYZ and CIE lab space can be seen[14-15]


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