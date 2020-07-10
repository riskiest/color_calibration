## Color Distance

The color distance quantifies the color difference that people feel.  

Generally, we use the CIE76, CIE94, or CIEDE2000 standard proposed by International Commission on illumination. They all need to convert the color space into the CIE lab space, and then use the mathematical formula [1] to calculate. There are some discontinuities in the formula of CIEDE2000, see [2] for details.

The program provides support for the CMC l:c (1984) distance. See formulas details in [1].

In addition, two simple distances are provided for reference. One is the RGB space distance: 

$$
distance_{RGB}=\sqrt{(R_1-R_2)^2+(G_1-G_2)^2+(B_1-B_2)^2}
$$

and linearized RGB space distance: 

$$
distance_{RGBL}=\sqrt{(R_{l1}-R_{l2})^2+(G_{l1}-G_{l2})^2+(B_{l1}-B_{l2})^2}
$$

The former is useful in machine vision, while the latter is simple and can be used as the initial value of a model based on other distances. 

## ColorChecker

The ColorChecker is used as the reference color in color correction, and all colors have been calibrated. The most popular standard ColorChecker is the Macbeth ColorChecker, which consists of 4 x 6 color blocks, as shown in Figure [3]. The last color block is gray and can be used for gray linearization or white balance. 

The colors of the Macbeth ColorChecker under the D50 illuminant at a 2 degree angle  have been calibrated by multiple people, and the results are different from each other[4–5]. The color of the D65 illuminant at a 2 degree angle can be obtained by measurement results  or calculated by chromatic adaptation. This program supports the Mecbeth ColorChecker, the data of the color table of 2 degree angle D50 and 2 degree angles D65 come from [6]. Note that the data of 2 degree angle D50 converted to 2 degree angle D65 by using the chromatic  adaptation is different from that of the program. 

In addition,  X-Rite also produces a variety of other ColorChecker[7]. 

The program supports the customization of the ColorChecker list and color, and supports the input of gray positions. 

![File:Gretag-Macbeth ColorChecker.jpg](https://upload.wikimedia.org/wikipedia/commons/a/ad/Gretag-Macbeth_ColorChecker.jpg)


## References

1. https://en.wikipedia.org/wiki/Color_difference
2. Sharma, Gaurav; Wu, Wencheng; Dalal, Edul N. (2005). ["The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations"](http://www.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf) (PDF). *Color Research & Applications*. [Wiley Interscience](https://en.wikipedia.org/wiki/Wiley_Interscience). **30** (1): 21–30. [doi](https://en.wikipedia.org/wiki/Doi_(identifier)):[10.1002/col.20070](https://doi.org/10.1002%2Fcol.20070)
3. https://en.wikipedia.org/wiki/ColorChecker
4. http://www.babelcolor.com/colorchecker.htm
5. https://xritephoto.com/ph_product_overview.aspx/?ID=938&Action=Support&SupportID=5884
6. https://www.imatest.com/wp-content/uploads/2011/11/Lab-data-Iluminate-D65-D50-spectro.xls
7. https://xritephoto.com/
